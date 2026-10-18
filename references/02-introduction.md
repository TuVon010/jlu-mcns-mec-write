# Introduction、Abstract、Contributions、Conclusion 写作指南

## 目录
1. 研究主题的边界
2. Introduction 四/五段叙事结构
3. 三个挑战的写法
4. 四项贡献
5. 摘要与结论
6. 常见错误/审查问题

## 1. 先判定主题，不要混用

用户论文可能涉及两种近似但不等价的任务：

- **Emergency communication / emergency response**：强调发生紧急事件时网络通信和救援信息服务的迅速恢复与保障；范围比灾后阶段宽。
- **Post-disaster rescue**：强调灾害发生后基础设施受损、人员搜救、现场任务执行和持续救援；在具体部署/时间条件上更窄。

哪一个适合取决于实际系统图、任务定义、灾害阶段、数据模型和用途，**不能只凭标题自行决定**。拟采用一种表达后，在题名、引言、相关工作、系统设定和图题中保持概念一致；如果确实包含不同阶段，用一句定义解释它们的关系，而不是硬替换。

## 2. Introduction 推荐段落地图

适用于 MEC/UAV/救援论文；段数可按篇幅缩放，重点是因果而非固定四段。

| 段落 | 核心问题 | 推荐展开 |
| --- | --- | --- |
| P1 场景驱动 | 为什么救援需要这个系统？ | 灾害/应急场景、任务时间敏感性、基础设施损坏/覆盖稀缺、计算密集任务；**先说需求再引 MEC**；传统 MEC 能减少处理时延但依赖地面设施或稳定连接 |
| P2 技术引入 | 为什么考虑 UAV-assisted MEC？ | 快速部署、按需覆盖、靠近 UD 的计算能力；转折：UAV 能源、载荷、覆盖、机动成本或协调瓶颈（仅写实际系统中存在的限制） |
| P3 场景系统挑战 | 为什么充分发挥其优势仍然困难？ | 从系统级动态性、异构节点、任务重要性/资源稀缺、耦合决策、局部观测等**有事实依据的特征**中提取 2–3 点 |
| P4 方法动机 | 为什么本文研究路径合理？ | 用一段从挑战引到共同优化方向；如果引入 DRL，解释其适应动态、多节点协同的动机，但不应把 Introduction 的系统挑战写成 actor/critic/policy/具体 reward 更新过程 |
| P5 贡献与文章安排 | 我们具体做了什么，读者往下看什么？ | 四项贡献（架构、优化问题、算法、实验）；末尾独立写组织安排（可简洁） |

P1 典型大到小的结构：`disaster-affected environment → delay-sensitive computing needs → conventional MEC advantage → failure mode of infrastructure-dependent MEC → UAV-assisted MEC as a direction`。

### 可改写的英文骨架（不是事实陈述，须填真实条件与引用）

> `In [specific rescue setting], [mission-critical tasks] require [verified service requirement]. Although conventional MEC can [documented benefit], its reliance on [verified infrastructure assumption] may limit its applicability when [specific adverse condition]. To address this limitation, UAV-assisted MEC can [documented capability]. However, [actual system-level constraint] still hinders [service objective].`

避免 Introduction 上来只说 MEC 历史而完全没有救援需求；避免一个技术没有约束就突然提出自己的架构。

## 3. 重点：System Challenges 与 Algorithmic Challenges 不同

Introduction：**系统/场景层**。算法 Motivation：**优化问题求解层**。同一事实可以分别转述，但焦点必须变化。

| Introduction 合适写法 | Algorithm Motivation 才合适写法 |
| --- | --- |
| 用户移动、信道波动和任务到达使服务需求持续变化 | 非平稳/部分可观测状态使在线策略求解和长期回报优化困难 |
| 空中服务节点算力和能量有限，需要跨节点协同 | 高维或混合决策空间使传统优化/学习求解代价过高 |
| 用户任务紧急程度不同，资源竞争会影响关键任务及时完成 | 奖励函数如何权衡优先级、时延、成本，如何设计约束处理机制 |
| 部分节点只能获取有限的实时局部信息 | 具体 MARL/CTDE 训练设置、action/state/policy 设计 |

### 挑战提取的三种路径（择其一，不能拼贴）

