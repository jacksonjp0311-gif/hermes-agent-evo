# HRCN v1.1 Bounded CMS Context Packet

- passed: true
- mode: bounded read-only context packet
- previous validated anchor: HRCN v1.0.3
- source mirror: `cms/`
- packet read file count: 58
- packet total bytes: 170447
- CMS mirror total files: 714
- CMS mirror total bytes: 3595722
- next recommended phase: HRCN v1.2 - Permission Bridge Dry-Run Design

## Primary Law

```text
A bounded CMS context packet orients Hermes; it does not authorize Hermes.
```

## What Hermes May Do

```text
read the bounded packet
use it for orientation
use it for route selection
use it for evidence-bounded summaries
```

## What Hermes May Not Do

```text
import cms/src as runtime
execute cms/scripts
treat CMS outputs as permission grants
write CMS memory
write APIs
apply repairs
create adapters or loaders
mutate runtime
```

## Bounded Read Set

| Path | Role | Class |
|---|---|---|
| `cms/MIRROR_READONLY_BOUNDARY.md` | mirror boundary and blocked-authority law | `boundary` |
| `cms/.hrcn-read-only-mirror.json` | machine-readable mirror marker | `boundary` |
| `cms/README.md` | CMS public orientation | `orientation` |
| `cms/README_90_SECONDS.md` | short CMS operator orientation | `orientation` |
| `cms/AGENTS.md` | CMS agent-facing operating rules | `orientation` |
| `cms/docs/context/THREAD_REHYDRATION_PROTOCOL.md` | CMS rehydration protocol | `rehydration` |
| `cms/docs/context/repository_context_index.json` | CMS context index | `index` |
| `cms/docs/context/rcc_nexus_index.json` | RCC nexus index | `index` |
| `cms/docs/context/validation_surface.md` | CMS validation surface summary | `evidence` |
| `cms/docs/roadmap/CMS_ROADMAP.md` | CMS roadmap | `roadmap` |
| `cms/docs/versions/VERSION_REGISTRY.md` | CMS version registry | `lineage` |
| `cms/outputs/cms/hermes_cms_context.json` | Hermes-facing CMS context packet from CMS source | `orientation` |
| `cms/outputs/agent_governance/latest_rcc_cms_orientation_packet.json` | RCC/CMS orientation packet | `orientation` |
| `cms/outputs/agent_governance/latest_agent_governance_kernel_bundle.json` | agent governance kernel bundle | `governance` |
| `cms/outputs/evidence/latest_evidence_package.json` | latest CMS evidence package | `evidence` |
| `cms/outputs/memory/latest_candidate_memory_actions.json` | candidate memory action output | `memory` |
| `cms/outputs/decision/latest_runtime_decision.json` | latest CMS runtime decision artifact | `decision` |
| `cms/outputs/loop/latest_authorized_repair_dry_run.json` | authorized repair dry-run evidence | `dry_run` |
| `cms/outputs/loop/latest_authorized_repair_apply_gate.json` | authorized repair apply-gate evidence | `apply_gate` |
| `cms/outputs/loop/latest_authorized_apply_packet_diff_manifest.json` | apply packet diff manifest | `apply_gate` |
| `cms/outputs/loop/latest_authorized_dry_apply_sandbox.json` | dry apply sandbox evidence | `dry_run` |
| `cms/outputs/state/latest_cms_state.json` | latest CMS state summary | `state` |
| `cms/configs/alignment/multilevel_alignment_contract.json` | CMS configuration contract | `contract` |
| `cms/configs/cms_default.json` | CMS configuration contract | `contract` |
| `cms/configs/controls/negative_control_contract.json` | CMS configuration contract | `contract` |
| `cms/configs/decision/runtime_decision_contract.json` | CMS configuration contract | `contract` |
| `cms/configs/feedback/feedback_lifecycle_contract.json` | CMS configuration contract | `contract` |
| `cms/configs/geometry/reflective_git_geometry_contract.json` | CMS configuration contract | `contract` |
| `cms/configs/loop/cybernetic_memory_loop_contract.json` | CMS configuration contract | `contract` |
| `cms/configs/loop/loop_drift_pressure_contract_v0_4_2.json` | CMS configuration contract | `contract` |
| `cms/configs/loop/loop_repair_recommendation_contract_v0_4_3.json` | CMS configuration contract | `contract` |
| `cms/configs/memory/candidate_action_contract_v0_4_1.json` | CMS configuration contract | `contract` |
| `cms/configs/memory/promotion_contract.json` | CMS configuration contract | `contract` |
| `cms/configs/metrics/cms_metric_contracts_v0_2.json` | CMS configuration contract | `contract` |
| `cms/configs/profiles/cms_core.json` | CMS configuration contract | `contract` |
| `cms/configs/profiles/cms_full.json` | CMS configuration contract | `contract` |
| `cms/configs/profiles/cms_lite.json` | CMS configuration contract | `contract` |
| `cms/configs/profiles/cms_research.json` | CMS configuration contract | `contract` |
| `cms/configs/rehydration/thread_rehydration_contract.json` | CMS configuration contract | `contract` |
| `cms/configs/rehydration/thread_rehydration_score_contract_v0_4_1.json` | CMS configuration contract | `contract` |
| `cms/configs/seeds/baseline_utility_seed.json` | CMS configuration contract | `contract` |
| `cms/configs/seeds/cms_lite_self_audit_seed.json` | CMS configuration contract | `contract` |
| `cms/configs/seeds/feedback_lifecycle_seed.json` | CMS configuration contract | `contract` |
| `cms/configs/seeds/memory_promotion_seed.json` | CMS configuration contract | `contract` |
| `cms/configs/seeds/public_surface_drift_seed.json` | CMS configuration contract | `contract` |
| `cms/configs/seeds/readme_rcc_drift_seed.json` | CMS configuration contract | `contract` |
| `cms/schemas/agent_governance_context.schema.json` | CMS schema contract | `schema` |
| `cms/schemas/authorized_apply_packet_diff_manifest.schema.json` | CMS schema contract | `schema` |
| `cms/schemas/authorized_dry_apply_sandbox.schema.json` | CMS schema contract | `schema` |
| `cms/schemas/authorized_repair_apply_gate.schema.json` | CMS schema contract | `schema` |
| `cms/schemas/authorized_repair_dry_run.schema.json` | CMS schema contract | `schema` |
| `cms/schemas/candidate_memory_action.schema.json` | CMS schema contract | `schema` |
| `cms/schemas/feedback_item.schema.json` | CMS schema contract | `schema` |
| `cms/schemas/loop_drift_pressure.schema.json` | CMS schema contract | `schema` |
| `cms/schemas/loop_repair_recommendation.schema.json` | CMS schema contract | `schema` |
| `cms/schemas/reflective_git_node.schema.json` | CMS schema contract | `schema` |
| `cms/schemas/repair_closure_plan.schema.json` | CMS schema contract | `schema` |
| `cms/schemas/thread_rehydration_scan.schema.json` | CMS schema contract | `schema` |


## Blocked Runtime Roots

```text
cms/src/
cms/scripts/
cms/tests/
```

## Non-Claim Lock

HRCN v1.1 compresses selected CMS mirror surfaces into a bounded read-only context packet. It does not wire CMS into Hermes runtime, does not create a loader, adapter, writer, dry-run executor, apply executor, benchmark executor, repair executor, API writer, live integration, or apply authority. The packet is orientation and evidence only; permissions and human authorization remain external gates.
