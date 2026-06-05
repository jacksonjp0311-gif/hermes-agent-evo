# CMS-SA v0.2b3c Injection Record

## Injection

Root-anchored stable public-sync repair.

## Changed surfaces

- README checkpoint and lesson ledger
- public-sync validator
- version registry
- roadmap
- release seal
- lineage and injection ledgers
- public-sync reports

## Reason

v0.2b3b failed usefully because relative file writes escaped the repo root and the script was pasted line-by-line.

## Permanent rule

All large repair scripts must be run as files, and all writes must join paths against the repository root.