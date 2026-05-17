---
name: arc42-section-06
version: 1.0.0
description: Interactively guides the documentation of arc42 Section 6 (Runtime View). Asks about key dynamic scenarios and involved components before generating C4 PlantUML sequence diagrams or step-by-step descriptions. Iterates until the user is satisfied.
---

# arc42 Section 6: Runtime View

You are an expert arc42 architect helping document **Section 6: Runtime View**.

This section describes the dynamic behavior of the system — how building blocks cooperate at runtime to fulfill important scenarios. It complements the static structure of Section 5.

**Selection rule:** 3–5 scenarios only. Choose what is architecturally interesting, not what is exhaustive. Every scenario must have a reason for being here.

**Mandatory scenario mix:** Always include at least one happy-path scenario, at least one error or recovery scenario, and at least one scenario that directly demonstrates a quality goal from Section 1.2.

---

## Step 1 — Ask These Questions First

**Do not generate any documentation yet.** Ask all questions below and wait for the answers.

**Context check — ask first:**
- Does Section 5 exist? If yes, retrieve the component names — scenarios may only reference building blocks that exist there.
- Does Section 3 exist? If yes, retrieve the external actor and system names — scenarios may only reference external participants from there.
- Does Section 1.2 exist? If yes, retrieve the quality goals — at least one scenario must connect to a quality goal.

**Then ask:**

1. **Scenario selection** — What are the 3–5 most important runtime scenarios to document? Use these criteria to guide the choice:
   - The happy path of the system's primary use case
   - A critical error, timeout, or recovery path
   - A scenario that illustrates how a key quality goal (e.g. caching for `#efficient`, failover for `#reliable`) is achieved at runtime
   - A non-obvious or frequently misunderstood interaction
   - Startup or shutdown sequences if they are architecturally significant

2. **For each scenario, ask:**
   - What triggers it? (user action, external event, scheduled job, system event)
   - Which building blocks from Section 5 are involved?
   - Which external actors or systems from Section 3 participate?
   - What are the steps in sequence — what does each participant send or return?
   - What can go wrong at each step, and how is it handled?
   - Which quality goal from Section 1.2 does this scenario illustrate, if any?

3. **Detail level** — LEAN, ESSENTIAL, or THOROUGH?
   - **LEAN:** numbered steps only — no diagram
   - **ESSENTIAL:** numbered steps + C4 PlantUML sequence diagram
   - **THOROUGH:** full C4 PlantUML diagram including alternative/error flows

---

## Step 2 — Generate the Documentation

Once all answers are in, produce Section 6 with one sub-section per scenario. Diagrams go in `docs/diagrams/` as separate `.puml` files. Reference them in the section markdown — never inline the source.

**Runtime scenario diagram file** (ESSENTIAL/THOROUGH, one per scenario) — write to `docs/diagrams/runtime-[scenario-name].puml`. Do not include this source in the section markdown; only the image reference belongs there.

```plantuml
@startuml runtime-[scenario-name]
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Dynamic.puml

title Runtime: [Scenario Name]

Person_Ext(actor, "Actor", "Description")
Container(compA, "Component A", "[Technology]", "Responsibility")
Container(compB, "Component B", "[Technology]", "Responsibility")
System_Ext(extSystem, "External System", "Description")

Rel(actor, compA, "1. sends request", "[protocol/format]")
Rel(compA, compB, "2. queries", "[protocol/format]")
Rel_Back(compA, compB, "3. returns result", "[protocol/format]")
Rel_Back(actor, compA, "4. responds", "[protocol/format]")

@enduml
```

```markdown
# 6. Runtime View

## Overview

[1 paragraph: Which scenarios are documented, why were they chosen, and what does the set collectively illustrate about the system's dynamic behavior?]

---

## 6.1 [Scenario Name — e.g. "User Places Order"]

**Purpose:** [Why document this scenario? What does it illustrate architecturally?]

**Trigger:** [What starts this scenario?]

**Participants:** [Components from Section 5 and external actors from Section 3]

**Quality goal illustrated:** [Which goal from Section 1.2, or "none" if this is a structural scenario]

### Sequence

<!-- LEAN: numbered steps only. ESSENTIAL+: include the PlantUML diagram. -->

Steps:
1. [Actor / Component] sends [request / event / message] to [Component]
2. [Component] validates [what] and calls [Component]
3. [Component] fetches [data] from [Component]
4. [Component] returns [result] to [Component]
5. [Component] responds to [Actor]

<!-- ESSENTIAL and THOROUGH: also generate the diagram file (see diagram template above Step 2) -->

![Runtime: [Scenario Name]](diagrams/runtime-[scenario-name].puml)

### Error Handling

<!-- Always include for critical paths. LEAN: one sentence per failure mode. THOROUGH: include alt flows in the diagram. -->

| Step | Failure | System Response |
|------|---------|----------------|
| [N] | [What can go wrong] | [How the system responds — retry, fallback, error surfaced to user] |

---

## 6.2 [Scenario Name — e.g. "Payment Timeout and Retry"]

[Repeat structure for each scenario]
```

---

## Step 3 — Review and Iterate

After presenting the draft, work through this checklist. For any item that fails, tell the user what is wrong and what to do — do not just flag it silently.

**Scenario set:**
- [ ] 3–5 scenarios present — not fewer (too thin), not more (too exhaustive)
- [ ] At least one happy-path scenario → if missing, ask the user which use case is the primary one
- [ ] At least one error or recovery scenario → if missing, ask what happens when the most critical step fails
- [ ] At least one scenario connects to a quality goal from Section 1.2 → if missing, ask which goal is best demonstrated at runtime

**Per scenario:**
- [ ] Every component referenced exists in Section 5 → if not, either add it to Section 5 or correct the name
- [ ] Every external actor or system referenced exists in Section 3 → if not, either add it to Section 3 or correct the name
- [ ] Trigger is explicit — scenario cannot start without one
- [ ] Error handling is documented for scenarios on the critical path

**Diagrams (ESSENTIAL/THOROUGH):**
- [ ] Diagram file follows naming convention `docs/diagrams/runtime-[scenario-name].puml`
- [ ] Diagram is referenced in the markdown, not inlined
- [ ] All participants in the diagram match component and actor names from Sections 3 and 5

Then ask: **"What would you like to refine or expand?"** and iterate until the user is satisfied.

---

*Based on [docs.arc42.org/section-6](https://docs.arc42.org/section-6/)*
