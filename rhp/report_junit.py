from __future__ import annotations
import argparse, json
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

RHP_JUNIT_REPORT_SCHEMA = "RHP-JUNIT-REPORT-v0.2"

def load_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def build_junit(evidence: dict) -> str:
    op = str(evidence.get("operation", "unknown"))
    cases = [
        ("authority_locks_false", not evidence.get("self_authorization", True) and not evidence.get("autonomous_authority", True)),
        ("focused_tests_passed", bool(evidence.get("focused_tests_passed", False))),
        ("validation_passed", bool(evidence.get("validation_passed", False))),
        ("operator_script_recorded", bool(evidence.get("operator_script_name", ""))),
        ("post_seal_residue_observer_added", bool(evidence.get("post_seal_residue_observer_added", False))),
        ("machine_reports_evidence_only", bool(evidence.get("machine_reports_are_evidence_only", False))),
        ("generated_source_escape_repair", bool(evidence.get("generated_source_escape_repair", False))),
    ]
    failures = sum(1 for _, ok in cases if not ok)
    suite = Element("testsuite", {
        "name": "RHPLOAD",
        "tests": str(len(cases)),
        "failures": str(failures),
        "errors": "0",
        "skipped": "0",
    })
    for name, ok in cases:
        case = SubElement(suite, "testcase", {"classname": "rhp", "name": name})
        if not ok:
            failure = SubElement(case, "failure", {"message": f"{name} failed for {op}"})
            failure.text = json.dumps(evidence, indent=2, ensure_ascii=False)
    xml = tostring(suite, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml + "\n"

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render RHP JUnit XML report")
    p.add_argument("--evidence", required=True)
    p.add_argument("--out", default="")
    args = p.parse_args(argv)
    xml = build_junit(load_json(args.evidence))
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(xml, encoding="utf-8", newline="\n")
    print(xml)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
