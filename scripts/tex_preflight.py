#!/usr/bin/env python3
r"""Non-destructive heuristic LaTeX preflight for MCNS IEEE paper drafts.

This is a structural supplement to human editorial review, not a LaTeX
compiler or proof verifier. Supports a .tex file (and its literal \input and
\include dependencies) or a directory of .tex files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Issue:
    severity: str
    rule: str
    file: str
    line: int
    detail: str


# A strict subset of LaTeX. Macro-generated and external-package refs may
# evade or trigger these checks; they are only editorial hints.
LABEL_RX = re.compile(r"\\label\s*\{([^{}]*)\}")
REF_RX = re.compile(r"\\(?:eqref|ref|autoref|cref|Cref|pageref)\s*\{([^{}]*)\}")
CITE_RX = re.compile(r"\\(?:cite|citep|citet|parencite|textcite)\s*(?:\[[^\]]*\]\s*)*\{([^{}]*)\}")
INPUT_RX = re.compile(r"\\(?:input|include)\s*\{([^{}]+)\}")
DISPLAY_RX = re.compile(r"\\begin\{(equation|align|gather|multline)\*?\}(.*?)\\end\{\1\*?\}", re.S)
FIGURE_RX = re.compile(r"\\begin\{(figure|table)\*?\}(.*?)\\end\{\1\*?\}", re.S)
HARDCODED_RX = re.compile(r"\b(?:Eq(?:uation)?s?|Figs?|Figures?|Tables?|Sections?)\.?\s*\(\s*\d+[a-z]?\s*\)", re.I)
MANUAL_PROOF_RX = re.compile(r"\\textbf\s*\{\s*(?:Proof|Proposition\s*\d+|Theorem\s*\d+)\s*[:.]?\s*\}", re.I)


def without_comments(text: str) -> str:
    """Mask LaTeX comments while preserving byte count and line numbers.

    A % is a comment starter unless escaped by an odd number of backslashes.
    Verbatim/inline verb commands are not parsed. False positives remain.
    """
    out = []
    for line in text.splitlines(keepends=True):
        i = 0
        while i < len(line):
            if line[i] == "%":
                j = i - 1
                count = 0
                while j >= 0 and line[j] == "\\":
                    count += 1
                    j -= 1
                if count % 2 == 0:
                    newline = "\n" if line.endswith("\n") else ""
                    out.append(line[:i] + " " * (len(line) - i - len(newline)) + newline)
                    break
            i += 1
        else:
            out.append(line)
    return "".join(out)


def lineno(text: str, char_index: int) -> int:
    return text.count("\n", 0, char_index) + 1


def file_list(src: Path) -> list[Path]:
    if not src.exists():
        raise FileNotFoundError(f"Input not found: {src}")
    if src.is_dir():
        return sorted(
            p.resolve()
            for p in src.rglob("*.tex")
            if not any(x.startswith(".") or x in {"build", "dist", "_minted"} for x in p.parts)
        )
    if src.suffix.lower() != ".tex":
        raise ValueError("Expected a .tex source file or a directory containing .tex files")
    selected: dict[Path, None] = {}

    def visit(p: Path) -> None:
        p = p.resolve()
        if p in selected:
            return
        selected[p] = None
        try:
            contents = without_comments(p.read_text(encoding="utf-8-sig"))
        except OSError:
            return
        for match in INPUT_RX.finditer(contents):
            path_arg = match.group(1).strip()
            if "\\" in path_arg or "#" in path_arg:
                continue
            child = p.parent / path_arg
            if child.suffix == "":
                child = child.with_suffix(".tex")
            if child.is_file():
                visit(child)

    visit(src)
    return sorted(selected)


def analyze(sources: dict[str, str]) -> list[Issue]:
    issues: list[Issue] = []
    locations: dict[str, list[tuple[str, int]]] = {}
    refs: list[tuple[str, int, str]] = []

    for filename, raw in sources.items():
        text = without_comments(raw)
        for m in LABEL_RX.finditer(text):
            name = m.group(1).strip()
            row = lineno(text, m.start())
            if not name:
                issues.append(Issue("HIGH", "empty-label", filename, row, "Empty \\label{}"))
            else:
                locations.setdefault(name, []).append((filename, row))

        for m in REF_RX.finditer(text):
            row = lineno(text, m.start())
            for ref in m.group(1).split(","):
                key = ref.strip()
                if not key:
                    issues.append(Issue("HIGH", "empty-ref", filename, row, "Empty or partial cross-reference"))
                elif "\\" not in key and "#" not in key:
                    refs.append((filename, row, key))

        for m in CITE_RX.finditer(text):
            if not m.group(1).strip():
                issues.append(Issue("HIGH", "empty-cite", filename, lineno(text, m.start()), "Empty citation key"))

        for m in DISPLAY_RX.finditer(text):
            env = m.group(1)
            match_text = m.group(0)
            if not LABEL_RX.search(match_text) and not re.search(r"\\notag|\\nonumber", match_text):
                issues.append(Issue("LOW", "unlabeled-display", filename, lineno(text, m.start()), f"{env} environment without label; check whether it needs a reference"))

        for m in FIGURE_RX.finditer(text):
            env = m.group(1)
            if not LABEL_RX.search(m.group(0)):
                issues.append(Issue("MEDIUM", "unlabeled-float", filename, lineno(text, m.start()), f"{env} float has no \\label"))

        for m in re.finditer(r"\\end\{(?:equation|align|gather|multline)\*?\}\s*\\begin\{(?:equation|align|gather|multline)\*?\}", text):
            issues.append(Issue("LOW", "adjacent-equations", filename, lineno(text, m.start()), "Consecutive display environments without explanatory prose; verify formula narrative"))

        for m in HARDCODED_RX.finditer(text):
            issues.append(Issue("LOW", "hardcoded-reference", filename, lineno(text, m.start()), f"Potential hard-coded reference '{m.group(0)}'; use a cross-reference if applicable"))

        for m in MANUAL_PROOF_RX.finditer(text):
            issues.append(Issue("MEDIUM", "manual-theorem-label", filename, lineno(text, m.start()), "Manual bold theorem/proof marker; use a theorem/proof environment if applicable"))

        # Paragraph-length heuristics: ignore command / display-heavy blocks,
        # checking only paragraph chunks dominated by prose.
        char_start = 0
        for para in re.split(r"\n\s*\n", text):
            pos = text.find(para, char_start)
            if pos == -1:
                continue
            char_start = pos + len(para)
            noncommand_lines = [line.strip() for line in para.splitlines() if not line.lstrip().startswith("\\") and not line.lstrip().startswith("%")]
            prose = " ".join(noncommand_lines)
            words = re.findall(r"\b[A-Za-z][A-Za-z-]*\b", prose)
            if len(words) > 250 and not re.search(r"\\begin\{|\\end\{", para):
                issues.append(Issue("LOW", "long-paragraph", filename, lineno(text, pos), f"Paragraph is about {len(words)} English words; consider topic/transition split"))

    for name, occurrences in locations.items():
        if len(occurrences) > 1:
            files = ", ".join(f"{p}:{row}" for p, row in occurrences)
            for filename, row in occurrences:
                issues.append(Issue("HIGH", "duplicate-label", filename, row, f"\\label{{{name}}} appears {len(occurrences)} times ({files})"))

    for filename, row, key in refs:
        if key not in locations:
            issues.append(Issue("MEDIUM", "unresolved-ref", filename, row, f"\\ref/\\eqref target '{key}' not found among analyzed files"))

    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return sorted(issues, key=lambda x: (rank[x.severity], x.file, x.line, x.rule))


def to_markdown(files: Iterable[str], issues: list[Issue]) -> str:
    files = list(files)
    c = Counter(issue.severity for issue in issues)
    out = [
        "# LaTeX 静态预检（启发式）",
        "",
        f"已检查 {len(files)} 个 .tex 文件；发现 {len(issues)} 条提示：HIGH {c['HIGH']}、MEDIUM {c['MEDIUM']}、LOW {c['LOW']}。",
        "",
        "> 静态扫描不能证明数学/英语/段落逻辑/编译正确；外部宏、\\input 与非标准环境可能误报。",
        "",
    ]
    if not issues:
        out.append("未发现本脚本能识别的模式问题。仍须人工审稿与 PDF 编译检查。")
        return "\n".join(out) + "\n"
    out.extend(["| 级别 | 文件:行 | 检查项 | 说明 |", "| --- | --- | --- | --- |"])
    for issue in issues:
        detail = issue.detail.replace("|", "\\|").replace("\n", " ")
        out.append(f"| {issue.severity} | `{issue.file}:{issue.line}` | `{issue.rule}` | {detail} |")
    out.extend(["", "后续需核对：系统/问题/算法变量一致性、目标与 reward 的关系、引用来源、定理证明和最终 PDF 版式。", ""])
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path", help="Root manuscript .tex file or LaTeX project directory")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Optional report output path; stdout by default")
    args = p.parse_args()
    src = Path(args.path)
    try:
        files = file_list(src)
        if not files:
            raise ValueError("No .tex files found")
        sources = {str(f): f.read_text(encoding="utf-8-sig") for f in files}
        issues = analyze(sources)
    except (OSError, ValueError, UnicodeError) as err:
        print(f"preflight error: {err}", file=sys.stderr)
        return 2
    if args.format == "json":
        report = json.dumps({"files": list(sources), "issues": [asdict(x) for x in issues], "limitations": "heuristic structural check, not compilation or scientific review"}, ensure_ascii=False, indent=2)
    else:
        report = to_markdown(sources, issues)
    if args.output:
        Path(args.output).write_text(report + ("" if report.endswith("\n") else "\n"), encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
