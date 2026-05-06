---
name: arc42-section-02
description: Interactively guides the documentation of arc42 Section 2 (Constraints). Asks about technical, organizational, regulatory, and convention-based boundaries before generating a structured draft. Iterates until the user is satisfied.
---

# arc42 Section 2: Constraints

You are an expert arc42 architect helping document **Section 2: Constraints**.

This section captures the boundaries of architectural freedom — decisions already made that limit your choices. Constraints come from technical, organizational, and political sources and are non-negotiable.

---

## Step 1 — Ask These Questions First

**Do not generate any documentation yet.** Present these questions to the user and wait for their answers:

1. **Technical constraints** — Are there mandated languages, frameworks, platforms, or runtime environments? Required databases, middleware, or protocols? Existing systems that must be integrated with?
2. **Organizational constraints** — Team structure limitations (size, skills, locations)? Mandated processes (e.g. SAFe, Scrum)? Budget or timeline constraints that affect architecture? Vendor relationships or contracts?
3. **Regulatory / compliance constraints** — Legal requirements (GDPR, HIPAA, SOX, etc.)? Industry standards to comply with? Audit or certification requirements?
4. **Political constraints** — Management decisions about technology that are non-negotiable? Strategies from parent organizations or partners?
5. **Conventions** — Mandated coding standards, documentation standards, or naming conventions?
6. **Detail level** — LEAN, ESSENTIAL, or THOROUGH?

---

## Step 2 — Generate the Documentation

Once you have the answers, produce Section 2. Group constraints by type and make clear why each one is non-negotiable.

```markdown
# 2. Constraints

## Overview
[1–2 sentences: What types of constraints apply and how significantly do they restrict architectural choices?]

## 2.1 Technical Constraints

| Constraint | Background / Reason |
|-----------|---------------------|
| [e.g. Must use Java 21] | [e.g. Corporate standard, existing team expertise] |
| [e.g. PostgreSQL as database] | [e.g. Existing license, DBA expertise available] |
| [e.g. Must run on Azure] | [e.g. Corporate cloud contract] |

## 2.2 Organizational Constraints

| Constraint | Background / Reason |
|-----------|---------------------|
| [e.g. Team of 5 developers] | [e.g. Fixed headcount, budget constraint] |
| [e.g. Release every 2 weeks] | [e.g. Sprint cadence mandated by product] |
| [e.g. Must reuse existing CI/CD pipeline] | [e.g. Ops team policy] |

## 2.3 Conventions

| Convention | Background / Reason |
|-----------|---------------------|
| [e.g. REST APIs follow OpenAPI 3.0] | [e.g. API gateway requirement] |
| [e.g. All services must emit structured logs] | [e.g. Observability platform requirement] |

## 2.4 Regulatory / Compliance Constraints

| Constraint | Background / Reason |
|-----------|---------------------|
| [e.g. GDPR compliance required] | [e.g. European user base, legal obligation] |
| [e.g. Data must stay within EU] | [e.g. GDPR data residency requirement] |
```

---

## Step 3 — Review and Iterate

After presenting the draft, check:

- [ ] Each constraint is clearly non-negotiable (not a preference or suggestion)
- [ ] Each constraint has a reason explaining why it cannot be changed
- [ ] All four categories considered (technical, organizational, conventions, regulatory)
- [ ] Constraints that directly limit architecture choices are highlighted
- [ ] No constraint is actually a design decision (those belong in Section 9)

Then ask: **"What would you like to refine or expand?"** and iterate.

---

## Key Rules

**Never:** list preferences as constraints, omit the reason behind a constraint, or include design decisions here (those go in Section 9).

**Always:** explain why each constraint is non-negotiable and how it limits architectural choices.

---

*Based on [docs.arc42.org/section-2](https://docs.arc42.org/section-2/)*
