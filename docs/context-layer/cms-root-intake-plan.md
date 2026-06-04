# HRCN v0.1.4 - CMS Root Intake Plan

Status: docs/context planning layer only.

## Purpose

The intended future direction is to pull Cybernetic Memory System into Hermes as a visible root-level governance substrate, then integrate and test carefully.

Candidate future root:

```text
cms/
```

## Current Lock

```text
No CMS root folder may grant live memory, repair, skill, dry-run, apply,
API-write, or runtime authority merely by existing in the Hermes repository.
```

## Intake Phases

| Phase | Meaning | Authority |
|---|---|---|
| `cms_intake_plan` | Document folder target, import method, and boundaries | docs only |
| `cms_read_only_mirror` | Bring CMS surfaces into Hermes without runtime wiring | read-only |
| `cms_context_packet` | Define what Hermes may read from CMS | read-only |
| `cms_adapter_design` | Specify proposal classification interfaces | design only |
| `cms_dry_run_bridge` | Simulate Hermes/CMS interactions | simulation only |
| `cms_apply_gate` | Require human authorization, rollback, and validation | gate only |
| `cms_runtime_integration` | Live integration after all prior gates | future authorized phase |

## Import Method Options

| Method | Use case | Guard |
|---|---|---|
| Git submodule | Preserve CMS as separately versioned source | pin commit and document update procedure |
| Git subtree | Vendor CMS history into Hermes | preserve provenance and commit lineage |
| Root folder copy | Simple local-first snapshot | include origin URL, source commit, and non-authority lock |
| Python/package dependency | Runtime-style integration | not allowed before bridge design |

## Preferred Near-Term Posture

```text
plan first
map second
read-only intake third
integration later
```

## Non-Claim Lock

HRCN v0.1.4 is a docs/context planning and boundary layer. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
