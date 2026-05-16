# Changelog

All notable changes to the arc42-toolkit skills are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). Each skill uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html): `MAJOR.MINOR.PATCH`.

- **MAJOR** — breaking change to the skill interface or output structure
- **MINOR** — new capability added in a backwards-compatible way
- **PATCH** — bug fix or wording improvement that does not change behavior

---

## [1.1.0] — 2026-05-16

### Added

| Artifact | Description |
|---|---|
| `scripts/arc42-lint.py` | Standalone Python linter (stdlib only) — validates cross-section ID consistency across 5 rules: IF-xx Section 3↔Section 5, building block names Section 5↔Section 7, Q42 tags Section 1↔Section 10, RISK-xx references Section 9↔Section 11, aspirational scenarios Section 10↔Section 11 |
| `.github/workflows/arc42-lint.yml` | GitHub Actions workflow — runs the linter on `docs/**` changes; also serves as a copy-paste template for user projects |
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
