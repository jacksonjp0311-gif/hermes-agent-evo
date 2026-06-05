# HRCN v2.0 Operational Hermes-CMS Nexus

- passed: true
- previous validated anchor: HRCN v1.9
- current checkpoint: HRCN v2.0
- next recommended phase: HRCN v2.1 - Runtime Adapter Readiness Boundary
- operational nexus sealed: true
- status tool path: `scripts/hrcn/operational_nexus_status_v2_0.py`
- operational for docs/context governance: true
- operational scope: `README.md`, `docs/context-layer/**`
- human operator required: true
- runtime integration enabled: false
- CMS write authority granted: false
- memory write authority granted: false
- API write authority granted: false
- self-authorization enabled: false
- autonomous authority granted: false

## Primary Law

```text
Operational does not mean autonomous; operational means the full governed path is visible, bounded, auditable, and human-gated.
```

## Operational Chain

```text
CMS mirror/context
bounded CMS packet
permission bridge
read-only bridge
dry-run contract
apply gate
limited apply executor
governed operational loop
replay/rollback hardening
operator command surface
```

## Non-Claim Lock

HRCN v2.0 seals Hermes-CMS as operational only for bounded docs/context governance. The operational nexus can report status across the CMS mirror/context packet, permission bridge, read-only bridge, dry-run contract, apply gate, limited apply executor, governed loop, replay/rollback hardening, and operator surface. It does not grant runtime mutation, CMS write authority, memory write authority, API authority, dependency mutation, autonomous authority, or self-authorization.
