# iteration-5：第 4 步退出条件写硬后的复测

## 改动

上一轮消融的结论是：第 4 步在诊断/容量类题上有净贡献，但在没有同构经典问题的题（h4）上会诱使模型硬套框架。本轮把它的退出条件从"没有同构问题就说没有"改成**先检验再写**：

> Ask which classic problem the stripped-down statement is a variant of, and test the mapping before writing it: name the causal structure, and state in one sentence what causes what here and which of the classic method's assumptions still hold. If you cannot do that, there is no usable mapping: skip this step entirely, say nothing about an analogy, and continue to the next step.

SKILL.md 4,193 → 4,242 字符（39 → 40 行）；README 第 4 条同步为"先检验映射是否成立，说不出'什么导致什么、前提还成立哪些'就整段跳过"。

## 设计

- 两题：h4-db-cost（上一轮 §4 丢分的那题）与 h1-latency（防止为了 h4 牺牲诊断题收益）。
- 两臂：`new_skill` = 现版本；`old_skill` = iteration-4 的 `with_skill` 答案（即收紧前版本，复用，不重新生成）。
- 两个盲裁判、顺序对调：J1 两题都先 A 后 B，J2 都先 B 后 A；映射见 [judgment/map.json](judgment/map.json)。

## 结果

| 题 | new_skill（J1/J2） | old_skill（J1/J2） | 判定 |
|---|---|---|---|
| h1-latency | 15 / 15 | 14 / 14 | 2:0 新版 |
| h4-db-cost | 15 / 14 | 14 / 14 | 1:0 新版，1 平 |

合计 **3 胜 / 0 负 / 1 平**，五维均分 **14.75 vs 14.0（+0.75）**。数据：[results.json](results.json)，裁判：[judge-1.json](judgment/judge-1.json)、[judge-2.json](judgment/judge-2.json)。

篇幅：h1 4,963 vs 4,977 字节；h4 5,111 vs 5,317 字节（新版都略短）。

## 行为变化（这是本轮真正要看的东西）

- **h4 不再写类比段。** 旧版有一段"借标准成本差异分析、再检验其前提"，J2 认为这是旧版最强处（D2=3），但同一份答案开篇"钱没花在存上"又与后文把多副本/快照列为首要嫌疑冲突，D1 只能给 2。新版直接进入"先证明 40% 从哪来"：存储占 30% 时只解释 4.5 个点，其余 35.5 个点约合涨 50%；再按成本项/环境/工作负载/单位成本四刀归因。J1 给 15、J2 给 14（平）。也就是说：**跳过类比没有损失严谨性，反而消除了一个自相矛盾的来源**。
- **h1 的收益保留。** 新版仍使用排队机制（`S/(1-ρ)`、P99 先于 P50 恶化、下游利用率才是要看的指标），但把它放在"事实与假设要分开"之后，并给出"关掉推荐调用看 P99、注入 500ms 延迟看是否被超时兜住"的证伪实验。两位裁判都给 15，旧版 14。
- 两份新版都没有出现"为流程而流程"的空转段落。

## 局限

- n=2 题、同族裁判、旧版答案复用；+0.75 不是效应量。
- h4 有一票平局，说明改动不是严格更优，只是消除了一个已观察到的失败模式。
- 本轮只验证了"退出条件变硬不会伤 h1/h4"，没有验证它是否减少 h4 在更多算账类题上的硬套率。

## 结论

保留这次改动。它把第 4 步从"总是走一遍"变成"能一句话说清因果与前提才走"，在不损失诊断题收益的前提下，去掉了上一轮观察到的硬套失败模式。

要对外宣称仍需在新题上复现（每层 ≥10 题、预注册判据、含通用提示对照组）；当前证据支持的表述是："对诊断与容量类问题有帮助；对没有同构经典问题的算账类问题，它应当被跳过，且新版本会跳过。"
