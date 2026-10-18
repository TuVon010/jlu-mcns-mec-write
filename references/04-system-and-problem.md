# System Model 与 Problem Formulation 写作指南

## 目录
1. 章节结构与模型归属
2. System Overview：先图后层，再时间
3. Basic/Task/Mobility Model
4. Communication Model
5. Computation/Energy/Offloading/Priority Model
6. Problem Formulation 与 Analysis
7. 公式引出与 LaTeX 小样
8. 严谨性自检

## 1. 先把系统模型重新分层

基于批注 10、14、18 和两篇参考论文，优先考虑如下组织（可依实际系统调整，不要硬套）：

```text
III. System Model
    A. System Model
       1) System Overview
       2) Basic Models
          UD and Task Model / Task Priority
          UAV Mobility and Node States
    B. Communication Model
       1) UD–UAV Link
       2) Other Links [only if actually modeled]
    C. Computation Model
       1) Local Computing
       2) Edge Computing and Partial Offloading
       3) Delay and Energy Consumption
IV. Problem Formulation and Analysis
    A. Problem Formulation
    B. Problem Analysis [if technically needed]
```

具体采用 IEEEtran 哪种标题层级以模板为准；三级之下用加粗段首标签即可。部分论文把 Problem Formulation 放在 Section III 的末尾（如 Qi），另一篇把它单独设为 Section IV（如 Qin）；两种均可，依内容体量/目标期刊选择，不把页码/节号视为固定标准。

判断一个模型归属的原则：

- **基础模型**：节点/任务/移动/位置/约束等所有后续模块共享的信息。
- **通信模型**：连接路径、链路条件、信道增益、速率和传输时延/能耗（依论文组织可在计算模型统一汇总 end-to-end cost）。
- **计算模型**：部分卸载比例、本地/边缘执行时延与能耗、各端算力分配和任务完成逻辑。
- **任务优先级**：属于 UD/task 属性，优先放在 `UD and Task Model`；若是较复杂的独立贡献，允许与 Communication/Computation 平行建 Task Priority Model，但需给出原因。
- **优化问题**：目标/决策/约束属于 Problem Formulation，不应把它们散落当作单个新的“模型”小节。

### 为什么“Offloading Model”不宜贸然独立

如果只是重复定义一个决策变量，就在后续真正使用它的公式前介绍；如果卸载比例是本地/边缘任务划分前提、会高频出现，则在 Computation Model 开头单独一小段定义即可。这正是师姐结合 Qin 部分卸载写法所说的**局部前置、服务于后续公式**，不意味着任何卸载决策都禁止单独小节。

## 2. System Overview：先给读者完整地图

推荐四个动作：

1. `As illustrated in Fig.~\ref{fig:architecture}, we consider ...` 描述系统、场景、主要目标。
2. 总述系统**由哪些层/角色**组成；如用户层、空中服务层、控制层。特别核对“高空大 UAV 只做控制，不承接用户计算任务”的真实设定，不能叫它边缘服务器或云服务器。
3. `Specifically, ...` 顺序解释**每一层职责**：谁产生任务、谁承接计算、谁调度、谁通信。图中的节点与文字一一对应。
4. `Moreover, the operation period is divided into ...` 引入时隙集合、时隙长度、离散/准静态假设，以及时隙内外变化条件。

错误示例：先介绍 UD 和 service layer → 突然跳到 SUAV → 再返回 service layer → 再谈任务。应一次讲完同层对象，读者才能绘出系统拓扑。

**核对清单**：节点所属层；是否真的存在云/控制层；谁有算力和电池约束；哪些链路可用；谁给谁卸载；移动位置和高度是否随时间变；训练/在线决策在哪个节点执行（如属于算法层也可以在 Algorithm 中说明）。

## 3. Basic Models：按需求介绍实体和状态

### UD and Task Model

- UD 标识与集合；位置/本地 CPU 资源/能量预算/生成任务规律。
- 任务模型 `(input size, CPU cycles, deadline, optional priority)`；各变量首次定义时给物理量/单位。
- 优先级若存在：说明来源（任务类别/严重程度/截止时间等**实际假设**）、定义范围和含义；区分“高 priority 权重”与“完成失败惩罚”的关系。严禁无依据地用 `not equally urgent, nor do their failures carry equal consequence` 这类语义生硬且未定义的句子。
- 任务是否可分、部分卸载是否可并行、本地剩余任务和边缘部分怎么共同决定**完成时延**。公式必须匹配计算执行规则；`sum`、`max` 不可随意替换。

