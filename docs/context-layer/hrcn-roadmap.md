# HRCN Roadmap

## Current

HRCN v1.0.3 - CMS Read-Only Mirror Copy With Evidence Package

## Phase Map

| Phase | Name | Boundary |
|---|---|---|
| HRCN v1.0 | Governed Hermes-CMS Nexus Planning | Nexus planning only; no CMS copy, adapter, runtime mutation, or write authority. |
| HRCN v1.0.1 | CMS Read-Only Mirror Import Authorization Path | Authorization path only; no CMS copy. |
| HRCN v1.0.2 | CMS Mirror Preflight Manifest and Secret-Scan Plan | Manifest and secret scan before copy. |
| HRCN v1.0.3 | CMS Read-Only Mirror Copy With Evidence Package | CMS copied under `cms/` as read-only context/evidence only. |
| HRCN v1.1 | Bounded CMS Context Packet | Future bounded read-only packet from CMS mirror into Hermes context. |
| HRCN v1.2 | Permission Bridge Dry-Run Design | Future adapter/dry-run design only. |
| HRCN v1.3 | CMS-Hermes Read-Only Bridge Prototype | Future prototype; no write authority by default. |

## Next Anchor

HRCN v1.1 - Bounded CMS Context Packet.

## Current CMS Boundary

CMS now exists under `cms/` as a read-only mirror snapshot. It is not runtime integration, not CMS authority, not memory write authority, not API authority, and not apply authority.

## Rollback

```powershell
Remove-Item -Recurse -Force .\cms
```

## Non-Claim Lock

HRCN v1.0.3 copies CMS as a read-only mirror evidence snapshot under cms/. It does not wire CMS into Hermes runtime, does not create a loader, adapter, writer, dry-run executor, apply executor, benchmark executor, repair executor, API writer, live integration, or apply authority. The cms/ mirror is context and evidence only until later explicitly authorized bridge phases.
