# RHP-014.2 Stream Collapse + Tool Candidate Matrix

- operation: RHP-014.2
- timestamp UTC: 2026-06-11T00:00:47.601169+00:00
- base commit: `410451dbf30dfd7ff34ccbf7a2ab4ed7b9427a2c`
- operator script name: `RHP_014_2_STREAM_COLLAPSE_TOOL_CANDIDATE_MATRIX_SINGLE_ALL_ONE.ps1`
- stream collapse added: true
- tool candidate matrix added: true
- grey streams minimized by default: true
- focused tests passed: true
- focused test mode: `pytest`
- next: RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run

## Boundary

RHP-014.2 adds stream display compression and tool candidate matrix only. It does not execute autoheal, mutate CI remotely, grant runtime authority, call providers/models/tools, write CMS/memory/API state, perform external ingestion, grant autonomy, or self-authorize.
