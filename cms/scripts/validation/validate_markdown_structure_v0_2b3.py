from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
text = README.read_text(encoding="utf-8", errors="replace") if README.exists() else ""
lines = text.splitlines()

errors = []

if len(lines) < 180:
    errors.append(f"line_count_too_low:{len(lines)}")

required_sections = [
    "# Cybernetic Memory System - Feedback-Governed Repository Memory Runtime",
    "## Current CMS Snapshot",
    "## Human Director Box",
    "## Current Public Metrics",
    "## Quick Start",
    "## Repository Layers",
    "## Historical Report Archive",
    "## PART I - Human README",
    "## PART II - RCC Nexus README",
    "## PART III - AI Agent README",
    "## README + Mini Repo Audit Map",
    "### Gap Classes the AI Must Detect",
    "## AI Failure Learning Ledger",
    "## Agent Geometry Layer",
    "## Process Alignment Layer",
    "## AI Rule - Directory Box and Mini README Synchronization",
    "## Law of Sufficient Form",
    "## Full Directory Box",
]

for section in required_sections:
    if section not in lines:
        errors.append(f"missing_isolated_section:{section}")

# Parse markdown table blocks correctly. A table block is valid when a header row is followed by a separator row.
table_blocks = 0
for i in range(len(lines) - 1):
    line = lines[i]
    nxt = lines[i + 1]
    if line.startswith("|") and line.endswith("|") and nxt.startswith("|") and "---" in nxt:
        table_blocks += 1

if table_blocks < 10:
    errors.append(f"table_block_count_too_low:{table_blocks}")

# Ensure no known collapsed-table fragments.
bad_fragments = [
    "Layer What it answers Primary output",
    "Surface Result",
    "Shell Meaning",
    "Change type Read first Validate",
    "Scan step Surface What to check",
    "Lesson ID Failure observed Root cause Permanent rule",
    "Rule Requirement",
]
for frag in bad_fragments:
    if frag in text:
        errors.append(f"collapsed_table_fragment:{frag}")

long_lines = [i + 1 for i, line in enumerate(lines) if len(line) > 500]
if long_lines:
    errors.append(f"long_lines_over_500:{long_lines[:10]}")

if text.count("```") % 2 != 0:
    errors.append("unbalanced_code_fences")

passed = not errors

report = {
    "schema": "CMS-SA-v0.2b3a-markdown-structure",
    "passed": passed,
    "errors": len(errors),
    "findings": errors,
    "line_count": len(lines),
    "table_blocks": table_blocks,
    "non_claim_lock": "Markdown structure validation improves public rendering but does not prove runtime correctness."
}

out_json = ROOT / "reports" / "markdown_structure" / "latest_markdown_structure.json"
out_md = ROOT / "reports" / "markdown_structure" / "latest_markdown_structure.md"
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
out_md.write_text(
    "# CMS-SA v0.2b3a Markdown Structure Validation\n\n"
    f"- passed: `{passed}`\n"
    f"- errors: `{len(errors)}`\n"
    f"- line_count: `{len(lines)}`\n"
    f"- table_blocks: `{table_blocks}`\n\n"
    "## Findings\n\n"
    + ("\n".join(f"- `{e}`" for e in errors) if errors else "- none\n")
    + "\n\nNon-claim lock: Markdown structure validation is not runtime correctness.\n",
    encoding="utf-8",
)

print(json.dumps(report, indent=2))
raise SystemExit(0 if passed else 1)