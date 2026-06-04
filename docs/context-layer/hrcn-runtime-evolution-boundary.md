# HRCN v0.1.4 - Runtime Evolution Boundary

Status: docs/context planning layer only.

## Purpose

This document clarifies the difference between current runtime safety and future runtime evolution.

## Current Boundary

```text
HRCN v0.1.4 does not modify Hermes runtime behavior.
```

Blocked now:

```text
run_agent.py
cli.py
model_tools.py
toolsets.py
agent/
tools/
skills/
optional-skills/
plugins/
providers/
gateway/
tui_gateway/
ui-tui/
web/
hermes_cli/
cron/
acp_adapter/
apps/
pyproject.toml
uv.lock
setup.py
package.json
package-lock.json
```

## Future Boundary

Future runtime changes are allowed only after:

1. read-only surface map
2. rehydration packet contract
3. CMS read-only bridge design
4. proposal classification
5. dry-run design
6. rollback coverage
7. validation evidence
8. explicit human authorization

## Main Lock

```text
No runtime mutation before route map, evidence boundary, dry-run path,
rollback plan, validation, and explicit human authorization.
```

## Non-Claim Lock

HRCN v0.1.4 is a docs/context planning and boundary layer. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
