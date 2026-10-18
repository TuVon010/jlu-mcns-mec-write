# Proposed Algorithm：先理清因果依赖，再写 DRL 壳子

## 目录
1. 算法写作总原则与框架
2. 先画模块输入/输出依赖图
3. POMG / POMDP 与真实决策集合
4. 服务区域划分、卸载与资源分配
5. Reward、MADDPG 与训练执行
6. 定理、证明与闭式解
7. 复杂度、伪代码及复核

## 1. 总原则

该部分是师姐特别强调的**最高优先级**：整章先重新梳理“哪些部件属于整个 CORA-MADDPG、谁给谁输入、什么先算、DRL 内外如何关联”，然后才决定子节顺序、段落内容与命名。不能把框架总述与其四个组成部分设为平行级别，不能让一个特别短的框架段孤零零作为一节。

### 推荐目录（仅在模块依赖支持时采用）

```text
V. Proposed CORA-MADDPG Algorithm
    A. [Integrated framework / Overview]  ← 可与章节导言合并，不必单独极短一节
       1) POMG Formulation
       2) Service Region Decomposition Mechanism
       3) Task Offloading and Resource Allocation Method
       4) MADDPG Algorithm
    B. Algorithm Implementation / Complexity Analysis  ← 可选、按实际内容
```

若真实执行先有区域划分，再用 MADDPG，再调用外部资源优化器，那么讲解次序**未必**应与上面的演示编号机械一致；可先在 POMG 中给原问题形式，再给模块执行依赖，随后按**信息和求解顺序**介绍。需要用户核实流程再确定最终目录。算法标题保持 `Algorithm`，其子部件可称 `Mechanism`、`Method`、`Module`，名称层级明确，不在各章里把整体同一对象一会儿叫 method、一会儿叫 algorithm。

## 2. 必须先画模块依赖表 / 有向流程

在读到实际算法代码、数学描述或 `manuscript.tex` 之前，**不要直接断定算法顺序**。对每个组件做如下表：

| 模块 | 输入（必须已经可得） | 输出 | 发生时机 | 对成本/约束/奖励的影响 |
| --- | --- | --- | --- | --- |
| 区域划分/聚类/分派 | UDs 位置、服务节点及其他真实输入 | 服务区域、每架 UAV 目标位置或用户归属 | 每时隙/每 episode/初始化？【待确认】 | 是否进入 state、限制轨迹或间接影响资源分配？ |
| MADDPG actor | 各 agent 可得 observation、目标区域等 | **真实**连续决策，例如卸载比例/轨迹参数 | 训练推理/在线决策？ | 经环境/后续求解器才产生实际成本 |
| 资源分配优化器 | 关联/卸载比例/坐标/速率、资源预算 | 分配 CPU、修复后的可行任务卸载？ | actor 之前还是之后？【待确认】 | 影响任务时延、能耗及 deadline 可行性 |
| 奖励与转移 | **最终实际执行**的卸载/轨迹/资源分配 | reward/next observation | 每次转移 | 与原始目标的关系及惩罚一致 |

### 当前 CORA-MADDPG 的已知线索（来自讨论，不是已审过源码）

转写指出：先用聚类/分派找每架服务 UAV 的目的地；MADDPG 可能学习**卸载比例 + UAV 轨迹**；资源分配由求解器根据轨迹/卸载比例取得，并可能对不可行卸载做本地处理；各步影响最终 cost/reward。**仍需明确**：

- 聚类目标是否每时隙更新？算法中是前处理、环境步骤还是内部模块？
- actor 是否同时输出轨迹参数、卸载比例？输出的是“建议值”还是“实际值”？
- 分配资源前是否先确定 UD–UAV association？若越界/超资源时如何处理？
- 不可行卸载被退回本地时，其 CPU 分配、额外时延及奖励如何重计算？
- 控制层 UAV 如何参与决策，它是否只是控制中心？
- reward 与问题 objective 是同一成本还是含优先级的不同评价函数？
- 训练阶段是否全部内嵌调用确定性求解器，在线阶段是否也如此？

