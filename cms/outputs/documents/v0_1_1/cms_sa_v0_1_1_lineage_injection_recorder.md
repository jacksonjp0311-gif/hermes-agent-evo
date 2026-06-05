# CODEX ΔΦ — CMS-SA v0.1.1
## Lineage and Injection Recorder Patch

### Purpose

CMS-SA v0.1.1 adds the missing governance surface: every version must be recorded
as a document or injection before it can be treated as part of the system.

### New Rule

```text
No version without a document.
No injection without a record.
No record without a ledger.
No release without a seal.
No seal without a next-anchor.
```

### What This Adds

1. `docs/versions/`
2. `docs/injections/`
3. `docs/release_seals/`
4. `outputs/version_registry/`
5. `outputs/lineage/`
6. `outputs/injections/`
7. `outputs/roadmap/`

### Version Recording Contract

Each version must define:

| Field | Meaning |
|---|---|
| version | semantic checkpoint |
| class | architecture / runtime / patch / injection / release |
| source | what it evolved from |
| document | canonical document path |
| injection | injection record path |
| validation | validation output path |
| release seal | release boundary |
| next anchor | next recommended move |

### Why This Matters

Without this layer, the system can run but forget why a version exists.
With this layer, every version becomes reconstructable.

### Non-Claim Lock

Lineage recording improves traceability. It does not prove truth, correctness,
external validation, consciousness, AGI, or provenance.