from __future__ import annotations
import argparse, json
from pathlib import Path
from rhp.zero_context_rebuild import build_packet
RHP_LATEST_POINTER_SCHEMA = "RHP-LATEST-POINTER-v0.3"
def pointer(root="."):
    p = build_packet(root)
    return {"schema": RHP_LATEST_POINTER_SCHEMA, "latest_operation": p.latest_operation, "latest_evidence": p.latest_evidence, "latest_commit_or_base": p.latest_commit_or_base, "next_operation": p.next_operation, "zero_context_rebuild": "docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md", "authority_ok": p.ok}
def main(argv=None):
    a = argparse.ArgumentParser(); a.add_argument("--repo-root", default="."); a.add_argument("--out", default=""); args = a.parse_args(argv)
    data = pointer(args.repo_root)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True); Path(args.out).write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps(data, indent=2, ensure_ascii=False)); return 0 if data["authority_ok"] else 1
if __name__ == "__main__":
    raise SystemExit(main())
