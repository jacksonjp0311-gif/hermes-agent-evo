# HRCN v1.6 Limited Apply Executor

- passed: true
- previous validated anchor: HRCN v1.5
- current checkpoint: HRCN v1.6
- next recommended phase: HRCN v1.7 - Governed Operational Loop
- local executor tool created: true
- executor path: `scripts/hrcn/limited_apply_executor_v1_6.py`
- executor was run by this release: false
- automatic apply enabled: false
- self-authorization enabled: false
- apply authority granted: false

## Primary Law

```text
A limited apply executor may apply only an explicitly authorized docs/context packet; creating the executor does not grant use.
```

## Allowed Future Apply Scope

```text
README.md
docs/context-layer/**
```

## Non-Claim Lock

HRCN v1.6 creates a local limited apply executor tool for future human-authorized README.md and docs/context-layer/** packets only. The executor is not run by this release, does not self-authorize, does not touch Hermes runtime, does not touch cms/, does not change dependencies, does not call APIs, and does not grant apply authority merely by existing.
