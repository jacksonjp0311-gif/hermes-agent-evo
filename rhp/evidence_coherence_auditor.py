from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any
SCHEMA="RHP-EVIDENCE-COHERENCE-AUDITOR-v0.1"
AUTH=["provider_call_executed","model_call_executed","tool_use_executed","cms_runtime_execution","cms_write","memory_write","memory_promotion","api_write","dependency_mutation_committed","external_ingestion","autonomous_authority","self_authorization"]
def load(p:str|Path)->dict[str,Any]: return json.loads(Path(p).read_text(encoding="utf-8"))
def chk(n:str,ok:bool,d:str)->dict[str,Any]: return {"name":n,"ok":bool(ok),"detail":d}
def audit(root:str|Path=".")->dict[str,Any]:
    root=Path(root); pp=root/"docs/context-layer/latest-rhp.json"; ptr=load(pp); er=str(ptr.get("latest_evidence","")); ep=root/er; ev=load(ep) if ep.exists() else {}
    checks=[chk("latest_pointer_exists",pp.exists(),str(pp)),chk("latest_evidence_exists",ep.exists(),er)]
    checks += [chk("operation_alignment",ptr.get("latest_operation")==ev.get("operation"),f"pointer={ptr.get('latest_operation')} evidence={ev.get('operation')}")]
    checks += [chk("next_alignment",ptr.get("next_operation")==ev.get("next_recommended_operation"),f"pointer={ptr.get('next_operation')} evidence={ev.get('next_recommended_operation')}")]
    checks += [chk("validation_passed",bool(ev.get("validation_passed",False)),"validation flag"),chk("focused_tests_passed",bool(ev.get("focused_tests_passed",False)),"focused flag")]
    locks={k:bool(ev.get(k,False)) for k in AUTH}; checks += [chk("authority_locks_false",all(v is False for v in locks.values()),json.dumps(locks,sort_keys=True))]
    fails=[c for c in checks if not c["ok"]]
    return {"schema":SCHEMA,"ok":not fails,"latest_operation":ptr.get("latest_operation"),"latest_evidence":er,"next_operation":ptr.get("next_operation"),"checks":checks,"failures":fails,"non_claim_lock":"Audits recorded evidence only; no repair, CI rerun, workflow mutation, or authority."}
def main(argv=None)->int:
    p=argparse.ArgumentParser(); p.add_argument("--repo-root",default="."); p.add_argument("--json",action="store_true"); p.add_argument("--out-json",default=""); a=p.parse_args(argv); rep=audit(a.repo_root)
    if a.out_json: Path(a.out_json).parent.mkdir(parents=True,exist_ok=True); Path(a.out_json).write_text(json.dumps(rep,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(rep,indent=2,ensure_ascii=False)); return 0 if rep["ok"] else 1
if __name__=="__main__": raise SystemExit(main())
