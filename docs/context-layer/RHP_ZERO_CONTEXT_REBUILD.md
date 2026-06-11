# RHP Zero-Context Rebuild Packet

- schema: `RHP-ZERO-CONTEXT-REBUILD-v1.9`
- ok: `True`
- latest operation: `RHP-016.2`
- latest evidence: `docs/context-layer/ops/RHP-016-2-final-evidence.json`
- failed subject commit: `1b61c682805e7083e5c410af705898ed4a373102`
- failed workflow: `Tests`
- active wound class: `browser_supervisor_websockets_dependency_api_drift`
- failed test file: `tests/tools/test_browser_supervisor.py`
- repro command: `python -m pytest tests/tools/test_browser_supervisor.py`
- next operation: `RHP-016.3 Bounded browser supervisor websockets dependency/API repair`

Non-claim lock: Zero-context rebuild grants no authority.
