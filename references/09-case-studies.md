# 参考论文与组内资料：借鉴写作结构，不照搬研究内容

## 目录
1. 案例定位与使用边界
2. Qin / User-Centric Cost Optimization
3. Qi / Space-Air-Sea Maritime Search and Rescue
4. 组内手册/笔记/批注的交叉验证
5. 如何比较参考写法与自己的论文

## 1. 来源与适用边界

以下是本 Skill 创建时读过的**用户提供原始材料**的“写法索引”，不是新增检索的文献，更不是当前 `manuscript.tex` 的数学正确性验证：

1. Weihong Qin et al., *User-Centric Cost Optimization for Integrated Space-Air-Ground Edge Computing Systems*（用户附件，PDF 约 18 页）：SAGIN-MEC、UCMOP、MADDPG-COCG；属于**结构/混合决策算法写法**的重要范例。
2. Jia Qi et al., *Space-Air-Sea Integrated Multi-Access Edge Computing for Maritime Search and Rescue*（用户附件，PDF 约 17 页）：SASIMEC、DMOP、LPPO-COPG；属于**救援场景叙事/架构到问题的递进**范例。
3. 《写作大纲参考 - JLU MCNS LAB》：Introduction、Related Work、System/Problem/Algorithm/Simulation 的常见大纲；其具体交通/LLM 实验是其他论文示例，**不要移植到 UAV 救援论文中**。
4. 《写作方法与共性问题 - JLU MCNS LAB》：组内常见语法、变量、图表、Related Work 组织方式与场景级挑战注意事项。
5. 《科技论文写作笔记.pptx》：系统模型、公式、证明、仿真写作和 Introduction/Contributions 的思路示意。
6. 《论文必查清单.md》：一致性、格式、引用、变量、图/表、参考文献、Acknowledgment 最终复核。
7. 师姐逐条批注 1–38、微信 W-01–W-03 与 1h+ 会议转写：包括 CORA-MADDPG 的原稿特定反馈。**转写中一些具体算法顺序/节点细节仍需作者核实**。

论文/资料来自用户上传，因此本文内部提及“参考 PDF 第 X 页”用于找写作模式；必要时重新打开原始 PDF 校验页码、公式或真实引用。**不要把两个案例相互混为同一个系统**：Qin 含 ground-air-space 与卫星转发到云端；Qi 是 maritime sea-air-space，USV/UAV/LEO 的任务与计算位置不同，当前用户论文的高空控制 UAV 又可能不同。

## 2. 案例 A：Qin 的写法逻辑

### Introduction（PDF 第 1–2 页）

LAE 应用驱动 → UAV-assisted MEC 的优势与局限 → SAGIN-MEC 融合的必要性 → 三个系统级挑战（高度动态、异构节点协同、部分可观测与混合/变维决策）→ MADRL + 确定性优化的方案 → 四项贡献。

可借鉴：挑战**由系统特性而来**，不是单纯“我们选择 MADDPG 很难”；算法 Motivation 再讲实现/求解挑战。

### Related Work（PDF 第 2–4 页，Section 2）

明确的综述开头。分：`MEC Architecture` → `Formulation of Joint Optimization Problems` → `Optimization Approach`；架构小节从 UAV-enabled 到 satellite-enabled 再到集成架构，每段示例后写 limitations，末段归纳 gap。

可借鉴：通过维度整理文献，不要把一篇论文的系统/目标/算法全部挤到每个子节里。章节标题和稿件自己的贡献一一对齐。

### System Model（PDF 第 4–7 页，Section 3）

`3.1 System Model`（`3.1.1 System Overview`、`3.1.2 Basic Models`）→ `3.2 Communication Model` → `3.3 Computation Model`。基本模型中分别放 UD/UAV mobility、UD/Task 及 satellite state 等，通信与计算分为独立并列层。

可借鉴：系统图先总述、按层解释，然后介绍时间离散化。部分卸载比例放在 Computation 的适当位置，并沿不同执行路径展开成本。

### Problem Formulation（PDF 第 7 页左右，Section 4）

先明确通过联合优化 task offloading ratio、UAV trajectory、CPU resource、UD association 最小化 UD cost；统一给 P 目标与子约束 (22a–22i)，随后逐条解释各类资源/时延/能耗/位置约束，再分析困难。

可借鉴：数学**问题的名字与约束意义**比把它叫 MINLP 更重要；能耗与 deadline 不应忘掉。

### Algorithm（PDF 第 8–12 页，Section 5）

Motivations → POMG 定义（state/observation/action/reward）→ POMG Analysis 识别 hybrid 和 varying-dimensional 决策 → MADDPG 处理任务卸载比和轨迹连续决策 → COCG 处理分配和关联 → Algorithm 汇总与复杂度。

特别重要的写法（源论文中确有）：**POMG 原联合动作集合包含四类决策，而后续通过分析重新定义学习动作子集**。所以当前用户论文若也有“部分学、部分求解器算”的做法，须解释 full decision vs learned action/derived decision 的转换。

### Simulation（PDF 第 13–16 页，Section 6）

