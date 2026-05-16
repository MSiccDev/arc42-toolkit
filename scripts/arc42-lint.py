#!/usr/bin/env python3
"""arc42 cross-section consistency linter.

Usage:
    python scripts/arc42-lint.py [docs_path] [--format text|github] [--strict]

Exit codes:
    0  no issues (or only warnings in non-strict mode)
    1  one or more errors found (or warnings with --strict)
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Section detection
# ---------------------------------------------------------------------------

SECTION_KEYWORDS: list[tuple[str, int]] = [
    (r"introduction.*goals", 1),
    (r"constraints", 2),
    (r"context.*scope|scope.*context", 3),
    (r"solution.*strat", 4),
    (r"building.*block", 5),
    (r"runtime.*view", 6),
    (r"deployment.*view", 7),
    (r"crosscutting|cross.cutting", 8),
    (r"architecture.*decision", 9),
    (r"quality.*req|quality.*scenario|quality.*requirement", 10),
    (r"risk.*technical.*debt|technical.*debt", 11),
    (r"glossary", 12),
]

_HEADING_RE = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)


def _section_from_heading(text: str) -> int | None:
    """Return the first arc42 section number detected in a heading, or None."""
    for pattern, num in SECTION_KEYWORDS:
        if re.search(pattern, text, re.IGNORECASE):
            return num
    return None


def _section_from_filename(name: str) -> int | None:
    """Return section number if the filename starts with or contains NN (01-12)."""
    m = re.search(r"(?<!\d)(0[1-9]|1[0-2])(?!\d)", name)
    if m:
        return int(m.group(1))
    return None


def detect_section(path: Path, content: str) -> int | None:
    """Best-effort: filename digits → first heading keyword → None."""
    num = _section_from_filename(path.stem)
    if num is not None:
        return num
    for m in _HEADING_RE.finditer(content):
        num = _section_from_heading(m.group(1))
        if num is not None:
            return num
    return None


def split_monolithic(content: str, path: Path) -> list[tuple[int, str, Path]]:
    """
    If a single file contains multiple arc42 sections (headings), split it into
    virtual windows. Returns list of (section_num, content_slice, path).
    """
    lines = content.splitlines(keepends=True)
    segments: list[tuple[int, list[str], Path]] = []
    current_sec: int | None = None
    current_lines: list[str] = []

    for line in lines:
        m = re.match(r"^(#{1,2})\s+(.+)$", line)
        if m:
            sec = _section_from_heading(m.group(2))
            if sec is not None:
                if current_sec is not None:
                    segments.append((current_sec, current_lines, path))
                current_sec = sec
                current_lines = [line]
                continue
        current_lines.append(line)

    if current_sec is not None:
        segments.append((current_sec, current_lines, path))

    return [(sec, "".join(lines), p) for sec, lines, p in segments]


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class SectionData:
    sec1_quality_tags:    set[str]            = field(default_factory=set)
    sec3_interfaces:      dict[str, int]       = field(default_factory=dict)
    sec5_interfaces:      dict[str, int]       = field(default_factory=dict)
    sec5_component_names: set[str]             = field(default_factory=set)
    sec7_content:         str | None           = None
    sec7_path:            str                  = ""
    sec9_adr_risks:       dict[str, list[str]] = field(default_factory=dict)
    sec10_quality_tags:   dict[str, str]       = field(default_factory=dict)
    sec10_aspirational:   set[str]             = field(default_factory=set)
    sec11_risks:          set[str]             = field(default_factory=set)
    sec11_content:        str                  = ""
    sec11_path:           str                  = ""
    # source paths for better error messages
    sec1_path:  str = ""
    sec3_path:  str = ""
    sec5_path:  str = ""
    sec9_path:  str = ""
    sec10_path: str = ""


@dataclass
class LintIssue:
    rule:     str
    severity: str   # "error" | "warning"
    file:     str
    line:     int   # -1 if not line-specific
    message:  str


# ---------------------------------------------------------------------------
# Extractors
# ---------------------------------------------------------------------------

def _line_of(content: str, match_start: int) -> int:
    """Return 1-based line number of a character offset."""
    return content.count("\n", 0, match_start) + 1


def extract_sec1_quality_tags(content: str) -> set[str]:
    """Q42 tags from the §1.2 quality goals table (second column)."""
    tags: set[str] = set()
    for m in re.finditer(r"^\|\s*\d+\s*\|\s*(#\w+)", content, re.MULTILINE):
        tags.add(m.group(1))
    return tags


def extract_sec3_interfaces(content: str) -> dict[str, int]:
    """IF-xx IDs from §3 interface table (first column)."""
    result: dict[str, int] = {}
    for m in re.finditer(r"^\|\s*(IF-\d+)\s*\|", content, re.MULTILINE):
        if_id = m.group(1)
        if if_id not in result:
            result[if_id] = _line_of(content, m.start())
    return result


def extract_sec5_data(content: str) -> tuple[dict[str, int], set[str]]:
    """
    Returns (interfaces, component_names) from §5 building block table.
    Table format: | Name | Responsibility | Interfaces |
    Skips header/separator rows.
    """
    interfaces: dict[str, int] = {}
    names: set[str] = set()

    for m in re.finditer(
        r"^\|\s*([^|*\-:][^|]*?)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|",
        content,
        re.MULTILINE,
    ):
        name_cell = m.group(1).strip()
        iface_cell = m.group(3).strip()

        # skip markdown table header separators and known header labels
        if re.match(r"^[-:\s]+$", name_cell):
            continue
        lower = name_cell.lower()
        if lower in ("name", "component", "building block", "element"):
            continue

        names.add(name_cell)
        for if_id in re.findall(r"IF-\d+", iface_cell):
            if if_id not in interfaces:
                interfaces[if_id] = _line_of(content, m.start())

    return interfaces, names


def extract_sec9_adr_risks(content: str) -> dict[str, list[str]]:
    """Map ADR_ID → [RISK_IDs] from §9 Implications blocks."""
    result: dict[str, list[str]] = {}
    current_adr: str | None = None

    for line in content.splitlines():
        adr_match = re.match(r"^#{1,3}\s+(ADR-\d+)\s*:", line)
        if adr_match:
            current_adr = adr_match.group(1)
            result.setdefault(current_adr, [])
            continue

        if current_adr and re.search(r"Risks created\s*\(→\s*§11\)", line, re.IGNORECASE):
            risks = re.findall(r"RISK-\d+", line)
            result[current_adr].extend(risks)

    return result


def extract_sec10_data(content: str) -> tuple[dict[str, str], set[str]]:
    """
    Returns (quality_tags, aspirational_ids).
    quality_tags: {QS_ID: "#tag"} from Quality property rows.
    aspirational_ids: QS-xx IDs from §10.3 'not measured' rows.
    """
    quality_tags: dict[str, str] = {}
    aspirational: set[str] = set()

    current_qs: str | None = None
    for line in content.splitlines():
        # QS heading: ### QS-01: Title
        qs_match = re.match(r"^#{1,4}\s+(QS-\d+)\s*:", line)
        if qs_match:
            current_qs = qs_match.group(1)
            continue

        # Also detect QS IDs from quality tree lines like "├── QS-01: ..."
        tree_match = re.search(r"\b(QS-\d+)\s*:", line)
        if tree_match and current_qs is None:
            current_qs = tree_match.group(1)

        # Quality property row: | Quality property | #tag |
        tag_match = re.search(
            r"\|\s*\*{0,2}Quality property\*{0,2}\s*\|\s*(#\w+)", line, re.IGNORECASE
        )
        if tag_match and current_qs:
            quality_tags[current_qs] = tag_match.group(1)

        # §10.3 aspirational row: | QS-xx | ... | not measured | ...
        asp_match = re.match(r"^\|\s*(QS-\d+)\s*\|[^|]*\|\s*not measured", line, re.IGNORECASE)
        if asp_match:
            aspirational.add(asp_match.group(1))

    return quality_tags, aspirational


def extract_sec11_risks(content: str) -> set[str]:
    """RISK-xx IDs from §11 risk matrix."""
    return set(re.findall(r"^\|\s*(RISK-\d+)\s*\|", content, re.MULTILINE))


# ---------------------------------------------------------------------------
# Document loader
# ---------------------------------------------------------------------------

def load_docs(docs_path: Path) -> SectionData:
    """Read all .md files under docs_path and populate SectionData."""
    data = SectionData()

    md_files = sorted(docs_path.rglob("*.md"))
    if not md_files:
        return data

    for path in md_files:
        content = path.read_text(encoding="utf-8", errors="replace")
        rel = str(path)

        # Try single-section detection first
        sec = detect_section(path, content)
        windows: list[tuple[int, str, str]] = []

        if sec is not None:
            windows = [(sec, content, rel)]
        else:
            # Try splitting as monolithic file
            splits = split_monolithic(content, path)
            if splits:
                windows = [(s, c, rel) for s, c, _ in splits]

        for sec_num, sec_content, src in windows:
            _populate(data, sec_num, sec_content, src)

    return data


def _populate(data: SectionData, sec: int, content: str, src: str) -> None:
    if sec == 1:
        data.sec1_quality_tags = extract_sec1_quality_tags(content)
        data.sec1_path = src
    elif sec == 3:
        data.sec3_interfaces = extract_sec3_interfaces(content)
        data.sec3_path = src
    elif sec == 5:
        data.sec5_interfaces, data.sec5_component_names = extract_sec5_data(content)
        data.sec5_path = src
    elif sec == 7:
        data.sec7_content = content
        data.sec7_path = src
    elif sec == 9:
        data.sec9_adr_risks = extract_sec9_adr_risks(content)
        data.sec9_path = src
    elif sec == 10:
        data.sec10_quality_tags, data.sec10_aspirational = extract_sec10_data(content)
        data.sec10_path = src
    elif sec == 11:
        data.sec11_risks = extract_sec11_risks(content)
        data.sec11_content = content
        data.sec11_path = src


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------

def rule_interface_consistency(data: SectionData) -> list[LintIssue]:
    """Rule 1: IF-xx IDs must be identical in §3 and §5."""
    issues: list[LintIssue] = []

    if not data.sec3_interfaces and not data.sec5_interfaces:
        return issues  # nothing to compare

    if not data.sec3_interfaces:
        return [LintIssue("RULE-1", "warning", data.sec5_path, -1,
                          "§3 not found; cannot verify interface ID consistency with §5")]
    if not data.sec5_interfaces:
        return [LintIssue("RULE-1", "warning", data.sec3_path, -1,
                          "§5 not found; cannot verify interface ID consistency with §3")]

    for if_id in sorted(data.sec3_interfaces.keys() - data.sec5_interfaces.keys()):
        issues.append(LintIssue(
            "RULE-1", "error", data.sec3_path, data.sec3_interfaces[if_id],
            f"{if_id} defined in §3 but missing from §5 Level-1 building blocks",
        ))
    for if_id in sorted(data.sec5_interfaces.keys() - data.sec3_interfaces.keys()):
        issues.append(LintIssue(
            "RULE-1", "error", data.sec5_path, data.sec5_interfaces[if_id],
            f"{if_id} referenced in §5 but not defined in §3 interface table",
        ))
    return issues


def rule_component_in_deployment(data: SectionData) -> list[LintIssue]:
    """Rule 2: Every §5 building block name must appear in §7."""
    issues: list[LintIssue] = []

    if not data.sec5_component_names:
        return issues

    if data.sec7_content is None:
        return [LintIssue("RULE-2", "warning", data.sec5_path, -1,
                          "§7 not found; cannot verify building block deployment coverage")]

    sec7_lower = data.sec7_content.lower()
    for name in sorted(data.sec5_component_names):
        if name.lower() not in sec7_lower:
            issues.append(LintIssue(
                "RULE-2", "error", data.sec5_path, -1,
                f'Building block "{name}" (§5) not found in §7 deployment view',
            ))
    return issues


def rule_quality_tag_coverage(data: SectionData) -> list[LintIssue]:
    """Rule 3: Every Q42 tag used in §10 scenarios must appear in §1.2 quality goals."""
    issues: list[LintIssue] = []

    if not data.sec10_quality_tags:
        return issues

    if not data.sec1_quality_tags:
        return [LintIssue("RULE-3", "warning", data.sec10_path, -1,
                          "§1 not found; cannot verify quality tag coverage")]

    tags_in_10 = set(data.sec10_quality_tags.values())
    for tag in sorted(tags_in_10 - data.sec1_quality_tags):
        qs_ids = [qs for qs, t in data.sec10_quality_tags.items() if t == tag]
        issues.append(LintIssue(
            "RULE-3", "error", data.sec10_path, -1,
            f"Q42 tag {tag} used in {', '.join(sorted(qs_ids))} (§10) "
            f"but not present in §1.2 quality goals",
        ))
    return issues


def rule_adr_risks_in_register(data: SectionData) -> list[LintIssue]:
    """Rule 4: Every RISK-xx in §9 ADR 'Risks created' must exist in §11."""
    issues: list[LintIssue] = []

    if not data.sec9_adr_risks:
        return issues

    if not data.sec11_risks and not data.sec11_content:
        return [LintIssue("RULE-4", "warning", data.sec9_path, -1,
                          "§11 not found; cannot verify ADR risk references")]

    for adr_id, risk_ids in sorted(data.sec9_adr_risks.items()):
        for risk_id in sorted(risk_ids):
            if risk_id not in data.sec11_risks:
                issues.append(LintIssue(
                    "RULE-4", "error", data.sec9_path, -1,
                    f"{risk_id} referenced in {adr_id} §9 'Risks created' "
                    f"but not found in §11 risk matrix",
                ))
    return issues


def rule_aspirational_in_risks(data: SectionData) -> list[LintIssue]:
    """Rule 5: Every §10 aspirational scenario must be referenced in §11."""
    issues: list[LintIssue] = []

    if not data.sec10_aspirational:
        return issues

    if not data.sec11_content:
        return [LintIssue("RULE-5", "warning", data.sec10_path, -1,
                          "§11 not found; cannot verify aspirational scenario traceability")]

    for qs_id in sorted(data.sec10_aspirational):
        if qs_id not in data.sec11_content:
            issues.append(LintIssue(
                "RULE-5", "error", data.sec10_path, -1,
                f"Aspirational scenario {qs_id} (§10.3) not referenced in §11 risks/debt",
            ))
    return issues


ALL_RULES = [
    rule_interface_consistency,
    rule_component_in_deployment,
    rule_quality_tag_coverage,
    rule_adr_risks_in_register,
    rule_aspirational_in_risks,
]

RULE_DESCRIPTIONS = {
    "RULE-1": "§3 ↔ §5  Interface IDs (IF-xx)",
    "RULE-2": "§5 ↔ §7  Building block deployment coverage",
    "RULE-3": "§1 ↔ §10 Quality goal tag coverage (Q42)",
    "RULE-4": "§9 ↔ §11 ADR risk references (RISK-xx)",
    "RULE-5": "§10 ↔ §11 Aspirational scenario traceability",
}


def run_all_rules(data: SectionData) -> list[LintIssue]:
    issues: list[LintIssue] = []
    for rule_fn in ALL_RULES:
        issues.extend(rule_fn(data))
    return issues


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(issues: list[LintIssue], docs_path: Path) -> str:
    if not issues:
        return "arc42-lint: no issues found — all consistency rules passed."

    lines: list[str] = [f"arc42-lint: checking {docs_path}\n"]
    by_rule: dict[str, list[LintIssue]] = {}
    for issue in issues:
        by_rule.setdefault(issue.rule, []).append(issue)

    for rule_id in sorted(by_rule):
        desc = RULE_DESCRIPTIONS.get(rule_id, rule_id)
        lines.append(f"[{rule_id}] {desc}")
        for issue in by_rule[rule_id]:
            loc = f"{issue.file}:{issue.line}" if issue.line > 0 else issue.file
            lines.append(f"  [{issue.severity.upper()}] {loc}: {issue.message}")
        lines.append("")

    errors   = sum(1 for i in issues if i.severity == "error")
    warnings = sum(1 for i in issues if i.severity == "warning")
    summary_parts = []
    if errors:
        summary_parts.append(f"{errors} error{'s' if errors != 1 else ''}")
    if warnings:
        summary_parts.append(f"{warnings} warning{'s' if warnings != 1 else ''}")
    lines.append("Found " + ", ".join(summary_parts))
    return "\n".join(lines)


def format_github(issues: list[LintIssue]) -> str:
    lines: list[str] = []
    for issue in issues:
        level = "error" if issue.severity == "error" else "warning"
        title = RULE_DESCRIPTIONS.get(issue.rule, issue.rule)
        file_part = f"file={issue.file}" if issue.file else ""
        line_part = f",line={issue.line}" if issue.line > 0 else ""
        lines.append(f"::{level} {file_part}{line_part},title={title}::{issue.message}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="arc42 cross-section consistency linter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "docs_path", nargs="?", default="docs",
        help="Path to arc42 docs directory (default: docs/)",
    )
    parser.add_argument(
        "--format", choices=["text", "github"], default="text",
        help="Output format: 'text' for local use, 'github' for Actions annotations",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Treat warnings as errors (non-zero exit)",
    )
    args = parser.parse_args()

    docs = Path(args.docs_path)
    if not docs.exists():
        print(f"arc42-lint: '{docs}' does not exist — nothing to lint.")
        sys.exit(0)

    data = load_docs(docs)

    if not any([
        data.sec1_quality_tags, data.sec3_interfaces, data.sec5_interfaces,
        data.sec7_content, data.sec9_adr_risks, data.sec10_quality_tags,
        data.sec11_risks,
    ]):
        print(f"arc42-lint: no arc42 sections detected in '{docs}' — nothing to lint.")
        sys.exit(0)

    issues = run_all_rules(data)

    if args.format == "github":
        output = format_github(issues)
    else:
        output = format_text(issues, docs)

    if output:
        print(output)

    errors   = sum(1 for i in issues if i.severity == "error")
    warnings = sum(1 for i in issues if i.severity == "warning")

    if errors:
        sys.exit(1)
    if args.strict and warnings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
