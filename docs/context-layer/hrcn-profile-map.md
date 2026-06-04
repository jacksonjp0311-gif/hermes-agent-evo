# HRCN v0.1.3 Profile Map

HRCN v0.1.3 compresses mini README governance into profiles so RCC improves navigation without turning every folder into a heavy governance document.

## Profiles

| Profile | Purpose | Folders |
|---|---|---|
| `full` | Full SHATIE/RCC mini README. Use for load-bearing runtime, tool, provider, UI, validation, or governance surfaces. | `agent, tools, skills, plugins, providers, gateway, hermes_cli, tui_gateway, ui-tui, web, scripts, tests, docs/context-layer` |
| `compact` | Compact mini README. Use for important but lower-risk docs/integration/support surfaces. | `optional-skills, cron, acp_adapter, apps, docs, website` |
| `pointer` | Pointer-only mini README. Use for planning or asset surfaces where full governance would add overhead. | `assets, plans, .plans` |

## Lock

```text
Use the lightest sufficient governance profile.
Do not over-govern simple repositories.
Do not under-govern high-risk repositories.
Profile adoption is not validation.
```

## Non-Claim Lock

HRCN v0.1.3 is a docs/context/navigation coherence and compression layer. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
