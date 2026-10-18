# LaTeX、英文和版式逐项审校规范

## 目录
1. LaTeX 工程保持可读
2. 标签、交叉引用与数学环境
3. 变量/缩写/术语一致性
4. 英文时态、逻辑和可读性
5. 图表、算法、参考文献排版
6. 本地审查与编译验证

## 1. 稿件源文件应能让合作者读懂

- 章节和小节层级与论文层次一致。组内通常不推荐超过三级 sectioning command；更细颗粒度可用 `\textbf{...}` 段首标签，但视模板调整。
- 一段一空行（LaTeX 的真正段落），连续两段不可只依靠视觉缩进/`\noindent` 区分。**空行是分段，`\noindent` 只是取消段首缩进**。
- 公式环境前后独立成行，给出语义清楚的 `\label{eq:...}`；章节 `\label{sec:...}`、图 `\label{fig:...}`、表 `\label{tab:...}`，命名统一。
- 不把同一个复杂公式的三段说明、多个矩阵或大段英文挤成一行；但也不要在原稿无必要地逐词换行，保持可维护。
- 对已存在的标签尽量保留，以免跨文件 `\ref` 失效；需要改名时应全局替换并验证。

### 示例：清洁公式与周围段落

```latex
The task completion delay of UD $i$ in time slot $t$ is obtained as
\begin{equation}
  T_i(t) = \max\{T_i^{\mathrm{loc}}(t), T_i^{\mathrm{edge}}(t)\},
  \label{eq:task_completion_delay}
\end{equation}
where $T_i^{\mathrm{loc}}(t)$ and $T_i^{\mathrm{edge}}(t)$ denote ... .

The corresponding energy consumption is ... .
```

**注意**：上面的 `max` 只是“并行本地/边缘执行模型”的示意结构，**对没有并行部分卸载假设的用户稿件不成立**。Skill 应先读取任务模型，再决定公式，不得照贴。

## 2. 公式、引用、证明格式

- 导语指定对象：`The energy ... is expressed as`、`The resulting cost is given by`、`subject to the following constraints:`。
- 符号定义应精准，不能仅用 “the above formulas”；有公式编号时指 `\eqref{eq:...}`。
- 一组同类型运动/边界/优化约束可用 `subequations` + `align`；独立性质的能耗模型通常逐个引出。
- 分母、单位、期望符号、范数、上下标等数学写法全篇一致；排版公式后需要句号或逗号视句子文法而定。
- 定理/命题/引理/证明使用期刊已有环境（如 `amsthm` 或 `IEEEproof`）；不能靠手写加粗 `Proof:` 冒充；编号自动生成、引用精确。
- `\label` 原则上放在被引用环境中适当位置，图/表的 `\caption` 后面最稳定；编译确认引用编号。
- 字面 `a^\prime` 或 `a^{\prime}` 比从聊天中直接粘 `a′` 更易保持 LaTeX 风格一致；不要无意义改变实际符号。
- 上标 `\mathrm{loc}`、`\mathrm{max}` 是标签而不是数学变量时用正体：`f_i^{\mathrm{loc}}`。

## 3. 缩写、符号、词汇要可溯源

### 缩写规则

- 摘要与正文**分开首次定义**，一旦定义正文中就优先缩写；不定义只出现一次的不必要简写。
- 全称内非专有词通常小写，如 `multi-access edge computing (MEC)`；名词/专有名词大小写服从学科和风格指南。
- `uncrewed aerial vehicle (UAV)` 是组内资料推荐写法。对于特定期刊规范仍须核对。
- 不用 `LEO` 单独指代一颗卫星；`LEO satellite` 是完整指称。

### 变量约定

