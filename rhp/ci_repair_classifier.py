# RHP-013.6 CI repair classifier.
from __future__ import annotations
import argparse, json, re
from dataclasses import dataclass, field
from typing import Any

CI_REPAIR_CLASSIFIER_SCHEMA = "RHP-CI-REPAIR-CLASSIFIER-v0.1"

@dataclass(frozen=True)
class CIRepairClassification:
    ok: bool
    schema: str
    classification: str
    confidence: float
    reason: str
    recommended_loop: str
    evidence_markers: list[str] = field(default_factory=list)
    non_claim_lock: str = "Diagnostic only. No mutation, rerun, tool authority, CMS/memory/API write, external ingestion, autonomy, or self-authorization."
    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def classify_failure_text(text: str) -> CIRepairClassification:
    lower = (text or "").lower()
    markers = []
    for pat in [r"evidence=rhp-0?\d+", r"keyerror: ['\"]previous_rhp", r"keyerror: ['\"]latest_rhp", r"expected.*rhp-", r"assert .*rhp-"]:
        if re.search(pat, lower):
            markers.append(pat)
    if markers:
        return CIRepairClassification(True, CI_REPAIR_CLASSIFIER_SCHEMA, "stale_test_or_guard_surface", 0.88, "Historical RHP evidence/key expectation detected.", "CI-REPAIR", markers)
    if "modulenotfounderror" in lower or "importerror" in lower:
        return CIRepairClassification(True, CI_REPAIR_CLASSIFIER_SCHEMA, "import_or_packaging_surface", 0.82, "Import/package resolution failure.", "CI-REPAIR", ["import failure"])
    if "timeout" in lower or "timed out" in lower:
        return CIRepairClassification(True, CI_REPAIR_CLASSIFIER_SCHEMA, "timeout_or_flaky_suspected", 0.65, "Timing-related failure; inspect repeatability.", "CI-WATCH", ["timeout"])
    if "assertionerror" in lower or "failed" in lower:
        return CIRepairClassification(True, CI_REPAIR_CLASSIFIER_SCHEMA, "assertion_failure_unknown", 0.55, "Assertion failed without strong classifier marker.", "DIAGNOSIS", ["assertion/failure"])
    return CIRepairClassification(False, CI_REPAIR_CLASSIFIER_SCHEMA, "unknown", 0.25, "No reliable repair class found.", "DIAGNOSIS", [])

def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--text", default="")
    p.add_argument("--file", default="")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    text = a.text
    if a.file:
        with open(a.file, "r", encoding="utf-8", errors="replace") as h:
            text = h.read()
    r = classify_failure_text(text)
    print(json.dumps(r.as_dict(), indent=2))
    return 0 if r.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