### UAV/UD Mobility and Constraints

- 位置、速度、方向、固定/可变高度、时隙 `t` 与 `t+1` 的对应。
- `trajectory evolves as ...` 引出运动方程；紧接着解释速度/边界/安全距离限制（成组子公式允许）。
- 使用同一坐标系、相同 t 约定；飞行距离/速率若影响推进能耗必须可追溯。
- 控制 UAV 与搭载 MEC 的服务 UAV 如是两种角色，分开说明并采用一致缩写。

## 4. Communication Model：先速率后解释组成

段落层级：

1. 概述接入方式（OFDMA/TDMA/其他）、链路类型、必要假设与覆盖限制。
2. 引出：`The uplink transmission rate from UD i to UAV u in slot t is given by`，然后写**真实**速率公式。
3. 解释带宽、分配系数、发送功率、增益、噪声等变量；若信道增益复杂，单独解释路径损耗/小尺度衰落模型及适用条件。
4. 仅给任务使用到的速率/链路时延，并指向计算模型的端到端成本。

避免单独给所有显然的距离公式单独编号；可在解释句写 `d_{i,u}(t)=\|\mathbf q_i(t)-\mathbf q_u(t)\|`，仅在频繁引用、结构关键或后续推导需要时独立编号。

大尺度衰落（路损/阴影）和小尺度衰落（Rician/Rayleigh 等）是否加入、具体分布、参数与单位，取决于系统任务的证据与建模需求；**不能为了显得先进擅自增加 fading 项**。

## 5. Computation/Energy：先总关系，后必要分解

### 部分任务卸载

首次介绍卸载比例时一句建立“任务被切成什么、在哪里计算”：

> `The offloading ratio [actual symbol] denotes the fraction of the task processed by an edge server; the remaining portion is executed locally.`

若其他场景包含多个不同目的地，比例之和、关联限制和互斥性要在变量/约束中明说。

### 分别推导本地、边缘和总成本

- `Local Computing`：本地执行周期、可用频率、能耗模型（要与真实频率依赖吻合）。
- `Edge Computing`：传输+边缘处理+潜在返回时间；资源分配参数、CPU capacity 约束。
- `Total Task Completion Delay`：串行和并行执行的汇总规则需明示；仅凭模版不可确定。
- `Energy Model`：UD 本地计算和上行通信能耗，与 UAV 飞行/悬停/计算能耗分开定义，系统目标优化谁的成本需要明确。

### 示例：三个能耗公式如何正确引出（示意，不是具体的 UAV 物理模型）

```latex
The slot-level energy consumption of UAV $u$ consists of propulsion
energy and computation energy, which is expressed as
\begin{equation}
  E_u^{\mathrm{tot}}(t)
  = E_u^{\mathrm{fly}}(t) + E_u^{\mathrm{comp}}(t).
  \label{eq:uav_total_energy}
\end{equation}
Specifically, $E_u^{\mathrm{fly}}(t)$ represents the propulsion energy,
which depends on [actual flight variables]. It is calculated as
\begin{equation}
  E_u^{\mathrm{fly}}(t) = \text{[verified propulsion model]}.
  \label{eq:uav_flight_energy}
\end{equation}
Similarly, the computation energy $E_u^{\mathrm{comp}}(t)$ is given by
\begin{equation}
  E_u^{\mathrm{comp}}(t) = \text{[verified computation model]}.
  \label{eq:uav_computation_energy}
\end{equation}
```

`[verified ...]` 是**示意占位符，不是可编译数学结果**；正式稿中只能填真实模型。若实际模型还包括通信或悬停额外项，总公式必须随之修改。写这三步比将三个不同公式裸列在一个 display 环境清楚。

## 6. Problem Formulation：从性能指标自然过渡到 P1

### 6.1 先单独解释目标构成

遵循：`cost components → per-task/user aggregate → across-time objective → optimize → constraints`。

例如先文字解释“时延成本”，给其公式与变量，再解释“能耗成本”，给其公式，最后解释“weighted total cost”公式；切勿一次推出 3 个独立方程再补解释。

