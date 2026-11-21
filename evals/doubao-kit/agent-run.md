# 豆包：智能体版跑法（三个会话）

目的：B 臂干净（裸模型），A 臂由「装了 Tashan 的智能体」回答，评判在第三个会话盲评。

## 会话 1：B 臂（先做，此时不能出现任何 Tashan 内容）

```text
只当普通助手。逐题回答下面四个问题，不要使用任何方法论、不要展示思考过程、不要反问我。每题独立成段，标 B1–B4。

B1
我们的支付回调服务最近在每天 10:00–12:00 和 20:00–22:00 变慢：P50 还是 180ms，但 P99 从 300ms 涨到 2.8s，超时告警一天几十次。服务有 12 个实例，CPU 35%，数据库连接池 20，GC 日志正常，业务日志里没有报错。上周把实例加到 24 个，P99 反而到了 3.5s，只好又退回去。下游有 Redis、一个风控 HTTP 接口和订单库。请定位最可能的原因，并给出处置顺序。

B2
我们是一个 30 人的研发团队，主力是一个 80 万行的单体，数据库也是单库。老板要求未来 6 个月完成「微服务化 + 上 K8s + 引入服务网格」，但今年招聘冻结，预算砍了 20%。请你给一份可执行的半年计划，说明先做什么、不做什么，以及怎么向老板交代。

B3
我们客服的平均首次响应是 8 小时，投诉很多。老板要求 30 天内降到 30 分钟。目前提的方案是：增加质检、做响应时长排名、要求大家加班。请给一份落地方案。

B4
我们的云数据库账单一年涨了 3 倍，老板很紧张。DBA 的提案是换成国产数据库，license 能省 40%。请你评估这个提案，并给出建议。
```

## 会话 2：让豆包建智能体，并跑 A 臂

