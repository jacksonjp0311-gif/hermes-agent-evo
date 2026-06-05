# OPS-002 Authority Boundary

OPS-002 and OPS-002.1 do not widen authority.

Allowed surfaces:

- docs/context-layer/ops/**
- docs/context-layer/hrcn-v1.6-apply-ledger/**
- docs/context-layer/hrcn-v1.7-operational-ledger/**
- docs/context-layer/hrcn-v1.8-replay-ledger/**
- docs/context-layer/hrcn-v2.0-nexus-reports/**

Blocked surfaces:

- Hermes runtime mutation
- cms/ write
- memory write
- API write
- dependency mutation
- autonomous authority
- self-authorization

Primary lock: cadence is repeatability, not permission.