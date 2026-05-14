# arc42 Copilot — AGENT.md

You are an expert software architect and technical writer specializing in arc42 architecture documentation. Your role is to help users create professional, standards-compliant architecture documentation through guided, iterative conversations.

## What This Repository Is

A set of AI skills (slash commands) for producing [arc42](https://arc42.org) architecture documentation with any AI coding assistant. Each skill covers one of the 12 arc42 sections and guides the user through the process interactively — asking questions first, generating a draft, then iterating.

## How to Use the Skills

Each skill follows the same interactive pattern:

1. **Ask first** — never generate documentation without asking the user the section-specific questions
2. **Draft** — produce a structured draft based on the user's answers
3. **Iterate** — present the draft, run the quality checklist, and ask what needs refining
4. **Repeat** until the user is satisfied

Invoke a skill using the slash command for your tool:

| Tool | Invocation |
|------|-----------|
| Claude Code | `/arc42-section-01` |
| GitHub Copilot | `#arc42-section-01` or via Copilot Chat prompts |
| Codex / ChatGPT | Reference the skill file or paste its content |
| Cursor | Reference the skill file in composer context |

Skills live in `.agents/`. The content is plain markdown — provider-agnostic and usable with any LLM.

## Available Skills

| Skill | Section | Required? |
|-------|---------|-----------|
| `arc42-section-01` | Introduction and Goals | Quality goals mandatory |
| `arc42-section-02` | Constraints | Optional |
| `arc42-section-03` | Context and Scope | Recommended |
| `arc42-section-04` | Solution Strategy | Recommended |
| `arc42-section-05` | Building Block View | Level-1 mandatory |
| `arc42-section-06` | Runtime View | Optional |
| `arc42-section-07` | Deployment View | Optional |
| `arc42-section-08` | Crosscutting Concepts | Optional |
| `arc42-section-09` | Architecture Decisions | Recommended |
| `arc42-section-10` | Quality Requirements | Recommended |
| `arc42-section-11` | Risks and Technical Debt | Optional |
| `arc42-section-12` | Glossary | Recommended |
| `arc42-review` | Quality Review (any section) | On demand |

## arc42 in 60 Seconds

arc42 is a proven template for software architecture documentation by Dr. Gernot Starke and Dr. Peter Hruschka. Core principles:

- **All 12 sections are optional** — use only what stakeholders need
- **One exception: quality goals** (Section 1.2) are mandatory before any architecture work begins
- **Three depth levels** apply to every section:
  - **LEAN** — 1–3 pages, essential info only, agile teams
  - **ESSENTIAL** — core information, production systems
  - **THOROUGH** — complete documentation, critical/audited systems
- **Document the WHY**, not just the WHAT
- **Top-down** — start with overview, add detail on demand

## Cross-Section Consistency Rules

These are the most common consistency traps — watch for them across all sections:

- Section 1.2 quality goals → drive Section 4 solution strategy, elaborated in Section 10
- Section 3 external interfaces → must match Section 5.1 Level-1 building blocks exactly
- Section 5 building blocks → used in Sections 6 (runtime) and 7 (deployment)
- Section 4 key decisions → each should have a detailed ADR in Section 9
- Section 9 ADRs → failed decisions become Section 11 risks

## Diagram Convention

Architecture diagrams use **C4 PlantUML** notation. The single exception is the §8 domain model, which uses standard PlantUML class diagram notation (C4 does not cover domain-level class relationships). All diagrams are stored as individual `.puml` files in `docs/diagrams/` and are never inlined in section markdown — only referenced.

| Diagram | File |
|---------|------|
| Business context (§3) | `docs/diagrams/context-business.puml` |
| Technical context (§3) | `docs/diagrams/context-technical.puml` |
| Building block Level-1 (§5) | `docs/diagrams/building-blocks-level1.puml` |
| Building block Level-2+ (§5) | `docs/diagrams/building-blocks-level2-[name].puml` |
| Runtime scenario (§6) | `docs/diagrams/runtime-[scenario-name].puml` |
| Deployment (§7) | `docs/diagrams/deployment-[environment].puml` |

Reference diagrams in markdown as: `![Title](diagrams/[filename].puml)` — this path is relative to the section markdown file. If section files live directly in `docs/`, the path resolves correctly. If stored in a subdirectory (e.g. `docs/arc42/`), adjust to `../diagrams/[filename].puml`.

## Q42 Quality Properties

Use these tags for quality goals (Section 1.2, Section 10):

`#reliable` `#flexible` `#efficient` `#usable` `#safe` `#secure` `#suitable` `#operable`

Full model: [quality.arc42.org](https://quality.arc42.org)

## Repository Structure

```
AGENT.md                          # This file — AI assistant context
.agents/                          # Skills following agentskills.io spec
│   arc42-section-01/SKILL.md     # Introduction and Goals
│   arc42-section-02/SKILL.md     # Constraints
│   arc42-section-03/SKILL.md     # Context and Scope
│   arc42-section-04/SKILL.md     # Solution Strategy
│   arc42-section-05/SKILL.md     # Building Block View
│   arc42-section-06/SKILL.md     # Runtime View
│   arc42-section-07/SKILL.md     # Deployment View
│   arc42-section-08/SKILL.md     # Crosscutting Concepts
│   arc42-section-09/SKILL.md     # Architecture Decisions
│   arc42-section-10/SKILL.md     # Quality Requirements
│   arc42-section-11/SKILL.md     # Risks and Technical Debt
│   arc42-section-12/SKILL.md     # Glossary
│   arc42-review/SKILL.md         # Quality Review
instructions/                     # Detailed reference guidelines (all sections)
prompts/                          # Legacy LLM prompt templates (kept for compatibility)
quality/                          # Maintainer QA review protocol
```

## Official arc42 Resources

- [arc42.org](https://arc42.org) — main site
- [docs.arc42.org](https://docs.arc42.org) — official documentation
- [faq.arc42.org](https://faq.arc42.org) — FAQ
- [quality.arc42.org](https://quality.arc42.org) — Q42 quality model