- 任务优先级权重必须精确指向定义它的**已有公式标签**，不用 `obtained in the above equations`。
- 多目标权重的归一化、单位、成本尺度和取值范围明确，否则 delay(s) 与 energy(J) 相加可能没有意义。
- 若包含任务的 deadline/优先级，明确其在目标或硬约束中的位置；奖励函数与任务失败惩罚不等价于物理模型约束。

### 6.2 描述内容性的优化问题，而非“构建一个 MINLP”

> `We formulate a [specific cost] minimization optimization problem (XXOP) by jointly optimizing [actual variables], subject to [key constraints].`

**LaTeX 子公式示意**（符号、函数与索引均是占位，按具体稿件替换）：

```latex
\begin{subequations}\label{eq:problem_p1}
\begin{align}
  \mathrm{(P1)}\quad
  \min_{\boldsymbol{\xi}}\;& C(\boldsymbol{\xi})
  \label{eq:problem_p1_objective}\\
  \text{s.t.}\quad
  & T_i(t;\boldsymbol{\xi}) \leq T_i^{\max}(t),
    \quad \forall i,t,\label{eq:problem_p1_delay}\\
  & E_u(\boldsymbol{\xi}) \leq E_u^{\max},
    \quad \forall u,\label{eq:problem_p1_energy}\\
  & \boldsymbol{\xi}\in\mathcal{X}.
    \label{eq:problem_p1_domain}
\end{align}
\end{subequations}
```

**注意**：`\mathcal{X}` 不是跳过约束的借口，必须在真实论文中展开或明确引用先前定义的轨迹、算力、关联等约束。Objective 以及 constraints (a)/(b)/(c) 对应的实际排版编号会随文档变化，编译验证。上述模型仅是排版蓝图，**不是用户 P1 的数学内容**。

### 6.3 子公式组下逐项解释

> `Constraint \eqref{eq:problem_p1_delay} ensures that ... . Constraint \eqref{eq:problem_p1_energy} limits ... . The feasible set in \eqref{eq:problem_p1_domain} enforces ... .`

时间/能耗/资源/无人机速度/飞行区域/防碰撞/关联一致性/卸载比例域如果属于题目定义，则在模型或者明确的约束引用中一一覆盖；不能只写一堆式子没解释。

### 6.4 Problem Analysis（可选但建议简洁）

列出真实求解困难及其来源：动态性、离散与连续耦合、变量维度随关联改变、非凸信道/轨迹耦合、局部信息、NP-hard 归约（如有）。

- `contains integer and continuous variables and a nonlinear function` 可说明属于 MINLP（前提定义成立）。
- `NP-hard` 要额外证据，不能只用 MINLP 名称推出。
- 如已有确切结构（例如某一子问题凸可解），说明可用于后文确定性求解，但不要提前展示完整更新算法。

## 7. 写作与审查时常用公式叙事短语

| 意图 | 句式骨架 |
| --- | --- |
| 动态定义 | `The [state] of [node] evolves as ...` |
| 速率 | `The transmission rate over [specific link] is given by ...` |
| 构成 | `The total energy consists of A and B, and is expressed as ...` |
| 约束 | `To ensure [physical requirement], [variable] must satisfy ...` |
| 优先级引用 | `Using the task-priority weight defined in \eqref{eq:priority_weight}, ...` |
| 归因后文 | `The resulting service cost is used to formulate [problem] in Section~\ref{...}.` |

## 8. 严谨性自检

- [ ] 系统图每种节点和任务流在文中均出现且角色一致。
- [ ] System Model 节/子节抽象层级合理。
- [ ] 任务重要性、deadline、计算在哪里进行及能耗由谁承担的定义清楚。
- [ ] 公式前引后释，有必要的物理量/单位/限制，没有三公式同时裸列。
- [ ] 决策变量只在真正需要时前置定义，P1 的变量及范围与系统模型相符。
- [ ] Objective 与 Constraints 逐条有编号/引用/解释；`Problem` 带描述性名称。
- [ ] 无无证据的 NP-hard、最优性/可行性/复杂度承诺。

**原批注对应**：10–22、29–30，W-03；参考：Qin Section 3–4；Qi Section 3；组内《科技论文写作笔记》System Model、Problem Formulation 页。
