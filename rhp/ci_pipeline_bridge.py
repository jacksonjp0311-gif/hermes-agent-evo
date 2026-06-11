# RHP-014.4 CI ingestion to wound/dry-run/human UI bridge.
from __future__ import annotations
import argparse, json
from pathlib import Path
from rhp.ci_artifact_extractor import classify_ci_text
from rhp.autoheal_executor_dry_run import dry_run_for_packet
from rhp.human_ui_summary import render_summary

RHP_CI_PIPELINE_BRIDGE_SCHEMA = "RHP-CI-PIPELINE-BRIDGE-v0.1"

def run_bridge(text_path: str | Path, evidence_path: str | Path, out_dir: str | Path) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    text = Path(text_path).read_text(encoding="utf-8", errors="replace")
    wound = classify_ci_text(text, "ingested-ci")
    wound_path = out / "wound-packet.json"
    wound_path.write_text(json.dumps(wound.as_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    dry = dry_run_for_packet(wound.as_dict())
    dry_path = out / "autoheal-dry-run.json"
    dry_path.write_text(json.dumps(dry.as_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    evidence = json.loads(Path(evidence_path).read_text(encoding="utf-8"))
    ui = render_summary(evidence, wound.as_dict(), dry.as_dict())
    ui_path = out / "human-ui-summary.txt"
    ui_path.write_text(ui + "\n", encoding="utf-8", newline="\n")
    return {
        "schema": RHP_CI_PIPELINE_BRIDGE_SCHEMA,
        "ok": wound.ok and dry.ok,
        "classification": wound.classification,
        "dry_run_ok": dry.ok,
        "wound_packet": str(wound_path),
        "autoheal_dry_run": str(dry_path),
        "human_ui_summary": str(ui_path),
        "non_claim_lock": "Bridge creates packets and summaries only. It does not mutate, commit, push, call remote APIs, or execute repairs.",
    }

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Bridge ingested CI text into wound/dry-run/human UI artifacts")
    p.add_argument("--text-path", required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    result = run_bridge(args.text_path, args.evidence, args.out_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
