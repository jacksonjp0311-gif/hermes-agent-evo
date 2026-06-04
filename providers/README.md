# providers/

Registry and ABC for every inference provider Hermes knows about.

Each provider is declared once as a `ProviderProfile`. Every other layer —
auth resolution, transport kwargs, model listing, runtime routing — reads from
these profiles instead of maintaining its own parallel data.

---

## Layout

```
providers/
├── base.py         ProviderProfile dataclass + OMIT_TEMPERATURE sentinel
├── __init__.py     Registry: register_provider(), get_provider_profile(), list_providers()
└── README.md       This file
```

The **profiles themselves** live as plugins under
`plugins/model-providers/<name>/` (bundled in this repo) and
`$HERMES_HOME/plugins/model-providers/<name>/` (per-user overrides). The
registry in `providers/__init__.py` lazily discovers them the first time any
consumer calls `get_provider_profile()` or `list_providers()`. See
`plugins/model-providers/README.md` for the plugin contract and examples.

---

## How it wires in

The registry is populated on first access. After that, every downstream
layer reads from it:

- `hermes_cli/auth.py` extends `PROVIDER_REGISTRY` with every api-key
  profile it sees (skipping `copilot`, `kimi-coding`, `kimi-coding-cn`,
  `zai`, `openrouter`, `custom` — those need bespoke token resolution).
- `hermes_cli/models.py` extends `CANONICAL_PROVIDERS` and calls
  `profile.fetch_models()` inside `provider_model_ids()`.
- `hermes_cli/doctor.py` adds a `/models` health check for each
  `auth_type="api_key"` profile.
- `hermes_cli/config.py` injects every `env_var` into
  `OPTIONAL_ENV_VARS` so the setup wizard knows about it.
- `hermes_cli/runtime_provider.py` reads `profile.api_mode` as a fallback
  when URL detection finds nothing.
- `agent/model_metadata.py` maps hostname → provider via
  `profile.get_hostname()`.
- `agent/auxiliary_client.py` reads `profile.default_aux_model` first
  before falling back to the legacy hardcoded dict.
- `agent/transports/chat_completions.py::_build_kwargs_from_profile()`
  invokes `profile.prepare_messages()`, `profile.build_extra_body()`,
  and `profile.build_api_kwargs_extras()` on every call.
- `run_agent.py` passes `provider_profile=<ProviderProfile>` so the
  transport takes the profile path instead of the legacy flag path.

---

## Adding a provider

See `plugins/model-providers/README.md` — drop a new directory there (or
under `$HERMES_HOME/plugins/model-providers/` for a private plugin).

---

## Hooks you can override on `ProviderProfile`

| Hook | Purpose |
|------|---------|
| `get_hostname()` | URL-based detection — default derives from `base_url`. |
| `prepare_messages(msgs)` | Provider-specific message preprocessing (Qwen normalises to list-of-parts, injects `cache_control`). |
| `build_extra_body(**ctx)` | Provider-specific `extra_body` (OpenRouter provider prefs, Gemini `thinking_config`). |
| `build_api_kwargs_extras(**ctx)` | `(extra_body_additions, top_level_kwargs)` — Kimi puts reasoning_effort top-level, Qwen splits `enable_thinking`/`thinking_budget`. |
| `fetch_models(*, api_key)` | Live catalog fetch — default hits `{models_url or base_url}/models` with Bearer auth. Override for no-REST providers (Bedrock), OAuth catalogs (Anthropic), or public catalogs (OpenRouter). |

---

## Configuration fields

Full reference in `providers/base.py` dataclass definition.

<!-- HRCN_MINI_README_START -->
# providers

## Folder Purpose

Provider abstractions and routing surfaces.

## S - Specification

This folder participates in the Hermes repository according to its local role. Under HRCN v0.1.3, this README is a navigation and context surface only.

Profile: `full`

## H - Hooks

Inbound hooks:

- `README.md`
- `AGENTS.md`
- `docs/context-layer/rcc-cms-hrcn.md`
- `docs/context-layer/hermes-agent-rehydration-protocol.md`
- `docs/context-layer/hrcn-profile-map.json`

Outbound hooks:

- local validation or test surfaces when this folder is changed in a future authorized phase
- HRCN validation report when this folder participates in documentation/navigation checks

## A - Artifacts

This folder may contain source files, docs, reports, schemas, scripts, UI assets, tests, tools, skills, plugins, providers, or generated support files depending on its role.

## T - Theory / Basis

Governed by HRCN v0.1.3, RCC repository orientation, CMS permission discipline, RCC-N profile-gated governance, and Hermes upstream development boundaries.

## I - Invariants

- Preserve upstream Hermes behavior unless a future phase explicitly authorizes runtime work.
- Preserve source attribution to Nous Research and upstream Hermes where applicable.
- Do not treat navigation as validation.
- Do not treat documentation as correctness.
- Do not claim AGI, consciousness, sentience, autonomy, self-awareness, security, production readiness, or external validation.
- Do not introduce secrets, API keys, local config, `.venv`, AppData files, session logs, or machine-local state.
- Run the rehydration protocol before proposing runtime changes.
- Update this mini README if folder purpose, files, routes, validation commands, or claim boundaries change.

## E - Examples

Read this README before editing this folder.

For HRCN v0.1.3 docs-only work, expected validation is:

```powershell
git status --short
```

## RCC Nexus Echo Location

Sphere Position:

- Shell: middle
- Meridian(s): provider
- Sector: runtime
- Version / TTL: HRCN-v0.1.3 / 180 days
- Last Verified: 2026-06-04

Local Role:

- Provider abstractions and routing surfaces.

Evidence Surface:

- `docs/context-layer/hrcn-v0.1.3.validation.json`

Validation Surface:

```powershell
git status --short
```

Claim Boundary:

- This mini README improves local navigation and agent orientation. It does not prove code correctness, patch safety, empirical validation, AI understanding, AGI, consciousness, production readiness, security, or external validation.

Non-Claim Locks:

- navigation_is_not_validation
- documentation_is_not_correctness
- context_reconstruction_is_not_code_quality
- validation_remains_required
- memory_is_not_consciousness
- hermes_context_is_not_runtime_integration
- agent_proposal_is_not_authority
- human_authorization_remains_write_boundary
- profile_adoption_is_not_validation
- rehydration_is_not_authority

Agent Route:

- Read root `README.md`, `AGENTS.md`, `docs/context-layer/README.md`, `docs/context-layer/rcc-cms-hrcn.md`, `docs/context-layer/hermes-agent-rehydration-protocol.md`, then this README before editing.

Update Obligation:

- Update this README and the root HRCN README block if folder purpose, hooks, evidence surfaces, validation commands, or claim boundaries change.

<!-- MINI_README_UPDATE_RULE_START -->
## AI Update Rule - Mini README and Directory Box Synchronization

This folder is part of the HRCN/RCC navigable repository surface.

When this folder's purpose, files, routes, evidence surfaces, validation commands, or claim boundaries change, update this mini README in the same commit. Also update the root README if any folder is added, removed, renamed, or repurposed.

Required after changes:

```powershell
git status --short
```

Non-claim lock: navigation is not validation, but stale navigation is repository drift.
<!-- MINI_README_UPDATE_RULE_END -->
<!-- HRCN_MINI_README_END -->
