# Related Work 写作指南：组织文献而不是罗列文献

## 目录
1. 三维度章节设计
2. 每一小节段落结构
3. 文献表与 gap 校验
4. 英文写法与误区

## 1. 章节先有综述，再按研究维度递进

建议在 `\section{Related Work}` 后先写一两句总述，说明将从三个方面回顾；**不直接进入小节标题**。例如：

> `This section reviews prior studies on [system architectures], [optimization formulations], and [solution approaches] most relevant to [the considered rescue scenario].`

适配本论文时的可选结构：

```latex
\section{Related Work}
[One or two bridging sentences.]

\subsection{MEC Architectures for Emergency Rescue}
\subsection{Formulation of Joint Optimization Problems}
\subsection{Optimization Approaches}
```

- 组内直接批评 `Air-to-Ground Channel and UAV Energy Models` 作为 Related Work 第二节过窄；前者是模型技术要素，而 Related Work 对应的核心创新通常是**优化问题（目标、变量及约束）**。
- 主标题可以替换为更适合实际贡献的名称；重点是每节与一类研究贡献平行对应。

## 2. 各小节 2–3 段或必要的 4 段

### 2.1 System Architecture / UAV-Assisted MEC

| 段落 | 主题句/证据 | 段落末尾 |
| --- | --- | --- |
| P1 传统/地面 MEC 在救援中的作用 | MEC for rescue/emergency 已有探索，举 2–4 篇代表性研究；每篇重点写**系统节点/架构和服务方式** | 地面设施受损、覆盖有限、响应灵活性差等实际限制 |
| P2 UAV-assisted MEC 的演化 | 用 `To reduce the dependence on terrestrial infrastructure, ...` 接上一段；举 2–4 篇 UAV/多 UAV 等研究，主要写架构如何改善部署/覆盖/处理 | UAV 能源/覆盖/任务承载等剩余缺口 |
| P3 总结 gap | 综合传统与空中两路研究的局限，指出本文**确有**的架构差异 | 自然导向下一维度（目标/求解方法） |

**若用户场景不适合直接写传统 rescue MEC**：优先检索该场景研究，缺少则扩大到临近的 MEC 应用并诚实解释迁移范围。不要为满足三篇的“配额”虚构文献。

### 2.2 Optimization Problem Formulations

按 **“优化什么”** 和 **“联合决策了什么”** 分析，选择最能说明 gap 的主线：

- 写法 A：第 1 段时延最小化研究，第 2 段能耗/成本相关研究，第 3 段总结为何需同时考虑时延与能耗，并明确任务截止时间或优先级在自己工作中的角色。
- 写法 B：第 1 段各类优化目标，第 2 段由单一决策→两类耦合决策→多变量联合优化，第 3 段总结 gap。
- 不要只列自己采用的 Air-to-Ground channel、UAV energy 公式，那是 System Model 中的模型成分；相关工作更关心**已有工作构建了怎样的优化任务**。
- 这里讲文献的“优化目标和变量”即可，尽量不详细介绍所用算法；如必要用一小短语限定研究背景，避免脱离情境。

### 2.3 Optimization Approaches

| 段落 | 重点 | 转折 |
| --- | --- | --- |
| P1 传统方法 | 代表性凸优化/分解、Lyapunov、迭代、启发式与演化计算方法，说明分别在何种 MEC 问题中使用 | 计算成本、迭代效率、动态重求解等**有根据的适用性限制** |
| P2 DRL/MARL | 代表性 DRL 多智能体优化研究，聚焦在线决策与多节点协同的优势 | 混合/变维决策、训练稳定性、部分可观测等**确有**的挑战 |
| P3 差异总结 | 用 gap 点明本研究方法的不同分工，例如连续决策学习与组合/资源决策确定性求解 | 为 Proposed Algorithm 动机铺垫 |

## 3. 一篇论文只抽取适合当前段落的那个视角

同一文献通常同时有架构、优化目标和算法：

- 在架构段：抽“系统层级、节点角色、计算位置、覆盖方式”。
- 在目标段：抽“优化指标、决策变量、约束条件”。
- 在方法段：抽“求解技术、适用环境、可证实限制”。

可以少量交代另外两项作为背景，但不能失去当前段焦点。每篇文献最好用结构化文献矩阵做证据记录：

| citation key | 场景/架构 | 优化目标 | 联合决策 | 求解方法 | 能证实的局限 | 对应段 |
| --- | --- | --- | --- | --- | --- | --- |
| 文献 1 | `【待查】` | `【待查】` | `【待查】` | `【待查】` | `【待查】` | Architecture |

**Gap 验证**：针对每项“已有文献未考虑 X”，检查这些引用的原文确实没有 X；避免“所有现有工作都只考虑某一变量”等容易被反例推翻的绝对句。方法相似不代表不能指出不同约束/场景，但必须公平比较。

## 4. 段落微结构与可用骨架

不要上来就 `Smith et al. proposed ...`，先讲该段研究方向：

> `Conventional MEC architectures have been investigated to support [a clearly scoped service requirement]. For example, [Author] investigated [architecture and node roles]~\cite{key1}. Moreover, [Author] considered [a different architecture]~\cite{key2}. Additionally, [Author] developed [another design]~\cite{key3}. However, these architectures [evidence-backed collective limitation].`

新段转新**方向**的正确转折：

> `To improve deployment flexibility in infrastructure-limited environments, UAV-assisted MEC architectures have also received attention.`

`Moreover`、`Additionally` 适合一个主题下并列几项研究，不是任何换段都自动使用。

### 时态/引用

- 描述前人特定研究通常过去时：`X et al. investigated/developed/considered ...`，但“广泛关注”可用现在完成时/现在时。
- IEEE 形式 `Smith \textit{et al.}~\cite{smith2025}`，具体模板可根据 `\bibliographystyle` 调整；除非提供确切作者/论文，不凭空造引用和 citation key。
- 代表论文数“每段约三篇”、相邻段长度相当只是写作标尺，**信息密度和准确性优先**；总参考文献数取决于期刊、篇幅和领域。

### 不做的事

- 不把 Related Work 写成堆叠摘要/论文流水账；每篇都涵盖系统、变量、算法会失去主题。
- 不只引用组内文献；同时也不遗漏最相关的先行工作；“相似论文少写”不是逃避引用的理由。
- 不用 `Morever` 把传统 MEC 和 UAV MEC 跨主题强行并列。
- 不写“传统方法不适合动态场景”而无条件、无研究范围、无来源。
- 不全文套用同一论文语言段落（抄写结构可以，抄写原文不行）。

**审阅清单**：章前有 overview；每个小节主线单一；每段有主题句、文献支撑、转折或总结；架构/目标/算法分工明确；最后总述 gap 可核查；引用实在且近年的代表工作和基础工作兼顾。

**原批注对应**：5–9、33、W-02；扩展来源：审阅会议 Related Work 大段讨论，Qin 第 2 节、Qi 第 2 节，组内《写作方法与共性问题》。
