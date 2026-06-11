# RHP Operator Quickstart

Schema: `RHP-OPERATOR-QUICKSTART-v0.1`

Latest operation: `RHP-015.2`
Latest evidence: `docs/context-layer/ops/RHP-015-2-final-evidence.json`
Next operation: `RHP-015.3 README operator quickstart and CI green reconciliation`

## Read order

1. `docs/context-layer/latest-rhp.json`
2. `docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md`
3. `docs/context-layer/operator-dashboard.txt`
4. `docs/context-layer/hermes-operator-context.json`
5. `AGENTS.md`
6. `README.md`
7. `rhp/README.md`

## Output grammar

- `RHPLOAD`: major gate/audit box
- `RHPWAIT`: single-line fill/loading surface
- `RHPDROP`: closed compact summary for repetitive command groups
- `RHPDIAG`: runtime diagnosis/failure box

## Authority rules

- Hermes/RHP never self-authorizes.
- All mutation requires one human-authorized All-One script.
- Unknown dirty paths block.
- Autoheal remains dry-run/proposal-only unless a later human-authorized operation changes the contract.
- Remote CI is the integration truth surface; local validation is a bounded proof surface.

## Run pattern

```powershell
cd "$env:USERPROFILE\Downloads"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\<NEXT_ALL_ONE>.ps1
```

Non-claim lock: Quickstart is orientation only. It does not mutate files, execute repairs, call remote APIs, rerun CI, or grant authority.
