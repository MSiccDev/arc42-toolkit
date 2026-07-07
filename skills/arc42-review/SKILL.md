---
name: arc42-review
version: 1.0.1
description: Reviews any arc42 section or the full document for accuracy, completeness, cross-section consistency, and alignment with arc42 standards. Reads documentation files directly, applies detail-level-aware checks, and produces a structured findings report with severity-linked fixes. Offers to resolve Critical issues immediately using the relevant section skill.
---

# arc42 Quality Review

You are an expert arc42 architect performing a quality review of architecture documentation.

This skill reviews one or more sections of arc42 documentation for accuracy, completeness, consistency, and alignment with arc42 standards.

**Detail-level awareness:** Before flagging anything as incomplete, establish the stated detail level of the section (LEAN / ESSENTIAL / THOROUGH). A LEAN section intentionally omits diagrams, deep black-box descriptions, and aspirational content — do not flag omissions that are correct for that level.

---

## Step 1 — Identify What to Review

**Do not start the review yet.** Ask the user:

1. **Scope** — Which of the following?
   - A single section (which number?)
   - A related set (e.g. structure: Section 5 + Section 6 + Section 7; quality: Section 1 + Section 10; decisions: Section 4 + Section 9 + Section 11)
   - The full document

2. **Where are the files?** — What is the path to the arc42 documentation? (e.g. `docs/arc42/`, `architecture/`, or a single file.) Do not ask the user to paste content — read the files directly.

3. **Review focus** — Should the review prioritize all dimensions equally, or focus on one?
   - **Completeness** — Is mandatory content present for the stated detail level?
   - **Consistency** — Do cross-section references, names, and IDs match?
   - **Quality** — Are quality goals, metrics, and risk assessments concrete and testable?
   - **All of the above** (default)

---

## Step 2 — Perform the Review

Read the specified files. For each section reviewed, determine the stated detail level (LEAN / ESSENTIAL / THOROUGH) and apply only the checks appropriate for that level. Apply universal checks to every section.

### Universal Checks (Every Section)

- [ ] Mandatory content for this section is present at the stated detail level → if missing, identify exactly what is absent
- [ ] No vague claims without measurable criteria — especially for quality statements ("fast", "reliable", "secure" without numbers) → flag every instance
- [ ] Writing is clear and free of unexplained jargon → flag terms that belong in Section 12 but are not defined there
- [ ] Tables have headers; diagrams are referenced by file path, not inlined → if a diagram is inlined, note the file it should be extracted to

---

### Section-Specific Checks

Apply only for sections included in the review scope. Items marked `(toolkit)` check compliance with toolkit conventions — not official arc42 requirements. All other items reflect official arc42 guidance.

**Section 1 (Introduction and Goals):**
- [ ] Section 1.2 quality goals are present (toolkit recommendation: document quality goals before any other section) → if absent, flag as high priority
- [ ] 3–5 quality goals maximum (toolkit) → if more, ask the user which to promote and which to demote to Section 10
- [ ] Every quality goal has a Q42 property tag (`#reliable`, `#efficient`, `#secure`, `#usable`, `#safe`, `#flexible`, `#suitable`, `#operable`) (toolkit — per quality.arc42.org) → if missing, suggest the correct tag
- [ ] Every quality goal has a concrete metric or measurable scenario — not "the system should be fast" → flag vague statements
- [ ] All relevant stakeholders are listed with their expectations → if a stakeholder group appears in other sections but not here, flag the gap
- [ ] Requirements overview is under 1 page (ESSENTIAL/THOROUGH) (toolkit) → if longer, suggest splitting into summary vs. reference

**Section 2 (Constraints):**
- [ ] Each constraint has a reason explaining why it is non-negotiable → if missing, ask who mandated it and why
- [ ] Apply the constraint test: "Does overriding this require a business, legal, or organisational change?" → if the answer is "no, a developer could change it", it is a design decision and belongs in Section 9, not here
- [ ] Constraints do not overlap with quality goals — a constraint is a hard boundary, not a target → flag any that read as aspirational rather than mandatory
- [ ] Technical, organisational, and regulatory categories are covered where relevant (ESSENTIAL/THOROUGH) → flag absent categories only if they are clearly applicable

**Section 3 (Context and Scope):**
- [ ] The system boundary is clear — no internal components appear in the context diagram → flag any building block from Section 5 that appears inside the system boundary in the context diagram
- [ ] Business context does not contain technical details (protocols, data formats, port numbers) → those belong in the technical context
- [ ] All external actors and systems are shown → check against Section 5 Level-1 interfaces
- [ ] C4 PlantUML context diagram exists as a separate `.puml` file in `docs/diagrams/` (ESSENTIAL/THOROUGH) → if inlined or absent, flag as toolkit convention deviation (C4 PlantUML is the toolkit default; official arc42 is format-agnostic)

**Section 4 (Solution Strategy):**
- [ ] Every quality goal from Section 1.2 has a corresponding approach described here → list any unaddressed goals
- [ ] Each technology decision has a clear rationale — not just "we use X" but "we use X because Y" → flag decisions without rationale
- [ ] Significant decisions are flagged for Section 9 ADRs → if a major decision is described here without a corresponding ADR, flag it
- [ ] Decomposition strategy is stated and consistent with Section 5 component structure → flag mismatches

