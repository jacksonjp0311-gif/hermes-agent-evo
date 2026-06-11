import json
from pathlib import Path
from rhp.evidence_coherence_auditor import audit
def test_evidence_coherence_auditor_passes_aligned_packet(tmp_path: Path):
    ops=tmp_path/"docs/context-layer/ops"; ops.mkdir(parents=True); ev={"operation":"RHP-TEST","validation_passed":True,"focused_tests_passed":True,"next_recommended_operation":"RHP-NEXT","self_authorization":False,"autonomous_authority":False}
    (ops/"RHP-TEST-final-evidence.json").write_text(json.dumps(ev),encoding="utf-8"); (tmp_path/"docs/context-layer/latest-rhp.json").write_text(json.dumps({"latest_operation":"RHP-TEST","latest_evidence":"docs/context-layer/ops/RHP-TEST-final-evidence.json","next_operation":"RHP-NEXT"}),encoding="utf-8")
    rep=audit(tmp_path); assert rep["ok"] is True; assert not rep["failures"]
