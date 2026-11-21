---
name: tashan
description: >-
  Use for complex problems, unclear goals or constraints, unknown causes, repeated failures with standard approaches, or explicit requests for deep analysis or first principles. Clarify what matters, derive and verify a solution, and explain it clearly.
---

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
