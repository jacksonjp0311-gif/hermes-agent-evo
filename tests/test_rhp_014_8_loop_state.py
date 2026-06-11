import json
from pathlib import Path
from rhp.loop_state import build_state
def test_loop_state_marks_red_ci_without_authority_drift(tmp_path: Path):
    ops=tmp_path/"docs/context-layer/ops"; ops.mkdir(parents=True); ev={"operation":"RHP-TEST","next_recommended_operation":"RHP-NEXT","validation_passed":True,"focused_tests_passed":True,"self_authorization":False,"autonomous_authority":False}
    (ops/"RHP-TEST-final-evidence.json").write_text(json.dumps(ev),encoding="utf-8"); (tmp_path/"docs/context-layer/latest-rhp.json").write_text(json.dumps({"latest_operation":"RHP-TEST","latest_evidence":"docs/context-layer/ops/RHP-TEST-final-evidence.json","next_operation":"RHP-NEXT"}),encoding="utf-8")
    st=build_state(tmp_path,"red"); assert st["authority_ok"] is True; assert st["gate_status"]["GITHUB-PUSH-BOX"]=="pushed_remote_ci_red"