只要这些未定，不能擅写“算法在一次行动中同时最优地解决三类变量”。

### 画出实证支持的数据流

候选图（必须用事实替换问号）：

`Node/task states → (Region mechanism?) → Agent observations → MADDPG output [offloading ratio, trajectory] → (Association/feasibility?) → resource optimization → actually executed tasks → delay/energy/priority cost → reward and next state → MARL update`。

强调有无反馈依赖：如果区域划分使用了新的轨迹，或者求解器结果反过来影响同一次 actor 输出，可能有循环依赖，需要给迭代或时间尺度说明。

## 3. POMG / POMDP 不是“直接写算法”

- 在定义状态、观察、参与 agent、动作、状态转移、奖励前，先说明为何联合优化问题可以视为序贯决策过程。
- **`state`** 包含系统真实信息；**`observation`** 必须对应 agent 可获得的局部信息；不能未经系统假设就声称 fully observable 或 partially observable。
- **动作空间完整性**：真实优化变量有哪些，先明确所有决策如何被表示/处理。如果部分变量由凸优化/博弈/匹配算法确定，区分：
  - `full system decisions`：原优化问题的全部可控量；
  - `learned actions`：actor 实际输出的变量；
  - `derived decisions`：由 learned actions 与状态经确定性优化/修复得到的量。
- 若使用扩展 POMG 描述全部联合决策，而 MADDPG actor 只负责其一部分，正文必须解释映射 `a^{full}=F(s,a^{RL})`。反之如果 POMG 仅定义 reduced learned action，也必须证明其环境转移/奖励内部如何包含外部优化器。**两种可以选，关键是形式化一致，不能 POMG 中三决策、actor 中两决策而毫无解释。**
- 文字必须写明连续动作到底是哪两个或哪三个决策以及其范围、维度；禁止一句 `The learning action space contains only continuous decisions` 就结束。
- `POMG` 是 *partially observable Markov game* 的缩写；其他资料若使用 POMDP/Markov game，依实际多智能体定义确定。首次出现给全称和名称解释。

## 4. 局部方法各有独立目标和输入输出

### Region Decomposition Mechanism

依次说明：为什么要划分服务区域（负载均衡/路径长度/服务可达性等经过证实的目标）→ 输入集合与时间尺度 → 数学目标或分派准则 → 输出区域/航点 → 给哪个后续模块作输入。不要只是写 `we apply K-means and Hungarian algorithm`，让读者自己猜对优化对象。

### Task Offloading and Resource Allocation Method

- 先明确卸载比例和用户与 UAV 关联如何确定；哪些 CPU、带宽等资源由该方法负责。
- 若是**闭式 CPU 分配解**：声明子问题，固定哪些其他变量，核对可行域/凸性/KKT 或其他定理适用条件，给出关键推导与解的形式，最后说明它如何回填总体 cost。
- 若存在 deadline 或 UAV energy 上界：区分 hard constraint、不可行回退、罚函数、投影等具体实现；不能把 infeasible action 当作可行优化结果。
- 说明每种变量是否离散/连续/变维，以及节点数量变化时为什么求解分工更合适。

### MADDPG Algorithm

系统输入 → agent 身份 → observation → actor action → critic 使用的联合信息 → replay/训练过程 → critic/actor 更新 → target network 更新 → 在线部署。讲每步时对照所用版本的 MADDPG 算法，正确标注损失与网络更新公式、变量含义。不要没有理由就大段泛写教科书定义；重点是**本系统如何应用和修改**。

## 5. Reward Function：从原问题出发，分段讲清楚

推荐的段落划分：

1. **映射目标**：原 P1 最小化什么（delay、UD energy、priority-weighted cost 等）？Reward 是负成本、归一化差值还是增量？需要一致的方向。
2. **约束与任务失败**：若使用惩罚项，说明对应哪个违反条件、权重、适用范围；不能声称罚项天然保证硬约束。
3. **最终奖励与观测更新**：奖励是用实际执行决策（含外部优化/不可行回退）算的吗？环境转移是否使用相同实现？
4. **权重释义**：`weights` 后面具体是哪一组数学变量或哪条式中的权重，写 `the weights $a$, $b$, and $c$` 或 `the weight coefficients in \eqref{eq:reward}`，不能说无主的 `the weights`。