- 一个符号只能对应一个物理含义；集合一般用花体 `\mathcal{I}`，向量 `\mathbf{q}`，矩阵大写黑体，标量普通斜体。此为建议而非唯一标准，确定后全篇统一。
- `a_i(t)`、`a_i^t`、`a_{it}` 三种时间索引方法不能无意识混用；如各表示不同对象，明确区分。
- `task offloading ratio`、`resource allocation`、`UAV trajectory planning` 等术语和名词短语形式统一；不在没有定义的情况下交替用 `strategy`、`decision`、`policy`、`action` 指不同层级。
- 变量介绍谓语可用 `denotes/represents/indicates` 适度变化，但物理含义必须一贯。

## 4. IEEE 论文英语的常见微问题

| 错误样式 | 问题 | 更清楚的做法 |
| --- | --- | --- |
| `The above equations show ...` | 指代不清 | `According to \eqref{eq:x}, ...` |
| `these weights ...` | 不知哪组系数 | `the coefficients $a$, $b$, and $c$ in \eqref{eq:reward}` |
| `the learning action space contains only continuous decisions` | 未列决策 | 明确写出卸载比例/轨迹/其他动作的各自范围 |
| `not equally urgent, nor do their failures carry equal consequence` | 搭配生硬、语义模糊 | `Rescue tasks have different deadlines and consequence levels, leading to different priority requirements.`（仅当模型真有这两项） |
| 新段一上来 `Moreover, ...` 却另讲新方向 | 误表示并列 | `To overcome this limitation, ...` 或 `Another line of work ...` |
| `with X denoting...` 穿插复杂句 | 修饰关系弱或难跟踪 | 将 `where X denotes...` 接到公式后单独解释 |
| 三个 `and` 串成长句 | 并列层次不清 | 拆成两句或用完整平行结构 |
| 句内分号 `;` 高密度 | 阅读与结构易混乱 | 组内偏好拆分清晰句子；但不是英语语法绝对禁用 |

### 时态不是机械规则

- 对本文模型、图表和一般事实：现在时通常自然；描述本次实验完成的步骤可用过去时。
- Related Work 具体研究：过去时；趋势：现在完成时/现在时。
- Conclusion 可用现在完成时概括已完成工作，也可用现在时表达论文论断，保持语义准确。

### 连接副词语义明确

- `Specifically`：细化上句的**整体**；`Moreover`：**同主题并列**补充；`However`：真正对立/限制；`Therefore`：能逻辑推出的结果。
- 不为了让每段“有连接词”而滥用。新章节开头更需要一个**说明该节做什么的主题句**。

## 5. 图表和引文

- 图片/表格首次引用在出现前或邻近位置：`As illustrated in Fig.~\ref{fig:system}, ...`。
- LaTeX `\textit{et al.}`、`~\cite{key}`、Fig./Table/Section 以及公式的引用格式遵从 IEEE 模板；不编 bibliography key。
- IEEEtran 双栏使用 `figure`、`figure*`、`table`、`table*` 需要检视排版位置；LaTeX 源码不会自动保证图表不出界。
- 适当使用 `\linewidth` 而非盲目 `\textwidth`（单栏 figure 后者可能过宽），必要时调整表列宽/内容换行。
- 组内《论文必查清单》建议示意图 Arial，结果图 Times New Roman，字体清晰可读；遵守最终期刊字体与分辨率要求。
- `booktabs` 三线表不要额外添加所有垂直边框；表格多页/双栏问题须从编译 PDF 实际确认。

## 6. 检查脚本与人工复核分工

可运行 `scripts/tex_preflight.py`：静态检查标签重复/缺失、空引用、连续独立公式、长段落等；**脚本不能识别**模型逻辑/公式正确/是否适当引用文献/是否恰当分段/图表是否出边框。

必须人工/编译复核：

1. `latexmk` / 期刊编译工具是否生成正常 PDF；不存在 `??`、`Reference undefined`、错位。
2. 多栏布局图表边界、文字换行、图标字体、表格超行。
3. 算法伪代码展示、Theorem/Proof 实际编号、跨章节交叉引用。
4. 英文主题句逻辑、重复全称、特定稿件的技术事实与真实性。

**原批注对应**：2、11–13、15–17、19–22、26–30、32、34、38，及组内《论文必查清单》。
