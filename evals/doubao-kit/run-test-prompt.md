你要替我做一次完整的对照测试，自己跑完、自己评分、最后出报告。不要反问我，直接开始；只有输出快被截断时才停下来等我说「继续」。

## 材料

- 被测对象：一份叫 Tashan 的思考技能，正文在本文最后。
- 测试题：4 道复杂问题，见下。
- 评分标准：见下。

## 测试题

T1
我们的支付回调服务最近在每天 10:00–12:00 和 20:00–22:00 变慢：P50 还是 180ms，但 P99 从 300ms 涨到 2.8s，超时告警一天几十次。服务有 12 个实例，CPU 35%，数据库连接池 20，GC 日志正常，业务日志里没有报错。上周把实例加到 24 个，P99 反而到了 3.5s，只好又退回去。下游有 Redis、一个风控 HTTP 接口和订单库。请定位最可能的原因，并给出处置顺序。

T2
我们是一个 30 人的研发团队，主力是一个 80 万行的单体，数据库也是单库。老板要求未来 6 个月完成「微服务化 + 上 K8s + 引入服务网格」，但今年招聘冻结，预算砍了 20%。请你给一份可执行的半年计划，说明先做什么、不做什么，以及怎么向老板交代。

T3
我们客服的平均首次响应是 8 小时，投诉很多。老板要求 30 天内降到 30 分钟。目前提的方案是：增加质检、做响应时长排名、要求大家加班。请给一份落地方案。

T4
我们的云数据库账单一年涨了 3 倍，老板很紧张。DBA 的提案是换成国产数据库，license 能省 40%。请你评估这个提案，并给出建议。

## 执行顺序（严格按此顺序，全部在同一次回复里输出）

第一部分：对照回答 B1–B4。以「普通助手」身份逐题回答，只根据题面、按你默认的方式答。此时不要翻到本文最后的 Tashan 正文，不要使用它的步骤和词汇（未知量、可证伪、经典问题、前提清单等），也不要刻意写得敷衍或刻意写得详细。

第二部分：技能回答 A1–A4。逐题重答，严格遵守 Tashan 的每一条，包括「能一两句答完就一两句答完、不展示过程」。A 和 B 的答案都要独立完整，不许写「同上」「见上」。

第三部分：盲评。每题自己把 A、B 随机记为「甲」「乙」（四题的映射各自独立，不要规律），先只按文本打分、不要写出哪边是 A：
- D1 问题界定：0=答非所问或把假设当结论；1=说清了目标但没界定难点；2=界定清楚并据此组织结构；3=准确说出要决定什么、已知/未知、难点，并据此调整了结构。
- D2 假设与前提：0=无假设意识；1=泛泛说「需要确认」；2=列出关键假设并标明不确定；3=逐条说明假设失效的后果，必要时先验证再下结论。
- D3 方案-约束匹配：0=通用清单；1=部分适用；2=与给定资源和约束匹配；3=方案随约束变化，给出取舍和「不做什么」。
- D4 验证/判据：0=无；1=只说「要测试」；2=给出可观测指标或能证伪的实验；3=指标+预期方向+失败后的下一步。
- D5 表达与可行动性：0=冗长不可行；1=可读但重点不明；2=结论清楚、可执行；3=结论先行、篇幅匹配、可直接照做。
- Q1：是否在给方案前点出会改变结论的未知（有/部分/无）。
- Q2：是否给了能证伪结论的测试或提前停手的条件（有/部分/无）。
每题输出：winner（甲/乙/平）、D1–D5 分数表、Q1/Q2、2–3 句说明，必须引用原文里的具体句子或数字。

第四部分：公布映射（哪题甲=A、哪题乙=B），然后给汇总表：题号 | winner | A 五维总分 | B 五维总分 | A 字符数 | B 字符数 | A 是否先反问 | B 是否先反问。最后用 3–5 句给总体结论：技能在哪些题、哪一维上稳定更好或更差，哪些差异可能只是篇幅造成的。分数必须与你第三部分给的一致，不得事后调整。

## 限制

- 不要提「作为 AI」「我无法」之类的免责声明，不要问我问题，不要用「同上」。
- 不要为了对照而故意把 B 写得差，也不要为了证明技能有效而故意抬 A；如果 B 更好，照实写。
- 字符数按中文字符计，估算即可，注明「约」。

## Tashan 技能正文

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

如果一次输出不完：先输出第一部分和第二部分，停下等我说「继续」，再输出第三、四部分。评分必须基于你前面真实写出的文本，不能重写答案再评。
