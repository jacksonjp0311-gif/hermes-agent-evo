from __future__ import annotations
import argparse, json
from pathlib import Path
from rhp.zero_context_rebuild import build_packet
RHP_HERMES_OPERATOR_CONTEXT_SCHEMA = "RHP-HERMES-OPERATOR-CONTEXT-v0.3"
def context(root="."):
    p = build_packet(root)
    return {"schema": RHP_HERMES_OPERATOR_CONTEXT_SCHEMA, "hermes_mode": "operator_shell_candidate", "hermes_can": ["display_dashboard","read_evidence","ingest_local_ci_artifacts","propose_dry_run_plans","emit_operator_context"], "hermes_cannot": ["self_authorize","mutate_without_all_one","push_without_gates","write_memory_or_cms","call_providers_from_rhp","bypass_entrypoint_gate","bypass_residue_manager"], "latest_operation": p.latest_operation, "next_operation": p.next_operation, "authority_locks": p.authority_locks, "non_claim_lock": "Hermes operator context is read-only orientation. It grants no direct mutation or self-authorization authority."}
def main(argv=None):
    a = argparse.ArgumentParser(); a.add_argument("--repo-root", default="."); a.add_argument("--out", default=""); args = a.parse_args(argv)
    data = context(args.repo_root)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True); Path(args.out).write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps(data, indent=2, ensure_ascii=False)); return 0 if all(v is False for v in data["authority_locks"].values()) else 1
if __name__ == "__main__":
    raise SystemExit(main())
