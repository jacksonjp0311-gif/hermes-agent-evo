# HRCN v0.2 - Hermes Surface Boundary Map

Status: read-only repository surface map.

## Purpose

HRCN v0.2 converts the HRCN profile/orientation layer into a machine-readable boundary map before any CMS root intake or runtime integration.

## Primary Lock

```text
HRCN v0.2 maps Hermes surfaces but may not mutate runtime, dependencies,
tools, skills, providers, gateways, UI, web, CMS, or package state.
```

## Summary

| Metric | Value |
|---|---:|
| Total mapped surfaces | `34` |
| Existing surfaces | `33` |
| Blocked/planned in v0.2 | `30` |
| v0.2 writable surfaces | `README.md, docs/context-layer` |

## Surface Table

| Surface | Kind | Profile | Authority | Risk | v0.2 permission | Exists |
|---|---|---|---|---|---|---|
| `.plans` | `documentation_or_planning_folder` | `pointer` | `planning_doc` | `low` | `blocked_except_authorized_plan` | `true` |
| `AGENTS.md` | `agent_instruction` | `full` | `read_only_context` | `high_if_changed` | `read_only_in_v0.2` | `true` |
| `README.md` | `root_doc` | `full` | `docs_only` | `none` | `editable_in_v0.2` | `true` |
| `acp_adapter` | `runtime_or_integration_folder` | `compact` | `runtime_apply_write` | `high` | `blocked_in_v0.2` | `true` |
| `agent` | `runtime_or_integration_folder` | `full` | `runtime_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `apps` | `runtime_or_integration_folder` | `compact` | `runtime_apply_write` | `high` | `blocked_in_v0.2` | `true` |
| `assets` | `documentation_or_planning_folder` | `pointer` | `docs_asset` | `low` | `blocked_except_authorized_asset` | `true` |
| `cli.py` | `runtime_entry` | `full` | `runtime_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `cms/` | `future_root_folder` | `full` | `future_read_only_intake_then_bridge` | `critical_if_miswired` | `planned_not_imported_in_v0.2` | `false` |
| `cron` | `runtime_or_integration_folder` | `compact` | `runtime_apply_write` | `high` | `blocked_in_v0.2` | `true` |
| `docs` | `documentation_or_planning_folder` | `compact` | `docs_only` | `low` | `editable_within_scope` | `true` |
| `docs/context-layer` | `documentation_or_planning_folder` | `full` | `docs_only` | `low` | `editable_in_v0.2` | `true` |
| `gateway` | `runtime_or_integration_folder` | `full` | `runtime_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `hermes_cli` | `runtime_or_integration_folder` | `full` | `runtime_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `model_tools.py` | `runtime_entry` | `full` | `runtime_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `optional-skills` | `runtime_or_integration_folder` | `compact` | `runtime_apply_write` | `high` | `blocked_in_v0.2` | `true` |
| `package-lock.json` | `dependency_or_build_file` | `full` | `dependency_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `package.json` | `dependency_or_build_file` | `full` | `dependency_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `plans` | `documentation_or_planning_folder` | `pointer` | `planning_doc` | `low` | `blocked_except_authorized_plan` | `true` |
| `plugins` | `runtime_or_integration_folder` | `full` | `runtime_apply_write` | `high` | `blocked_in_v0.2` | `true` |
| `providers` | `runtime_or_integration_folder` | `full` | `runtime_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `pyproject.toml` | `dependency_or_build_file` | `full` | `dependency_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `run_agent.py` | `runtime_entry` | `full` | `runtime_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `scripts` | `validation_or_test_folder` | `full` | `script_write` | `medium_high` | `blocked_except_docs_context_in_v0.2` | `true` |
| `setup.py` | `dependency_or_build_file` | `full` | `dependency_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `skills` | `runtime_or_integration_folder` | `full` | `runtime_apply_write` | `high` | `blocked_in_v0.2` | `true` |
| `tests` | `validation_or_test_folder` | `full` | `validation_write` | `medium` | `blocked_except_docs_context_in_v0.2` | `true` |
| `tools` | `runtime_or_integration_folder` | `full` | `runtime_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `toolsets.py` | `runtime_entry` | `full` | `runtime_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `tui_gateway` | `runtime_or_integration_folder` | `full` | `runtime_apply_write` | `high` | `blocked_in_v0.2` | `true` |
| `ui-tui` | `runtime_or_integration_folder` | `full` | `runtime_apply_write` | `high` | `blocked_in_v0.2` | `true` |
| `uv.lock` | `dependency_or_build_file` | `full` | `dependency_apply_write` | `critical` | `blocked_in_v0.2` | `true` |
| `web` | `runtime_or_integration_folder` | `full` | `runtime_apply_write` | `high` | `blocked_in_v0.2` | `true` |
| `website` | `documentation_or_planning_folder` | `compact` | `docs_only` | `low_medium` | `blocked_except_docs_context_in_v0.2` | `true` |

## CMS Intake Meaning

The future `cms/` root is mapped but not imported. Its existence in a future phase must not imply live authority.

```text
cms/ mapped != cms/ imported
cms/ imported != cms authority active
cms authority active != runtime write authority
```

## Non-Claim Lock

HRCN v0.2 is a read-only repository surface boundary map. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, CMS folder state, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
