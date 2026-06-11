import json
from pathlib import Path
from rhp.rhploop_doctor import diagnose
def test_rhploop_doctor_reports_remote_ci_red_as_issue(tmp_path: Path):
    ops=tmp_path/"docs/context-layer/ops"; ops.mkdir(parents=True); ev={"operation":"RHP-TEST","next_recommended_operation":"RHP-NEXT","validation_passed":True,"focused_tests_passed":True,"self_authorization":False,"autonomous_authority":False}
    (ops/"RHP-TEST-final-evidence.json").write_text(json.dumps(ev),encoding="utf-8"); (tmp_path/"docs/context-layer/latest-rhp.json").write_text(json.dumps({"latest_operation":"RHP-TEST","latest_evidence":"docs/context-layer/ops/RHP-TEST-final-evidence.json","next_operation":"RHP-NEXT"}),encoding="utf-8")
    rep=diagnose(tmp_path,"red"); assert rep["ok"] is True; assert "remote_ci_red" in rep["issues"]
