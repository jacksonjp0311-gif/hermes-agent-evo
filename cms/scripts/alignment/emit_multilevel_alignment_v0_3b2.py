
from __future__ import annotations

import json
from pathlib import Path
from cms.alignment.multilevel import build_multilevel_alignment_report, report_to_markdown

ROOT = Path(__file__).resolve().parents[2]

def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def main() -> int:
    report = build_multilevel_alignment_report()
    write_json(ROOT / "outputs/alignment/latest_multilevel_alignment_report.json", report)
    write_json(ROOT / "reports/alignment/latest_multilevel_alignment_report.json", report)
    (ROOT / "reports/alignment").mkdir(parents=True, exist_ok=True)
    (ROOT / "reports/alignment/latest_multilevel_alignment_report.md").write_text(report_to_markdown(report) + "\n", encoding="utf-8")
    print(json.dumps({
        "schema": "CMS-SA-" + report["version"] + "-multilevel-alignment-emission",
        "passed": report["passed"],
        "version": report["version"],
        "seal_mode": report["seal_mode"],
        "feedback_items_checked": report["feedback_items_checked"],
        "feedback_items_aligned": report["feedback_items_aligned"],
        "findings": report["findings"],
        "pressure_findings": report["pressure_findings"],
        "wrote": [
            "outputs/alignment/latest_multilevel_alignment_report.json",
            "reports/alignment/latest_multilevel_alignment_report.json",
            "reports/alignment/latest_multilevel_alignment_report.md",
        ],
        "non_claim_lock": "Alignment emission writes repository evidence artifacts only.",
    }, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