Setup（场景/参数/benchmarks/metrics）→ Algorithm Performance → Convergence & Efficiency → Impact of System Settings（UD 数量/任务大小/算力等）→ 可选 trajectory。默认性能图与收敛图均作较充分的机制解释，并讨论 UAV/UD 能耗的权衡。

可借鉴：不同图验证不同内容，不能一个图半段、另一个图三段而没有科学理由。实验“实时性”涉及推理时延和外部资源算法时延两个部分。

## 3. 案例 B：Qi 的写法逻辑

### Introduction（PDF 第 1–2 页）

从 maritime rescue 的高度时间敏感性与基础设施稀缺出发，讲 USV 实时计算需求，再写 conventional MEC 的覆盖限制 → UAV-mounted MEC 的灵活性及航时约束 → space-air-sea 融合必要性 → challenges → LPPO-COPG。

可借鉴：特别适合本用户 Intro 的“**先救援，后 MEC，再 UAV**”逻辑；但 Maritime/USV 的具体事实不可直接移植到地面 UD 场景。

### Related Work（PDF 第 2–4 页，Section 2）

`Maritime Search and Rescue Communications` → `Edge Computing Architecture` → `Optimization Approaches`。篇章从通信覆盖到计算资源，再到优化方法，**是与论文真实贡献一致的另一种合理组织**，不是 Qin 三分法的唯一替代。

可借鉴：先判断自己的 novelty 着重通信、MEC 架构、模型还是优化问题，再决定相关工作该怎样分。

### System 与 Problem（PDF 第 4–7 页，Section 3）

`3.1 System Model` → `3.2 Communication` → `3.3 Computing` → `3.4 Problem Formulation and Analysis`。同一章中完成模型到问题的过渡。目标为 DMOP（总服务时延最小化），联合 UAV trajectory、bandwidth and computing allocation、task offloading。

可借鉴：模型和问题可以合章，但过渡必须明确；成组约束和各自解释均不能省。

### Algorithm（PDF 第 7–12 页，Section 4）

先 Motivation，随后 MDP 的各个要素；对联动/混合决策进行分析，再将学习的轨迹动作和外部优化的资源/卸载策略分开，最终汇成 LPPO-COPG。理论部分有关于子问题的推导与分工。

可借鉴：要先解释“为何拆分”，再引入“如何拆分”，还要把外部求解结果回到整体目标中。需要注意 Qi 的方法是 MDP/LPPO，不可误称 MADDPG/POMG。

### Simulation（PDF 第 12–16 页，Section 5）

先模型配置与 benchmark，再给默认性能图（完成率、时延、不同节点能耗），收敛/稳定性，然后系统参数敏感性；解释性能提升伴随的 UAV 能耗变化。

可借鉴：图分析包括 trade-off，而不是只挑“优势”指标。

## 4. 手册与批注的交叉验证

| 命题 | 组内资料/师姐意见 | 案例位置 | 在用户原稿中怎么用 |
| --- | --- | --- | --- |
| Introduction 先描述背景需求和系统挑战 | 写作笔记 Introduction；批注 1 | Qi Introduction；Qin Introduction | 用本文真实灾后/应急任务代替海上/LAE 事实 |
| Related Work 按架构/目标/算法分方向 | 共性问题第 2 页；批注 5–9 | Qin Section 2，Qi Section 2 的变体 | 一节一个视角，有主题句与 gap |
| 模型先总览、基础/通信/计算再问题 | 写作笔记 System Model；批注 10–22 | Qin Section 3–4；Qi Section 3 | 控制 UAV 与服务 UAV 角色先说明 |
| DRL 壳内模块必须有明确依赖 | W-01；会议 00:50–01:08 | Qin Section 5；Qi Section 4 | 确认区划、actor、CPU 优化、最终 reward 依赖 |
| 段落/公式不能裸列、需引入与解释 | 共性问题第 3、9 页；批注 16–17、21、29 | 两篇模型和问题章节 | 多公式按“总式→组成”改写 |
| 实验默认指标→收敛→系统设置 | 写作笔记仿真部分；批注 36–37 | Qin Section 6；Qi Section 5 | 指标与贡献一一映射，不机械照搬图号 |

## 5. 最有效的参考方法

1. **先列本文自己的模型事实**：节点、场景、决策、约束、算法模块、实验指标；没输入不要凭论文截图复制科学主张。
2. **找同类型论文的对应段落**：比如 Intro 背景段、System Overview 总分段、Problem Constraints 解释段、Algorithm Analysis 段、图 3 解释段。
3. **抽出结构**：主题句类型、证据排序、过渡、结论的作用，不采集成片原句。
4. **用自己的变量/数学模型重写**，再查来源/术语/标签/各章交叉一致性。
5. **标明不适用项**：Qin 的 satellite relay、Qi 的 maritime USV、用户高空控制 UAV 不能随意互换。

**重要**：这些参考 PDF/手册并非自动永久随 ZIP 携带；本 ZIP 仅内置提炼后的规则。若需要逐式对照其数学推导，请在新对话重新提供 PDF 或可访问的资料。
