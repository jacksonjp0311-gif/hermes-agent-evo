# RHP-012.2 Compact CLI Gold Banner Rehydration Strip

RHP-012.2 binds the compact `$NOUS HERMES - AI Agent Framework` banner renderer in `cli.py` to the RHP Rehydration Protocol strip.

## Cause

RHP-012.1 correctly fixed the early boot stream, but the gold banner was rendered by `_build_compact_banner()` in `cli.py`, not by the Rich `hermes_cli/banner.py` path.

## Fix

`_build_compact_banner()` now reads:

- `HERMES_RHP_PROTOCOL_STRIP`
- `HERMES_RHP_PROTOCOL_LOCKS`

and appends those lines inside the compact gold box.

Boundary: compact banner display only. No provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.