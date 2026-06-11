from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any
from rhp.evidence_coherence_auditor import audit
from rhp.loop_state import build_state
SCHEMA="RHPLOOP-DOCTOR-v0.1"
def diagnose(root:str|Path=".",ci_status:str="unknown")->dict[str,Any]:
    coh=audit(root); st=build_state(root,ci_status); issues=[]
    if not coh["ok"]: issues.append("evidence_coherence_failed")
    if ci_status=="red": issues.append("remote_ci_red")
    if ci_status=="unknown": issues.append("remote_ci_unknown")
    if not st["authority_ok"]: issues.append("authority_drift")
    return {"schema":SCHEMA,"ok":"evidence_coherence_failed" not in issues and "authority_drift" not in issues,"ci_status":ci_status,"issues":issues,"latest_operation":st["latest_operation"],"next_operation":st["next_operation"],"recommendation":"repair CI with evidence-first wound packet, then advance after green checks" if ci_status=="red" else "continue with gated next operation","non_claim_lock":"Doctor reports only; no repair, CI rerun, workflow mutation, or authority."}
def main(argv=None)->int:
    p=argparse.ArgumentParser(); p.add_argument("--repo-root",default="."); p.add_argument("--ci-status",default="unknown",choices=["green","red","unknown"]); p.add_argument("--json",action="store_true"); p.add_argument("--out-json",default=""); a=p.parse_args(argv); rep=diagnose(a.repo_root,a.ci_status)
    if a.out_json: Path(a.out_json).parent.mkdir(parents=True,exist_ok=True); Path(a.out_json).write_text(json.dumps(rep,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(rep,indent=2,ensure_ascii=False)); return 0 if rep["ok"] else 1
if __name__=="__main__": raise SystemExit(main())
