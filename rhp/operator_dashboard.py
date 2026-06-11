from __future__ import annotations
import argparse, json
from pathlib import Path
from rhp.zero_context_rebuild import build_packet
RHP_OPERATOR_DASHBOARD_SCHEMA = "RHP-OPERATOR-DASHBOARD-v0.3"
def dashboard(root="."):
    p = build_packet(root)
    return {"schema": RHP_OPERATOR_DASHBOARD_SCHEMA, "status": "ok" if p.ok else "blocked", "latest_operation": p.latest_operation, "next_operation": p.next_operation, "latest_evidence": p.latest_evidence, "authority_ok": p.ok, "sequence_count": len(p.active_sequence), "required_gate_count": len(p.required_gates)}
def render(d):
    g = "[OK]" if d["status"] == "ok" else "[BLOCKED]"
    return "\n".join([f"RHPLOAD [100%] HUMAN-UI-SUMMARY operation={d['latest_operation']} | status={d['status']} {g}","`- Hermes/RHP operator dashboard",f"   +- latest: {d['latest_operation']}",f"   +- next: {d['next_operation']}",f"   +- evidence: {d['latest_evidence']}",f"   +- active sequence boxes: {d['sequence_count']}",f"   +- required gates: {d['required_gate_count']}",f"   +- authority ok: {str(d['authority_ok']).lower()}",f"   `- verified: {str(d['authority_ok']).lower()} {g}"])
def main(argv=None):
    a = argparse.ArgumentParser(); a.add_argument("--repo-root", default="."); a.add_argument("--out", default=""); a.add_argument("--json", action="store_true"); args = a.parse_args(argv)
    data = dashboard(args.repo_root)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True); Path(args.out).write_text(render(data)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps(data, indent=2, ensure_ascii=False) if args.json else render(data)); return 0 if data["authority_ok"] else 1
if __name__ == "__main__":
    raise SystemExit(main())
