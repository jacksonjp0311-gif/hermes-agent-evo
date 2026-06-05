# CODEX DeltaPhi — CMS-SA v0.2b2
## README Render Hygiene and Badge Status Guard

### Purpose

CMS-SA v0.2b2 repairs the public README rendering and makes badge/status refresh
part of the permanent checkpoint discipline.

### Failure Observed

v0.2b1 passed anchor and directory validators, but the public README could still
contain render corruption such as damaged paths, malformed code fences, escaped
control-character residue, and unresolved literal variables.

### Repair

v0.2b2 adds:

1. Clean ASCII-safe README rewrite.
2. Updated current-status badges.
3. Current Public Metrics refresh.
4. README render hygiene validator.
5. Badge/status guard.
6. Render hygiene report surface.
7. Updated process rule requiring badge/status refresh every checkpoint.

### Operating Law

```text
Anchor correctness is not render correctness.
Directory correctness is not public readability.
Badge/status correctness must update every time.
```

### Non-Claim Lock

README render hygiene and badges improve traceability. They do not prove code
correctness, truth, AGI, consciousness, production readiness, security, or
external validation.