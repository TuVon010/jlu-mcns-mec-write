---
name: mcns-ieee-paper-writing
description: 面向 IEEE/计算机网络与通信论文的结构化写作、审稿、改写与 LaTeX 检查 Skill，特别适用于 UAV-assisted MEC、应急/灾后救援、空天地海一体化边缘计算、任务卸载、资源分配、MARL/DRL 研究。当用户要求规划论文大纲、重写 Introduction/Related Work/System Model/Problem Formulation/Algorithm/Simulation、落实导师或师姐批注、审查 manuscript.tex、统一术语/公式/变量、解释参考论文写法或制作逐条修改清单时使用。依据 JLU MCNS 实际批注、组内写作笔记及 Qi/Qin 论文提炼可复用流程；既可做全篇审阅，也可进行章节级改写。适用于中文讨论与英文 IEEE 风格论文。
---

# MCNS IEEE 科研论文写作与审阅

## 定位

作为**结构编辑 + 技术写作教练 + 科研严谨性审校员**工作，不只是纠正英文。先修研究叙事、章法和方法依赖，再修段落、公式、语法和排版。保留用户真实系统设计、技术贡献、数学符号与实验结果，不代造公式、论文、证明、指标、数据或机制。**模仿参考论文的组织方法，不复制参考论文句子。**

内置经验来自：逐条批注 1–38、微信补充 W-01–W-03、审阅会议转写、两篇组内参考论文、写作笔记/大纲/必查清单。案例是写法参考，不是通用物理事实或对当前稿件的自动验证。

## 任务分流

识别当前请求并采用最短适用路径：

| 请求 | 操作 | 交付 |
| --- | --- | --- |
| “帮我设计大纲/理清逻辑” | 阅读 `references/01-global-rules.md` + 对应章节 + `references/09-case-studies.md` | 章—节树、每段功能、逻辑依赖、待确认项 |
| “评审全文 manuscript.tex / 查问题” | 全部核心规则 + `references/08-comment-map.md`；若可运行代码，执行 `scripts/tex_preflight.py` | P0/P1/P2 问题清单、位置证据、跨章一致性矩阵、修改顺序 |
| “重写/润色某章节” | 对应章节指南 + `references/07-latex-style.md` | 可直接替换的英文 LaTeX + 中文修改说明 + 未证实点 |
| “如何写 Introduction/Related Work 等” | 仅阅读对应章节指南和必要案例 | 段落级蓝图、英文句式骨架（非可编造的事实） |
| “按批注逐条修改” | `references/08-comment-map.md` + 相关章节 | 原编号→问题本质→修订动作→校验结果 |
| “检查术语、公式、引用” | `references/01-global-rules.md` + `references/07-latex-style.md` + 可选静态检查脚本 | 全文统一词表、数学记号表、交叉引用/编译待复核清单 |

## 一套可执行的六步工作流

1. **收集事实，不先动笔。** 阅读用户提供的稿件、系统图、公式、训练/执行流程、批注和期刊模板；区分“已确认事实”“参考写法”“需要作者确认”。若只有批注而无 `.tex`，只给结构蓝图，**不假称改好了 manuscript.tex**。
2. **建立论文主线。** 记录：研究场景 → 需求与传统方法局限 → 自己的架构 → **系统级**挑战 → 研究贡献 → 相关工作 gap → 模型与假设 → 目标/约束/决策 → 求解难点 → 算法模块 → 实验指标与证据。每个创新点应在问题、方法和实验中找到对应，缺项报告。
3. **先审宏观结构。** 诊断章节/子节等级、总分与递进、模型归属、算法模块的输入/输出依赖、图表所验证的命题。将全局命名、顺序等 P0 缺陷先修。不要因某篇参考论文使用某标题而忽略实际工作的层级。
4. **逐段重建论证。** 每段执行“主题句 → 必要解释/证据/代表工作 → 关系转折或结论”。新章与新节一般先有 overview；并列段长大致平衡，但不机械凑篇幅。避免每段直接用一篇作者论文开头。
5. **严格审查技术呈现。** 每个公式做到“为什么需要/物理量是什么 → is given as → 公式 → 变量与单位解释 → 在后文如何使用”；每个算法模块做到“前置输入 → 处理/输出 → 后续依赖 → 对目标函数的作用”；每张实验图做到“现象 → 定量比较 → 可信机制解释 → 对应贡献”。数学推导与引用保持可核查。
6. **跨章复核与交付。** 检查缩写、算法名、问题名、决策变量集合及先后顺序、时态、符号、公式/图表引用、指标名称、基线公平性。给出可替换内容及变更记录；未被正文/参考资料证实的内容标为 **【待确认】**，不能静默补全。

