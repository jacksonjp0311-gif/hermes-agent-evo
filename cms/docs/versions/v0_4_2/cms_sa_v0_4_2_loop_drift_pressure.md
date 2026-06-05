# CMS-SA v0.4.2 - Loop Drift Pressure Metrics

## Purpose

CMS-SA v0.4.2 adds loop drift pressure metrics: a bounded pressure layer that detects when a green loop may still be accumulating stale repository pressure.

## Metrics

- `loop_drift_pressure`
- `memory_action_drift`
- `rehydration_gap_count`
- `registry_status_drift`
- `public_surface_delta`
- `validator_expectation_drift`
- `non_claim_lock_drift`
- `report_surface_lag`

## Primary Lock

No green loop is considered stable if drift pressure exceeds the declared threshold without downgrade, warning, or repair recommendation.

## Non-Claim Lock

Loop drift pressure metrics are repository-bound and do not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.