避免公式 10 行 + 解释 1 行、以及连续多页大段不分段。无依据的 penalty 的数量级/性能结论均标【待确认】。

## 6. Proposition、Proof、Closed-form Result 的正文地位

### 格式（按模板选 `amsthm` 或 IEEEtran 规范）

```latex
\begin{proposition}\label{prop:resource_allocation}
Under [the explicitly stated assumptions], the solution to
[subproblem] satisfies [precise statement].
\end{proposition}

\begin{proof}
[Introduce the objective and feasible set, demonstrate relevant
conditions, derive key steps, and conclude the stated claim.]
\end{proof}

Based on Proposition~\ref{prop:resource_allocation}, we obtain
[the actual closed-form allocation] for [which variables].
```

- 以上是**环境和叙述占位结构**，不是定理或数学证明。
- 避免自己在正文写 `Proposition 1:` 或 `Proof:`，应使用已有 theorem-like environment；模板若提供 `IEEEproof` 则依其实际环境。
- 声明为何定理对算法有用、在哪里应用。如果删掉该命题和证明后正文完全不受影响，要审查是否确有必要。
- 推导必须给出关键步骤：子问题/条件 → 证明结构（例如分情况/拉格朗日/KKT）→ 最优条件 → 解/性质 → 使用位置，别只突然宣布结果。**没有真实证明时不能为了整齐伪造。**
- 证明过长时用自然段/`Case 1 ... Case 2 ...` 等内部结构；若期刊允许可放附录但正文仍交代所用结论。

## 7. 伪代码、复杂度和图示

### 可运行性审查

- **Algorithm 1/2**：Inputs/Outputs 的名称与 P1 和章节一致；每个循环/初始化/调用有清楚的前置条件；资源分配器是 `call ...` 还是在线步骤写明。
- 不能引用后面才创建的变量；应说明在线执行与训练不同的模块开销。
- 可列出训练复杂度与在线推理复杂度（若有依据），确认硬件、规模和循环上界；混合算法还应考虑匹配/求解器迭代成本，不能只算神经网络的前向推理。
- 绘制算法框图：用实线箭头表达数据输入/输出，虚线或另一形式表达学习反馈；每条箭头在正文可解释。

### 算法章节正文组织示例

第一段：本节提出 XX algorithm 用于求解 XXOP，指出**整体**由 A/B/C 组成并说明为何这个组合合理。

第二段：解释决策拆分的原因（例如连续时间决策 vs 变维分配；前提须真实）及数据流。

后续小节：POMG 描述；各模块（按照依赖）、MADDPG 训练；Algorithm 汇总与复杂度分析。**标题级别跟包含关系走，不凭长度随意升节。**

## 8. 修改自检

- [ ] CORA 的全称、缩写、作用与算法名称在 Intro 第一次出现与本章一致。
- [ ] 全部决策空间、学习动作空间、外部解的区别交代清楚。
- [ ] 区域划分、策略输出、分配资源、执行回退、cost/reward 算法的先后可以画成无歧义流程图。
- [ ] 每个模块只保留一个职责；标题使用一致的名词层级。
- [ ] Reward 分段且权重、量纲、约束位置明确。
- [ ] theorem/proposition/proof 有正式环境、前提、正文引用、作用说明。
- [ ] 闭式解可追溯到子问题/推导；MADDPG 更新既数学合理也与实际实现一致。
- [ ] 训练/在线复杂度分别有真实成本来源。

**原批注对应**：23–31、W-01、W-03；审阅会议 00:49–01:14；参考 Qin Section 5 与 Qi Section 4。注意两篇采用不同的模块组合，借鉴组织方式而非强制复刻算法。
