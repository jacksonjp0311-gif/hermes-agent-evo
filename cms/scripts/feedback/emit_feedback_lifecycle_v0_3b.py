from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from cms.feedback.lifecycle import write_feedback_lifecycle_report  # noqa: E402


def main() -> int:
    report = write_feedback_lifecycle_report()
    print(json.dumps({
        "schema": "CMS-SA-v0.3b-feedback-lifecycle-emission",
        "passed": True,
        "version": report.get("version"),
        "item_count": report.get("item_count"),
        "class_counts": report.get("class_counts"),
        "wrote": [
            "outputs/feedback/latest_feedback_lifecycle_report.json",
            "reports/feedback/latest_feedback_lifecycle_report.json",
            "reports/feedback/latest_feedback_lifecycle_report.md",
        ],
        "non_claim_lock": "Feedback lifecycle emission writes repository evidence artifacts only."
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())