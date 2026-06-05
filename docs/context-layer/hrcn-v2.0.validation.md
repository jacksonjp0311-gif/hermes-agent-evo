# HRCN v2.0 Validation

- passed: true
- checkpoint: Operational Hermes-CMS Nexus
- previous validated anchor: HRCN v1.9
- operational nexus sealed: true
- status tool created: true
- status tool path: `scripts/hrcn/operational_nexus_status_v2_0.py`
- v1.9 operator dependency verified: true
- v1.8 replay dependency verified: true
- v1.7 loop dependency verified: true
- v1.6 limited apply dependency verified: true
- operational for docs/context governance: true
- operational scope: `README.md`, `docs/context-layer/**`
- human operator required: true
- runtime integration enabled: false
- CMS write authority granted: false
- memory write authority granted: false
- API write authority granted: false
- apply authority granted: false
- apply executed: false
- automatic apply enabled: false
- automatic rollback enabled: false
- self authorization enabled: false
- autonomous authority granted: false
- roadmap current: HRCN v2.0
- roadmap next: HRCN v2.1

## Primary Law

```text
Operational does not mean autonomous; operational means the full governed path is visible, bounded, auditable, and human-gated.
```

## Non-Claim Lock

HRCN v2.0 seals Hermes-CMS as operational only for bounded docs/context governance. The operational nexus can report status across the CMS mirror/context packet, permission bridge, read-only bridge, dry-run contract, apply gate, limited apply executor, governed loop, replay/rollback hardening, and operator surface. It does not grant runtime mutation, CMS write authority, memory write authority, API authority, dependency mutation, autonomous authority, or self-authorization.
