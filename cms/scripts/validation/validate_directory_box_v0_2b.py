from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
MANIFEST_CANDIDATES = [
    ROOT / "docs" / "directory" / "cms_full_directory_box_v0_2b3a.json",
    ROOT / "docs" / "directory" / "cms_full_directory_box_v0_2b3.json",
    ROOT / "docs" / "directory" / "cms_full_directory_box_v0_2b2.json",
]

manifest_path = next((p for p in MANIFEST_CANDIDATES if p.exists()), MANIFEST_CANDIDATES[0])
readme = README.read_text(encoding="utf-8", errors="replace") if README.exists() else ""
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

required_anchors = [
    "## Human Director Box",
    "## Current Public Metrics",
    "## Repository Layers",
    "## Historical Report Archive",
    "## Agent Geometry Layer",
    "## Process Alignment Layer",
    "## Law of Sufficient Form",
    "## AI Rule - Directory Box and Mini README Synchronization",
    "## Full Directory Box",
]
missing_anchors = [a for a in required_anchors if a not in readme]

missing_directory_rows = []
for row in manifest.get("rows", []):
    p = row["path"]
    if f"`{p}`" not in readme:
        missing_directory_rows.append(p)

seen = set()
duplicate_rows = []
for row in manifest.get("rows", []):
    p = row["path"]
    if p in seen:
        duplicate_rows.append(p)
    seen.add(p)

missing_paths_on_disk = []
for row in manifest.get("rows", []):
    p = row["path"].rstrip("/")
    if not (ROOT / p).exists():
        missing_paths_on_disk.append(row["path"])

passed = not missing_anchors and not missing_directory_rows and not duplicate_rows and not missing_paths_on_disk

report = {
    "schema": "CMS-SA-v0.2b3a-directory-box-validation",
    "passed": passed,
    "errors": len(missing_anchors) + len(missing_directory_rows) + len(duplicate_rows) + len(missing_paths_on_disk),
    "manifest": str(manifest_path.relative_to(ROOT)).replace("\\", "/"),
    "missing_anchors": missing_anchors,
    "missing_directory_rows": missing_directory_rows,
    "duplicate_rows": duplicate_rows,
    "missing_paths_on_disk": missing_paths_on_disk,
    "row_count": len(manifest.get("rows", [])),
    "non_claim_lock": "Directory box validation is navigation validation, not code correctness."
}

out_json = ROOT / "reports" / "directory" / "latest_directory_box_validation.json"
out_md = ROOT / "reports" / "directory" / "latest_directory_box_validation.md"
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
out_md.write_text(
    "# CMS-SA v0.2b3a Directory Box Validation\n\n"
    f"- passed: `{passed}`\n"
    f"- errors: `{report['errors']}`\n"
    f"- manifest: `{report['manifest']}`\n"
    f"- row_count: `{report['row_count']}`\n"
    f"- missing_anchors: `{missing_anchors}`\n"
    f"- missing_directory_rows: `{missing_directory_rows}`\n"
    f"- duplicate_rows: `{duplicate_rows}`\n"
    f"- missing_paths_on_disk: `{missing_paths_on_disk}`\n\n"
    "Non-claim lock: directory validation is navigation validation, not code correctness.\n",
    encoding="utf-8",
)

print(json.dumps(report, indent=2))
raise SystemExit(0 if passed else 1)