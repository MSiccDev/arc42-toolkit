#!/usr/bin/env python3
"""arc42 cross-section consistency linter.

Usage:
    python scripts/arc42-lint.py [docs_path] [--lang LANG] [--format text|github] [--strict]

Exit codes:
    0  no issues (or only warnings in non-strict mode)
    1  one or more errors found (or warnings with --strict)

Language files live in languages/ next to this script's parent directory.
Default language is English (en). Run with --lang de, fr, it, es, or pt for
other built-in languages, or add a new JSON file to contribute a language.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Language loading
# ---------------------------------------------------------------------------

def load_language(lang_code: str, script_path: Path) -> dict:
    """Load language definition from languages/{lang_code}.json."""
    lang_dir = script_path.parent / "languages"
    lang_file = lang_dir / f"{lang_code}.json"

    if not lang_file.exists():
        available = sorted(p.stem for p in lang_dir.glob("*.json")) if lang_dir.exists() else []
        print(f"arc42-lint: language '{lang_code}' not found.", file=sys.stderr)
        if available:
            print(f"  Available languages: {', '.join(available)}", file=sys.stderr)
        else:
            print(f"  No language files found in {lang_dir}", file=sys.stderr)
            print(f"  Make sure the languages/ directory is present alongside scripts/",
                  file=sys.stderr)
        sys.exit(1)

    with open(lang_file, encoding="utf-8") as f:
        return json.load(f)


def _matches_any(text: str, patterns: list[str]) -> bool:
    """Return True if text matches any pattern (all patterns are case-insensitive regex)."""
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


# ---------------------------------------------------------------------------
# Section detection
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)


def _section_from_number(heading_text: str) -> int | None:
    """Detect section from the numeric prefix of a heading — language-agnostic.

    Matches: '1. Title', '10 Title', '3: Title'
    Returns None for sub-section numbers like '5.1'.
    """
    m = re.match(r"^(\d+)[.\s:]", heading_text.strip())
    if m:
        num = int(m.group(1))
        if 1 <= num <= 12:
            return num
    return None


def _section_from_keyword(heading_text: str, section_keywords: dict) -> int | None:
    """Detect section from language-specific keyword patterns."""
    for sec_str, patterns in section_keywords.items():
        if _matches_any(heading_text, patterns):
            return int(sec_str)
    return None


def detect_section(path: Path, content: str, lang: dict) -> int | None:
    """Return the arc42 section number for a file, or None if undetermined.

    Detection order:
      1. Numeric digits in filename stem (01–12)
      2. Numeric prefix in the first heading (language-agnostic)
      3. Keyword match in the first heading (language-specific fallback)
    """
    m = re.search(r"(?<!\d)(0[1-9]|1[0-2])(?!\d)", path.stem)
    if m:
        return int(m.group(1))

    for hm in _HEADING_RE.finditer(content):
        heading = hm.group(1)
        num = _section_from_number(heading)
        if num is not None:
            return num
        num = _section_from_keyword(heading, lang["section_keywords"])
        if num is not None:
            return num

    return None


def split_monolithic(content: str, path: Path, lang: dict) -> list[tuple[int, str, Path]]:
    """Split a monolithic arc42 file into (section_num, content_slice, path) windows."""
    lines = content.splitlines(keepends=True)
    segments: list[tuple[int, list[str], Path]] = []
    current_sec: int | None = None
    current_lines: list[str] = []

    for line in lines:
        m = re.match(r"^(#{1,2})\s+(.+)$", line)
        if m:
            heading = m.group(2)
            sec = _section_from_number(heading)
            if sec is None:
                sec = _section_from_keyword(heading, lang["section_keywords"])
            if sec is not None:
                if current_sec is not None:
                    segments.append((current_sec, current_lines, path))
                current_sec = sec
                current_lines = [line]
                continue
        current_lines.append(line)

    if current_sec is not None:
        segments.append((current_sec, current_lines, path))

    return [(sec, "".join(lines_), p) for sec, lines_, p in segments]


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
    return content.count("\n", 0, match_start) + 1


def extract_sec1_quality_tags(content: str) -> set[str]:
    """Q42 tags from the Section 1.2 quality goals table (second column)."""
    tags: set[str] = set()
    for m in re.finditer(r"^\|\s*\d+\s*\|\s*(#\w+)", content, re.MULTILINE):
        tags.add(m.group(1))
    return tags


def extract_sec3_interfaces(content: str) -> dict[str, int]:
    """IF-xx IDs from Section 3 interface table (first column)."""
    result: dict[str, int] = {}
    for m in re.finditer(r"^\|\s*(IF-\d+)\s*\|", content, re.MULTILINE):
        if_id = m.group(1)
        if if_id not in result:
            result[if_id] = _line_of(content, m.start())
    return result


def extract_sec5_data(content: str, lang: dict) -> tuple[dict[str, int], set[str]]:
    """IF-xx IDs and component names from Section 5 building block table.

    Table format: | Name | Responsibility | Interfaces |
    Header row is skipped using language-specific header names.
    """
    interfaces: dict[str, int] = {}
    names: set[str] = set()
    header_names = [h.lower() for h in lang["patterns"]["section5_header_names"]]

    for m in re.finditer(
        r"^\|\s*([^|*\-:][^|]*?)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|",
        content,
        re.MULTILINE,
    ):
        name_cell = m.group(1).strip()
        iface_cell = m.group(3).strip()

        if re.match(r"^[-:\s]+$", name_cell):
            continue
        if name_cell.lower() in header_names:
            continue

        names.add(name_cell)
        for if_id in re.findall(r"IF-\d+", iface_cell):
            if if_id not in interfaces:
                interfaces[if_id] = _line_of(content, m.start())

    return interfaces, names


def extract_sec9_adr_risks(content: str, lang: dict) -> dict[str, list[str]]:
    """Map ADR_ID → [RISK_IDs] from Section 9 ADR Implications blocks."""
    result: dict[str, list[str]] = {}
    current_adr: str | None = None
    risks_labels = lang["patterns"]["risks_created_label"]

    for line in content.splitlines():
        adr_match = re.match(r"^#{1,3}\s+(ADR-\d+)\s*:", line)
        if adr_match:
            current_adr = adr_match.group(1)
            result.setdefault(current_adr, [])
            continue

        if current_adr and _matches_any(line, risks_labels):
            result[current_adr].extend(re.findall(r"RISK-\d+", line))

    return result


def extract_sec10_data(content: str, lang: dict) -> tuple[dict[str, str], set[str]]:
    """Extract quality tags and aspirational scenario IDs from Section 10.

    quality_tags:  {QS_ID: "#tag"} from Quality property rows
    aspirational:  QS-xx IDs whose Current State matches a 'not measured' pattern
    """
    quality_tags: dict[str, str] = {}
    aspirational: set[str] = set()
    quality_prop_labels = lang["patterns"]["quality_property_label"]
    not_measured_values = lang["patterns"]["not_measured"]

    current_qs: str | None = None
    for line in content.splitlines():
        qs_match = re.match(r"^#{1,4}\s+(QS-\d+)\s*:", line)
        if qs_match:
            current_qs = qs_match.group(1)
            continue

        # Also pick up QS IDs from quality tree lines: "├── QS-01: Title"
        tree_match = re.search(r"\b(QS-\d+)\s*:", line)
        if tree_match and current_qs is None:
            current_qs = tree_match.group(1)

        # Quality property row: | Quality property | #efficient |
        if current_qs and _matches_any(line, quality_prop_labels):
            tag_m = re.search(r"(#\w+)", line)
            if tag_m:
                quality_tags[current_qs] = tag_m.group(1)

        # Aspirational row: | QS-xx | description | <not measured> | target | ... |
        asp_row = re.match(r"^\|\s*(QS-\d+)\s*\|([^|]*)\|\s*([^|]+)\|", line)
        if asp_row:
            current_state = asp_row.group(3).strip()
            if _matches_any(current_state, not_measured_values):
                aspirational.add(asp_row.group(1))

    return quality_tags, aspirational


def extract_sec11_risks(content: str) -> set[str]:
    """RISK-xx IDs from Section 11 risk matrix (first column)."""
    return set(re.findall(r"^\|\s*(RISK-\d+)\s*\|", content, re.MULTILINE))


# ---------------------------------------------------------------------------
# Document loader
# ---------------------------------------------------------------------------

def load_docs(docs_path: Path, lang: dict) -> SectionData:
    """Read all .md files under docs_path and populate SectionData."""
    data = SectionData()

    md_files = sorted(docs_path.rglob("*.md"))
    if not md_files:
        return data

    for path in md_files:
        content = path.read_text(encoding="utf-8", errors="replace")
        rel = str(path)

        sec = detect_section(path, content, lang)
        windows: list[tuple[int, str, str]] = []

        if sec is not None:
            windows = [(sec, content, rel)]
        else:
            splits = split_monolithic(content, path, lang)
            if splits:
                windows = [(s, c, rel) for s, c, _ in splits]

        for sec_num, sec_content, src in windows:
            _populate(data, sec_num, sec_content, src, lang)

    return data


def _populate(data: SectionData, sec: int, content: str, src: str, lang: dict) -> None:
    if sec == 1:
        data.sec1_quality_tags = extract_sec1_quality_tags(content)
        data.sec1_path = src
    elif sec == 3:
        data.sec3_interfaces = extract_sec3_interfaces(content)
        data.sec3_path = src
    elif sec == 5:
        data.sec5_interfaces, data.sec5_component_names = extract_sec5_data(content, lang)
        data.sec5_path = src
    elif sec == 7:
        data.sec7_content = content
        data.sec7_path = src
    elif sec == 9:
        data.sec9_adr_risks = extract_sec9_adr_risks(content, lang)
        data.sec9_path = src
    elif sec == 10:
        data.sec10_quality_tags, data.sec10_aspirational = extract_sec10_data(content, lang)
        data.sec10_path = src
    elif sec == 11:
        data.sec11_risks = extract_sec11_risks(content)
        data.sec11_content = content
        data.sec11_path = src


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------

def rule_interface_consistency(data: SectionData) -> list[LintIssue]:
    """Rule 1: IF-xx IDs must be identical in Section 3 and Section 5."""
    issues: list[LintIssue] = []

    if not data.sec3_interfaces and not data.sec5_interfaces:
        return issues

    if not data.sec3_interfaces:
        return [LintIssue("RULE-1", "warning", data.sec5_path, -1,
                          "Section 3 not found; cannot verify interface ID consistency with Section 5")]
    if not data.sec5_interfaces:
        return [LintIssue("RULE-1", "warning", data.sec3_path, -1,
                          "Section 5 not found; cannot verify interface ID consistency with Section 3")]

    for if_id in sorted(data.sec3_interfaces.keys() - data.sec5_interfaces.keys()):
        issues.append(LintIssue(
            "RULE-1", "error", data.sec3_path, data.sec3_interfaces[if_id],
            f"{if_id} defined in Section 3 but missing from Section 5 Level-1 building blocks",
        ))
    for if_id in sorted(data.sec5_interfaces.keys() - data.sec3_interfaces.keys()):
        issues.append(LintIssue(
            "RULE-1", "error", data.sec5_path, data.sec5_interfaces[if_id],
            f"{if_id} referenced in Section 5 but not defined in Section 3 interface table",
        ))
    return issues


def rule_component_in_deployment(data: SectionData) -> list[LintIssue]:
    """Rule 2: Every Section 5 building block name must appear in Section 7."""
    issues: list[LintIssue] = []

    if not data.sec5_component_names:
        return issues

    if data.sec7_content is None:
        return [LintIssue("RULE-2", "warning", data.sec5_path, -1,
                          "Section 7 not found; cannot verify building block deployment coverage")]

    sec7_lower = data.sec7_content.lower()
    for name in sorted(data.sec5_component_names):
        if name.lower() not in sec7_lower:
            issues.append(LintIssue(
                "RULE-2", "error", data.sec5_path, -1,
                f'Building block "{name}" (Section 5) not found in Section 7 deployment view',
            ))
    return issues


def rule_quality_tag_coverage(data: SectionData) -> list[LintIssue]:
    """Rule 3: Every Q42 tag used in Section 10 must appear in Section 1.2 quality goals."""
    issues: list[LintIssue] = []

    if not data.sec10_quality_tags:
        return issues

    if not data.sec1_quality_tags:
        return [LintIssue("RULE-3", "warning", data.sec10_path, -1,
                          "Section 1 not found; cannot verify quality tag coverage")]

    tags_in_10 = set(data.sec10_quality_tags.values())
    for tag in sorted(tags_in_10 - data.sec1_quality_tags):
        qs_ids = sorted(qs for qs, t in data.sec10_quality_tags.items() if t == tag)
        issues.append(LintIssue(
            "RULE-3", "error", data.sec10_path, -1,
            f"Q42 tag {tag} used in {', '.join(qs_ids)} (Section 10) "
            f"but not present in Section 1.2 quality goals",
        ))
    return issues


def rule_adr_risks_in_register(data: SectionData) -> list[LintIssue]:
    """Rule 4: Every RISK-xx in a Section 9 ADR 'Risks created' must exist in Section 11."""
    issues: list[LintIssue] = []

    if not data.sec9_adr_risks:
        return issues

    if not data.sec11_risks and not data.sec11_content:
        return [LintIssue("RULE-4", "warning", data.sec9_path, -1,
                          "Section 11 not found; cannot verify ADR risk references")]

    for adr_id, risk_ids in sorted(data.sec9_adr_risks.items()):
        for risk_id in sorted(risk_ids):
            if risk_id not in data.sec11_risks:
                issues.append(LintIssue(
                    "RULE-4", "error", data.sec9_path, -1,
                    f"{risk_id} referenced in {adr_id} (Section 9 'Risks created') "
                    f"but not found in Section 11 risk matrix",
                ))
    return issues


def rule_aspirational_in_risks(data: SectionData) -> list[LintIssue]:
    """Rule 5: Every Section 10 aspirational scenario must be referenced in Section 11."""
    issues: list[LintIssue] = []

    if not data.sec10_aspirational:
        return issues

    if not data.sec11_content:
        return [LintIssue("RULE-5", "warning", data.sec10_path, -1,
                          "Section 11 not found; cannot verify aspirational scenario traceability")]

    for qs_id in sorted(data.sec10_aspirational):
        if qs_id not in data.sec11_content:
            issues.append(LintIssue(
                "RULE-5", "error", data.sec10_path, -1,
                f"Aspirational scenario {qs_id} (Section 10.3) not referenced in Section 11 risks/debt",
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
    "RULE-1": "Section 3 ↔ Section 5  Interface IDs (IF-xx)",
    "RULE-2": "Section 5 ↔ Section 7  Building block deployment coverage",
    "RULE-3": "Section 1 ↔ Section 10 Quality goal tag coverage (Q42)",
    "RULE-4": "Section 9 ↔ Section 11 ADR risk references (RISK-xx)",
    "RULE-5": "Section 10 ↔ Section 11 Aspirational scenario traceability",
}


def run_all_rules(data: SectionData) -> list[LintIssue]:
    issues: list[LintIssue] = []
    for rule_fn in ALL_RULES:
        issues.extend(rule_fn(data))
    return issues


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(issues: list[LintIssue], docs_path: Path, lang_name: str) -> str:
    if not issues:
        return f"arc42-lint: no issues found — all consistency rules passed. [{lang_name}]"

    lines: list[str] = [f"arc42-lint: checking {docs_path} [{lang_name}]\n"]
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
    parts = []
    if errors:
        parts.append(f"{errors} error{'s' if errors != 1 else ''}")
    if warnings:
        parts.append(f"{warnings} warning{'s' if warnings != 1 else ''}")
    lines.append("Found " + ", ".join(parts))
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
        "--lang", default="en", metavar="LANG",
        help="Documentation language, e.g. en, de, fr, it, es, pt (default: en)",
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

    script_path = Path(__file__).resolve()
    lang = load_language(args.lang, script_path)

    docs = Path(args.docs_path)
    if not docs.exists():
        print(f"arc42-lint: '{docs}' does not exist — nothing to lint.")
        sys.exit(0)

    data = load_docs(docs, lang)

    if not any([
        data.sec1_quality_tags, data.sec3_interfaces, data.sec5_interfaces,
        data.sec7_content, data.sec9_adr_risks, data.sec10_quality_tags,
        data.sec11_risks,
    ]):
        print(f"arc42-lint: no arc42 sections detected in '{docs}' — nothing to lint.")
        sys.exit(0)

    issues = run_all_rules(data)

    lang_name = lang.get("name", args.lang)
    if args.format == "github":
        output = format_github(issues)
    else:
        output = format_text(issues, docs, lang_name)

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
