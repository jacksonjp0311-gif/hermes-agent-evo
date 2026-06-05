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
