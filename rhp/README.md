<!-- HRCN_MINI_README_START -->
# rhp

## Folder Purpose

Hermes-local Rehydration Protocol substrate: origin manifest, alignment report, origin certificate, schemas, ledger, reports, and evidence used by `rhp_runtime_bridge.py` before HRCN proposal-context injection.

## S - Specification

This folder participates in the Hermes repository according to its local role. Profile source: RHP-001. Current repository boundary: RHP-004 repair. This README remains a navigation and context surface only.

RHP is the first boot-orientation layer for Hermes-local origin alignment. It does not replace HRCN. RHP checks whether Hermes has loaded declared repository-origin surfaces before proposal work. HRCN continues to classify authority after RHP orientation.

## HRCN Boundary Note

Profile source: RHP-001.
Current repository boundary: RHP-004 repair.
This README is a navigation/context surface only.
Runtime, dependency, CMS, API-write, memory-promotion, Codex-ingestion, provider/model, tool, autonomous, or apply/write authority is not granted by this README.

Profile: `full`

## H - Hooks

Inbound hooks:

- `README.md`
- `AGENTS.md`
- `agent/agent_init.py`
- `rhp_runtime_bridge.py`
- `docs/context-layer/ops/RHP-001-final-evidence.json`
- `docs/context-layer/ops/RHP-002-final-evidence.json`
- `docs/context-layer/ops/RHP-003-final-evidence.json`
- `docs/context-layer/ops/RHP-004-final-evidence.json`

Outbound hooks:

- `rhp/origin_manifest.json`
- `rhp/latest_alignment_report.json`
- `rhp/latest_origin_certificate.json`
- `rhp/ledger/rhp_rehydration_ledger.jsonl`
- `rhp/reports/rhp_alignment_report.md`
- `tests/test_rhp_runtime_bridge.py`
- `tests/test_rhp_context_injection.py`
- `tests/test_rhp_hrcn_order.py`
- `tests/test_rhp_runtime_startup_smoke.py`
- `tests/test_rhp_004_hrcn_bridge_anchor_alignment.py`
- root README RHP Runtime Activation chart

## A - Artifacts

This folder contains the Hermes-local RHP protocol substrate:

| Artifact | Role |
|---|---|
| `origin_manifest.json` | Declares origin surfaces and surface hashes. |
| `latest_alignment_report.json` | Reports alignment and drift status. |
| `latest_origin_certificate.json` | Proposal-mode origin certificate. |
| `schemas/` | JSON schemas for RHP artifacts. |
| `ledger/rhp_rehydration_ledger.jsonl` | Append-only RHP event ledger. |
| `reports/` | Human-readable and machine-readable reports. |
| `evidence/` | RHP-local evidence package. |

Runtime adapter lives outside this folder:

```text
rhp_runtime_bridge.py
```

## T - Theory / Basis

RHP is based on the repository-origin alignment rule:

```text
The geometry must align before the output can compound.
```

Operationally:

```text
Hermes starts
→ /rhp origin manifest loads
→ RHP bridge validates origin surfaces
→ RHP context injects if HERMES_RHP_CONTEXT=proposal
→ HRCN context injects if HERMES_HRCN_CONTEXT=proposal
→ Hermes proposes only inside declared boundaries
```

RHP asks:

```text
Is this session aligned enough with repository origin to orient proposal work?
```

HRCN asks:

```text
What authority, if any, does this session have?
```

## I - Invariants

- RHP loads before HRCN when both context gates are enabled.
- RHP is orientation, not authority.
- RHP proposal-mode certificate does not permit compounding.
- RHP does not grant write authority.
- RHP does not grant tool authority.
- RHP does not grant provider/model authority.
- RHP does not grant CMS runtime execution.
- RHP does not grant CMS write authority.
- RHP does not grant memory write or memory promotion.
- RHP does not grant API-write authority.
- RHP does not grant dependency mutation.
- RHP does not grant Codex ingestion.
- RHP does not grant autonomy or self-authorization.
- Generated runtime Python must be compile-checked before pytest.
- Repair events must emit evidence and lessons.
- Evidence readers must distinguish missing fields from explicit `true` authority flags.
- Update this mini README if folder purpose, files, routes, validation commands, evidence surfaces, or claim boundaries change.

## E - Examples

Read this README before editing this folder.

Expected validation when this folder or RHP runtime surfaces change:

```powershell
python -m py_compile rhp_runtime_bridge.py agent/agent_init.py
python -m pytest -q -o addopts= tests/test_rhp_runtime_bridge.py tests/test_rhp_context_injection.py tests/test_rhp_hrcn_order.py tests/test_rhp_runtime_startup_smoke.py
git status --short
```