**Section 5 (Building Block View):**
- [ ] Level-1 diagram and component table are present (toolkit convention: Level-1 is the minimum expected output at all detail levels) → if absent, flag as Critical
- [ ] All external interfaces from Section 3 appear at Level-1 with matching toolkit IF-xx IDs → if any are missing or renamed, flag as toolkit convention deviation
- [ ] No circular dependencies between components → if any are present, flag them as Critical
- [ ] No building block maps to an individual file, class, or method — only modules, services, libraries, or subsystems → if too granular, flag it
- [ ] Source code locations are specified for each component (ESSENTIAL/THOROUGH) (toolkit) → if missing, ask the user to provide them
- [ ] C4 PlantUML diagrams exist as separate `.puml` files in `docs/diagrams/` → if inlined or absent, flag as toolkit convention deviation

**Section 6 (Runtime View):**
- [ ] 3–5 scenarios (toolkit) — not fewer (too thin), not more (too exhaustive) → flag if outside this range
- [ ] At least one happy-path scenario, one error/recovery scenario, and one scenario demonstrating a quality goal → flag any missing type
- [ ] All components referenced exist in Section 5 — exact name match → list any name mismatches
- [ ] All external actors referenced exist in Section 3 → list any that don't
- [ ] Error handling documented for scenarios on the critical path → flag missing error handling
- [ ] C4 Dynamic PlantUML diagrams in `docs/diagrams/runtime-[name].puml` (ESSENTIAL/THOROUGH) → if absent or inlined, flag as toolkit convention deviation

**Section 7 (Deployment View):**
- [ ] Every Section 5 building block appears in the software-to-infrastructure mapping → list any missing
- [ ] Production environment is fully described before other environments → flag if non-production is more detailed than production
- [ ] TLS termination point is identified → if absent, flag as a security gap
- [ ] At least one `#reliable`, `#efficient`, or `#operable` goal from Section 1.2 has a corresponding infrastructure mechanism → if none are mapped, flag it
- [ ] No infrastructure choice violates a constraint from Section 2 → flag any conflict
- [ ] C4 Deployment PlantUML diagrams in `docs/diagrams/deployment-[env].puml` (ESSENTIAL/THOROUGH) → if absent or inlined, flag as toolkit convention deviation

**Section 8 (Crosscutting Concepts):**
- [ ] Every documented concept applies to 2 or more building blocks — apply the crosscutting test → flag any concept that only affects one component
- [ ] No subsection contains generic industry advice without system-specific content → flag anything that reads like a textbook
- [ ] Security is present unless the system has no users and no sensitive data → if absent without justification, flag as Critical
- [ ] Patterns described here are consistent with Section 4 solution strategy → flag any contradiction
- [ ] Domain model (if present) uses standard PlantUML class diagram notation, stored as `docs/diagrams/domain-model.puml` (toolkit) → C4 is not appropriate for domain models

**Section 9 (Architecture Decisions):**
- [ ] Every significant decision flagged in Section 4 has a corresponding ADR → list any missing
- [ ] Every ADR covers all five Nygard base fields: Title, Context, Decision, Status, Consequences (positive AND negative) → flag entries missing any of these or listing only benefits
- [ ] Alternatives table is present when alternatives were actually evaluated (toolkit extension — do not flag its absence if the decision was forced or had no real alternatives); Implications block present at ESSENTIAL/THOROUGH → flag if absent at those levels
- [ ] Lifecycle rule: no ADR has been edited to change a past decision — superseded decisions must be marked "Superseded by ADR-XXX" with a new ADR created → flag any apparent overwrites
- [ ] Status (Nygard) and Date (toolkit addition) are set on every ADR → flag any missing
- [ ] "Risks created" field in the Implications block is populated and each risk appears in Section 11 (toolkit convention: use RISK-xx IDs if Section 11 follows toolkit format) → flag any gap

**Section 10 (Quality Requirements):**
- [ ] Every Section 1.2 quality goal has at least one scenario → list any unaddressed goals
- [ ] Every scenario has a quantified, testable success measure — no vague criteria → flag every instance of "fast", "reliable", "secure" without a number
- [ ] Every scenario has an environment context (normal / peak / degraded) → flag any missing
- [ ] QS IDs are sequential and stable — no gaps unless a scenario is marked "Retired" → flag renumbering
- [ ] Quality requirements overview (if present) is in sync with the scenario tables — every QS ID appears in both → flag mismatches; note: overview format (table, quality tree, or prose) is the author's choice per docs.arc42.org/section-10

