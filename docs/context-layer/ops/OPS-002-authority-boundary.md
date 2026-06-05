# OPS-002 Authority Boundary

OPS-002 does not widen authority.

Allowed:

- docs/context-layer/ops/**
- docs/context-layer/hrcn-v1.6-apply-ledger/**
- docs/context-layer/hrcn-v1.7-operational-ledger/**
- docs/context-layer/hrcn-v1.8-replay-ledger/**
- docs/context-layer/hrcn-v1.9-operator-packets/**
- docs/context-layer/hrcn-v2.0-nexus-reports/**

Blocked:

- Hermes runtime mutation
- cms/ write
- memory write
- API write
- dependency mutation
- autonomous authority
- self-authorization

Primary lock: operational cadence makes the governed path repeatable; it does not become permission.
