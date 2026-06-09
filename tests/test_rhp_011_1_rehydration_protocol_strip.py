from __future__ import annotations

from hermes_cli.banner import _rhp_rehydration_protocol_lines


def test_rhp_011_1_rehydration_protocol_strip_verified(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_BOOT_PREFLIGHT_STATUS", "ok")
    monkeypatch.setenv(
        "HERMES_RHP_OPERATOR_STATUS",
        "\n".join(
            [
                "RHP rehydration sequence:",
                "[OK] repo root found",
                "[OK] RHP-010 evidence green",
                "[OK] HRCN boundary green",
                "[OK] alignment guard green",
                "[OK] startup packet created",
                "[OK] authority=false",
                "[OK] external_ingestion=false",
                "[OK] provider/model/tool execution=false",
                "[OK] CMS/memory/API write=false",
                "RHP rehydration complete: ok | phase=pre-interaction | evidence=RHP-010",
            ]
        ),
    )
    joined = "\n".join(_rhp_rehydration_protocol_lines())
    assert "Rehydration Protocol" in joined
    assert "verified" in joined
    assert "phase=pre-interaction" in joined
    assert "authority=false" in joined
    assert "repo ok" in joined
    assert "HRCN ok" in joined
    assert "#7DF9FF" in joined
    assert "#B388FF" in joined