**Section 11 (Risks and Technical Debt):**
- [ ] Every "Risks created" entry from Section 9 ADRs appears as a toolkit RISK-xx entry → if any are missing, flag as toolkit convention deviation
- [ ] Every aspirational scenario from Section 10 that is not yet met has a corresponding risk entry (toolkit) → list any missing
- [ ] Risks are ordered Critical → High → Medium → Low (toolkit) → flag if out of order
- [ ] Priority is consistent with probability × impact — flag any mismatch
- [ ] No risk is marked "Mitigated" without a concrete mitigation strategy → flag vague or empty mitigations
- [ ] Toolkit RISK-xx and DEBT-xx IDs are stable — no gaps unless an item is marked "Closed" → flag renumbering as toolkit convention deviation
- [ ] Technical debt items reference a specific component from Section 5 (toolkit) → flag any that don't

**Section 12 (Glossary):**
- [ ] All building block names from Section 5 that are not plain English have a glossary entry → list any missing
- [ ] All acronyms appearing in Sections 1–11 are expanded → scan for all-caps words and verify
- [ ] No definition is a generic dictionary entry — every definition is system-specific → flag any that are not
- [ ] Preferred terms in the glossary match the terms used in Section 5 exactly → flag any mismatch
- [ ] No circular definitions (a term defined using itself) → flag if found

---

### Cross-Section Consistency Checks

Apply when multiple sections are in scope.

| Check | Sections | What to Verify |
|-------|----------|----------------|
| Interface IDs (toolkit) | Section 3 ↔ Section 5 | Toolkit IF-xx IDs in Section 3 match IF-xx IDs used at Section 5 Level-1 exactly |
| Component names | Section 5 ↔ Section 6 | Every component name in runtime scenarios matches Section 5 name exactly |
| Component names | Section 5 ↔ Section 7 | Every component in Section 5 appears in Section 7 deployment mapping |
| Component names | Section 5 ↔ Section 8 | Building blocks referenced in crosscutting concepts match Section 5 names |
| Quality goals | Section 1.2 ↔ Section 4 | Every quality goal has a solution approach in Section 4 |
| Quality goals | Section 1.2 ↔ Section 7 | `#reliable`, `#efficient`, `#operable` goals have infrastructure mechanisms in Section 7 |
| Quality goals | Section 1.2 ↔ Section 10 | Every quality goal has at least one scenario in Section 10 |
| Constraints | Section 2 ↔ Section 5 | No component structure violates a Section 2 constraint |
| Constraints | Section 2 ↔ Section 7 | No infrastructure choice violates a Section 2 constraint |
| Decisions | Section 4 ↔ Section 9 | Every significant decision in Section 4 has a full ADR in Section 9 |
| Risks (toolkit) | Section 9 ↔ Section 11 | Every "Risks created" field in Section 9 ADRs has a toolkit RISK-xx entry in Section 11 |
| Risks (toolkit) | Section 10 ↔ Section 11 | Toolkit aspirational scenarios in Section 10 have corresponding RISK-xx entries in Section 11 |
| Crosscutting | Section 8 ↔ Section 4 | Crosscutting patterns are consistent with Section 4 solution strategy |
| Terminology | Section 12 ↔ all | Preferred terms in Section 12 are used consistently across all sections |

---

## Step 3 — Report Findings

Present the review results in this format:

```markdown
## Review Report — [Scope: Section N / Sections N+M / Full Document]

**Detail level reviewed:** LEAN / ESSENTIAL / THOROUGH
**Review focus:** Completeness / Consistency / Quality / All

---

### Summary

[2–3 sentences: Overall quality assessment. How many Critical, Minor, and Suggestion items were found? What is the dominant issue type?]

---

### Strengths

- [What is done well — be specific, not generic]
- [What is accurate, complete, or particularly clear]

---

### Issues Found

**Critical (Must Fix before using this documentation):**
- [ ] [Section N] [Issue title]: [Description] → [Specific fix] → Run `/arc42-section-N` to address this

**Minor (Should Fix — impacts clarity or consistency):**
- [ ] [Section N] [Issue title]: [Description] → [Specific fix]

**Suggestions (Nice to Have):**
- [Section N] [Suggestion — no action required]

---

### Cross-Section Consistency

| Check | Status | Detail |
|-------|--------|--------|
| Section 3 interfaces ↔ Section 5 Level-1 | PASS / FAIL | [Detail if FAIL] |
| Section 1.2 goals ↔ Section 4 approaches | PASS / FAIL | [Detail if FAIL] |
| [Other checks performed] | PASS / FAIL | [Detail if FAIL] |

---

### Verdict

- [ ] **APPROVED** — Documentation is ready to use at the stated detail level
- [ ] **APPROVED WITH MINOR CHANGES** — Usable, but minor issues should be addressed soon
- [ ] **NEEDS REVISION** — One or more Critical issues must be fixed before use
```

---

## Step 4 — Offer to Fix

After presenting the report:

1. For each **Critical** issue: offer to fix it immediately — either by running the relevant section skill (`/arc42-section-N`) or by directly editing the content if the fix is small and well-defined.
2. For **Minor** issues: ask "Which of these would you like to address now?" and handle them one by one.
3. After any fixes are applied, re-run the affected checks and update the verdict.

Ask: **"Shall I start with the Critical issues?"**

---

*Based on [arc42.org](https://arc42.org), [docs.arc42.org](https://docs.arc42.org), [quality.arc42.org](https://quality.arc42.org)*
