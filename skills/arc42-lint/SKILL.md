---
name: arc42-lint
version: 1.0.0
description: Validates cross-section ID consistency in generated arc42 documentation. Checks IF-xx interface IDs (§3↔§5), building block deployment coverage (§5↔§7), Q42 quality tag traceability (§1↔§10), ADR risk references (§9↔§11), and aspirational scenario linkage (§10↔§11). Runs the automated linter script when available, or applies rules manually when not.
---

# arc42 Consistency Linter

You are an expert arc42 architect validating cross-section ID consistency in architecture documentation.

This skill checks that identifiers defined in one section are correctly referenced in all related sections, and that every cross-section traceability rule is satisfied. It does not review content quality or completeness — use `arc42-review` for that.

**Five consistency rules:**

| Rule | Sections | What is checked |
|------|----------|-----------------|
| 1 | §3 ↔ §5 | IF-xx interface IDs defined in §3 must appear in §5 Level-1, and vice versa |
| 2 | §5 ↔ §7 | Every §5 building block name must appear in the §7 deployment mapping |
| 3 | §1 ↔ §10 | Every Q42 tag used in §10 quality scenarios must appear in §1.2 quality goals |
| 4 | §9 ↔ §11 | Every RISK-xx in an ADR's "Risks created" field must have a §11 risk matrix entry |
| 5 | §10 ↔ §11 | Every aspirational (unmet) scenario from §10.3 must be referenced in §11 |

---

## Step 1 — Locate the Documentation

**Do not start linting yet.** Ask the user:

1. **Where are the arc42 docs?** — What is the path to the documentation directory (e.g. `docs/`, `architecture/`, or a single monolithic file)?
2. **Is `scripts/arc42-lint.py` present?** — Check whether the automated linter script exists in the project. If it does, prefer running it. If not, apply the rules manually.

If the user is unsure about the docs path, look for `.md` files in `docs/`, `architecture/`, `arc42/`, or the project root.

---

## Step 2 — Run or Simulate

Choose the path based on what is available:

### Path A — Automated script is present

Run the linter:

```bash
python scripts/arc42-lint.py <docs_path> --format text
```

Capture the output. If the exit code is 0, all rules passed — proceed to Step 3 to present a clean report.

If there are errors or warnings, parse the output and continue to Step 3.

**Strict mode** (treat warnings as errors):
```bash
python scripts/arc42-lint.py <docs_path> --format text --strict
```

---

### Path B — No script available (manual check)

Read the relevant documentation sections. Apply each rule in order:

**Rule 1 — §3 ↔ §5 Interface IDs**
1. Read §3: collect every `IF-xx` from the interface table (first column)
2. Read §5 Level-1: collect every `IF-xx` from the Interfaces column of the building block table
3. Check both directions — each IF-xx in §3 must appear in §5, and each IF-xx in §5 must appear in §3
4. Record any orphan IDs as errors

**Rule 2 — §5 ↔ §7 Building Block Coverage**
1. Read §5: collect every component name (Name column of the building block table)
2. Read §7: search for each component name in the deployment view text and tables
3. Any component name absent from §7 is an error

**Rule 3 — §1 ↔ §10 Quality Tag Coverage**
1. Read §1.2: collect every Q42 tag (`#reliable`, `#efficient`, `#secure`, etc.) from the Quality Goal column
2. Read §10: collect the Q42 tag from every quality scenario's "Quality property" row
3. Any tag used in §10 that does not appear in §1.2 is an error

**Rule 4 — §9 ↔ §11 ADR Risk References**
1. Read §9: for each ADR, find the `Risks created (→ §11):` line in its Implications block; collect all `RISK-xx` IDs mentioned
2. Read §11: collect every `RISK-xx` from the risk matrix (ID column)
3. Any RISK-xx mentioned in §9 but absent from §11 is an error

**Rule 5 — §10.3 ↔ §11 Aspirational Scenarios**
1. Read §10.3 (aspirational scenarios table): collect every `QS-xx` where Current State is "not measured"
2. Read §11: check that each aspirational QS-xx is referenced somewhere in the risks/debt section
3. Any aspirational QS-xx absent from §11 is an error

---

## Step 3 — Report Findings

Present results in this format:

```markdown
## arc42 Consistency Lint Report

**Docs path:** [path checked]
**Method:** Automated script / Manual check

---

### Rule Results

| Rule | Sections | Status | Details |
|------|----------|--------|---------|
| 1 | §3 ↔ §5  IF-xx | PASS / FAIL | [e.g. "IF-03 missing from §5"] |
| 2 | §5 ↔ §7  Building blocks | PASS / FAIL / SKIP | [detail or "§7 not found"] |
| 3 | §1 ↔ §10 Q42 tags | PASS / FAIL | [e.g. "#usable used in QS-04 but absent from §1.2"] |
| 4 | §9 ↔ §11 RISK-xx | PASS / FAIL | [e.g. "RISK-02 in ADR-003 missing from §11"] |
| 5 | §10 ↔ §11 Aspirational | PASS / FAIL / SKIP | [detail or "no aspirational scenarios found"] |

---

### Issues

**Errors (must fix — IDs are inconsistent):**
- [ ] [Rule N] [Section]: [Specific ID or name] — [what is missing and where]

**Warnings (advisory — a section was not found):**
- [ ] [Rule N]: [Which section is missing] — consistency cannot be fully verified

---

### Verdict

- [ ] **CLEAN** — All applicable rules pass
- [ ] **ISSUES FOUND** — N error(s), M warning(s) — see Issues above
```

---

## Step 4 — Offer to Fix

After presenting the report:

1. For each **error**: offer to fix it immediately — either by adding the missing ID to the correct section, or by running the relevant section skill (`/arc42-section-N`) to regenerate that section with the correct references.
2. For **warnings** about missing sections: offer to create the missing section using the relevant skill.
3. After fixes are applied, re-run the lint check (script or manual) and confirm the rule now passes.

Ask: **"Would you like me to fix these issues now?"**

---

*Based on [arc42.org](https://arc42.org), [docs.arc42.org](https://docs.arc42.org), [quality.arc42.org](https://quality.arc42.org)*