1. **按三个创新点**：某项架构缺口、某项目标与决策耦合、某种自适应/实时性需求。
2. **按算法章节的三个求解难点**：回溯每项难点对应的真实系统特性，把 action、policy、convergence 等词在 Introduction 中退回为“资源、动态和服务协调问题”。这是组内常用写法，Qin 论文可参考。
3. **按联合决策**：卸载选择/比例、资源分配、轨迹/区域分配如何相互影响；不应把变量名列表冒充真正的挑战，要说明物理冲突和后果。

不要为“凑三个挑战”编造系统不存在的“局部观测”或“高度动态”；需要证据时先查模型与部署前提。难以概括时，**留待系统模型和算法框架稳定后回写 Introduction**，不是随意先编。

## 4. Contributions 四项并列，长度与信息密度大体均衡

建议使用组内 Title Case 加粗标签：

```latex
\begin{itemize}
  \item \textbf{System Architecture.} We develop [a verified architecture] for
  [scenario], in which [distinct node roles] jointly support [purpose].

  \item \textbf{Problem Formulation.} We formulate a
  [descriptive problem name] ([ACRONYM]) to minimize [actual objective]
  by jointly optimizing [actual decisions] subject to [major constraints].

  \item \textbf{Algorithm Design.} We propose the [full algorithm name]
  ([ACRONYM]) algorithm, which [module A and its purpose], while
  [module B and its purpose].

  \item \textbf{Performance Evaluation.} Extensive simulations evaluate
  [key metrics and verified properties], showing [only evidence-backed
  comparative outcomes].
\end{itemize}
```

- **Problem Formulation** 写构建的目标/变量/约束问题；“MINLP”是问题的一种数学**性质**，不能代替描述性名称。示例：`UD cost minimization optimization problem (UCMOP)`（仅可借鉴命名方式，不复用名称给不同问题）。
- **Algorithm Design** 在总算法名称与内部组件之间建立“包含—组成”的关系，不只是堆三种算法名字。
- **Performance Evaluation** 不在 Contributions 中枚举所有 benchmarks；说核心验证点和实际结果。无结果可核实则留占位。
- 按实际创新决定四项是否都成立；任务书一般四方面最清晰，但不能把标准仿真框架吹成全新算法。

## 5. Abstract 与 Conclusion 的写法

### Abstract（通常一整段）

`场景痛点（1–2句）→ 架构（1句）→ 优化问题名/目标/联合变量（1–2句）→ 难度属性（有依据时）→ 求解算法与模块职责（2句）→ 定量实验主要结论（1–2句）`。

- 摘要中的缩写**独立定义**。
- 不将“算法比所有方法好”当作结果，需同一评价条件下真实数值或审慎定性表述。
- 保持与正文一致的节点角色，例如“高空 UAV 仅控制不计算”就不能在摘要说它提供边缘处理。
- 真实实验未有量化结果时，不得写 `improves X by 37%`；用验证目的占位要求补证据。

### Conclusion（回到目标而不是重述细节）

`回顾解决的科学问题 → 概括系统与优化建模 → 概括算法分工 → 总结已有实证结果（量化、有指标）→ 真实局限与合理未来工作`。

文中可以“we have developed...”或“this paper develops...”；**组内提醒结论常用现在完成时不是强制一律**。

## 6. 逐段复核

- [ ] 首段首先交代应用需求，而不是直接介绍某种已有技术。
- [ ] 主场景名称已定、含义准确、没有 emergency/post-disaster 意义混淆。
- [ ] MEC → UAV-assisted MEC 每次引入均有具体约束和因果连接。
- [ ] Intro 挑战集中于系统需求/特性，没有提前出现 actor、critic、policy update、convergence 等求解层概念。
- [ ] 三个挑战和贡献均能在系统模型/问题/算法中找到证据。
- [ ] Contributions 用并列加粗 Title Case 标签，四项长度相对平衡，问题名为内容性简称，实验不罗列一堆基线。
- [ ] Remainder 准确描述真实章节次序，未照抄参考论文编号。

**原批注对应**：1–4、11–13、24、W-02；相关资料：组内写作笔记 Introduction 页、Qin/Qi 论文 Abstract/Introduction。