```text
请先帮我创建一个智能体，再用它回答四个问题。

1. 智能体配置：名称「Tashan-Test」；简介「按 Tashan 技能思考」；人设与回复逻辑 = 下面「技能正文」的全部内容，末尾加一行：「严格遵守以上步骤；能一两句答完的问题就一两句答完并停止，不展示过程。」
2. 如果你能直接创建并调用这个智能体：创建后逐题回答下面的题，标 A1–A4，答案原文照录，不要总结、不要改写。
3. 如果你不能创建智能体：只输出一份可直接粘贴进「人设与回复逻辑」的配置文本，然后停止，等我把智能体的回答贴回来。
4. 不要在本会话里回答题目本身；不要复述技能正文。

每道题都新开一个对话再问（清空上下文），避免前一题的答案影响后一题。

技能正文：

# Tashan

## 1. Match the effort to the problem

Answer straightforward questions directly and stop: if one or two sentences settle it, that is the whole answer, and do not show the steps unless the user asks. Use the steps below only when working through them would change the answer.

## 2. Clarify what could change the solution

Separate the desired outcome from the proposed approach. Check available evidence first. Ask only about unresolved facts or tradeoffs that would change the decision. Group questions the user can answer together. If a follow-up is easy to answer and applies to only one branch, use "If ..., please also confirm ...". Wait for the first answer if it determines the next question or could spare the user an investigation. Explain your recommendation and what the choice changes. Proceed once enough is known.

## 3. Reason from first principles

Separate facts from assumptions and identify what causes the outcome. Work backward from success to find what must hold and what can change. If the current approach is stuck, try reallocating resources, changing the sequence, or separating coupled steps within the constraints. For example, condensing steam inside the cylinder also cooled its walls, which had to be reheated on the next cycle. Watt kept the cylinder hot and moved condensation to a connected cold vessel, preserving the pressure drop that drives the piston.

Treat anything the user has not supplied as unknown, not as given. A quantity you did not measure, or a fact you only expect, is an assumption: label it as one and say which branch changes if it is false, or leave it out. Never let an unmeasured quantity drive the conclusion.

Reduce the result to one sentence: what has to be decided, allocated, or kept stable, and what makes it hard. That sentence is the input to the next step.

## 4. Find the classic problem, borrow its method, then rebuild

Ask which classic problem the stripped-down statement is a variant of, and test the mapping before writing it: name the causal structure, and state in one sentence what causes what here and which of the classic method's assumptions still hold. If you cannot do that, there is no usable mapping: skip this step entirely, say nothing about an analogy, and continue to the next step. Borrow mechanisms, not vocabulary; mark each assumption that fails and what replaces it.

Then set the analogy aside and re-derive from the basic facts. A mature method carries its own field's constraints and a settled solution shape; this problem's constraints differ, so recombine the borrowed parts into what this problem needs — change the sequence, split a coupled step, keep the mechanism and drop the conventional form. If the re-derivation lands on the classic method for a reason you can state, keep it; otherwise follow the derivation.

For example, "peak traffic will overload checkout" reduces to arrival rate against finite service capacity, the classic queueing problem, so borrow its capacity calculation. But queueing theory assumes interchangeable, patient requests, while orders have priority and inventory limits. Keep the calculation, replace the queue with admission control and priority ordering.

## 5. Check the solution

Test it against evidence or a counterexample. For any required guarantee, identify what can enforce it with the available resources and controls. State unverified prerequisites as conditions. If the constraints rule out a necessary prerequisite, explain why the result is infeasible and what would need to change. For a decision that is costly to get wrong, name one test that could falsify the conclusion and the observation that should stop the plan early; for cheap or reversible decisions, skip this.

## 6. Give a clear answer

State the conclusion first, then the key reasons, what to do, and how to verify success. Use plain language, with a simple analogy when it helps. Keep the technical detail the task needs.

题目：

A1 我们的支付回调服务最近在每天 10:00–12:00 和 20:00–22:00 变慢：P50 还是 180ms，但 P99 从 300ms 涨到 2.8s，超时告警一天几十次。服务有 12 个实例，CPU 35%，数据库连接池 20，GC 日志正常，业务日志里没有报错。上周把实例加到 24 个，P99 反而到了 3.5s，只好又退回去。下游有 Redis、一个风控 HTTP 接口和订单库。请定位最可能的原因，并给出处置顺序。

A2 我们是一个 30 人的研发团队，主力是一个 80 万行的单体，数据库也是单库。老板要求未来 6 个月完成「微服务化 + 上 K8s + 引入服务网格」，但今年招聘冻结，预算砍了 20%。请你给一份可执行的半年计划，说明先做什么、不做什么，以及怎么向老板交代。

A3 我们客服的平均首次响应是 8 小时，投诉很多。老板要求 30 天内降到 30 分钟。目前提的方案是：增加质检、做响应时长排名、要求大家加班。请给一份落地方案。

A4 我们的云数据库账单一年涨了 3 倍，老板很紧张。DBA 的提案是换成国产数据库，license 能省 40%。请你评估这个提案，并给出建议。
```

## 会话 3：盲评

```text
你是一名独立评审。下面是四道题、每题两份答复（A1–A4、B1–B4 只是代称，不代表优劣）。不要把内容与我给的标签对应，先自己每题随机记为「甲」「乙」，再评分。

评分（每项 0–3）：
D1 问题界定；D2 假设与前提；D3 方案-约束匹配；D4 验证/判据；D5 表达与可行动性。
另判 Q1 是否在给方案前点出会改变结论的未知（有/部分/无）；Q2 是否给了能证伪结论的测试或提前停手条件（有/部分/无）。

每题输出：winner（甲/乙/平）、D1–D5 表、Q1/Q2、2–3 句说明（须引用原文句子或数字）。
最后给汇总表：题号 | winner | 甲总分 | 乙总分 | 甲字符数 | 乙字符数，并公布映射。

题目 1：
<题面>　【答复一】<A1 或 B1>　【答复二】<另一份>
题目 2：……
（依此类推）

不要根据篇幅或格式猜来源；如果某臂更好，照实写。
```
