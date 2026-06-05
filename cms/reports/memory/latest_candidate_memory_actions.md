# CMS-SA v0.4.1 Candidate Memory Actions

- passed: `True`
- candidate_action_count: `4`
- action_hash: `9966f1fb234ff5b6aebeadcf9331d27bcc40456ddd536870c20ba330bb1ead56`

## Actions

- `CMS-MEM-001-runtime-decision-kernel` -> `promote_memory` / `may_influence_next_cycle_after_rehydration_scan`
- `CMS-MEM-002-negative-control-refusal` -> `promote_memory` / `may_influence_next_cycle_after_rehydration_scan`
- `CMS-MEM-003-paste-safe-execution` -> `downgrade_memory` / `remain_visible_as_downgraded_boundary`
- `CMS-MEM-004-incomplete-external-correlation` -> `observe_only` / `hold_for_future_evidence_recheck`

## Primary Lock

No promoted memory may influence the next cycle without a typed candidate-level action, downgrade boundary, evidence requirement, and rehydration-visible status.

## Non-Claim Lock

Candidate memory actions are repository-bound and do not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.
