# Simulation 与 Performance Evaluation 写作指南

## 目录
1. 章节树
2. Setup/Benchmarks/Indicators
3. 图表与结果段落
4. 收敛性、系统参数与公平性
5. 常见批注的实际修法

## 1. 推荐章节结构

```text
VI. Simulation and Performance Evaluation
    A. Simulation Setup
       1) Scenario / Parameters
       2) Benchmark Algorithms
       3) Performance Indicators
    B. Evaluation Results
       1) Algorithm Performance Evaluation
       2) Convergence and Efficiency Performance [or Convergence Evaluation]
       3) Impact of System Settings
          a) Impact of the Number of UDs
          b) Impact of Average Task Size / UAV Computing Capacity [...]
```

这沿用师姐要求的“先总述 → 默认参数下关键指标 → 收敛 → 系统参数影响”顺序。另一种组内大纲是对比/消融→SOTA DRL 对比→超参数→系统参数。两种都可以，**按实际要证明的主张、图数量与版面选择，不能把单纯的横坐标换个顺序当作分析**。

章节开头用一段概述模拟目的和小节内容；如果 Setup 过短，可简化标题层级，但保持总分关系。

## 2. Simulation Setup

### Scenarios and Simulation Parameters

按顺序交代：

1. 场景区域大小、UD/UAV/控制节点数量、位置生成与运动模式、任务输入分布、时隙/episode 设置。
2. 链路/计算/电池/优先级等关键物理参数及其来源；不同实验改变的参数单列。
3. 硬件软件与训练参数：如仅有 Python/PyTorch 等已证实配置，不能凭习惯编版本或 GPU 型号。
4. 参数表用清楚的名称、数学符号、单位与值；引用 `Table~\ref{tab:parameters}`。

表格必须在期刊版心之内；IEEE 双栏优先符合列宽或合理使用 `table*`；数据多时采用适当换行、缩写/分组，而不是把所有字体强行缩小。

### Benchmark Algorithms

先解释基线分组、再定义具体策略：

- **策略级/消融**：例如随机卸载、最近节点卸载、等量资源分配、取消区域划分；名称写为独立策略名而不统一冠以自己算法前缀。
- **算法级**：相近的 DRL/MARL 方法、传统优化、启发式，按照模型/环境可比性选取。
- **可比性**：给定相同的系统模型、资源约束、目标、训练预算、任务/信道随机种子、评价时段和硬件条件；若不同方法本身假设不同，明确揭示。
- **公平性**：不能把本算法不同变量联合优化却强制基线不允许这些变量优化，然后无条件宣称“方法本身优越”；若是消融，需明确它的用途是验证模块贡献。

Random 通常只是经验基线，不因结果较差就成为 upper/lower bound；数学界需另有证明。MADDPG、SAC 等名称也不自动意味着 SOTA：按当前任务的可比性与可核查证据选择，不确定时称代表性基线。组内 LLM 实验例子只适用于实际有 LLM 组件的工作。

在不误导的前提下，建议把基线按**传统/启发式→DRL/MARL**进行介绍。Introduction 的贡献部分不需列全基线名单。

### Performance Indicators

组内要求通常**写入一段文字**，避免为 average cost、delay、energy 等显然指标逐个占用独立公式。推荐：

> `We evaluate [the algorithm] using [name of metric 1], [metric 2], and [metric 3]. Specifically, [metric 1] measures [unambiguous statistical definition], whereas [metric 2] quantifies [meaning]. [Metric 3] is reported to assess [trade-off or constraint].`

必要时若统计计算方法有歧义、创新或与目标函数不同，单独给公式有充分理由。**指标的期望、平均范围、分母/单位要明确**，例如时隙平均 vs 用户平均、用户成本 vs UAV 能耗、per-task vs per-episode。

再核对：只统计成功任务还是所有生成任务，失败/超时如何计入；先求比值再平均还是总量之比；用户数变化时是否仍使用总和成本。总成本上升不必然意味着人均服务恶化。百分比改善写清比较基线和分母，成功率等比例指标区分相对百分比与百分点；零基线时不直接除。坐标轴简写不能隐去关键统计口径。（写作笔记 14–16；共性问题第 4、10 页）

## 3. Evaluation Results：每张图都有“读数→解释→意义”

对每张结果图按照以下四步写（必要时分为 2–3 段）：

1. **定位图/坐标**：`Fig.~\ref{fig:xxx} illustrates ... under [evaluation condition].` 说明 x/y/对比组。
2. **描述可见趋势与量化对比**：谁高谁低、从多少到多少、升降多少，明确比较基线与参数设定；不把 `reward` 的高低误称为原问题 `cost` 的高低。
3. **解释机制**：指出与算法模块的已知关系。分清**实验支持的解释**与**合理的机制推测**，除非有消融/证据否则不要把推测写成证明。
4. **回扣研究目标及权衡**：说明效果（收敛稳定/低时延/低成本/能量代价）、局限/负面变化，避免单纯“our algorithm is superior”。

### 示例（所有数值需来自实际图表，以下不提供虚构数字）

> `As shown in Fig.~\ref{fig:cost}, the proposed algorithm achieves a lower average UD cost than [verified baselines] under [settings]. In particular, the cost difference is [insert measured comparison with units]. This trend is consistent with [the explicitly evaluated mechanism], which [causally plausible and evidenced action]. However, [trade-off, if observed] should be considered when [system condition].`

