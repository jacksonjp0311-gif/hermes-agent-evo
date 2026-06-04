<p align="center">
  <img src="assets/banner.png" alt="Hermes Agent" width="100%">
</p>

# Hermes Agent ☤

<p align="center">
  <a href="https://hermes-agent.nousresearch.com/docs/"><img src="https://img.shields.io/badge/Docs-hermes--agent.nousresearch.com-FFD700?style=for-the-badge" alt="Documentation"></a>
  <a href="https://discord.gg/NousResearch"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://github.com/NousResearch/hermes-agent/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://nousresearch.com"><img src="https://img.shields.io/badge/Built%20by-Nous%20Research-blueviolet?style=for-the-badge" alt="Built by Nous Research"></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/Lang-中文-red?style=for-the-badge" alt="中文"></a>
</p>

**The self-improving AI agent built by [Nous Research](https://nousresearch.com).** It's the only agent with a built-in learning loop — it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions. Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop — talk to it from Telegram while it works on a cloud VM.

Use any model you want — [Nous Portal](https://portal.nousresearch.com), [OpenRouter](https://openrouter.ai) (200+ models), [NovitaAI](https://novita.ai) (AI-native cloud for Model API, Agent Sandbox, and GPU Cloud), [NVIDIA NIM](https://build.nvidia.com) (Nemotron), [Xiaomi MiMo](https://platform.xiaomimimo.com), [z.ai/GLM](https://z.ai), [Kimi/Moonshot](https://platform.moonshot.ai), [MiniMax](https://www.minimax.io), [Hugging Face](https://huggingface.co), OpenAI, or your own endpoint. Switch with `hermes model` — no code changes, no lock-in.

<table>
<tr><td><b>A real terminal interface</b></td><td>Full TUI with multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output.</td></tr>
<tr><td><b>Lives where you do</b></td><td>Telegram, Discord, Slack, WhatsApp, Signal, and CLI — all from a single gateway process. Voice memo transcription, cross-platform conversation continuity.</td></tr>
<tr><td><b>A closed learning loop</b></td><td>Agent-curated memory with periodic nudges. Autonomous skill creation after complex tasks. Skills self-improve during use. FTS5 session search with LLM summarization for cross-session recall. <a href="https://github.com/plastic-labs/honcho">Honcho</a> dialectic user modeling. Compatible with the <a href="https://agentskills.io">agentskills.io</a> open standard.</td></tr>
<tr><td><b>Scheduled automations</b></td><td>Built-in cron scheduler with delivery to any platform. Daily reports, nightly backups, weekly audits — all in natural language, running unattended.</td></tr>
<tr><td><b>Delegates and parallelizes</b></td><td>Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns.</td></tr>
<tr><td><b>Runs anywhere, not just your laptop</b></td><td>Six terminal backends — local, Docker, SSH, Singularity, Modal, and Daytona. Daytona and Modal offer serverless persistence — your agent's environment hibernates when idle and wakes on demand, costing nearly nothing between sessions. Run it on a $5 VPS or a GPU cluster.</td></tr>
<tr><td><b>Research-ready</b></td><td>Batch trajectory generation, trajectory compression for training the next generation of tool-calling models.</td></tr>
</table>

<!-- HRCN_CONTEXT_LAYER_START -->
## Codex / RCC-CMS-HRCN Context Layer

This fork includes an internal, docs-only Codex/RCC/CMS/HRCN governance layer for James Paul Jackson's Hermes work.

The upstream Hermes product README above this section is preserved. This block is additive: it explains the fork's local governance context without changing Hermes runtime behavior.

```text
Hermes acts.
RCC orients.
CMS governs.
Human authorization unlocks dangerous transitions.
```

### Current HRCN Snapshot

| Layer | What it answers | Primary surface |
|---|---|---|
| HRCN v0.1 | Can Hermes carry a docs-only RCC/CMS/HRCN context anchor without runtime mutation? | `docs/context-layer/rcc-cms-hrcn.md` |
| HRCN v0.1.1 | Can the root README and mini README surfaces become navigable without touching runtime code? | `docs/context-layer/rcc-cms-hrcn.validation.json` |
| HRCN v0.1.2 | Can Cyber/CMS/RCC-N lessons be injected before runtime bridge work? | `docs/context-layer/cybernetic-lessons-injection.md` |
| HRCN v0.1.3 | Can README state, mini README profiles, and rehydration protocol cohere without runtime mutation? | `docs/context-layer/hrcn-v0.1.3.validation.json` |
| HRCN v0.1.4 | Can Hermes state future runtime evolution and CMS root-folder intake without granting live authority? | `docs/context-layer/hrcn-v0.1.4.validation.json` |
| HRCN v0.2 | Can Hermes runtime, docs, tool, provider, UI, dependency, and future CMS surfaces be mapped without mutation? | `docs/context-layer/hermes-surface-boundary-map.json` |
| HRCN v0.2.4 | Can public README rendering, roadmap, rehydration, mini READMEs, and failure lessons agree before v0.3? | `docs/context-layer/hrcn-v0.2.4.public-surface-coherence.validation.json` |
| HRCN v0.3 | Can a future agent load a bounded rehydration packet before proposing work? | `docs/context-layer/hrcn-v0.3-agent-rehydration-packet-contract.json` |
| HRCN v0.4 | Can CMS context be designed as read-only orientation without write authority? | `docs/context-layer/hrcn-v0.4-cms-read-only-bridge-design.json` |
| HRCN v0.5 | Can memory visibility, use, proposal, dry-run, and apply authority be separated? | `docs/context-layer/hrcn-v0.5-memory-permission-adapter-design.json` |
| HRCN v0.6 | Can repair recommendations be generated without repair execution or apply authority? | `docs/context-layer/hrcn-v0.6-repair-recommendation-adapter-design.json` |
| HRCN v0.6.1 | Can README render hygiene and HRCN block placement be closed before dry-run design? | `docs/context-layer/hrcn-v0.6.1-readme-geometry-closure.validation.json` |
| HRCN v0.7 | Can future changes be simulated without live mutation or apply authority? | `docs/context-layer/hrcn-v0.7-dry-run-adapter-design.json` |
| HRCN v0.8 | Can apply/write be gated by explicit authorization, rollback, validation, and evidence? | `docs/context-layer/hrcn-v0.8-apply-gate-adapter-design.json` |

Current public finding: Hermes provides the actor/runtime body. RCC provides repository orientation. CMS provides governed memory, repair, dry-run, apply-gate, rollback, evidence, and permission boundaries. HRCN is the bridge contract between those surfaces and human authorization.

### Human Director Box

#### What this fork is

This fork is a local-first Hermes Agent workspace prepared for governed agent evolution:

```text
Hermes runtime -> repository orientation -> proposal classification
-> dry-run / evidence -> CMS permission boundary -> human authorization
```

Hermes already supplies CLI/TUI, model routing, tools, skills, memory hooks, terminal backends, gateway surfaces, scheduler, and documentation. HRCN adds a repository-governance map before any direct runtime bridge is attempted.

#### What this fork is not

This fork does not prove Hermes correctness, CMS correctness, code correctness, security, production readiness, external validation, AGI, ASI, consciousness, sentience, autonomy, or self-awareness. Through HRCN v0.8, the fork remains documentation, navigation, profile compression, rehydration, runtime-evolution planning, CMS intake planning, read-only surface mapping, packet/bridge/permission/recommendation/dry-run/apply-gate design, and README geometry closure only.

### Current Public Metrics

| Surface | Result |
|---|---:|
| Current checkpoint | `HRCN v0.8` |
| Previous validated anchor | `HRCN v0.7` |
| Runtime code changed | `False` |
| Dependency files changed by HRCN | `False` |
| README pointer present | `True` |
| Context layer doc | `docs/context-layer/rcc-cms-hrcn.md` |
| Context layer mini README | `docs/context-layer/README.md` |
| Rehydration protocol | `docs/context-layer/hermes-agent-rehydration-protocol.md` |
| Profile map | `docs/context-layer/hrcn-profile-map.json` |
| Runtime evolution boundary | `docs/context-layer/hrcn-runtime-evolution-boundary.md` |
| CMS root intake plan | `docs/context-layer/cms-root-intake-plan.md` |
| Surface boundary map | `docs/context-layer/hermes-surface-boundary-map.json` |
| Validation report | `docs/context-layer/hrcn-v0.8.validation.json` |
| Mini README profiles | `full / compact / pointer` |
| Agent rehydration packet contract | `docs/context-layer/hrcn-v0.3-agent-rehydration-packet-contract.json` |
| CMS read-only bridge design | `docs/context-layer/hrcn-v0.4-cms-read-only-bridge-design.json` |
| Memory permission adapter design | `docs/context-layer/hrcn-v0.5-memory-permission-adapter-design.json` |
| Repair recommendation adapter design | `docs/context-layer/hrcn-v0.6-repair-recommendation-adapter-design.json` |
| Dry-run adapter design | `docs/context-layer/hrcn-v0.7-dry-run-adapter-design.json` |
| Apply-gate adapter design | `docs/context-layer/hrcn-v0.8-apply-gate-adapter-design.json` |

### Core Law

- No docs context is runtime integration.
- No README surface is correctness.
- No mini README is validation.
- No agent proposal is authority.
- No memory bridge without CMS permission.
- No repair apply without human authorization.
- No runtime mutation in the current HRCN phase.
- No production, security, consciousness, sentience, AGI, or autonomy claim.
- Rehydration is orientation, not authority.
- Profile adoption is not validation.
- A future `cms/` root folder is not live CMS integration by itself.
- CMS intake cannot begin until the surface boundary map is validated.
- A mapped surface remains read-only unless the current phase explicitly grants write authority.
- Surface mapping is not runtime mutation.
- Future runtime mutation requires route map, evidence boundary, dry-run path, rollback plan, validation, and explicit human authorization.
- Current docs-only status does not mean runtime will never change.
- If a validator or writer fails, staging, commit, and push are forbidden.
- Candidate text must validate in memory before files are written.
- Location verification must happen before every script writer or validator.
- Public README render hygiene is part of the repository evidence surface.
- Packet contract presence is not loader presence.
- No packet grants runtime, dependency, CMS, API, or apply/write authority.
- A rehydration packet orients an agent; it does not authorize an agent.
- No CMS read-only bridge design grants CMS write authority.
- CMS context is orientation/evidence, not command authority.
- A CMS bridge may inform Hermes; it may not command Hermes.
- No memory permission design grants apply authority.
- Memory records cannot upgrade their own permission class.
- Memory may surface context; permission determines use; humans authorize action.
- Repair recommendation is not repair execution.
- No repair recommendation grants staging, commit, push, runtime mutation, or apply authority.
- A repair recommendation may describe a path; it may not apply the path.
- README geometry must keep HRCN version blocks inside the HRCN context layer.
- No dry-run design grants live mutation authority.
- Dry-run evidence is not apply authority.
- A dry-run may simulate a change; it may not become the change.
- Human authorization, rollback, validation, and evidence are required before any future apply/write transition.
- No apply-gate design grants live apply authority.
- Apply is a gated transition, not an agent decision.

### Current HRCN Surface Lock

```text
No Hermes HRCN context surface is current unless the root README,
docs/context-layer contract, roadmap, profile map, rehydration protocol,
mini README profiles, validation report, runtime lock, and non-claim
boundaries agree.
```

<!-- HRCN_RUNTIME_EVOLUTION_BOUNDARY_START -->
### Current Runtime Boundary and Future Runtime Evolution

HRCN v0.6.1 keeps the current repository state docs/context/design-only, but it does not lock Hermes into docs-only forever.

Current boundary:

```text
HRCN v0.6.1 does not change Hermes runtime.
```

Future boundary:

```text
Hermes runtime may evolve only after surface mapping, evidence boundaries,
dry-run design, rollback coverage, validation, and explicit human authorization.
```

This distinction matters:

| Statement | Status |
|---|---|
| HRCN changes Hermes runtime now. | `False` |
| HRCN forbids future runtime work forever. | `False` |
| HRCN requires runtime work to pass gates before execution. | `True` |
| CMS can be copied into the repo and immediately become authority. | `False` |
| CMS root-folder intake can be planned before integration. | `True` |

Runtime evolution sequence:

```text
map surfaces -> define packet -> design read-only bridge -> classify proposals
-> design dry-run -> bind rollback -> validate -> human authorize -> execute
```

Non-claim lock: runtime evolution planning is not runtime mutation, not production readiness, not security proof, not external validation, and not autonomous write authority.
<!-- HRCN_RUNTIME_EVOLUTION_BOUNDARY_END -->

<!-- HRCN_CMS_ROOT_INTAKE_START -->
### Future CMS Root Folder Intake Plan

The intended direction is to pull Cybernetic Memory System into Hermes as a visible root-level governance substrate after the Hermes surface boundary map is complete.

Candidate future root:

```text
cms/
```

Current rule:

```text
No CMS root folder may grant live memory, repair, skill, dry-run, apply,
API-write, or runtime authority merely by existing in the Hermes repository.
```

Intake phases:

| Phase | Meaning | Authority |
|---|---|---|
| `cms_intake_plan` | Document folder target, import method, and boundaries | docs only |
| `cms_read_only_mirror` | Bring CMS surfaces into Hermes without runtime wiring | read-only |
| `cms_context_packet` | Define what Hermes may read from CMS | read-only |
| `cms_adapter_design` | Specify proposal classification interfaces | design only |
| `cms_dry_run_bridge` | Simulate Hermes/CMS interactions | simulation only |
| `cms_apply_gate` | Require human authorization, rollback, and validation | gate only |
| `cms_runtime_integration` | Live integration after all prior gates | future authorized phase |

Possible import methods:

| Method | Use case | Risk |
|---|---|---|
| Git submodule | Preserve CMS as separately versioned source | requires submodule discipline |
| Git subtree | Vendor CMS history into Hermes | larger repo history |
| Root folder copy | Simple local-first snapshot | must preserve provenance |
| Python/package dependency | Runtime-style integration | too early before bridge design |

Preferred near-term posture:

```text
plan first
map second
read-only intake third
integration later
```

Non-claim lock: CMS root intake planning does not activate CMS runtime, does not grant CMS authority, does not prove Hermes correctness, and does not make Hermes production-ready or secure.
<!-- HRCN_CMS_ROOT_INTAKE_END -->

<!-- HRCN_V02_SURFACE_BOUNDARY_START -->
### HRCN v0.2 Surface Boundary Map

HRCN v0.2 introduces a read-only map of Hermes repository surfaces before CMS is pulled into the repo or runtime integration is attempted.

Map artifacts:

```text
docs/context-layer/hermes-surface-boundary-map.json
docs/context-layer/hermes-surface-boundary-map.md
docs/context-layer/hrcn-v0.2.validation.json
docs/context-layer/hrcn-v0.2.validation.md
```

Current rule:

```text
Mapping a surface does not grant write authority over that surface.
```

v0.2 separates four things that must not collapse into one another:

```text
readable surface
mapped surface
editable surface
runtime-authorized surface
```

Only README/context-layer documentation surfaces are writable in this phase. Runtime, dependency, tool, skill, provider, gateway, TUI, web, and CMS-root surfaces remain blocked until later gates.

Non-claim lock: HRCN v0.2 is a read-only repository surface boundary map. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, CMS folder state, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
<!-- HRCN_V02_SURFACE_BOUNDARY_END -->

### HRCN Version Geometry Blocks

<!-- HRCN_V03_AGENT_PACKET_START -->
### HRCN v0.3 Agent Rehydration Packet Contract

HRCN v0.3 defines the packet a future human or AI agent must load before proposing work.

Current rule:

```text
A rehydration packet orients an agent; it does not authorize an agent.
```

Packet artifacts:

```text
docs/context-layer/hrcn-v0.3-agent-rehydration-packet-contract.json
docs/context-layer/hrcn-v0.3-agent-rehydration-packet-contract.md
docs/context-layer/hrcn-v0.3.validation.json
docs/context-layer/hrcn-v0.3.validation.md
```

v0.3 separates five things that must not collapse into one another:

```text
orientation packet
proposal classification
dry-run design
apply/write authority
human authorization
```

Non-claim lock: HRCN v0.3 does not create a loader, does not modify runtime, does not import CMS, does not grant API or CMS write authority, and does not prove safety, production readiness, autonomy, consciousness, sentience, AGI, ASI, or external validation.
<!-- HRCN_V03_AGENT_PACKET_END -->

<!-- HRCN_V04_CMS_READ_ONLY_BRIDGE_START -->
### HRCN v0.4 CMS Read-Only Bridge Design

HRCN v0.4 defines how a future bridge may expose CMS context as read-only orientation.

Current rule:

```text
A CMS bridge may inform Hermes; it may not command Hermes.
```

Bridge artifacts:

```text
docs/context-layer/hrcn-v0.4-cms-read-only-bridge-design.json
docs/context-layer/hrcn-v0.4-cms-read-only-bridge-design.md
docs/context-layer/hrcn-v0.4.validation.json
docs/context-layer/hrcn-v0.4.validation.md
```

v0.4 separates five things that must not collapse into one another:

```text
CMS context
read-only orientation
proposal classification
apply/write authority
human authorization
```

Non-claim lock: HRCN v0.4 does not create a loader, adapter, runtime bridge, CMS folder, CMS writer, API writer, repair applier, or live integration.
<!-- HRCN_V04_CMS_READ_ONLY_BRIDGE_END -->

<!-- HRCN_V05_MEMORY_PERMISSION_START -->
### HRCN v0.5 Memory Permission Adapter Design

HRCN v0.5 defines the permission geometry a future memory adapter must obey.

Current rule:

```text
Memory may surface context; permission determines use; humans authorize action.
```

Permission artifacts:

```text
docs/context-layer/hrcn-v0.5-memory-permission-adapter-design.json
docs/context-layer/hrcn-v0.5-memory-permission-adapter-design.md
docs/context-layer/hrcn-v0.5.validation.json
docs/context-layer/hrcn-v0.5.validation.md
```

v0.5 separates six things that must not collapse into one another:

```text
memory visibility
permitted use
proposal authority
dry-run candidacy
apply/write authority
human authorization
```

Non-claim lock: HRCN v0.5 does not create a loader, adapter, runtime bridge, CMS folder, CMS writer, API writer, repair applier, or live integration.
<!-- HRCN_V05_MEMORY_PERMISSION_END -->

<!-- HRCN_V06_REPAIR_RECOMMENDATION_START -->
### HRCN v0.6 Repair Recommendation Adapter Design

HRCN v0.6 defines how future context may produce bounded repair recommendations without executing repairs.

Current rule:

```text
A repair recommendation may describe a path; it may not apply the path.
```

Recommendation artifacts:

```text
docs/context-layer/hrcn-v0.6-repair-recommendation-adapter-design.json
docs/context-layer/hrcn-v0.6-repair-recommendation-adapter-design.md
docs/context-layer/hrcn-v0.6.validation.json
docs/context-layer/hrcn-v0.6.validation.md
```

v0.6 separates six things that must not collapse into one another:

```text
observation
diagnosis
recommendation
dry-run candidacy
apply-gate candidacy
human authorization
```

Non-claim lock: HRCN v0.6 does not create a loader, adapter, repair executor, dry-run executor, runtime bridge, CMS folder, CMS writer, API writer, repair applier, or live integration.
<!-- HRCN_V06_REPAIR_RECOMMENDATION_END -->

<!-- HRCN_V07_DRY_RUN_START -->
### HRCN v0.7 Dry-Run Adapter Design

HRCN v0.7 defines how future proposals and repair recommendations may be simulated without live mutation.

Current rule:

```text
A dry-run may simulate a change; it may not become the change.
```

Dry-run artifacts:

```text
docs/context-layer/hrcn-v0.7-dry-run-adapter-design.json
docs/context-layer/hrcn-v0.7-dry-run-adapter-design.md
docs/context-layer/hrcn-v0.7.validation.json
docs/context-layer/hrcn-v0.7.validation.md
```

v0.7 separates seven things that must not collapse into one another:

```text
proposal
dry-run plan
sandbox boundary
expected diff
evidence package
rollback plan
human authorization
```

Non-claim lock: HRCN v0.7 does not create a loader, adapter, dry-run executor, repair executor, runtime bridge, CMS folder, CMS writer, API writer, repair applier, or live integration.
<!-- HRCN_V07_DRY_RUN_END -->

<!-- HRCN_V08_APPLY_GATE_START -->
### HRCN v0.8 Apply-Gate Adapter Design

HRCN v0.8 defines the gate required before any future write/apply transition can be requested.

Current rule:

```text
Apply is a gated transition, not an agent decision.
```

Apply-gate artifacts:

```text
docs/context-layer/hrcn-v0.8-apply-gate-adapter-design.json
docs/context-layer/hrcn-v0.8-apply-gate-adapter-design.md
docs/context-layer/hrcn-v0.8.validation.json
docs/context-layer/hrcn-v0.8.validation.md
```

v0.8 separates eight things that must not collapse into one another:

```text
apply request
authority classification
human authorization
rollback plan
validation plan
evidence package
staged scope
live apply
```

Non-claim lock: HRCN v0.8 does not create a loader, adapter, dry-run executor, apply executor, repair executor, runtime bridge, CMS folder, CMS writer, API writer, repair applier, or live integration.
<!-- HRCN_V08_APPLY_GATE_END -->

### Rehydration Protocol

A fresh human or AI thread must complete five scans before proposing work:

1. Identity Scan: `README.md`, `AGENTS.md`, `docs/context-layer/rcc-cms-hrcn.md`
2. Boundary Scan: `docs/context-layer/hrcn-profile-map.json`, roadmap, target mini README
3. State Scan: validation reports and `git status --short`
4. Target Scan: target folder README, source, tests, docs
5. Authority Scan: classify as `docs_only`, `read_only_context`, `dry_run`, or `apply_write`

Version-readiness lock:

```text
No fresh-thread versioning without identity, boundary, state, target, and authority scans.
```

### Mini README Profile Map

| Profile | Use | Folders |
|---|---|---|
| `full` | Load-bearing runtime, tool, provider, UI, validation, or governance surfaces | `agent/`, `tools/`, `skills/`, `plugins/`, `providers/`, `gateway/`, `hermes_cli/`, `tui_gateway/`, `ui-tui/`, `web/`, `scripts/`, `tests/`, `docs/context-layer/` |
| `compact` | Important support/docs/integration surfaces | `optional-skills/`, `cron/`, `acp_adapter/`, `apps/`, `docs/`, `website/` |
| `pointer` | Low-risk planning/assets surfaces | `assets/`, `plans/`, `.plans/` |

### PART I - Human README

Author: James Paul Jackson.

The working model:

```text
Hermes = capable actor runtime
RCC    = repository orientation
CMS    = governed memory and permission substrate
HRCN   = bridge contract
Human  = write boundary
```

Human operating rule:

```text
Do not hack runtime first.
Orient the repository.
Map the surfaces.
Preserve non-claim locks.
Rehydrate before versioning.
Then decide whether a bridge deserves a dry-run.
```

### PART II - RCC Nexus README

RCC tells the agent what the repository means. RCC-N tells the agent where it is. Validation tells the agent whether repository-bound checks agreed.

HRCN treats the Hermes repo as a navigable field:

| Shell | Meaning |
|---|---|
| center | Source identity, README, AGENTS.md, context layer, non-claim locks |
| inner | Runtime body: agent loop, CLI, model/tools/session primitives |
| middle | Tools, skills, gateways, providers, TUI, web, scripts, tests |
| outer | Docs, website, local assets, validation reports, future evidence |

Meridians:

```text
source, runtime, tools, skills, provider, gateway, ui, docs, context, safety, governance
```

### PART III - AI Agent README

Before editing this fork, an AI agent should read:

1. `README.md`
2. `AGENTS.md`
3. `docs/context-layer/README.md`
4. `docs/context-layer/rcc-cms-hrcn.md`
5. `docs/context-layer/hermes-agent-rehydration-protocol.md`
6. `docs/context-layer/hrcn-profile-map.json`
7. the target folder `README.md`
8. relevant source, tests, and upstream docs

Patch routing:

| Change type | Read first | Boundary |
|---|---|---|
| Docs/context patch | `README.md`, `docs/context-layer/README.md` | Allowed in current docs/context phase |
| Mini README patch | target folder `README.md`, profile map | Docs-only |
| Runtime patch | `AGENTS.md`, target source, tests | Blocked until future HRCN phase |
| Tool/skill/provider patch | target folder, tests, security notes | Blocked until future HRCN phase |
| Dependency patch | `pyproject.toml`, `uv.lock`, package files | Blocked in current HRCN phase |
| Apply/write bridge | HRCN contract + CMS authorization | Future phase only |

### README + Mini Repo Audit Map

A patch is incomplete if it changes folder purpose, route meaning, evidence surface, validation command, or claim boundary without updating the matching README/mini README surface.

Gap classes:

| Gap class | Detection question | Required repair |
|---|---|---|
| README drift | Does the root README describe the current HRCN state? | Patch the HRCN block. |
| Mini README drift | Did a folder gain or change governance meaning? | Patch the affected folder README. |
| Runtime drift | Did non-doc source change? | Stop; this is outside the current HRCN phase. |
| Claim drift | Does text imply correctness, safety, sentience, autonomy, AGI, or production readiness? | Restore non-claim lock. |
| Context drift | Does context imply a loader or runtime integration? | Restore docs-only language. |
| Local artifact drift | Are `.venv`, local configs, icons, logs, or package-lock changes mixed in? | Separate or explicitly classify before commit. |
| Rehydration drift | Did a fresh thread skip scans before proposing version work? | Stop and complete rehydration protocol. |
| Profile drift | Is a surface over- or under-governed for its risk? | Adjust `hrcn-profile-map.json` and affected mini README. |

### AI Failure Learning Ledger

| Lesson ID | Failure observed | Root cause | Permanent rule |
|---|---|---|---|
| HRCN-L-001 | HRCN v0.1 validation reported `README.md` as `EADME.md` and `package-lock.json` as `ackage-lock.json`. | Git status parser trimmed the line before slicing the status prefix. | Parse Git short status by taking characters after the two status columns and space without trimming first. |
| HRCN-L-002 | Context docs were valid but `context_files_exist` reported false. | Validation checked path state before validation files were fully written and status paths were malformed. | Recompute validation after all files are written and verify actual file existence directly. |
| HRCN-L-003 | Local UX/icon and package-lock changes appeared beside HRCN docs. | Pre-existing local files were not separated from new HRCN docs surfaces. | Record pre-existing dirty state and validate only HRCN-introduced docs paths unless the human authorizes broader cleanup. |
| HRCN-L-004 | Mini README expansion became heavy across all folders. | Full RCC blocks were applied before profile selection existed. | Use profile-gated mini README surfaces: full, compact, pointer. |
| HRCN-L-005 | Fresh threads can become version-eager after context expansion. | The repo had context surfaces but not an explicit rehydration protocol. | Require identity, boundary, state, target, and authority scans before proposing version work. |
| HRCN-L-006 | Agent visibility wording could imply runtime will never change. | Permanent visibility-only language conflicts with the intended CMS-to-Hermes integration path. | Use phase-bounded language: no runtime mutation now; future runtime work only after mapping, dry-run, rollback, validation, and human authorization. |
| HRCN-L-007 | README carried stale v0.1.3/v0.1.4 current-phase wording after v0.2 mapped surfaces. | Versioned sections advanced faster than current-state language. | README coherence closure must replace stale current-phase tokens before the next version step. |
| HRCN-L-008 | v0.2.1 pushed after a validation stop, leaving two patch-routing cells and the final non-claim lock stale. | Manual continuation after validator failure bypassed the remaining repair. | If a validator throws, stop and rerun a closure patch before proceeding to the next version. |
| HRCN-L-009 | Public README rendered double-encoded title, punctuation, and language-badge text. | UTF-8 text was round-tripped through the wrong encoding path. | Public README patches must run render-hygiene scans before commit. |
| HRCN-L-010 | A render-hygiene validator failed, but later add/commit/push commands were still attempted. | Manual continuation after a thrown validator bypassed the intended stop boundary. | If a validator throws, stop immediately; no add, commit, or push after failure. |
| HRCN-L-011 | A failed writer left partial context-doc changes that were committed without README repair or validation artifacts. | The script wrote some files before full candidate validation succeeded. | Build candidate text in memory, validate all candidates, then write files. |
| HRCN-L-012 | Git cleanup was once attempted from the user profile instead of the repo root. | Location/root verification was not the first operation. | Every script must set location, verify root, and check status before any writer, validator, staging, commit, or push logic. |

### HRCN Roadmap

| Phase | Name | Boundary |
|---|---|---|
| HRCN v0.1 | Hermes README/RCC Documentation Anchor | Internal docs only. |
| HRCN v0.1.1 | README + Mini README Surface Expansion | Root README and mini READMEs only. |
| HRCN v0.1.2 | Cyber/CMS/RCC-N Lesson Injection | Docs/context lesson injection only. |
| HRCN v0.1.3 | Coherence, Profile Compression, and Rehydration Protocol | Docs/context profile gating and rehydration only. |
| HRCN v0.1.4 | Runtime Evolution Boundary and CMS Root Intake Plan | Docs/context planning only; no runtime or CMS folder import. |
| HRCN v0.2 | Hermes Surface Boundary Map | Read-only runtime/docs/tool/provider/UI/dependency/CMS surface map; no edits. |
| HRCN v0.2.4 | Public Surface Coherence Recovery | README render, roadmap, rehydration, mini README, and lesson closure; no runtime or CMS import. |
| HRCN v0.3 | Agent Rehydration Packet Contract | Context packet design; no loader. |
| HRCN v0.4 | CMS Read-Only Bridge Design | Read-only bridge spec; no memory writes. |
| HRCN v0.5 | Memory Permission Adapter Design | Proposal classification only. |
| HRCN v0.6 | Repair Recommendation Adapter Design | Recommendations only. |
| HRCN v0.7 | Dry-Run Adapter Design | Simulation only. |
| HRCN v0.8 | Apply-Gate Adapter Design | Human authorization + rollback requirements. |
| HRCN v0.9 | Evidence Package and Benchmark Harness | Evidence contract. |
| HRCN v1.0 | Governed Hermes-CMS Nexus | Only after prior gates survive validation. |

### Full Directory Box

| Surface | Purpose |
|---|---|
| `agent/` | Agent internals: providers, memory, compression, context helpers, runtime utilities. |
| `tools/` | Built-in tools and terminal/environment backends. |
| `skills/` | Bundled procedural skill surfaces. |
| `optional-skills/` | Optional/niche skill surfaces. |
| `plugins/` | Plugin families for memory, providers, context engines, observability, platforms, and extensions. |
| `providers/` | Provider abstractions and routing surfaces. |
| `hermes_cli/` | CLI subcommands, setup/config flows, registry, skin engine, and distribution surfaces. |
| `gateway/` | Messaging gateway adapters and session routing. |
| `cron/` | Scheduler and recurring job surfaces. |
| `acp_adapter/` | ACP server integration. |
| `tui_gateway/` | Python JSON-RPC backend for the TUI. |
| `ui-tui/` | Ink/React terminal UI. |
| `web/` | Dashboard/frontend app. |
| `apps/` | Desktop/bootstrap/shared apps. |
| `docs/` | Internal and supplemental docs. |
| `website/` | Public Docusaurus documentation. |
| `scripts/` | Install, test, release, dev, and utility scripts. |
| `tests/` | Pytest suite and fixtures. |
| `assets/` | README/local UX assets. |
| `plans/` | Planning surfaces when present. |
| `.plans/` | Hidden/local planning surfaces when present. |
| `docs/context-layer/` | HRCN/RCC/CMS context layer for this fork. |

### Mini README Update Rule

If a folder's purpose, files, routes, evidence surfaces, validation commands, claim boundaries, or profile changes, update the folder mini README in the same commit.

Non-claim lock: navigation is not validation, but stale navigation is repository drift.

### Non-Claim Lock

HRCN v0.8 is a docs/context apply-gate adapter design layer. It defines the authorization, rollback, validation, evidence, and staged-scope requirements for future apply/write transitions. It does not create a loader, adapter, runtime bridge, dry-run executor, apply executor, CMS folder, memory writer, repair applier, API writer, live integration, or apply authority. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
<!-- HRCN_CONTEXT_LAYER_END -->
---

## Quick Install

### Linux, macOS, WSL2, Termux

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

### Windows (native, PowerShell)

> **Heads up:** Native Windows runs Hermes without WSL — CLI, gateway, TUI, and tools all work natively. If you'd rather use WSL2, the Linux/macOS one-liner above works there too. Found a bug? Please [file issues](https://github.com/NousResearch/hermes-agent/issues).

Run this in PowerShell:

```powershell
iex (irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1)
```

The installer handles everything: uv, Python 3.11, Node.js, ripgrep, ffmpeg, **and a portable Git Bash** (MinGit, unpacked to `%LOCALAPPDATA%\hermes\git` — no admin required, completely isolated from any system Git install). Hermes uses this bundled Git Bash to run shell commands.

If you already have Git installed, the installer detects it and uses that instead. Otherwise a ~45MB MinGit download is all you need — it won't touch or interfere with any system Git.

> **Android / Termux:** The tested manual path is documented in the [Termux guide](https://hermes-agent.nousresearch.com/docs/getting-started/termux). On Termux, Hermes installs a curated `.[termux]` extra because the full `.[all]` extra currently pulls Android-incompatible voice dependencies.
>
> **Windows:** Native Windows is fully supported — the PowerShell one-liner above installs everything. If you'd rather use WSL2, the Linux command works there too. Native Windows install lives under `%LOCALAPPDATA%\hermes`; WSL2 installs under `~/.hermes` as on Linux.  The only Hermes feature that currently needs WSL2 specifically is the browser-based dashboard chat pane (it uses a POSIX PTY — classic CLI and gateway both run natively).

After installation:

```bash
source ~/.bashrc    # reload shell (or: source ~/.zshrc)
hermes              # start chatting!
```

---

## Getting Started

```bash
hermes              # Interactive CLI — start a conversation
hermes model        # Choose your LLM provider and model
hermes tools        # Configure which tools are enabled
hermes config set   # Set individual config values
hermes gateway      # Start the messaging gateway (Telegram, Discord, etc.)
hermes setup        # Run the full setup wizard (configures everything at once)
hermes claw migrate # Migrate from OpenClaw (if coming from OpenClaw)
hermes update       # Update to the latest version
hermes doctor       # Diagnose any issues
```

📖 **[Full documentation →](https://hermes-agent.nousresearch.com/docs/)**

---

## Skip the API-key collection — Nous Portal

Hermes works with whatever provider you want — that's not changing. But if you'd rather not collect five separate API keys for the model, web search, image generation, TTS, and a cloud browser, **[Nous Portal](https://portal.nousresearch.com)** covers all of them under one subscription:

- **300+ models** — pick any of them with `/model <name>`
- **Tool Gateway** — web search (Firecrawl), image generation (FAL), text-to-speech (OpenAI), cloud browser (Browser Use), all routed through your sub. No extra accounts.

One command from a fresh install:

```bash
hermes setup --portal
```

That logs you in via OAuth, sets Nous as your provider, and turns on the Tool Gateway. Check what's wired up any time with `hermes portal info`. Full details on the [Tool Gateway docs page](https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-gateway).

You can still bring your own keys per-tool whenever you want — the gateway is per-backend, not all-or-nothing.

---

## CLI vs Messaging Quick Reference

Hermes has two entry points: start the terminal UI with `hermes`, or run the gateway and talk to it from Telegram, Discord, Slack, WhatsApp, Signal, or Email. Once you're in a conversation, many slash commands are shared across both interfaces.

| Action                         | CLI                                           | Messaging platforms                                                              |
| ------------------------------ | --------------------------------------------- | -------------------------------------------------------------------------------- |
| Start chatting                 | `hermes`                                      | Run `hermes gateway setup` + `hermes gateway start`, then send the bot a message |
| Start fresh conversation       | `/new` or `/reset`                            | `/new` or `/reset`                                                               |
| Change model                   | `/model [provider:model]`                     | `/model [provider:model]`                                                        |
| Set a personality              | `/personality [name]`                         | `/personality [name]`                                                            |
| Retry or undo the last turn    | `/retry`, `/undo`                             | `/retry`, `/undo`                                                                |
| Compress context / check usage | `/compress`, `/usage`, `/insights [--days N]` | `/compress`, `/usage`, `/insights [days]`                                        |
| Browse skills                  | `/skills` or `/<skill-name>`                  | `/<skill-name>`                                                                  |
| Interrupt current work         | `Ctrl+C` or send a new message                | `/stop` or send a new message                                                    |
| Platform-specific status       | `/platforms`                                  | `/status`, `/sethome`                                                            |

For the full command lists, see the [CLI guide](https://hermes-agent.nousresearch.com/docs/user-guide/cli) and the [Messaging Gateway guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging).

---

## Documentation

All documentation lives at **[hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/)**:

| Section                                                                                             | What's Covered                                             |
| --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)                 | Install → setup → first conversation in 2 minutes          |
| [CLI Usage](https://hermes-agent.nousresearch.com/docs/user-guide/cli)                              | Commands, keybindings, personalities, sessions             |
| [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)                | Config file, providers, models, all options                |
| [Messaging Gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging)                | Telegram, Discord, Slack, WhatsApp, Signal, Home Assistant |
| [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security)                          | Command approval, DM pairing, container isolation          |
| [Tools & Toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools)            | 40+ tools, toolset system, terminal backends               |
| [Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)              | Procedural memory, Skills Hub, creating skills             |
| [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)                     | Persistent memory, user profiles, best practices           |
| [MCP Integration](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)               | Connect any MCP server for extended capabilities           |
| [Cron Scheduling](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)              | Scheduled tasks with platform delivery                     |
| [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)       | Project context that shapes every conversation             |
| [Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)             | Project structure, agent loop, key classes                 |
| [Contributing](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing)             | Development setup, PR process, code style                  |
| [CLI Reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands)                  | All commands and flags                                     |
| [Environment Variables](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) | Complete env var reference                                 |

---

## Migrating from OpenClaw

If you're coming from OpenClaw, Hermes can automatically import your settings, memories, skills, and API keys.

**During first-time setup:** The setup wizard (`hermes setup`) automatically detects `~/.openclaw` and offers to migrate before configuration begins.

**Anytime after install:**

```bash
hermes claw migrate              # Interactive migration (full preset)
hermes claw migrate --dry-run    # Preview what would be migrated
hermes claw migrate --preset user-data   # Migrate without secrets
hermes claw migrate --overwrite  # Overwrite existing conflicts
```

What gets imported:

- **SOUL.md** — persona file
- **Memories** — MEMORY.md and USER.md entries
- **Skills** — user-created skills → `~/.hermes/skills/openclaw-imports/`
- **Command allowlist** — approval patterns
- **Messaging settings** — platform configs, allowed users, working directory
- **API keys** — allowlisted secrets (Telegram, OpenRouter, OpenAI, Anthropic, ElevenLabs)
- **TTS assets** — workspace audio files
- **Workspace instructions** — AGENTS.md (with `--workspace-target`)

See `hermes claw migrate --help` for all options, or use the `openclaw-migration` skill for an interactive agent-guided migration with dry-run previews.

---

## Contributing

We welcome contributions! See the [Contributing Guide](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) for development setup, code style, and PR process.

Quick start for contributors — clone and go with `setup-hermes.sh`:

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
./setup-hermes.sh     # installs uv, creates venv, installs .[all], symlinks ~/.local/bin/hermes
./hermes              # auto-detects the venv, no need to `source` first
```

Manual path (equivalent to the above):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

---

## Community

- 💬 [Discord](https://discord.gg/NousResearch)
- 📚 [Skills Hub](https://agentskills.io)
- 🐛 [Issues](https://github.com/NousResearch/hermes-agent/issues)
- 🔌 [computer-use-linux](https://github.com/avifenesh/computer-use-linux) — Linux desktop-control MCP server for Hermes and other MCP hosts, with AT-SPI accessibility trees, Wayland/X11 input, screenshots, and compositor window targeting.
- 🔌 [HermesClaw](https://github.com/AaronWong1999/hermesclaw) — Community WeChat bridge: Run Hermes Agent and OpenClaw on the same WeChat account.

---

## License

MIT — see [LICENSE](LICENSE).

Built by [Nous Research](https://nousresearch.com).

