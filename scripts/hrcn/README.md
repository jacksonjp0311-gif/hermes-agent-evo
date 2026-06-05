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

