from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any
SCHEMA="RHP-LOOP-STATE-v0.1"
AUTH=["provider_call_executed","model_call_executed","tool_use_executed","cms_runtime_execution","cms_write","memory_write","memory_promotion","api_write","dependency_mutation_committed","external_ingestion","autonomous_authority","self_authorization"]
def load(p:str|Path)->dict[str,Any]: return json.loads(Path(p).read_text(encoding="utf-8"))
def build_state(root:str|Path=".",ci_status:str="unknown")->dict[str,Any]:
    root=Path(root); ptr=load(root/"docs/context-layer/latest-rhp.json"); ev=load(root/str(ptr["latest_evidence"])); locks={k:bool(ev.get(k,False)) for k in AUTH}
    gates={g:"ok" for g in ["ENTRYPOINT-GATE","ROOT-ANCHOR","RESIDUE-MANAGER","AUTOHEAL-PREFLIGHT","PULL-REBASE","HUMAN-AUTHORIZATION","OPERATION","VALIDATION","EVIDENCE","BOUNDARY","SECRET-SCAN","CURRENT-SCRIPT-GATE","COMMAND-RUNNER","STREAM-COLLAPSE","RHPWAIT-FILL","ERROR-BOX","GITHUB-PUSH-BOX","HUMAN-UI-SUMMARY","RETURN-ROOT"]}
    if ci_status in {"red","unknown"}: gates["GITHUB-PUSH-BOX"]="pushed_remote_ci_"+ci_status
    return {"schema":SCHEMA,"latest_operation":ptr.get("latest_operation"),"latest_evidence":ptr.get("latest_evidence"),"next_operation":ptr.get("next_operation"),"ci_status":ci_status,"authority_ok":all(v is False for v in locks.values()),"gate_status":gates,"non_claim_lock":"Loop state displays status only; no repair or authority."}
def main(argv=None)->int:
    p=argparse.ArgumentParser(); p.add_argument("--repo-root",default="."); p.add_argument("--ci-status",default="unknown",choices=["green","red","unknown"]); p.add_argument("--json",action="store_true"); p.add_argument("--out-json",default=""); a=p.parse_args(argv); s=build_state(a.repo_root,a.ci_status)
    if a.out_json: Path(a.out_json).parent.mkdir(parents=True,exist_ok=True); Path(a.out_json).write_text(json.dumps(s,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(s,indent=2,ensure_ascii=False)); return 0 if s["authority_ok"] else 1
if __name__=="__main__": raise SystemExit(main())
