# HRCN v1.0.1 CMS Read-Only Mirror Import Authorization Path

Status: docs/context authorization-path only.

## Primary Law

```text
CMS may be mirrored only as evidence-bounded read-only context, never as immediate authority.
```

## Purpose

HRCN v1.0.1 defines the gates required before CMS can be copied or mirrored into Hermes as read-only context.

It does not copy CMS yet.

## Current Authorization State

```text
current_phase: authorization_path_only
cms_copy_allowed_in_v1_0_1: false
cms_import_allowed_in_v1_0_1: false
cms_folder_created_in_v1_0_1: false
future_initial_mode: read_only_mirror_candidate
future_runtime_mode_allowed: false
```

## Source Candidates

```text
preferred_local_source: C:/Users/jacks/OneDrive/Desktop/cybernetic-memory-system
preferred_remote_source: https://github.com/jacksonjp0311-gif/cybernetic-memory-system
target_future_root: cms/
source_required_before_copy: true
source_commit_or_snapshot_required: true
```

## Required Authorization Fields

```text
authorization_id
human_authorizer
timestamp_utc
source_type
source_location
source_commit_or_snapshot
target_root
import_method
pre_copy_manifest_plan
secret_scan_plan
license_provenance_note
read_only_boundary_statement
blocked_authority_statement
rollback_removal_plan
post_import_validation_commands
evidence_package_reference
explicit_authorization_phrase
```

## Allowed Future Import Methods

| Method | Initial authority | Risk |
|---|---|---|
| root_folder_copy_snapshot | read-only | simple but provenance must be explicit |
| git_subtree | read-only | larger repo history |
| git_submodule | read-only | submodule discipline required |

## Disallowed Initial Authorities

```text
runtime integration
CMS write authority
memory write authority
API authority
repair apply authority
dry-run execution authority
apply authority
autonomous authority
security/production correctness claims
```

## Pre-Copy Gate Sequence

```text
verify Hermes repo root
verify clean Hermes working tree
verify CMS source exists
record CMS source provenance
produce pre-copy CMS manifest
run secret scan against CMS source
define target cms/ boundary
define rollback/removal plan
define post-import validation commands
create evidence package
receive explicit human authorization
```

## Future Post-Import Gate Sequence

```text
verify only cms/ target changed
verify no runtime/dependency/API files changed
verify CMS mirror is read-only context
verify no adapter/loader/writer/executor created
record manifest and hash summary
record secret scan result
record rollback/removal command
commit with evidence package
```

## Decision Rules

```text
No CMS copy may occur in v1.0.1.
No CMS import may occur in v1.0.1.
No cms/ root folder may be created in v1.0.1.
Future CMS copy must be read-only mirror candidate first.
Future CMS mirror cannot grant runtime, memory, API, repair, dry-run, apply, or autonomous authority.
If source provenance is missing, CMS copy remains blocked.
If secret scan is missing or fails, CMS copy remains blocked.
If rollback/removal plan is missing, CMS copy remains blocked.
If explicit human authorization is missing, CMS copy remains blocked.
```

## Non-Claim Lock

HRCN v1.0.1 is a docs/context CMS read-only mirror import authorization path layer. It defines the gates required before a future CMS mirror/import can occur. It does not create a loader, adapter, runtime bridge, dry-run executor, apply executor, benchmark executor, CMS folder, CMS copy, memory writer, repair applier, API writer, live integration, or apply authority. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
