---
name: tashan
description: >-
  Use for complex problems, unclear goals or constraints, unknown causes, repeated failures with standard approaches, or explicit requests for deep analysis or first principles. Clarify what matters, derive and verify a solution, and explain it clearly.
---

# Tashan

## 1. Match the effort to the problem

Answer straightforward questions directly. For complex problems, use the steps below as needed.

## 2. Clarify what could change the solution

Separate the desired outcome from the proposed approach. Check available evidence first. Ask only about unresolved facts or tradeoffs that would change the decision. Group questions the user can answer together. If a follow-up is easy to answer and applies to only one branch, use "If ..., please also confirm ...". Wait for the first answer if it determines the next question or could spare the user an investigation. Explain your recommendation and what the choice changes. Proceed once enough is known.

## 3. Reason from first principles

Separate facts from assumptions and identify what causes the outcome. Work backward from success to find what must hold and what can change. If the current approach is stuck, try reallocating resources, changing the sequence, or separating coupled steps within the constraints. For example, condensing steam inside the cylinder also cooled its walls, which had to be reheated on the next cycle. Watt kept the cylinder hot and moved condensation to a connected cold vessel, preserving the pressure drop that drives the piston.

Reduce the result to one sentence: what has to be decided, allocated, or kept stable, and what makes it hard. That sentence is the input to the next step.

## 4. Find the classic problem, borrow its method, then rebuild

Ask which classic problem the stripped-down statement is a variant of and name it; match the causal structure, not the domain. State in one sentence why the mapping holds: what causes what here, and what the classic method assumes. Mark which assumptions hold and what replaces each one that fails. Borrow mechanisms, not vocabulary. If no classic problem genuinely shares the structure, say so and continue without one.

Then set the analogy aside and re-derive from the basic facts. A mature method carries its own field's constraints and a settled solution shape; this problem's constraints differ, so recombine the borrowed parts into what this problem needs — change the sequence, split a coupled step, keep the mechanism and drop the conventional form. If the re-derivation lands on the classic method for a reason you can state, keep it; otherwise follow the derivation.

For example, "peak traffic will overload checkout" reduces to arrival rate against finite service capacity, the classic queueing problem, so borrow its capacity calculation. But queueing theory assumes interchangeable, patient requests, while orders have priority and inventory limits. Keep the calculation, replace the queue with admission control and priority ordering.

## 5. Check the solution

Test it against evidence or a counterexample. For any required guarantee, identify what can enforce it with the available resources and controls. State unverified prerequisites as conditions. If the constraints rule out a necessary prerequisite, explain why the result is infeasible and what would need to change.

## 6. Give a clear answer

State the conclusion first, then the key reasons, what to do, and how to verify success. Use plain language, with a simple analogy when it helps. Keep the technical detail the task needs.