## Failure Lessons

| Lesson | Finding | Rule |
|---|---|---|
| RHP-L-001 | Generated Python source broke because escaped newline handling crossed PowerShell → Python → Python boundaries. | Any All-One that emits runtime Python must run `python -m py_compile` on emitted files before pytest. |
| RHP-L-002 | The first RHP-001 attempt failed before commit/push and then recovered with a repair script. | Failed bridge scripts must stop before commit/push and emit repair evidence. |
| RHP-L-003 | Adding `/rhp` created a new navigable surface. | Any new top-level folder must receive a full mini README and root README synchronization in the same version track. |
| RHP-L-004 | RHP-002 initially treated missing authority-false evidence fields as drift. | Evidence readers must distinguish missing fields from explicit `true`; only explicit `true` is dangerous authority drift, while missing false fields are normalized forward. |
| RHP-L-005 | RHP-004 aligned the runtime anchor while old tests still encoded the v0.2 contract, and the failed test output was committed. | Rehydration is orientation, not implementation coercion; version-anchor changes must migrate tests and hard-stop before commit when tests fail. |

## RCC Nexus Echo Location

Sphere Position:

- Shell: inner
- Meridian(s): rehydration, runtime, governance
- Sector: rhp
- Version / TTL: RHP-004 repair boundary / inherits RHP-001 substrate / 180 days
- Last Verified: 2026-06-08

Local Role:

- Hermes-local Rehydration Protocol substrate for origin manifest, alignment report, origin certificate, schemas, ledger, evidence, and reports.

Evidence Surface:

- `docs/context-layer/ops/RHP-001-final-evidence.json`
- `docs/context-layer/ops/RHP-002-final-evidence.json`
- `docs/context-layer/ops/RHP-003-final-evidence.json`
- `docs/context-layer/ops/RHP-004-final-evidence.json`
- `rhp/origin_manifest.json`
- `rhp/latest_alignment_report.json`
- `rhp/latest_origin_certificate.json`
- `rhp/ledger/rhp_rehydration_ledger.jsonl`
- `rhp/reports/rhp_alignment_report.md`

Validation Surface:

```powershell
python -m py_compile rhp_runtime_bridge.py agent/agent_init.py
python -m pytest -q -o addopts= tests/test_rhp_runtime_bridge.py tests/test_rhp_context_injection.py tests/test_rhp_hrcn_order.py tests/test_rhp_runtime_startup_smoke.py
git status --short
```

Claim Boundary:

- This mini README improves local navigation and agent orientation. It does not prove code correctness, patch safety, empirical validation, AI understanding, AGI, consciousness, production readiness, security, external validation, runtime authority, memory authority, or autonomous authority.

Non-Claim Locks:

- navigation_is_not_validation
- documentation_is_not_correctness
- context_reconstruction_is_not_code_quality
- validation_remains_required
- memory_is_not_consciousness
- rhp_context_is_not_runtime_authority
- rhp_certificate_is_not_write_permission
- agent_proposal_is_not_authority
- human_authorization_remains_write_boundary
- profile_adoption_is_not_validation
- rehydration_is_not_authority
- generated_code_requires_compile_check
- repair_evidence_is_required_after_failure
- folder_creation_requires_mini_readme
- missing_false_evidence_fields_are_not_authority
- rehydration_is_not_implementation_coercion
- failed_tests_are_commit_blockers

Agent Route:

- Read root `README.md`, `AGENTS.md`, `docs/context-layer/README.md`, HRCN context surfaces, `rhp_runtime_bridge.py`, then this README before editing `/rhp`.

Update Obligation:

- Update this README and the root README RHP Activation chart if folder purpose, hooks, evidence surfaces, validation commands, claim boundaries, or RHP stage status changes.

<!-- MINI_README_UPDATE_RULE_START -->
## AI Update Rule - Mini README and Directory Box Synchronization

This folder is part of the RHP/HRCN/RCC navigable repository surface.

When this folder's purpose, files, routes, evidence surfaces, validation commands, or claim boundaries change, update this mini README in the same commit. Also update the root README if any folder is added, removed, renamed, or repurposed.

Required after changes:

```powershell
python -m py_compile rhp_runtime_bridge.py agent/agent_init.py
python -m pytest -q -o addopts= tests/test_rhp_runtime_bridge.py tests/test_rhp_context_injection.py tests/test_rhp_hrcn_order.py tests/test_rhp_runtime_startup_smoke.py
git status --short
```

Non-claim lock: navigation is not validation, but stale navigation is repository drift.
<!-- MINI_README_UPDATE_RULE_END -->
<!-- HRCN_MINI_README_END -->