务必用数据：可报告平均值、相对变化百分比、置信区间/多随机种子分布（如果确实测了）；不把看图估算值当精确测量。

### 文章篇幅

- 相关、同类的多子图分析篇幅大致平衡；批注 37 的“图 4 三段、图 3 半段”本质是**关键性能图解释不足**。
- 一个完整实验假设与关键机制可能需要两段以上，但无需每张图机械三段；重点是读者知道结果在**验证哪一个贡献**。
- 新的 `Impact of Number of UDs` 分析必须通过空行/结构明确另起段，不能仅靠 LaTeX 取消首行缩进伪装分段（批注 38）。

## 4. 收敛、系统设置与其他检验

### Performance Evaluation（默认设置）

重点显示目标函数及关键构成，例如聚合 UD cost、task delay、UD energy、UAV energy、任务截止时间满足率（若建模及实验确有）。对权衡尤其要客观：更低用户成本可能换来略高 UAV 能耗，不能隐藏。

### Convergence / Stability / Runtime

- 训练曲线：定义 reward 对应哪一个目标，x 轴 episode/train steps，稳定阶段、波动、样本方差。
- 不要只写“收敛快”而不对比达到稳定性能的 episodes、计算预算，训练与运行在线推理应区分。
- 若标称 real-time，报告**推理+外部资源求解+匹配算法**全流程端到端在线时延，不只报 actor 前向时间；`stable reward` 本身不保证理论收敛。
- 速度和稳定性分析应在图中可核查，避免“稳定”“显著”“鲁棒”等未经多种条件验证的形容。

### Impact of System Settings

按系统重要参数（UD 数量、任务数据量、UAV 算力、能量预算等）逐个分析。每个参数变动保持其他设置固定，明说变化范围和单位；对“自己的算法”与基线展示范围依据图安排说明，不能从缺失基线曲线推断优势不变。

注明每个扫描点采用重新训练、微调、固定 checkpoint 测试还是仅改变输入分布。“不同配置各自重训后有效”不能写成“同一策略无需重训即可泛化”。参数数量由主张与计算预算决定，不固定最多两项。

### Ablation

如果贡献点包含分区机制、任务优先级、外部优化器或混合策略，尽量设计每项机制是否有效的直接消融，保证设置公平；没有消融时对应贡献只能做有限的间接解释。

**贡献粒度不能比证据粒度更细。** 最近卸载/等分算力/固定轨迹主要检验决策分工，整体对比 TD3/SAC 主要检验框架表现；这些不能独立证明某个生成 actor 或探索模块分别带来收益。若分别声称表达能力与探索效率改善，需要相应控制其他因素的替换/去除实验，或者降低机制结论强度。

若声称照顾紧急任务，按实际模型检查类别/紧急程度的完成率、违约率或服务差异及普通任务代价；仅平均成本改善不充分支持优先服务主张。没有分类数据就列出证据缺口，不能编造曲线。轨迹图可解释行为和约束，但通常仍需定量安全/可行性检查。

## 5. 图表和规范

- 结果图优先低冗余的扁长版式，去除上下左右大量空白；线条 marker 清晰、不同方案容易区分，考虑灰度打印。
- 数据图文字/坐标轴清晰可辨，组内约定可只将轴标题第一个单词首字母大写，全篇统一；字体规范参照《论文必查清单》（示意图 Arial、结果图 Times New Roman），**最终仍服从投稿模板**。
- 图例长度要匹配空间，横排/外置可优先于压缩正文字号；同一算法在不同图表中颜色/线型尽量一致；组内建议“自己的算法放 legend 最后”是可调整的样式约定，不是科学定律。
- 图题、图号、引用与指标名一一对应；绝不能把绘图用的临时代号留在论文。
- 三线表优先用 `booktabs`；避免参数表和内容超出页边界或断到两栏边界；检查脚注与单位。

## 6. 针对现有批注的修改动作

| 批注 | 根因 | 修改动作 |
| --- | --- | --- |
| 32 参数表超边框 | 版心/列宽布局不合理 | 调整列宽/换行/必要时 table*，编译视觉核查 |
| 33（截图在仿真附近） | 实际针对 Related Work 的方法综述 | 回到相关工作检查传统方法→DRL 的论证；不是要求在 Simulation 重复该段 |
| 34 指标公式过多 | 普通指标不需全部独立推导 | 改为一段文字，必要的指标统计才保留公式 |
| 35 复用训练与设置说明不清 | 训练/评估样本独立性和使用什么参数不明确 | 说清模型是否重新训练、训练环境和测试环境是否共享、训练轮数、哪些参数固定/变化 |
| 36 Results 目录混乱 | 先后没有性能主线 | 默认指标→收敛→系统参数及子项 |
| 37 图 3 太少图 4 太多 | 关键性能结论缺分析 | 补定量读数和可证实的原因，再结论 |
| 38 未分段 | 把 `\noindent` 当作新段落 | 用空行建真正段落并保持合理自然缩进 |

**原批注对应**：4、32–38、W-03；参考 Qin Section 6、Qi Section 5、写作笔记第 14–16 页和组内大纲中的两类实验布局。
