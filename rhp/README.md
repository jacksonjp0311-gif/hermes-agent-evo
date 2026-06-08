# Rehydration Protocol Substrate for Hermes

This folder is the Hermes-local Rehydration Protocol substrate.

It is not a standalone package yet. It is not Codex ingestion. It is not CMS write authority. It is not memory promotion. It is not autonomy.

## Purpose

RHP makes Hermes load declared repository origin surfaces before proposal-context work begins.

```text
Hermes starts
→ /rhp origin manifest loads
→ RHP bridge validates origin surfaces
→ RHP context injects if HERMES_RHP_CONTEXT=proposal
→ HRCN context injects if HERMES_HRCN_CONTEXT=proposal
→ Hermes proposes only inside declared boundaries
```

## Files

| File | Role |
|---|---|
| `origin_manifest.json` | Declares origin surfaces and surface hashes. |
| `latest_alignment_report.json` | Reports alignment/drift status. |
| `latest_origin_certificate.json` | Proposal-mode certificate. |
| `schemas/` | Minimal JSON schemas for RHP artifacts. |
| `ledger/rhp_rehydration_ledger.jsonl` | Append-only RHP event ledger. |
| `reports/` | Human-readable and machine-readable reports. |
| `evidence/` | RHP-local evidence package. |

## Boundary

RHP grants no write authority, no CMS authority, no memory promotion, no Codex ingestion, no API write, no provider/model authority, no tool authority, no autonomy, and no self-authorization.
