# HRCN Scripts

This folder contains local HRCN governance tooling for this fork.

## HRCN v1.6 Limited Apply Executor

`limited_apply_executor_v1_6.py` is a bounded local executor tool. It is not Hermes runtime integration.

Allowed future apply scope:

```text
README.md
docs/context-layer/**
```

Blocked future apply scope:

```text
cms/**
agent/**
tools/**
skills/**
plugins/**
providers/**
gateway/**
hermes_cli/**
tui_gateway/**
ui-tui/**
web/**
dependency files
local secrets
external APIs
```

Non-claim lock: the tool existing in `scripts/hrcn/` does not grant permission to run it.

## HRCN v1.7 Governed Operational Loop

`governed_operational_loop_v1_7.py` coordinates the bounded operational loop:

```text
observe -> propose -> classify -> dry-run -> evidence -> authorize -> limited apply -> validate -> ledger
```

It validates an HRCN-v1.7 operation packet and may write a docs/context ledger status. It does not apply changes by itself and does not widen the v1.6 executor scope.

## HRCN v1.8 Replay and Rollback Hardening

`replay_rollback_hardening_v1_8.py` validates replay/rollback manifests for governed docs/context operations.

It checks:

```text
expected base commit
operation hashes
allowed scope
limited apply audit ref
rollback packet ref
post-apply validation ref
automatic rollback disabled
self-authorization disabled
```

It does not automatically rollback and does not widen the v1.6/v1.7 scope.

## HRCN v1.9 Operator Dashboard / Command Surface

`operator_command_surface_v1_9.py` is the human-facing local command surface.

Commands:

```text
--status
--gates
--next-commands
--make-packet-template --summary "..." --target README.md
```

It can create packet templates under `docs/context-layer/hrcn-v1.9-operator-packets/`.
It does not apply changes, rollback changes, call APIs, self-authorize, or widen scope.

## HRCN v2.0 Operational Nexus Status

`operational_nexus_status_v2_0.py` reports whether the bounded Hermes-CMS governance stack is operational for docs/context governance.

Commands:

```text
python scripts/hrcn/operational_nexus_status_v2_0.py --status
python scripts/hrcn/operational_nexus_status_v2_0.py --write-report
```

It does not apply changes, rollback changes, call APIs, self-authorize, or widen scope.

