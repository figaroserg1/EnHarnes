---
name: startup-anti-overengineering
description: Enforce pragmatic startup engineering. Prefer simple, readable, low-complexity solutions over speculative architecture. Optional — install only if your team follows lean/startup methodology. Once installed, rules are mandatory.
---

# Startup Anti-Overengineering Rules

**Optional skill. If installed — strictly enforced.**

These rules override architectural preferences when they conflict. They do NOT override safety rules (golden principles, security, boundary validation).

## When Active

Apply these rules to ALL code changes: new features, refactors, reviews, and plan creation. When the agent-reviewer skill runs, it must also check against these rules.

---

## Rule 1: Simplicity First

Startup code must be easy to ship, read, and change.

**Detection:** A solution adds layers, patterns, or indirection not required for the current task.
**Action:** Choose the simplest working implementation: function over class, module over layer, explicit code over abstraction.

## Rule 2: No Speculative Architecture

Most future assumptions are wrong; premature architecture slows iteration.

**Detection:** Interfaces, factories, strategies, extension points, or service splits exist only "in case we need them later."
**Action:** Do not add them. Build only for current requirements.

## Rule 3: Abstraction Only After Repetition

Real duplication is cheaper than premature abstraction.

**Detection:** An abstraction is proposed before multiple real use cases exist.
**Action:** Introduce abstraction only if ALL are true:
- 3+ real repeated cases exist
- Complexity is reduced now
- Readability improves

## Rule 4: Readability Over Pattern Purity

Code should be understandable quickly by another engineer.

**Detection:** Understanding requires jumping across many files, layers, or wrappers.
**Action:** Prefer direct, linear, top-to-bottom code flow.

## Rule 5: Linear Flow Is Good

For startup products, straightforward execution is usually better than "clean" indirection.

**Detection:** Simple business logic is wrapped in managers, handlers, adapters, or orchestration classes without real need.
**Action:** Keep the flow explicit and close to the product scenario.

## Rule 6: Minimal Layers

Every extra layer increases cognitive load and slows changes.

**Detection:** A chain like controller → service → manager → handler → adapter exists without clear boundaries.
**Action:** Add a layer only for:
- External integrations
- Async processing
- Security isolation
- Transaction boundaries

## Rule 7: Explicit Dependencies

Hidden magic makes debugging and onboarding harder.

**Detection:** The design depends on runtime injection, dynamic resolution, or framework magic.
**Action:** Prefer explicit parameters, direct imports, and visible wiring.

## Rule 8: Monolith by Default

One service, repo, and DB maximize speed early on.

**Detection:** Microservices or distributed boundaries are proposed without proven need.
**Action:** Stay monolithic unless scale, domain boundaries, or multi-team ownership are already real.

## Rule 9: Pragmatic Duplication Is Acceptable

Small duplication is often cheaper than the wrong abstraction.

**Detection:** Code is being generalized too early only to remove limited repetition.
**Action:** Allow small duplication if it keeps the code clearer.

## Rule 10: Tech Debt May Be Intentional

Temporary shortcuts can accelerate product learning.

**Detection:** A shortcut is needed to ship faster.
**Action:** Allow it only if:
- It is visible in code (comment with rationale)
- Its risk is understood
- It will be revisited when it starts slowing development

## Rule 11: Refactor Only on Real Signals

Refactoring without pain signals wastes time.

**Detection:** Refactor is proposed mainly for aesthetics or architectural neatness.
**Action:** Refactor only when there is:
- Repeated logic causing bugs
- Difficult modification blocking a feature
- Recurring bugs in the same area

## Rule 12: Code Review Is a Complexity Filter

Reviews should reduce long-term complexity, not reward pattern usage.

**Detection:** A change adds abstraction, indirection, or layers.
**Action:** Ask:
- Did this simplify the code today?
- Does it solve a real current problem?
- Will it make future changes faster?

If any answer is no, prefer the simpler version.

---

## Default Behavior

When multiple solutions are possible:
1. Choose the least abstract one
2. Choose the most explicit one
3. Choose the easiest one to change next month

## Output Mode

When generating or reviewing code:
- Optimize for clarity
- Optimize for speed of iteration
- Avoid overengineering by default
- Do not suggest advanced architecture unless explicitly required
