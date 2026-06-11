# RHP Zero-Context Rebuild Packet

- schema: `RHP-ZERO-CONTEXT-REBUILD-v0.4`
- ok: `True`
- latest operation: `RHP-014.7`
- latest evidence: `docs/context-layer/ops/RHP-014-7-final-evidence.json`
- latest commit/base: `3d89d9cce5a9c6b256526870b42fb3dacfcc1e79`
- next operation: `RHP-014.8 Evidence coherence auditor + loop_state + rhploop doctor`

## Required read order
1. `docs/context-layer/latest-rhp.json`
2. `docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md`
3. `docs/context-layer/all-one-script-contract.md`
4. `docs/context-layer/rhp_gate_checklist.md`
5. `README.md`
6. `AGENTS.md`
7. `rhp/README.md`
8. `docs/context-layer/ops/RHP-014-7-final-evidence.json`
9. `docs/context-layer/ops/RHP-014-7-operator-dashboard-bundle.json`

## Active sequence
1. `ENTRYPOINT-GATE`
2. `ROOT-ANCHOR`
3. `RESIDUE-MANAGER`
4. `AUTOHEAL-PREFLIGHT`
5. `PULL-REBASE`
6. `HUMAN-AUTHORIZATION`
7. `OPERATION`
8. `VALIDATION`
9. `EVIDENCE`
10. `BOUNDARY`
11. `SECRET-SCAN`
12. `CURRENT-SCRIPT-GATE`
13. `COMMAND-RUNNER`
14. `STREAM-COLLAPSE`
15. `RHPWAIT-FILL`
16. `ERROR-BOX`
17. `GITHUB-PUSH-BOX`
18. `HUMAN-UI-SUMMARY`
19. `RETURN-ROOT`

## Required gates
- entrypoint must be file invocation
- residue manager must classify failed-run residue
- operator_script_name must match expected script
- operation in evidence must match current operation
- authority locks must remain false
- unknown dirty paths must block
- no push before current-script gate
- RHPWAIT is display-only and separate from RHPLOAD audit grammar

## Authority locks
- `provider_call_executed`: `False`
- `model_call_executed`: `False`
- `tool_use_executed`: `False`
- `cms_runtime_execution`: `False`
- `cms_write`: `False`
- `memory_write`: `False`
- `memory_promotion`: `False`
- `api_write`: `False`
- `dependency_mutation_committed`: `False`
- `external_ingestion`: `False`
- `autonomous_authority`: `False`
- `self_authorization`: `False`

## Roles
- Hermes: agent/runtime surface and operator shell candidate
- RHP: governance, evidence, reconstruction, residue classification, safety gating, and dashboard geometry
- All-One: local human-authorized actuator
- Evidence: proof memory and zero-context replay surface
- Human: authorization boundary

Non-claim lock: Zero-context rebuild reconstructs loop state only. It grants no provider/model/tool/CMS/memory/API/autonomous/self-authorization authority.
