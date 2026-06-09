# Context Layer

Status: documentation-only.

This directory contains diagnostic context-layer notes for Hermes Agent.

These files do not change Hermes runtime behavior.

| Surface | Status |
|---|---|
| RHP docs | present |
| HRCN docs | present |
| Rehydration checklist | present |
| RHP runtime bridge | absent |
| HRCN runtime bridge | absent |
| Runtime wiring | absent |
| Default behavior change | none |

## Files

- `RHP.md` — Repository / Runtime Rehydration Protocol notes.
- `HRCN.md` — Hermes Rehydration Context Notes.
- `REHYDRATION_PROTOCOL.md` — read-only rehydration checklist.

## Boundary

This directory is diagnostic only.

It does not:

- add imports
- register CLI commands
- register tools
- alter prompt construction
- alter memory behavior
- mutate configuration
- call external APIs
- grant autonomous authority
