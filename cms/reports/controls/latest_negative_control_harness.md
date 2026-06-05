# CMS-SA v0.3b4 Negative Control and Downgrade Harness

- schema: `CMS-SA-v0.3b4-negative-control-harness`
- version: `v0.3b4`
- passed: `True`
- control_count: `5`
- false_promote_rejected: `True`
- downgrade_preserved: `True`
- observe_only_preserved: `True`
- harness_hash: `839cfdcac84c7d6d703adc8751c00af308c47d1d49b071021448c14a57c8d1a9`

## Controls

| Control | Class | Expected | Observed | Passed |
|---|---|---:|---:|---:|
| `NC-001-positive-promote` | `positive_control` | `promote` | `promote` | `True` |
| `NC-002-required-validator-block` | `negative_control` | `block` | `block` | `True` |
| `NC-003-false-promote-rejected` | `false_promote_control` | `block` | `block` | `True` |
| `NC-004-downgrade-preserved` | `downgrade_control` | `downgrade` | `downgrade` | `True` |
| `NC-005-observe-only` | `observe_only_control` | `observe_only` | `observe_only` | `True` |

## Non-Claim Lock

Negative control validation is repository-bound and does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.