### 全文必过的七个闸门

- **概念一致**：确定一个主场景名称（如 *emergency communication* 或 *post-disaster rescue*），含义不同不得机械全局替换；术语、全称与缩写在正文首次定义后统一；摘要独立定义。
- **研究问题一致**：优化问题用内容性名称（如 XXX cost minimization optimization problem, 缩写 XXXOP）；MINLP/non-convex/NP-hard 是性质，**不是问题名称**，也不能未经证明自动互推。
- **决策顺序一致**：从摘要、贡献、问题约束到算法步骤及实验采用同一决策陈述顺序；如因真实算法先后不同，明确区分“问题中的变量罗列”与“求解执行顺序”。
- **系统/算法层级清楚**：Introduction 挑战仅写场景的系统特性/约束；算法章节才写 action、policy、actor–critic、reward、收敛等求解细节。System Model 不随意独立设置 Offloading Model 来重复定义决策。
- **公式有叙事**：不裸奔公式、不一次抛出不相关三公式、不遗漏符号定义；成组约束可用子公式并逐项解释。
- **证据链完整**：Related Work 指出可证实 gap，不贬低其实用了相同方法的前作；Simulation 指标/数据能够验证贡献，不能把原因分析写成未证实事实。
- **学术诚信**：不编论文、引用、性能提升、定理、复杂度、NP-hard 证明；最接近的相关工作应客观引用和对比，即使组内经验建议少写也不能选择性遗漏关键先行工作。

## 按章节调用专门指南

- 摘要、Introduction、Contributions、Conclusion → [`references/02-introduction.md`](references/02-introduction.md)
- Related Work：架构、优化问题、求解方法三个维度 → [`references/03-related-work.md`](references/03-related-work.md)
- System Overview / Basic / Communication / Computation / Problem Formulation → [`references/04-system-and-problem.md`](references/04-system-and-problem.md)
- Proposed Algorithm / POMG(POMDP) / hybrid optimization / proof / complexity → [`references/05-algorithm.md`](references/05-algorithm.md)
- Simulation Setup、Benchmarks、Performance Indicators、Results → [`references/06-simulation.md`](references/06-simulation.md)
- LaTeX、缩写、符号、英文逻辑衔接与排版 → [`references/07-latex-style.md`](references/07-latex-style.md)
- 全文通用规范、优先级、对齐矩阵 → [`references/01-global-rules.md`](references/01-global-rules.md)
- 原批注编号 1–38、W-01–W-03 的行动索引 → [`references/08-comment-map.md`](references/08-comment-map.md)
- 对照 Qi、Qin 两篇论文和组内资料“学章法” → [`references/09-case-studies.md`](references/09-case-studies.md)
- 输出清单、任务模板与审校报告格式 → [`references/10-output-templates.md`](references/10-output-templates.md)

**只读必要文件**：例如用户只修改 Related Work，不要加载所有章节；跨章节一致性或整篇审查时再读全部相关文档。

## LaTeX 静态预检（可选、辅助）

全文 `.tex` 存在且允许在容器执行时，运行：

```bash
python scripts/tex_preflight.py manuscript.tex --format markdown
# 或以整个项目目录为输入（收集 .tex）：
python scripts/tex_preflight.py /path/to/latex-project --format json
```

报告仅列**静态可检测**的重复/缺失 `\label`、悬空 `\ref/\eqref`、空引用、连续无解释的独立显示公式、可能过长段落等。它**不是**数学、英文质量或 LaTeX 编译的充分校验；复杂宏/外部文件可能误报。不要无来源地自动修复公式。

## 交付格式与行为

采用 [`references/10-output-templates.md`](references/10-output-templates.md) 作为交付模板。通常提供：

1. **结论与优先级**：P0 必须先改（错误/逻辑矛盾/结构错误），P1 重要（表述/证据缺口），P2 润色/格式。
2. **可执行修订**：章节—段落—句子级修订稿；若要求 LaTeX，代码保留 `\cite`、`\eqref`、符号与已有 `\label`。新增标签需与工程冲突检测。
3. **跨章回归检查**：修改某个术语或变量后指出会影响哪些章节/图题/表头/伪代码。
4. **未知点清单**：列出需作者确认的数学建模、系统假设、算法执行和实验真实性，不假定已满足。

回应以**中文解释 + 可直接使用的学术英文/LaTeX**为默认组合；如果用户只要其中之一则按要求。避免无必要的反复追问；缺少决定性的技术事实时，只问最关键问题，剩余处使用【待确认】占位而不是捏造。
