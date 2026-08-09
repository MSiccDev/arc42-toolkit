# arc42 Toolkit

[![arc42](https://img.shields.io/badge/arc42-based-brightgreen)](https://arc42.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> Provider-agnostic arc42 documentation skills for AI coding assistants — Claude Code, GitHub Copilot, Cursor, Codex, and any LLM tool that reads markdown.

Create professional software architecture documentation through guided, interactive AI conversations. Each of the 12 arc42 sections is covered by a dedicated skill that asks the right questions first, generates a structured draft, then iterates until you are satisfied.

---

## Features

- **14 interactive skills** — one per arc42 section, plus quality review and consistency linting
- **Provider-agnostic** — works with Claude Code, GitHub Copilot, Cursor, Codex, and any LLM tool
- **Ask-first approach** — every skill gathers your project details before generating anything
- **Three depth levels** — LEAN, ESSENTIAL, or THOROUGH, chosen per section based on your needs
- **C4 PlantUML diagrams** — toolkit default notation for architecture diagrams, stored as separate `.puml` files, never inlined (official arc42 is format-agnostic — any notation works)
- **Q42 quality model** — 492 quality attributes across 8 properties integrated into relevant skills
- **Cross-section consistency** — skills check related sections and flag contradictions
- **Automated consistency linting** — catch IF-xx, QS-xx, ADR, and RISK-xx mismatches before they accumulate
- **Standards-based** — grounded in arc42.org, docs.arc42.org, and quality.arc42.org

---

## What is arc42?

arc42 is the proven, open-source template for software architecture documentation created by Dr. Gernot Starke and Dr. Peter Hruschka. Used in thousands of projects worldwide, it provides a pragmatic, tool-agnostic approach.

**Core philosophy:**
- Document economically but continuously
- "Painless documentation" — only what stakeholders truly need
- All sections are optional — use what fits your project
- Suitable for agile and traditional environments

**Toolkit recommendation:** Start with Section 1.2 (Quality Goals) — it anchors all architectural decisions that follow.

---

## Quick Start

### 1. Install the toolkit

**Claude Code**

```bash
claude plugin install MSiccDev/arc42-toolkit
```

Skills are available as slash commands immediately.

**GitHub Copilot CLI**

```bash
copilot plugin install arc42-toolkit
```

If the arc42-toolkit marketplace is not yet registered, add it first:

```bash
copilot plugin marketplace add MSiccDev/arc42-toolkit
copilot plugin install arc42-toolkit
```

**OpenAI Codex**

Register the repository as a marketplace source once, then install the plugin from the Codex app:

```bash
codex plugin marketplace add MSiccDev/arc42-toolkit --ref main
```

After registration, restart Codex, open **Plugins**, choose the **arc42 Toolkit** marketplace, and install `arc42-toolkit`.

If you open this repository directly in Codex, the repo-local `.agents/skills/` symlinks also expose the skills without plugin installation.

**Cursor, Copilot Chat, and other tools**

Clone or copy into your project:

```bash
git clone https://github.com/MSiccDev/arc42-toolkit.git
```

Or copy `AGENTS.md`, the `skills/` directory, and the `.agents/` symlink into your existing project.

> **Windows / ZIP installs:** If symlinks are unavailable, create a directory junction instead:
> `mklink /J .agents skills` (Windows CMD) — or simply copy the `skills/` directory to `.agents/`.

### 2. Start with Section 1

Invoke the skill for your AI tool:

| Tool | Command |
|------|----------|
| Claude Code | `/arc42-section-01` |
| GitHub Copilot Chat | `#arc42-section-01` |
| Cursor | Reference `skills/arc42-section-01/SKILL.md` in context |
| Codex | Use `$arc42-section-01` after installing the plugin, or open the repo directly |

### 3. Answer the questions

The skill asks about your project — requirements, stakeholders, quality goals. No generation happens until you have answered.

### 4. Review and iterate

The skill produces a draft, runs a built-in quality checklist, and asks what you want to refine. Repeat until satisfied.

### 5. Continue section by section

Use the same pattern for each section you need. The `/arc42-review` skill validates any section or the full document at any time.

---

## Repository Structure

```
arc42-toolkit/
│
├── AGENTS.md                           # Project context — read by all AI assistants
├── README.md                          # This file
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guidelines
│
├── .codex-plugin/
│   └── plugin.json                    # Codex plugin manifest
├── .agents/
│   ├── plugins/
│   │   └── marketplace.json           # Repo-scoped Codex marketplace
│   └── skills/                        # Codex skill-discovery symlinks
│
├── skills/                            # Canonical skill source (agentskills.io spec)
│   ├── arc42-section-01/SKILL.md      # Introduction and Goals
│   ├── arc42-section-02/SKILL.md      # Constraints
│   ├── arc42-section-03/SKILL.md      # Context and Scope
│   ├── arc42-section-04/SKILL.md      # Solution Strategy
│   ├── arc42-section-05/SKILL.md      # Building Block View
│   ├── arc42-section-06/SKILL.md      # Runtime View
│   ├── arc42-section-07/SKILL.md      # Deployment View
│   ├── arc42-section-08/SKILL.md      # Crosscutting Concepts
│   ├── arc42-section-09/SKILL.md      # Architecture Decisions
│   ├── arc42-section-10/SKILL.md      # Quality Requirements
│   ├── arc42-section-11/SKILL.md      # Risks and Technical Debt
│   ├── arc42-section-12/SKILL.md      # Glossary
│   ├── arc42-review/SKILL.md          # Quality review (any section or full doc)
│   └── arc42-lint/SKILL.md            # Cross-section consistency linter
│
├── scripts/
│   ├── arc42-lint.py                  # Standalone linter (stdlib only, CI-ready)
│   └── languages/
│       ├── en.json                    # English (default)
│       ├── de.json                    # Deutsch
│       ├── fr.json                    # Français
│       ├── it.json                    # Italiano
│       ├── es.json                    # Español
│       └── pt.json                    # Português
│
├── templates/
│   └── arc42-lint.yml                 # GitHub Actions workflow template (copy to your project)
│
```

Generated documentation goes in your project's `docs/` directory. Architecture diagrams are stored as `.puml` files in `docs/diagrams/`.

---

## The 12 arc42 Sections

| Section | Name | Skill | Toolkit guidance |
|---------|------|-------|----------|
| **1** | Introduction and Goals | `/arc42-section-01` | **Recommended starting point** (Section 1.2 quality goals) |
| **2** | Constraints | `/arc42-section-02` | Optional |
| **3** | Context and Scope | `/arc42-section-03` | Recommended |
| **4** | Solution Strategy | `/arc42-section-04` | Recommended |
| **5** | Building Block View | `/arc42-section-05` | **Core section** (Level-1 view essential) |
| **6** | Runtime View | `/arc42-section-06` | Optional |
| **7** | Deployment View | `/arc42-section-07` | Optional |
| **8** | Crosscutting Concepts | `/arc42-section-08` | Optional |
| **9** | Architecture Decisions | `/arc42-section-09` | Recommended |
| **10** | Quality Requirements | `/arc42-section-10` | Recommended |
| **11** | Risks and Technical Debt | `/arc42-section-11` | Optional |
| **12** | Glossary | `/arc42-section-12` | Recommended |

Use `/arc42-review` at any point to validate one section, a related set, or the full document.
Use `/arc42-lint` to check cross-section ID consistency automatically.

---

## Three Depth Levels

Every skill supports three depth levels. Choose based on your project's needs — you can use different levels for different sections. These levels are toolkit conventions — they are not part of the official arc42 template.

### LEAN (Agile / Minimal)
**Best for:** Agile teams, time-constrained projects, evolving systems

- 1–3 pages per section maximum
- Essential information only — "dare to leave gaps"
- Minimum viable documentation: Section 1.2, Section 3, Section 5 Level-1, Section 9, Section 12

### ESSENTIAL (Core Information)
**Best for:** Most projects — the balanced default

- Non-negotiable minimum for production systems
- Critical architectural information enabling team understanding
- Includes LEAN content plus requirements overview, stakeholders, black-box descriptions

### THOROUGH (Comprehensive)
**Best for:** Critical systems, regulated environments, audit requirements, large teams

- Complete documentation across all sections
- Detailed scenarios, multiple diagram levels, extensive validation
- Full Q42 quality scenario coverage

---

## How to Use with AI Tools

### Claude Code

```
/arc42-section-01
```

Skills are automatically available as slash commands when `AGENTS.md` and the `skills/` directory (with `.agents/` symlink) are in your project.

### GitHub Copilot

```
#arc42-section-01
```

Use in Copilot Chat. Copilot reads `AGENTS.md` for project context automatically.

### Cursor

Open `skills/arc42-section-01/SKILL.md` in the Composer context, or reference it with `@SKILL.md` in chat.

### Codex

Install the plugin from the Codex marketplace flow above, then invoke skills directly:

```text
$arc42-section-01
$arc42-review
$arc42-lint
```

If you are working inside a clone of this repository, Codex also discovers the skills through `.agents/skills/` automatically.

### ChatGPT / Other LLMs

Paste the content of the relevant `SKILL.md` file as a system prompt or context message. All skills are plain markdown and remain portable outside plugin runtimes.

---

## Key Benefits

### For Architects
- Save documentation time through guided, structured generation
- Consistent, high-quality output across all sections
- Standards-compliant documentation without needing to memorise arc42 rules
- Focus on architectural decisions, not formatting

### For Teams
- Shared vocabulary and structure across the organisation
- Easy onboarding — new members understand the system faster
- Reduced documentation debt through iterative, incremental documentation
- Better stakeholder communication with consistent artifact format

### For Organizations
- Standardized architecture documentation across projects
- Knowledge preservation — decisions and rationale are captured, not just the outcome
- Improved audit readiness
- Scalable process that works from startup to enterprise

---

## Q42 Quality Model Integration

The skills integrate the **Q42 quality model** — a comprehensive framework with 492 quality attributes in 8 properties. Quality goals from Section 1 are traced through constraints, solution strategy, deployment, crosscutting concepts, and quality scenarios.

| Property | Attributes | Focus |
|----------|-----------|-------|
| **#reliable** | 97 | Availability, Fault Tolerance, Accuracy |
| **#flexible** | 50 | Adaptability, Maintainability, Extensibility |
| **#efficient** | 71 | Response Time, Throughput, Resource Usage |
| **#usable** | 103 | Learnability, Operability, Accessibility |
| **#safe** | 28 | Risk-free, Fail-safe, Hazard Warnings |
| **#secure** | 36 | Confidentiality, Integrity, Authentication |
| **#suitable** | 52 | Functional Completeness, Testability |
| **#operable** | 55 | Installability, Monitorability, Deployability |

**Learn more:** [quality.arc42.org](https://quality.arc42.org)

---

## Consistency Linting

The arc42 toolkit ships a standalone linter that validates cross-section ID consistency in your generated documentation. It catches mismatches that accumulate silently over time — interface IDs renamed in one section but not another, ADR risks never registered, quality scenarios with no matching goal.

### What it checks

| Rule | Sections | Validates |
|------|----------|-----------|
| 1 | Section 3 ↔ Section 5 | `IF-xx` interface IDs match between the context diagram and Level-1 building blocks |
| 2 | Section 5 ↔ Section 7 | Every building block name appears in the deployment mapping |
| 3 | Section 1 ↔ Section 10 | Every Q42 tag used in quality scenarios is present in Section 1.2 quality goals |
| 4 | Section 9 ↔ Section 11 | Every `RISK-xx` in an ADR's "Risks created" field has a Section 11 risk matrix entry |
| 5 | Section 10 ↔ Section 11 | Every aspirational (not yet met) scenario from Section 10.3 is referenced in Section 11 |

### Run locally

```bash
# Check docs/ in English (default)
python scripts/arc42-lint.py

# Check docs written in another language
python scripts/arc42-lint.py --lang de
python scripts/arc42-lint.py --lang fr
python scripts/arc42-lint.py --lang it
python scripts/arc42-lint.py --lang es
python scripts/arc42-lint.py --lang pt

# Check a custom path
python scripts/arc42-lint.py path/to/your/docs --lang de

# Treat warnings as errors (useful in CI)
python scripts/arc42-lint.py --strict
```

Exit code `0` = clean, `1` = issues found.

### GitHub Actions

Copy `templates/arc42-lint.yml` from this repo to `.github/workflows/arc42-lint.yml` in your project. It runs automatically when files under `docs/**` change.

**To use in your own project:** copy the entire `scripts/` directory (script + languages) and `templates/arc42-lint.yml` (to `.github/workflows/arc42-lint.yml`) into your repo. No Python dependencies to install — stdlib only.

### Adding a language

Copy any file from `scripts/languages/` as a starting point, name it `scripts/languages/{code}.json`, and translate the keyword patterns. All values are case-insensitive regular expressions — plain text works too. Multiple alternatives are supported per pattern. Once merged, the new language is available via `--lang {code}`.

### AI-assisted linting

Use `/arc42-lint` to run the linter interactively through your AI tool. The skill runs the script when available, or applies the five rules manually when not. It also offers to fix any issues it finds.

---

## AI Evaluation Tests

The toolkit includes a small suite of LLM-as-judge evaluations under `tests/arc42Toolkit.Evaluations/`, built on the [Microsoft.Extensions.AI.Evaluation](https://learn.microsoft.com/dotnet/ai/evaluation-libraries) libraries. The `AdrCompletenessEvaluator` scores ADRs against a fixed rubric (context, decision, consequences, alternatives considered), guarding against regressions in how well AI-generated documentation follows the arc42 structural contract.

### Running the tests

The judge is a locally hosted [LM Studio](https://lmstudio.ai/) model (`microsoft/phi-4-reasoning-plus`) at `http://localhost:1234/v1` — start it before running any of these tests.

```bash
dotnet test tests/arc42Toolkit.Evaluations
```

This runs the full golden dataset (`TestData/golden-dataset.json` and `TestData/adrs/`) against the judge, which can take a while since every fixture round-trips through the local reasoning model.

For a quick, single-file demo run — evaluating the toolkit's own `docs/adrs/ADR-0001-extract-ai-evaluation-prototype-into-a-distributable-net-cli-tool.md` against the same rubric, without touching the golden dataset — use:

```bash
dotnet test tests/arc42Toolkit.Evaluations --filter "Category=Demo"
```

### Generating the report

The `aieval` CLI ships as part of the `Microsoft.Extensions.AI.Evaluation.Console` .NET tool, registered in this repo as a local tool via `dotnet-tools.json`. Restore it once (also runs automatically on `dotnet restore`):

```bash
dotnet tool restore
```

Then, after running the tests at least once, generate (and optionally open) the report:

```bash
dotnet tool run aieval report \
  --path tests/arc42Toolkit.Evaluations/eval-results \
  --output tests/arc42Toolkit.Evaluations/eval-results/report.html \
  --open
```

- `--path` points at the result store populated by the test run.
- `--output` is where the HTML report is written.
- `--open` launches it in your default browser; omit it to just generate the file.

Re-run the tests and the `aieval report` command any time `AGENTS.md` changes to confirm it still satisfies the structural contract.

---

## Contributing

Contributions are welcome. Here is how you can help:

- **Report issues** — found a problem with a skill? Open a bug report
- **Improve skills** — better questions, clearer checklists, sharper output templates
- **Add examples** — submit real-world arc42 documentation produced with this toolkit
- **Domain-specific variants** — skills tuned for microservices, embedded systems, data platforms
- **Share feedback** — used it on a real project? Tell us what worked and what did not

**[Read our Contributing Guide](CONTRIBUTING.md)** for detailed guidelines.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

**Note:** arc42® is a registered trademark of Dr. Gernot Starke and Dr. Peter Hruschka. This project is based on the freely available arc42 template and is not officially affiliated with arc42.org.

---

## How This Project Was Created

This repository is a demonstration of AI-assisted technical content development. The arc42 skills were created through iterative collaboration between a human architect (Marco) and Claude (Anthropic's AI assistant), grounded in official arc42 sources throughout.

### Process

1. **Research** — Extensive review of arc42.org, docs.arc42.org, quality.arc42.org, faq.arc42.org
2. **Skill development** — Section-by-section creation of interactive skills following the agentskills.io specification
3. **Quality assurance** — Systematic review against arc42 standards for accuracy and completeness
4. **Iterative refinement** — Multiple review and improvement cycles, including Copilot code review
5. **Provider-agnostic refactor** — Migrated from Copilot-specific prompts to the AGENTS.md + skills standard

### Principles

- **Authenticity first** — all content based on official arc42 sources, nothing invented
- **Standards compliance** — validated against docs.arc42.org and quality.arc42.org
- **Human oversight** — human architect provided direction, requirements, and validation
- **AI efficiency** — AI assistant handled research, synthesis, and structured content creation

### Transparency

This repository was researched and structured by AI from authoritative arc42 sources, directed by human expertise in software architecture, validated through systematic quality reviews, and is maintained with ongoing human oversight.

---

## Acknowledgments

- **arc42 Template** — Created by Dr. Gernot Starke and Dr. Peter Hruschka
- **Official Sources:**
  - [arc42.org](https://arc42.org) — Main website
  - [docs.arc42.org](https://docs.arc42.org) — Official documentation
  - [quality.arc42.org](https://quality.arc42.org) — Q42 quality model
  - [faq.arc42.org](https://faq.arc42.org) — Frequently asked questions
- **Claude (Anthropic)** — AI assistant used in creating and refining this repository's content
- **Contributors** — See [CONTRIBUTORS.md](CONTRIBUTORS.md) for everyone who has helped

---

## Related Resources

- [Architecture Decision Records (ADR)](https://adr.github.io)
- [C4 Model](https://c4model.com) — Recommended diagramming approach (used throughout this toolkit)
- [agentskills.io](https://agentskills.io) — Skills specification this toolkit follows

---

## Support

- **Issues:** [GitHub Issues](https://github.com/MSiccDev/arc42-toolkit/issues)
- **Discussions:** [GitHub Discussions](https://github.com/MSiccDev/arc42-toolkit/discussions)
- **Questions:** Open a discussion or issue

---

## Project Status

- **v1.0** — Complete arc42 coverage, all 12 sections + review skill
- **Skills-based** — Migrated to provider-agnostic AGENTS.md + skills standard
- **Actively maintained** — Regular improvements based on real-world usage
- **Community driven** — Open to contributions

---

## Roadmap

### Phase 1: Skills Refactor — Done

Migrated from a Copilot-specific prompt library to a provider-agnostic skills toolkit following the agentskills.io standard. All 12 section skills and the review skill are complete with:

- Interactive question-first approach
- LEAN / ESSENTIAL / THOROUGH depth levels
- C4 PlantUML diagram generation
- Cross-section consistency checks
- Actionable quality checklists

### Phase 2: Real-World Validation (Next)
**Goal:** Battle-test the toolkit on an actual project

- **Use case: persona-template MCP Server** — a developer tool for managing persona preferences and software projects across AI providers
- Purpose: document the MCP (Model Context Protocol) server architecture using this toolkit
- Output: complete example arc42 documentation in the repository, serving as a reference implementation

### Phase 3: Community Growth (Future)
**Goal:** Expand examples and community contributions

- More real-world documentation examples
- Domain-specific skill variants (microservices, embedded systems, data platforms)
- Community-submitted examples and improvements
- Tutorial content and walkthroughs

### How You Can Help

- **Test it** — use the toolkit on your project and share feedback
- **Contribute examples** — submit your arc42 documentation as reference material
- **Report issues** — help identify and fix problems
- **Suggest improvements** — share ideas for better skills or output templates
- **Star the repo** — help others discover this resource

---

*Made for the software architecture community.*

*Bringing structured, AI-assisted efficiency to architecture documentation while maintaining standards compliance.*
