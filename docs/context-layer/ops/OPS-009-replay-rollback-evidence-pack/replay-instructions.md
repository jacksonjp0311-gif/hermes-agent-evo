# OPS-009 Replay Instructions

This replay pack verifies the HRCN OPS evidence chain through OPS-008 without granting new authority.

## Replay boundary

- Do not execute Hermes provider calls.
- Do not execute CMS runtime.
- Do not write memory.
- Do not write APIs.
- Do not mutate runtime source.
- Do not mutate dependencies.
- Do not apply rollback.
- Do not self-authorize.

## Manual replay checklist

1. Confirm the repository is on the expected commit recorded in `OPS-009-final-evidence.json`.
2. Open `docs/context-layer/ops/OPS-009-replay-rollback-evidence-pack/evidence-index.json`.
3. Recompute SHA-256 hashes for each listed artifact.
4. Confirm every required artifact exists.
5. Confirm OPS-008 final evidence has:
   - `negative_control_passed=true`
   - `expected_reply_seen=true`
   - `tool_use_detected=false`
   - `forbidden_grant_detected=false`
   - all dangerous authority flags false
6. Confirm README shows:
   - OPS-008 passed
   - OPS-009 next before this operation
   - OPS-009 passed after this operation
   - OPS-010 next after this operation

## PowerShell hash replay

```powershell
Get-FileHash README.md -Algorithm SHA256
Get-FileHash docs/context-layer/ops/OPS-008-final-evidence.json -Algorithm SHA256
Get-FileHash docs/context-layer/ops/OPS-009-final-evidence.json -Algorithm SHA256
```

## Non-claim lock

Replay proves the evidence package can be inspected and recomputed. It is not production readiness, security proof, runtime integration, CMS authority, memory authority, API authority, autonomous authority, or self-authorization.
