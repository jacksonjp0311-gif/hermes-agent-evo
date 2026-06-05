# HRCN Roadmap

## Current

HRCN v1.1 - Bounded CMS Context Packet

## Phase Map

| Phase | Name | Boundary |
|---|---|---|
| HRCN v1.0 | Governed Hermes-CMS Nexus Planning | Nexus planning only; no CMS copy, adapter, runtime mutation, or write authority. |
| HRCN v1.0.1 | CMS Read-Only Mirror Import Authorization Path | Authorization path only; no CMS copy. |
| HRCN v1.0.2 | CMS Mirror Preflight Manifest and Secret-Scan Plan | Manifest and secret scan before copy. |
| HRCN v1.0.3 | CMS Read-Only Mirror Copy With Evidence Package | CMS copied under `cms/` as read-only context/evidence only. |
| HRCN v1.1 | Bounded CMS Context Packet | Bounded read-only packet from CMS mirror into Hermes context; no loader or authority. |
| HRCN v1.2 | Permission Bridge Dry-Run Design | Future adapter/dry-run design only. |
| HRCN v1.3 | CMS-Hermes Read-Only Bridge Prototype | Future prototype; no write authority by default. |
| HRCN v1.4 | Dry-Run Execution Harness | Future simulation harness; no apply. |
| HRCN v1.5 | Apply-Gate Contract | Future apply gate contract; human authorization and rollback required. |
| HRCN v1.6 | Limited Apply Executor | Future bounded reversible docs/context executor only after apply gate. |
| HRCN v1.7 | Governed Operational Loop | Future observe/propose/dry-run/evidence/authorize/apply/validate/ledger loop. |
| HRCN v2.0 | Operational Hermes-CMS Nexus | Future operational nexus only after all prior gates validate. |

## Next Anchor

HRCN v1.2 - Permission Bridge Dry-Run Design.

## Current CMS Boundary

CMS exists under `cms/` as a read-only mirror snapshot. HRCN v1.1 adds a bounded CMS context packet that Hermes may read for orientation/evidence only. It is not runtime integration, not CMS authority, not memory write authority, not API authority, and not apply authority.

## Non-Claim Lock

HRCN v1.1 compresses selected CMS mirror surfaces into a bounded read-only context packet. It does not wire CMS into Hermes runtime, does not create a loader, adapter, writer, dry-run executor, apply executor, benchmark executor, repair executor, API writer, live integration, or apply authority. The packet is orientation and evidence only; permissions and human authorization remain external gates.
