# Changelog

All notable changes to the arc42-toolkit skills are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). Each skill uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html): `MAJOR.MINOR.PATCH`.

- **MAJOR** — breaking change to the skill interface or output structure
- **MINOR** — new capability added in a backwards-compatible way
- **PATCH** — bug fix or wording improvement that does not change behavior

---

## [1.1.1] — 2026-07-07

### Fixed

Clarified the boundary between official arc42 guidance and toolkit conventions throughout all skills and documentation. No behavioral changes — wording and attribution corrections only.

| Artifact | Change |
|---|---|
| `README.md` | Badge changed from `arc42-compliant` to `arc42-based`; Section 1.2 reframed as toolkit recommendation; depth levels labelled as toolkit conventions; C4 PlantUML noted as toolkit default |
| `AGENTS.md` | Aligned with README framing: depth levels, C4 PlantUML, and Section 1.2 recommendation all labelled as toolkit conventions |
| `arc42-lint` → `1.0.1` | Renamed to "arc42 Toolkit Convention Linter"; all five rules reworded from "must" to "should/toolkit convention"; findings say "toolkit convention deviation" not "error" |
| `arc42-review` → `1.0.1` | Legend added to section-specific checks; all toolkit-specific items tagged `(toolkit)`; Nygard base fields now complete (Title, Context, Decision, Status, Consequences); quality overview source corrected to `docs.arc42.org/section-10` |
| `arc42-section-01` → `1.0.1` | Section `1.3` heading corrected to singular "Stakeholder" per official arc42 template |
| `arc42-section-05` → `1.0.1` | Section `5.1` heading changed to "Whitebox Overall System" per official arc42 template name |
| `arc42-section-09` → `1.0.1` | ADR format credited to Nygard; alternatives table and implications block labelled as toolkit additions; alternatives table now conditional on real alternatives existing; Date field labelled as toolkit addition |
| `arc42-section-10` → `1.0.1` | Quality Requirements Overview replaces forced quality tree; Q42 coaching references `quality.arc42.org`; QS-xx IDs and Section 10.3 labelled as toolkit conventions |
| `arc42-section-11` → `1.0.1` | RISK-xx and DEBT-xx ID conventions labelled at the top of the skill |

---

## [1.1.0] — 2026-05-16

### Added

| Artifact | Description |
|---|---|
| `scripts/arc42-lint.py` | Standalone Python linter (stdlib only) — validates cross-section ID consistency across 5 rules: IF-xx Section 3↔Section 5, building block names Section 5↔Section 7, Q42 tags Section 1↔Section 10, RISK-xx references Section 9↔Section 11, aspirational scenarios Section 10↔Section 11 |
| `scripts/languages/` | Language definition files (en, de, fr, it, es, pt) — section keywords and content patterns per language; contributors can add new files |
| `templates/arc42-lint.yml` | GitHub Actions workflow template — copy to `.github/workflows/` in your project to run the linter automatically on `docs/**` changes |
| `skills/arc42-lint/` | New skill — AI-assisted consistency linting via `/arc42-lint`; runs the script when available, applies rules manually when not, and offers to fix any issues found |

---

## [1.0.0] — 2026-05-16

Initial versioned release. All skills ship at `1.0.0`, aligned with the `arc42-toolkit` plugin version in `.claude-plugin/plugin.json`.

### Added

| Skill | Description |
|---|---|
| `arc42-section-01` | Interactive guide for Section 1 — Introduction and Goals |
| `arc42-section-02` | Interactive guide for Section 2 — Constraints |
| `arc42-section-03` | Interactive guide for Section 3 — Context and Scope |
| `arc42-section-04` | Interactive guide for Section 4 — Solution Strategy |
| `arc42-section-05` | Interactive guide for Section 5 — Building Block View |
| `arc42-section-06` | Interactive guide for Section 6 — Runtime View |
| `arc42-section-07` | Interactive guide for Section 7 — Deployment View |
| `arc42-section-08` | Interactive guide for Section 8 — Crosscutting Concepts |
| `arc42-section-09` | Interactive guide for Section 9 — Architecture Decisions (ADR) |
| `arc42-section-10` | Interactive guide for Section 10 — Quality Requirements |
| `arc42-section-11` | Interactive guide for Section 11 — Risks and Technical Debt |
| `arc42-section-12` | Interactive guide for Section 12 — Glossary |
| `arc42-review`     | Cross-section quality review with severity-linked fixes |
