<p align="center">
  <img src="assets/banner.png" alt="Hermes-Cybernetics" width="100%">
</p>

<p align="center">
  <a href="https://hermes-agent.nousresearch.com/docs/">
    <img src="https://img.shields.io/badge/Docs-hermes--agent.nousresearch.com-FFD700?style=for-the-badge" alt="Documentation">
  </a>
  <a href="https://discord.gg/NousResearch">
    <img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord">
  </a>
</p>

<p align="center">
  <a href="https://github.com/NousResearch/hermes-agent/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT">
  </a>
  <a href="https://nousresearch.com">
    <img src="https://img.shields.io/badge/Built%20by-Nous%20Research-blueviolet?style=for-the-badge" alt="Built by Nous Research">
  </a>
  <a href="README.md">
    <img src="https://img.shields.io/badge/Lang-English-blue?style=for-the-badge" alt="English">
  </a>
</p>

**The self-improving AI agent built by [Nous Research](https://nousresearch.com).** It's the only agent with a built-in learning loop - it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions. Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop - talk to it from Telegram while it works on a cloud VM.

Use any model you want - [Nous Portal](https://portal.nousresearch.com), [OpenRouter](https://openrouter.ai) (200+ models), [NovitaAI](https://novita.ai) (AI-native cloud for Model API, Agent Sandbox, and GPU Cloud), [NVIDIA NIM](https://build.nvidia.com) (Nemotron), [Xiaomi MiMo](https://platform.xiaomimimo.com), [z.ai/GLM](https://z.ai), [Kimi/Moonshot](https://platform.moonshot.ai), [MiniMax](https://www.minimax.io), [Hugging Face](https://huggingface.co), OpenAI, or your own endpoint. Switch with `hermes model` - no code changes, no lock-in.

<table>
<tr><td><b>A real terminal interface</b></td><td>Full TUI with multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output.</td></tr>
<tr><td><b>Lives where you do</b></td><td>Telegram, Discord, Slack, WhatsApp, Signal, and CLI - all from a single gateway process. Voice memo transcription, cross-platform conversation continuity.</td></tr>
<tr><td><b>A closed learning loop</b></td><td>Agent-curated memory with periodic nudges. Autonomous skill creation after complex tasks. Skills self-improve during use. FTS5 session search with LLM summarization for cross-session recall. <a href="https://github.com/plastic-labs/honcho">Honcho</a> dialectic user modeling. Compatible with the <a href="https://agentskills.io">agentskills.io</a> open standard.</td></tr>
<tr><td><b>Scheduled automations</b></td><td>Built-in cron scheduler with delivery to any platform. Daily reports, nightly backups, weekly audits - all in natural language, running unattended.</td></tr>
<tr><td><b>Delegates and parallelizes</b></td><td>Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns.</td></tr>
<tr><td><b>Runs anywhere, not just your laptop</b></td><td>Six terminal backends - local, Docker, SSH, Singularity, Modal, and Daytona. Daytona and Modal offer serverless persistence - your agent's environment hibernates when idle and wakes on demand, costing nearly nothing between sessions. Run it on a $5 VPS or a GPU cluster.</td></tr>
<tr><td><b>Research-ready</b></td><td>Batch trajectory generation, trajectory compression for training the next generation of tool-calling models.</td></tr>
</table>

<!-- HERMES_AGENT_EVO_IDENTITY_START -->
## Hermes-Agent-Evo: Cybernetic Systems Upgrade

This fork preserves the upstream Nous Research Hermes Agent product surface while adding a governed cybernetic evolution layer for James Paul Jackson's Hermes work.

**What "Evo" means here:** Evo is not a claim of autonomy, consciousness, AGI, production readiness, or self-authorization. Evo means the repository is being upgraded into a governed cybernetic system: runtime capability plus repository orientation, evidence-bounded memory/governance, visible boot-state locks, CI closure, rollback-aware scripts, and human authorization gates.

```text
Hermes Agent          = capable actor runtime
Hermes-Agent-Evo      = Hermes runtime + RHP/HRCN/CMS governance geometry
Hermes Cybernetic Sys = evidence-bounded loop: orient -> diagnose -> plan -> test -> authorize -> seal
```

### Evo Upgrade Surface

| Surface | Upgrade |
|---|---|
| RHP | Runtime rehydration, startup evidence, visible lock sequence, degraded-safe boot status. |
| HRCN | Read-only runtime/context governance boundary for Hermes/CMS/RCC surfaces. |
| CMS | Governed memory and permission substrate, still bounded by read-only / dry-run / apply-gate phases. |
| All-One scripts | Human-authorized PowerShell + Python operations that anchor, validate, evidence, secret-scan, commit, rebase, push, and return. |
| CI closure | GitHub Tests/Lint/Nix must be green before architecture evolution. |
| Budget guard | Full rehydration is gated; compact checkpoints are the default unless drift or authorization requires more. |
| Next architecture target | `RHP-014.7 Operator dashboard bundle`. |

Non-claim lock: Hermes-Agent-Evo upgrades governance, continuity, evidence, and operator visibility. It does not grant provider/model/tool authority, CMS write authority, memory promotion, API write authority, external ingestion, autonomy, AGI/consciousness claims, production-readiness claims, or self-authorization.
<!-- HERMES_AGENT_EVO_IDENTITY_END -->

<!-- HRCN_CONTEXT_LAYER_START -->
## RCC-CMS-HRCN Runtime Governance Layer

This fork includes an internal RCC/CMS/HRCN governance layer for James Paul Jackson's Hermes work.

The upstream Hermes product README above this section is preserved. This block is additive: it explains the fork's local governance context and the read-only RHP/HRCN runtime-native boot-orientation path without granting runtime authority.

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
| HRCN v0.9 | Can future claims/actions bind to reproducible evidence before CMS nexus work? | `docs/context-layer/hrcn-v0.9-evidence-package-benchmark-harness.json` |
| HRCN v0.9.1 | Can runtime-boundary wording align to the v0.9 evidence gate before v1.0 planning? | `docs/context-layer/hrcn-v0.9.1-runtime-boundary-alignment.validation.json` |
| HRCN v1.0 | Can Hermes, RCC, CMS, HRCN, evidence, rollback, and human authorization be planned as one governed nexus? | `docs/context-layer/hrcn-v1.0-governed-hermes-cms-nexus-plan.json` |
| HRCN v1.0.1 | Can the CMS mirror/import path be authorized before any CMS copy occurs? | `docs/context-layer/hrcn-v1.0.1-cms-read-only-mirror-import-authorization-path.json` |
| HRCN v1.0.2 | Can CMS source be manifested and secret-scanned before mirror copy? | `docs/context-layer/hrcn-v1.0.2-cms-mirror-preflight-manifest.json` |
| HRCN v1.0.3 | Can CMS be copied as a read-only evidence mirror without runtime authority? | `docs/context-layer/hrcn-v1.0.3-cms-read-only-mirror-copy-evidence.json` |
| HRCN v1.1 | Can the mirrored CMS be compressed into a bounded read-only context packet for Hermes orientation? | `docs/context-layer/hrcn-v1.1-bounded-cms-context-packet.json` |
| HRCN v1.1.1 | Can HRCN restore the readable Python-backed all-one coding format after paste-safe Base64 transport? | `docs/context-layer/hrcn-v1.1.1-python-format-technique-lock.json` |
| HRCN v1.1.2 | Can HRCN close stale context-surface current-state drift before permission bridge design? | `docs/context-layer/hrcn-v1.1.2-context-surface-coherence-closure.json` |
| HRCN v1.2 | Can Hermes classify requested authority before any CMS/Hermes action or dry-run? | `docs/context-layer/hrcn-v1.2-permission-bridge-dry-run-design.json` |
| HRCN v1.3 | Can Hermes define a read-only bridge prototype over the bounded CMS packet without runtime authority? | `docs/context-layer/hrcn-v1.3-cms-hermes-read-only-bridge-prototype.json` |
| HRCN v1.4 | Can Hermes define a dry-run harness contract that simulates without applying changes? | `docs/context-layer/hrcn-v1.4-dry-run-execution-harness-contract.json` |
| HRCN v1.5 | Can Hermes define the apply gate that a future apply candidate must pass without applying now? | `docs/context-layer/hrcn-v1.5-apply-gate-contract.json` |
| HRCN v1.6 | Can Hermes create a bounded docs/context-only apply executor without granting self-authorization? | `docs/context-layer/hrcn-v1.6-limited-apply-executor.json` |
| HRCN v1.7 | Can Hermes coordinate the governed operational loop without bypassing gates or widening scope? | `docs/context-layer/hrcn-v1.7-governed-operational-loop.json` |
| HRCN v1.8 | Can Hermes harden governed operations with replay, audit, and rollback requirements? | `docs/context-layer/hrcn-v1.8-replay-rollback-hardening.json` |
| HRCN v1.9 | Can Hermes expose a human operator command surface without becoming the operator? | `docs/context-layer/hrcn-v1.9-operator-dashboard-command-surface.json` |
| HRCN v2.0 | Can Hermes-CMS be sealed as operational for bounded docs/context governance only? | `docs/context-layer/hrcn-v2.0-operational-hermes-cms-nexus.json` |

Current public finding: Hermes provides the actor/runtime body. RCC provides repository orientation. CMS provides governed memory, repair, dry-run, apply-gate, rollback, evidence, and permission boundaries. HRCN is the bridge contract between those surfaces and human authorization.

<!-- HERMES_CURRENT_PUBLIC_METRICS_START -->
### Current Public Metrics

| Metric | Current value |
|---|---|
| Latest OPS bridge proof | `docs/context-layer/ops/OPS-027-final-evidence.json` |
| Current OPS status | `OPS-027 HRCN v0.3 seal and tag passed` |
| Current HRCN OPS tag | `hrcn-ops-v0.3.0` |
| Latest RHP proof | `docs/context-layer/ops/RHP-018-11-final-evidence.json` |
| Current RHP status | `RHP-018.11 V4 Top Progress Console Canon sealed; active wound preserved` |
| Previous RHP seal | `docs/context-layer/ops/RHP-018-10-final-evidence.json` |
| Previous RHP status | `RHP-018.10 Runtime Loop Order Canon sealed` |
| Current RHP state | `RUNTIME_PROGRESS_CONSOLE_CANON_ALIGNED_SUBJECT_UNRESOLVED` |
| Blocking CI/wound state preserved | `RUNTIME_LOOP_ORDER_CANON_ALIGNED_SUBJECT_UNRESOLVED` |
| Active wound class | `readiness_gate_install` |
| Active subject commit | `ddb24363e2fac630e7527a2c9eab31e6df50db52` |
| Next RHP gate | `operator_rerun_or_ingest_replacement_ci_before_repair` |
| Runtime progress console | `rhp/progress_console.py` |
| Runtime loop module | `rhp/runtime_loop.py` |
| RHPLOOP Doctor module | `rhp/loop_doctor.py` |
| Visible console renderer | `rhp/visible_console.py` |
| Runtime source authority | `False` |
| CMS write authority | `False` |
| Memory promotion authority | `False` |
| External ingestion authority | `False` |
| Autonomous authority | `False` |
| Human authorization required | `True` |

Public metrics lock: current public metrics must match latest OPS/RHP evidence before any future RHP commit. README status is subordinate to `docs/context-layer/latest-rhp.json` when a mismatch is discovered.
<!-- HERMES_CURRENT_PUBLIC_METRICS_END -->







<!-- HERMES_AI_AGENT_PREFERENCES_ENHANCEMENTS_START -->
## AI / Agent Preferences and Reflective Coding Enhancements

This section teaches future AI assistants, coding agents, and human operators how James Paul Jackson wants this repository handled.

It is appendable: future validated lessons may be added here when they improve coding accuracy, reduce drift, improve operator visibility, or strengthen evidence-bounded development.

### Agent Preference Chart

| Preference / Enhancement | Why it exists | Agent behavior required | Status / load indicator |
|---|---|---|---|
| Visible loading status | Long AI/coding operations feel opaque without progress. | Emit `RHPLOAD [000%..100%]` lines during multi-step work. | `RHPLOAD [010%] anchor repo root` |
| Targeted rehydration first | Prevent stale assumptions and README drift. | Read latest GitHub `main`, README, AGENTS.md, latest RHP evidence, and target files before scripting. | `RHPLOAD [020%] load README + AGENTS.md` |
| Minimal mutation | Over-broad edits create new failures. | Change the smallest surface that resolves the current gate. | `RHPLOAD [060%] plan minimal mutation` |
| Test stale tests as surfaces | Failed CI can come from old tests, not broken runtime. | Repair tests when implementation evolved and evidence proves the new surface. | `RHPLOAD [080%] run focused tests` |
| Evidence before claim | Claims must be backed by JSON, logs, hashes, or test output. | Write final evidence and cite it before calling a phase sealed. | `RHPLOAD [090%] write evidence` |
| Inaction can be correct | Agents often over-edit. | If no mutation is required, say so and seal a no-op diagnostic instead of forcing code. | `status=no-op-valid` |
| Runtime authority lock | This repo has many agent/provider surfaces. | Never imply provider/model/tool/CMS/memory/API/external-ingestion authority without explicit bounded evidence. | `authority=false` |
| Appendable learning surface | The process should improve as failures reveal missing guards. | Add concise lessons to this section and AGENTS.md only after validation. | `lesson=validated` |

### Load Status Contract

Use this visible grammar in All-One scripts, long-running coding passes, and AI handoffs:

```text
RHPLOAD [000%] initialize runner | status=running
RHPLOAD [010%] anchor repo root + pull origin/main | status=ok
RHPLOAD [020%] load README.md + AGENTS.md | status=ok
RHPLOAD [030%] load latest RHP evidence | status=ok
RHPLOAD [040%] load target runtime/docs/test surfaces | status=ok
RHPLOAD [050%] validate authority boundary | status=ok
RHPLOAD [060%] plan minimal mutation | status=ok
RHPLOAD [070%] apply bounded mutation | status=running
RHPLOAD [080%] run compile/tests/guards | status=running
RHPLOAD [090%] write evidence + hashes + staged secret scan | status=running
RHPLOAD [100%] commit/push/return clean | status=ok
```

### How Future Agents May Add To This Section

Add a new row only when all are true:

1. A real failure, inefficiency, or operator need was observed.
2. The lesson is specific enough to change future behavior.
3. The lesson does not grant new authority.
4. The lesson is reflected in AGENTS.md if it affects coding agents.
5. Evidence is written under `docs/context-layer/ops/`.

Boundary: this section teaches coding preferences and process enhancements. It is not a runtime authority grant and does not authorize provider/model/tool execution, CMS writes, memory promotion, API writes, external ingestion, autonomy, production-readiness claims, or self-authorization.
<!-- HERMES_AI_AGENT_PREFERENCES_ENHANCEMENTS_END -->

<!-- RHP_OPERATOR_BOOTSTRAP_START -->
## RHP Operator Bootstrap: Current Canon

This repository must be operated from the sealed RHP state, not from intuition, memory, or stale README text.

### Source-of-truth order

1. Read `docs/context-layer/latest-rhp.json`.
2. Read the `latest_evidence` file named by `latest-rhp.json`.
3. Read `docs/context-layer/operator-dashboard.txt`.
4. Read `docs/context-layer/hermes-operator-context.json`.
5. Follow `next_operation`.
6. Run `RHPREADY` before any mutation when the current state permits mutation.
7. Never mutate outside a human-authorized All-One script.

### Core execution law

```text
Hermes thinks and displays.
RHP gates.
All-One acts.
Evidence remembers.
Human authorizes.
```

### Current RHP loop states

| State | Meaning | Legal next action |
|---|---|---|
| `CI_RECONCILED_GREEN` | Named subject commit is green and integrated. | Bounded evolution may proceed after RHPREADY. |
| `READINESS_GATE_INSTALLED_REMOTE_UNKNOWN` | Local readiness gate installed, current operation CI not yet observed. | Observe current operation CI through loop kernel. |
| `CI_PENDING` | Named subject CI is not final. | Wait or ingest final CI result. |
| `CI_RED_WOUND_OPEN` | Named subject CI is red. | Create CI wound packet before repair. |
| `CI_WOUND_PACKET_OPEN_LOGS_REQUIRED` | Wound exists but failed logs are not sufficient. | Ingest failed/cancelled CI logs. |
| `CI_LOGS_INGESTED_CANCELLED_JOB_REVIEW_REQUIRED` | Logs show cancellation, not deterministic failure. | Review cancellation before repair. |
| `CI_CANCELLATION_REVIEWED_RERUN_REQUIRED` | Cancellation reviewed; no code repair basis exists. | Rerun or ingest replacement CI before repair. |
| `README_OPERATOR_BOOTSTRAP_ALIGNED_RERUN_REQUIRED` | README/AGENTS loop instructions are aligned while active wound remains open. | Rerun or ingest replacement CI before repair. |

### Non-negotiable invariants

```text
No claim without subject.
No mutation without human authorization.
No local seal implies remote green.
No green claim for the current operation commit from inside that same commit.
Unknown is not pass.
Pending is a named state, not failure.
Red becomes wound packet.
Cancelled CI is not a code failure.
Warnings are not repair warrants.
Green reconciles the named subject commit only.
No autonomous authority.
```

### Subject/base distinction

```text
subject_commit:
  The commit whose CI/state is being observed.

operation_base_commit:
  The current HEAD from which the new RHP operation is sealed.

These may differ during historical CI observation.
```

### Failure handling

```text
Raw traceback must not be normal operator output.
Expected/classifiable failures render as RHPDIAG boxes.
Raw logs belong in raw artifacts.
Repair proposals are no-execution until human-authorized.
```

### Post-seal residue rule

```text
Before commit:
  repo evidence files may be written under docs/context-layer/ops/.

After commit/push:
  command streams, sealed-head files, final summaries, and raw command outputs go to temp only.

Post-seal repo residue is a hygiene failure and must be cleaned before continuing.
```

### CI repair rule

```text
A red or cancelled CI state does not automatically authorize repair.

Repair requires:
  1. commit-scoped CI observation,
  2. wound packet,
  3. failed log ingestion,
  4. deterministic failure surface,
  5. bounded repair proposal,
  6. human-authorized All-One execution.
```

Non-claim lock: this bootstrap teaches future agents how to preserve the RHP loop. It does not close the active wound, rerun CI, repair code, grant provider/model/tool/CMS/memory/API authority, or authorize autonomous action.
<!-- RHP_OPERATOR_BOOTSTRAP_END -->


<!-- RHP_VISIBLE_DEBUG_LOOP_CANON_START -->
## RHP Visible Debug Loop Canon

RHP is not only a governance loop. RHP is an observability loop, a debugging loop, and an operator-trust loop.

Every future All-One operation should expose named stages instead of compressing failures into a vague script failure.

### Required visible stages

| Stage | Debug question |
|---|---|
| `ENTRYPOINT-GATE` | Did we run the correct file as a file invocation? |
| `ROOT-ANCHOR` | Are we inside the correct repository root? |
| `RESIDUE-MANAGER` | Is the worktree clean or is residue bounded/classified before start? |
| `PREAUTH-PULL` | Did `origin/main` integrate before authorization? |
| `HUMAN-AUTHORIZATION` | Did the human explicitly authorize this bounded operation? |
| `RHPREADY` | Is this operation legal from the current sealed RHP state? |
| `OPERATION-START` | Did the bounded operation begin inside the declared scope? |
| `RHPDROP` | Where is the compact command summary / raw artifact index? |
| `RHPDIAG` | What class of failure occurred, and where is the raw artifact? |
| `VALIDATION` | Did compile/tests/evidence compatibility pass? |
| `SECRET-SCAN` | Did the staged diff avoid forbidden credential-like material? |
| `COMMIT-SEAL` | Did the local evidence seal commit? |
| `PUSH-SEAL` | Did the remote publication succeed? |
| `POST-SEAL-RESIDUE` | Did command streams or raw outputs leak into repo after commit? |
| `RETURN-ROOT` | Was the operator returned to the repository root? |

### Debugging law

```text
If a script can fail, it needs a named RHP stage.
If a stage can fail, it needs a raw artifact.
If a raw artifact exists, the terminal should show an RHPDIAG box.
If the operation seals, the final state must update latest-rhp.json.
```

### Visibility doctrine

```text
RHP is not only a governance loop.
RHP is an observability loop.
RHP is a debugging loop.
RHP is an operator-trust loop.
```

Non-claim lock: this canon improves operator visibility and future debugging discipline. It does not close the active wound, repair code, rerun CI, grant authority, or authorize autonomous action.
<!-- RHP_VISIBLE_DEBUG_LOOP_CANON_END -->


<!-- RHP_UNCOMPRESSED_OPERATOR_CONSOLE_CANON_START -->
## RHP Uncompressed Operator Console Canon

RHP must remain visibly debuggable. Do not compress the operator loop until the human loses the ability to see where the system is thinking, gating, diagnosing, sealing, and reflecting.

### Console doctrine

```text
RHP is not only a governance loop.
RHP is an observability loop.
RHP is a debugging loop.
RHP is an operator-trust loop.
```

### Required panel families

| Panel | Tone | Purpose |
|---|---|---|
| `RHPLOAD` | green/cyan/red | Stage progress, root anchoring, authorization, operation status, and return-root. |
| `RHPREADY` | gold | Readiness decision, state, allowed classes, active wound, and authority lock. |
| `RHPDROP` | gold/cyan | Compact command summary with raw artifact index. |
| `RHPDIAG` | magenta/red | Failure class, symptom, raw artifact, likely cause, and next repair route. |
| `RHPDEBUG` | gold | Debug-canon alignment, visible-stage preservation, and state-machine learning. |
| `RHPREFLECT` | gold | Human-readable reflection: what happened, what it means, what was learned, and what remains blocked. |
| `HUMAN-UI-SUMMARY` | green/gold | Final operator summary: latest state, active wound, subject, repair basis, blocked actions, and next legal operation. |

### Minimum fields for expandable/drop-panel output

```text
stage
decision
state
evidence
raw artifact
authority
repair basis
blocked actions
next operation
```

### Gold reflection requirement

Use gold/yellow emphasis for diagnostic and reflective panels, especially:

```text
RHPREADY [DIAGNOSTIC]
RHPDROP [closed]
RHPDEBUG [ALIGNED]
RHPREFLECT [GOLD]
HUMAN-UI-SUMMARY
```

### End-of-operation reflection summary

Every non-trivial All-One should end with a human-readable reflection panel:

```text
RHPREFLECT [GOLD] status=aligned
`- operator reflection summary
   +- what-happened: <plain English event>
   +- what-it-means: <state-machine interpretation>
   +- what-we-learned: <new invariant or preserved rule>
   +- active-wound: <wound class or none>
   +- repair-basis: true|false
   +- blocked-actions: <what remains forbidden>
   +- next: <next legal operation>
   `- authority: no grant [LOCKED]
```

Non-claim lock: this canon improves operator visibility and debugging comprehension. It does not close wounds, repair code, rerun CI, grant authority, or authorize autonomous action.
<!-- RHP_UNCOMPRESSED_OPERATOR_CONSOLE_CANON_END -->


<!-- RHPLOOP_DOCTOR_SELF_LEARNING_CANON_START -->
## RHPLOOP Doctor and Self-Learning Canon

RHP has two explicit meta-loops that must stay visible:

```text
RHPLOOP-DOCTOR
  read -> inspect -> classify -> summarize blocked reasons -> propose next lawful operation
  mutation: false

RHPLOOP-SELF-LEARNING
  observe friction/failure -> bind evidence -> propose future behavior rule -> preserve authority boundary
  mutation: documentation/evidence only unless separately authorized
```

### RHPLOOP-DOCTOR

The Doctor loop is the read-only cockpit. It does not heal directly. It tells the operator what is true, what is blocked, and what legal operation comes next.

Required Doctor surfaces:

```text
rhp/rhpload_doctor.py
rhp/doctor_cli.py
rhp/loop_doctor.py
docs/context-layer/latest-rhp.json
docs/context-layer/<latest evidence>
```

Required Doctor panel:

```text
RHPLOOP-DOCTOR [GOLD] status=diagnostic
`- read-only loop doctor cockpit
   +- latest-operation: <latest RHP operation>
   +- state: <derived/current state>
   +- evidence-api-ok: true|false
   +- replay-ok: true|false
   +- worktree-clean: true|false
   +- can-mutate: false
   +- blocked-reasons: <reasons>
   +- next: <next lawful operation>
   `- authority: no grant [LOCKED]
```

### RHPLOOP-SELF-LEARNING

Self-learning means the environment learns by preserving validated operational lessons. It does not mean autonomous mutation, memory promotion, or self-authorization.

A self-learning candidate must name:

```text
observed_event
evidence_path
lesson
future_behavior_change
authority_boundary
```

Required self-learning panel:

```text
RHPLOOP-SELF-LEARNING [GOLD] status=proposed|blocked
`- validated lesson candidate
   +- observed-event: <what happened>
   +- evidence: <artifact path>
   +- lesson: <what was learned>
   +- future-behavior: <how future operations change>
   +- classification: promotable_lesson_candidate|blocked_learning_candidate
   +- authority: no grant
   `- promotion: evidence-gated / human-authorized [LOCKED]
```

### Self-learning law

```text
No lesson without evidence.
No evidence, no promotion.
No promotion that grants autonomous authority.
No learning rule that bypasses RHPREADY, RHPDIAG, RHPDROP, or human authorization.
The environment may become smarter without becoming sovereign.
```

Non-claim lock: RHPLOOP Doctor and Self-Learning are read/classify/propose/preserve loops. They do not repair, rerun CI, close wounds, mutate dependencies, grant authority, or self-authorize.
<!-- RHPLOOP_DOCTOR_SELF_LEARNING_CANON_END -->


<!-- RHP_RUNTIME_LOOP_ORDER_CANON_START -->
## RHP Runtime Loop Order Canon

The self-learning loop is not only a documentation section. It must appear as a runtime loop panel before reflection and before the final human summary.

### Canonical runtime order

```text
ENTRYPOINT-GATE
ROOT-ANCHOR
RESIDUE-MANAGER
PREAUTH-PULL
HUMAN-AUTHORIZATION
RHPREADY
OPERATION-START
RHPLOOP-DOCTOR
RHPLOOP-SELF-LEARNING
VALIDATION
SECRET-SCAN
COMMIT-SEAL
PUSH-SEAL
RHPDROP
RHPREFLECT
POST-SEAL-RESIDUE
RETURN-ROOT
HUMAN-UI-SUMMARY
```

### Runtime loop law

```text
Doctor classifies before Self-Learning.
Self-Learning records lessons before Reflection.
Reflection interprets before Human Summary.
Human Summary closes the operator-visible turn.
```

### Diagnostic nonzero rule

```text
Some read-only diagnostic tools intentionally return nonzero when they find a blocked state.

If the tool emits valid JSON evidence:
  diagnostic nonzero is not a hard failure.

If the tool emits no valid evidence:
  nonzero is a hard failure.
```

Known diagnostic-nonzero surfaces:

```text
rhpready-diagnostic
doctor-cli-readonly
```

### Required runtime panels

```text
RHPLOOP-RUNTIME [GOLD]
RHPLOOP-DOCTOR [GOLD]
RHPLOOP-SELF-LEARNING [GOLD]
RHPDROP [closed]
RHPREFLECT [GOLD]
HUMAN-UI-SUMMARY [GOLD]
```

Non-claim lock: this canon changes operator visibility and command classification only. It does not repair, rerun CI, close wounds, grant authority, or self-authorize.
<!-- RHP_RUNTIME_LOOP_ORDER_CANON_END -->


<!-- RHP_RUNTIME_PROGRESS_CONSOLE_CANON_START -->
## RHP Runtime Progress Console Canon

RHP must show operator progress as one live top progress surface, not as noisy printed animation frames.

Every runtime should prefer a single global progress bar, then emit concise settled panels:

```text
Write-Progress activity=<operation> percent=<percent> status=<stage>
RHPLOAD [035%] loop=RHPREADY operation=<operation> | status=<status>
`- settled: <human detail>
```

### Required progress surfaces

```text
percentage
single global top progress bar
percentage
current stage
status
concise settled panel
human-readable detail
```

### Canonical progress order

| Stage | Percent |
|---|---:|
| `ENTRYPOINT-GATE` | 005% |
| `ROOT-ANCHOR` | 010% |
| `RESIDUE-MANAGER` | 015% |
| `PREAUTH-PULL` | 020% |
| `RHPLOOP-RUNTIME` | 025% |
| `HUMAN-AUTHORIZATION` | 030% |
| `RHPREADY` | 035% |
| `OPERATION-START` | 040% |
| `RHPLOOP-DOCTOR` | 050% |
| `RHPLOOP-SELF-LEARNING` | 060% |
| `VALIDATION` | 070% |
| `SECRET-SCAN` | 078% |
| `COMMIT-SEAL` | 084% |
| `PUSH-SEAL` | 090% |
| `RHPDROP` | 094% |
| `RHPREFLECT` | 097% |
| `POST-SEAL-RESIDUE` | 098% |
| `RETURN-ROOT` | 099% |
| `HUMAN-UI-SUMMARY` | 100% |

### Progress law

```text
Progress must move in one global top bar, not by flooding the terminal with frame lines.
If a stage can fail, its settled panel must include percent, status, detail, and raw artifact route.
If Self-Learning occurs, it must have its own progress checkpoint before Reflection and Human Summary.
```

Non-claim lock: progress console canon changes operator visibility only. It does not repair, rerun CI, close wounds, mutate dependencies, grant authority, or self-authorize.
<!-- RHP_RUNTIME_PROGRESS_CONSOLE_CANON_END -->


<!-- HERMES_OPERATIONAL_LOOP_BOXES_START -->
## Operational Loop Boxes and AI Takeover Runbook

This section tells a future AI agent exactly which loop to run before it edits the repository.

The word "takeover" here means procedural continuity, not autonomous authority. A coding agent may continue the work only by selecting the correct bounded loop, showing `RHPLOAD` progress, validating evidence, and stopping at the next human gate.

### Loop Registry Chart

| Loop box | Trigger | Required loaded surfaces | Mutation allowed | Exit condition |
|---|---|---|---|---|
| Rehydration Loop | New chat, stale context, branch drift, broken CI, or explicit request. | `README.md`, `AGENTS.md`, latest RHP evidence, latest commit/status, target files. | None unless separately authorized. | Current state summarized with evidence. |
| Diagnosis Loop | Failure log, red CI, broken script, stale docs, or user asks "assess". | Failing log/file, latest evidence, changed files, relevant tests. | None unless repair is authorized. | Failure class chosen: code defect, stale test, stale README, stale guard, flaky/env, or unknown. |
| Mutation Loop | Human authorizes a bounded change. | Target files, evidence prerequisite, matching tests. | Smallest surface only. | Focused validation passes. |
| Evidence Loop | Any operation claims completion. | Candidate diff, validation output, authority flags. | Evidence/docs only. | Final evidence JSON, closure markdown, hashes, and non-claim lock exist. |
| CI Watch Loop | Push completes or GitHub Actions turns red. | Workflow name, job name, failing file, failure output, commit SHA. | None during watch; repair requires a new bounded loop. | CI status classified as green, red-actionable, flaky-suspected, skipped-expected, or unknown. |
| CI Repair Loop | Red CI with actionable failing file. | Failing test/job output, changed files, current guard/evidence. | Only failing surface plus matching evidence/docs. | Focused local reproduction or explicit non-repro note. |
| Learning Loop | Repeated failure, operator friction, or useful new process discovery. | README preference chart, AGENTS.md, latest evidence. | Append concise preference/lesson only. | Future agents get one better rule, backed by evidence. |
| Runtime Status Loop | Hermes CLI/TUI/operator startup needs status truth. | `RuntimeBootState`, boot preflight, operator status, banner/CLI surfaces. | Runtime display surfaces only after authorization. | One visible boot truth: loaded surface, percent/status, authority=false, evidence version. |
| Security Boundary Loop | Agentic workflow, issue/PR text, external context, or generated script enters a workflow. | Untrusted input source, script sink, workflow/env permissions. | Guardrails/docs/tests only unless authorized. | Prompt/script injection route is blocked or documented as unavailable. |
| No-Op Loop | User asks to improve but repo already satisfies the gate. | Current evidence, README/AGENTS, target files. | None. | No-op diagnostic evidence or concise report. |

### AI Takeover Runbook

```text
1. Emit RHPLOAD [000%].
2. Select exactly one loop box.
3. Load only required surfaces for that loop.
4. State current authority boundary.
5. Decide: no-op, diagnose, repair, document, or implement.
6. Mutate the smallest allowed surface.
7. Run focused validation first.
8. Write evidence before claiming success.
9. Secret-scan staged added lines.
10. Commit/push only after gates pass.
11. If CI goes red, return to CI Watch Loop.
```

### Loop Status Boxes

```text
[LOOP:REHYDRATION] status=ok          output=current-state-summary
[LOOP:DIAGNOSIS]    status=ok          output=failure-class
[LOOP:MUTATION]     status=authorized  output=bounded-diff
[LOOP:EVIDENCE]     status=required    output=final-evidence-json
[LOOP:CI-WATCH]     status=required    output=green|red-actionable|flaky-suspected|unknown
[LOOP:CI-REPAIR]    status=authorized  output=focused-repair
[LOOP:LEARNING]     status=appendable   output=new-chart-row
[LOOP:RUNTIME]      status=deferred     output=RuntimeBootState-display-wiring
[LOOP:SECURITY]     status=required    output=injection-boundary-check
[LOOP:NO-OP]        status=valid        output=no-change-evidence
```

Boundary: loop boxes teach procedure. They do not grant runtime authority, provider/model/tool authority, CMS write authority, memory promotion, API write authority, external ingestion, autonomy, production-readiness claims, or self-authorization.
<!-- HERMES_OPERATIONAL_LOOP_BOXES_END -->

<!-- HERMES_RHP_013_4_RUNTIME_DISPLAY_START -->
### RHP-013.4 RuntimeBootState Display Wiring

RHP-013.4 wires the typed `RuntimeBootState` into the visible operator and banner surfaces.

```text
RuntimeBootState
-> HERMES_RHP_RUNTIME_BOOT_STATE
-> HERMES_RHP_OPERATOR_STATUS
-> HERMES_RHP_PROTOCOL_STRIP
-> HERMES_RHP_PROTOCOL_LOCKS
-> CLI stderr boot status
-> gold banner Rehydration Protocol strip
```

This is still read-only orientation. The display proves what loaded and which authority locks are false; it does not grant provider/model/tool, CMS, memory, API, external-ingestion, autonomous, or self-authorization authority.

Next: `RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run`.
<!-- HERMES_RHP_013_4_RUNTIME_DISPLAY_END -->

<!-- HERMES_RHP_013_5_CI_WATCH_START -->
### RHP-013.5 CI Watch Loop Automation + Operator Test Repair

RHP-013.5 adds a local CI Watch Loop tool and repairs the stale operator-visible startup test that still expected `evidence=RHP-012`.

```text
commit SHA -> GitHub Actions runs -> selected Tests workflow -> jobs
-> classification: green | pending | red-actionable | unknown
-> evidence packet
```

The watch loop is observational. It does not rerun jobs, edit files without authorization, write remote state, or self-authorize repairs.

Next: `RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run`.
<!-- HERMES_RHP_013_5_CI_WATCH_END -->

<!-- HERMES_RHP_013_6_RHPLOAD_FEEDBACK_START -->
### RHP-013.6 RHPLOAD Feedback Tree + CI Repair Classifier

RHP-013.6 upgrades `RHPLOAD` from a single progress line into a zero-context feedback tree.

```text
RHPLOAD [035%] loop=CI-REPAIR operation=RHP-013.6
`- [035%] All-One execution | status=running | expanded feedback tree
   +- [010%] Rehydrate | status=ok | repo root, branch, latest evidence
   +- [020%] Select loop | status=ok | CI-REPAIR
   +- [035%] Inspect target surfaces | status=running | README, AGENTS, RHP evidence, tests
   +- [060%] Mutate bounded surface | status=pending | smallest valid patch
   +- [080%] Validate | status=pending | compile, focused tests, alignment guard
   +- [090%] Seal | status=pending | evidence, hashes, secret scan
   `- [100%] Push and watch | status=pending | commit, push, CI watch
```

This gives a zero-context AI a portable process map: what loop is running, what has loaded, what remains, and which feedback should decide the next action.

RHP-013.6 also adds a CI repair classifier for failure text:

```text
stale_test_or_guard_surface
import_or_packaging_surface
timeout_or_flaky_suspected
assertion_failure_unknown
unknown
```

Next: `RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run`.
<!-- HERMES_RHP_013_6_RHPLOAD_FEEDBACK_END -->


<!-- HERMES_RHP_013_7_RHPLOAD_LIVE_START -->
### RHP-013.7 RHPLOAD Live Console Renderer + Evidence Transcript

RHP-013.7 adds `rhp/load_console.py`, which turns each RHPLOAD step into both operator-visible text and an append-only JSONL transcript.

```text
RHPLOAD [042%] validate transcript | loop=EVIDENCE operation=RHP-013.7 | status=running | jsonl
`- live feedback
   +- loaded: jsonl
   +- active: validate transcript
   `- transcript: jsonl append-ready
```

Transcript rule: every future All-One runner should be able to emit `RHPLOAD` lines, expanded feedback trees, and JSONL evidence events. This lets a zero-context AI resume from a transcript instead of guessing from terminal scrollback.

Next: `RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run`.
<!-- HERMES_RHP_013_7_RHPLOAD_LIVE_END -->


<!-- HERMES_RHP_013_8_LOOP_REGISTRY_START -->
### RHP-013.8 Loop Registry Enforcement + Transcript-Backed Resume Packet

RHP-013.8 adds the first bounded autoheal substrate without executing autoheal.

```text
RHPLOAD transcript + latest evidence
-> rhp/resume_packet.py
-> RHP-RESUME-PACKET-v0.1
-> recommended_loop
-> rhp/loop_registry.py
-> allowed next loops and attempt budget
```

Legal loops are now explicit:

```text
REHYDRATION
DIAGNOSIS
CI-WATCH
CI-REPAIR
EVOLUTION
AUTOHEAL-PLAN
AUTOHEAL-EXECUTE
NO-OP
```

Autoheal rule: plan before mutation. `AUTOHEAL-PLAN` cannot mutate or commit. `AUTOHEAL-EXECUTE` has a one-attempt budget and may only run from an approved plan with allowlisted paths.

Next: `RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run`.
<!-- HERMES_RHP_013_8_LOOP_REGISTRY_END -->



<!-- HERMES_RHP_013_9_AUTOHEAL_PREFLIGHT_START -->
### RHP-013.9 Autoheal Preflight Box + Bounded Plan Generator

RHP-013.9 adds the first visible healing reflex.

```text
RHPLOAD [003%] loop=AUTOHEAL-PREFLIGHT operation=RHP-013.9 | status=bounded_residue_detected
`- autoheal preflight box
   +- dirty paths: 3
   +- allowed residue: 3
   +- blocked paths: 0
   +- action: clean_bounded_residue_then_continue
   `- verified: false [WARN]

RHPLOAD [009%] autoheal preflight verified | status=ok [OK]
`- autoheal preflight box
   +- dirty paths: 0
   +- allowed residue: 0
   +- blocked paths: 0
   +- action: continue
   `- verified: true [OK]
```

The feature is intentionally bounded:

```text
detect dirty failed-attempt residue
classify allowed vs blocked paths
clean only allowed operation residue
verify clean
continue to pull/rebase
```

RHP-013.9 also adds `RHP-AUTOHEAL-PLAN-v0.1`. The plan generator can propose bounded fixes, but it does not execute them.

Next: `RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run`.
<!-- HERMES_RHP_013_9_AUTOHEAL_PREFLIGHT_END -->


<!-- HERMES_RHP_014_0_PUSH_GATE_START -->
### RHP-014.0 Current Script Gate + GitHub Push Box Controller

RHP-014.0 adds the missing push safety primitive.

```text
RHPLOAD [088%] loop=CURRENT-SCRIPT-GATE operation=RHP-014.0 | status=ok [OK]
`- current script gate
   +- expected: RHP_014_0_CURRENT_SCRIPT_GATE_AUTOHEAL_PUSH_CONTROLLER_SINGLE_ALL_ONE.ps1
   +- actual: RHP_014_0_CURRENT_SCRIPT_GATE_AUTOHEAL_PUSH_CONTROLLER_SINGLE_ALL_ONE.ps1
   +- evidence: RHP_014_0_CURRENT_SCRIPT_GATE_AUTOHEAL_PUSH_CONTROLLER_SINGLE_ALL_ONE.ps1
   `- verified: true [OK]
```

If the current script name does not match evidence, the script must not push. It must classify the miss, self-heal the evidence/script identity if bounded, verify `[OK]`, then continue.

The GitHub push sequence is now explicit:

```text
secret-scan -> current-script-gate -> commit -> pull-rebase -> push -> seal
```

Next: `RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run`.
<!-- HERMES_RHP_014_0_PUSH_GATE_END -->

<!-- HERMES_RHP_014_1_OPERATOR_UX_START -->
### RHP-014.1 Operator UX Compression + Dev Loop Tool Chart

RHP-014.1 formalizes the PowerShell development loop used to evolve Hermes-Agent-Evo.

Required future All-One sequence:

```text
AUTOHEAL-PREFLIGHT
PULL-REBASE
HUMAN-AUTHORIZATION
OPERATION
VALIDATION
EVIDENCE
SECRET-SCAN
WARNING-COMPRESSOR
CURRENT-SCRIPT-GATE
GITHUB-PUSH-BOX
RETURN-ROOT
```

Enhancement and tool chart:

| Box | Tool | Purpose |
|---|---|---|
| AUTOHEAL-PREFLIGHT | `rhp/autoheal_preflight.py` | Clean bounded failed-attempt residue before pull/rebase. |
| RESUME-PACKET | `rhp/resume_packet.py` | Resume from evidence and transcript without memory guessing. |
| LOOP-REGISTRY | `rhp/loop_registry.py` | Enforce legal loops, attempt budgets, and mutation/commit permissions. |
| CURRENT-SCRIPT-GATE | `rhp/current_script_gate.py` | Block push when active script and evidence mismatch. |
| WARNING-COMPRESSOR | `rhp/warning_compressor.py` | Collapse noisy CRLF warning streams into one verified box. |
| GITHUB-PUSH-BOX | `rhp/push_controller.py` | Compress commit/pull-rebase/push/seal into verified stages. |
| OPERATOR-INTERFACE | `rhp/operator_interface.py` | Render stable human-facing boxes. |

Interface rule: future scripts should compress noisy warning streams, avoid `Press Enter to close`, return to repo root, and end with a verified green seal.

Next: `RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run`.
<!-- HERMES_RHP_014_1_OPERATOR_UX_END -->

<!-- HERMES_RHP_014_2_STREAM_COLLAPSE_START -->
### RHP-014.2 Stream Collapse + Tool Candidate Matrix

RHP-014.2 fixes the remaining grey-output problem: command streams are minimized by default and raw detail is written to evidence artifacts.

Default operator view:

```text
RHPLOAD [089%] loop=STREAM-COLLAPSE operation=RHP | status=ok [OK]
`- stream collapse box
   +- total lines: 18
   +- suppressed lines: 17
   +- CRLF warnings: 12
   +- git status lines: 5
   +- raw: evidence artifact
   `- verified: true [OK]
```

Expansion rule: details are not printed by default. They are stored in `docs/context-layer/ops/<operation>/command-streams/*.txt`.

Added tool rows:

| STREAM-COLLAPSE | `rhp/stream_collapse.py` | Suppress noisy grey streams by default; raw output goes to evidence. |
| TOOL-CANDIDATE-MATRIX | `rhp/tool_candidate_matrix.py` | Tracks candidate platform tools and loop boxes for future integration. |

Next: `RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run`.
<!-- HERMES_RHP_014_2_STREAM_COLLAPSE_END -->

<!-- HERMES_RHP_014_2_V3_RESIDUE_AWARE_STREAM_START -->
### RHP-014.2 V3 Strict Stream Collapse + Residue-Aware Preflight

RHP-014.2 V3 fixes the command-stream residue edge case.

Problem observed: RHP-014.2 created post-commit command-stream artifacts after staging. A later strict run correctly blocked those as unknown dirty files.

Resolution: command-stream artifacts under the immediately previous RHP-014.2 stream-collapse operation are now classified as bounded transient residue and may be cleaned by AUTOHEAL-PREFLIGHT.

Rule:

```text
old command-stream residue -> bounded cleanup
unknown user work -> blocked
noisy command -> captured command runner
operator terminal -> boxes only
raw stream -> evidence artifact
```

Next: `RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run`.
<!-- HERMES_RHP_014_2_V3_RESIDUE_AWARE_STREAM_END -->

<!-- HERMES_RHP_014_3_CI_WOUND_DRY_RUN_START -->
### RHP-014.3 CI Wound Packet + Autoheal Executor Dry-Run + Human UI

RHP-014.3 turns failing CI/log artifacts into structured wound packets and dry-run repair plans.

```text
CI log / screenshot text / job output
-> rhp/ci_artifact_extractor.py
-> RHP-CI-WOUND-PACKET-v0.1
-> rhp/autoheal_executor_dry_run.py
-> RHP-AUTOHEAL-DRY-RUN-v0.1
-> rhp/human_ui_summary.py
-> compact operator dashboard
```

This is still dry-run only: no mutation, no commit, no remote CI action, no autonomy.

Next: `RHP-014.4 CI artifact ingestion from GitHub API + local paste fallback`.
<!-- HERMES_RHP_014_3_CI_WOUND_DRY_RUN_END -->

<!-- HERMES_RHP_014_4_CI_INGEST_START -->
### RHP-014.4 CI Artifact Ingestion + Source Router + Human UI Bridge

RHP-014.4 adds source ingestion before wound classification.

```text
local pasted text
local log file
exported GitHub JSON
optional read-only gh run view
-> RHP-CI-INGEST-v0.1
-> RHP-CI-WOUND-PACKET-v0.1
-> RHP-AUTOHEAL-DRY-RUN-v0.1
-> HUMAN-UI-SUMMARY
```

Active sources:

```text
local-paste-fallback
github-json-file
gh-cli-run-view optional read-only
```

Next: `RHP-014.5 GitHub Actions job-summary annotations + SARIF/JUnit report planning`.
<!-- HERMES_RHP_014_4_CI_INGEST_END -->

<!-- HERMES_RHP_014_5_ZERO_CONTEXT_START -->
### RHP-014.5 V6 Residue Manager + Error Box + Zero-Context Rebuild

RHP-014.5 V6 repairs the failed RHP-014.5 line and promotes residue handling into a reusable tool.

```text
RESIDUE-MANAGER
-> classifies bounded failed-run residue
-> blocks unknown user/source work
-> feeds AUTOHEAL-PREFLIGHT

ERROR-BOX
-> renders failure class
-> stores raw traceback path
-> gives next action
-> supports expandable artifact review
```

Return-root rule:

```text
Every success or failure path must Set-Location to the repository root.
```

Zero-context surfaces:

```text
docs/context-layer/latest-rhp.json
docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md
docs/context-layer/rhp_zero_context_rebuild.json
docs/context-layer/operator-dashboard.txt
docs/context-layer/hermes-operator-context.json
docs/context-layer/all-one-script-contract.md
docs/context-layer/rhp_gate_checklist.md
```

Next: `RHP-014.6 GitHub Actions job-summary annotations + SARIF/JUnit report planning`.
<!-- HERMES_RHP_014_5_ZERO_CONTEXT_END -->

<!-- HERMES_RHP_014_6_MACHINE_REPORTS_START -->
### RHP-014.6 Post-Seal Residue + Machine Reports

RHP-014.6 adds a post-seal residue observer and evidence-only machine report emitters.

```text
rhp/post_seal_residue.py              -> classifies bounded post-seal command residue
rhp/report_github_summary.py          -> GitHub job-summary Markdown output
rhp/report_junit.py                   -> JUnit XML output
rhp/report_sarif.py                   -> SARIF JSON output
rhp/machine_report_registry.py        -> machine report registry
```

Boundary:

```text
No workflow mutation.
No CI rerun.
No repair execution.
No self-authorization.
Post-seal commit/pull/push streams are volatile and externalized to avoid repo residue.
Generated Python report sources must be py_compile validated before evidence can seal.
```

Next: `RHP-014.7 Operator dashboard bundle`.
<!-- HERMES_RHP_014_6_MACHINE_REPORTS_END -->

<!-- HERMES_RHP_014_7_OPERATOR_DASHBOARD_START -->
### RHP-014.7 Operator Dashboard Bundle

RHP-014.7 makes the loop geometry readable by joining the active evidence surfaces into one operator bundle.

```text
origin      -> latest sealed evidence
axes        -> evidence, transcript, wound, dry_run, residue, authority, tools, geometry
boundary    -> human authorization
motion      -> validated delta
adaptation  -> failure classes become bounded tools before autonomy is considered
```

UI rule: `RHPLOAD` remains stable audit grammar. `RHPWAIT` is separate single-line fill progress.

Next: `RHP-014.8 Evidence coherence auditor + loop_state + rhploop doctor`.
<!-- HERMES_RHP_014_7_OPERATOR_DASHBOARD_END -->










<!-- RHP_012_3_BUDGET_GUARD_START -->
### RHP-012.3 Compact Rehydration + Budget Guard

Current status: RHP-012.3 seals the post-repair CI closure and installs compact-mode governance before RHP-013 RuntimeBootState work.

#### Default Operating Mode

| Rule | State |
|---|---:|
| Compact checkpoint by default | `True` |
| Full rehydration by default | `False` |
| Repo-wide scan requires reason | `True` |
| Long Hermes trace must be summarized before re-feed | `True` |
| Architecture evolution allowed while CI is red | `False` |
| RuntimeBootState implemented here | `False` |
| Next architecture target | `RHP-013 RuntimeBootState v0.1` |

#### Full Rehydration Gate

Full rehydration is permitted only for:

1. cold start,
2. major drift,
3. branch reset,
4. broken CI,
5. explicit human authorization.

Otherwise use a compact checkpoint: current commit, current phase, directly relevant files, exact failing tests or checks, and next bounded action.

#### Output Budget Rule

Routine analysis should stay compact. Long outputs are allowed only when exact failure logs, diffs, or evidence artifacts are necessary for repair or audit.

#### Non-Claim Lock

RHP-012.3 seals CI/budget governance only. It grants no provider/model/tool authority, CMS authority, memory promotion, API write authority, external ingestion, autonomy, AGI/consciousness claim, production-readiness claim, or self-authorization.
<!-- RHP_012_3_BUDGET_GUARD_END -->

<!-- HERMES_RHP_RUNTIME_ACTIVATION_START -->
### Rehydration Protocol Runtime Activation Track

Human summary: this fork contains a Hermes-local Rehydration Protocol substrate under `/rhp`. RHP now provides a runtime-native, operator-visible boot lock sequence. RHP-011 makes the locks visible to the human before interaction: evidence, HRCN boundary, alignment, startup packet, authority=false, external_ingestion=false, provider/model/tool=false, and CMS/memory/API=false.

#### RHP Activation Chart

| Stage | Meaning | Status |
|---|---|---:|
| RHP-007 | First governed RHP -> HRCN -> Hermes proposal-loop proof. | passed |
| RHP-008 | Proposal-loop negative-control and apply-gate boundary proof. | passed |
| RHP-009 | Runtime boot preflight integration. | passed |
| RHP-010 | Runtime-native boot interconnect. | passed |
| RHP-011 | Operator-visible startup lock sequence. | passed |
| RHP-011.1 | Gold interface Rehydration Protocol strip. | passed |
| RHP-011.2 | README geometry and evidence hygiene closure. | passed |
| RHP-012 | Safe boot failure mode and degraded startup status. | passed |
| RHP-013.1 | RuntimeBootState v0.1 typed packet. | passed |
| RHP-013.2 | AI/agent preferences and CI stale-test repair. | passed |
| RHP-013.3 | Operational loop boxes and AI takeover runbook. | passed |
| RHP-013.4 | Wire CLI/banner/operator surfaces to RuntimeBootState status. | passed |

#### Runtime Boot Order

```text
Hermes executable starts
-> hermes_cli/main.py loads
-> runtime-native RHP hook sets read-only orientation gates unless disabled
-> RHP boot preflight checks latest local evidence
-> HRCN read-only boundary is checked
-> alignment guard is checked
-> operator-visible lock sequence is rendered
-> RHP/HRCN context gates are available before agent initialization
-> agent_init appends read-only boot/context packets
-> Hermes enters interaction mode already oriented
```

#### Operator-Visible Lock Sequence

```text
RHP rehydration sequence:
[OK] repo root found
[OK] RHP-013.4 evidence green
[OK] HRCN boundary green
[OK] alignment guard green
[OK] startup packet created
[OK] authority=false
[OK] external_ingestion=false
[OK] provider/model/tool execution=false
[OK] CMS/memory/API write=false
RHP rehydration complete: ok | phase=pre-interaction | evidence=RHP-013.4
```

#### Current Boundary

| Surface | Current state |
|---|---|
| Runtime-native boot hook | `hermes_cli/main.py` |
| Operator-visible status | `rhp/operator_startup_status.py` |
| RHP boot preflight | `rhp/boot_preflight.py` |
| Startup context packet | `rhp/startup_context_packet.py` |
| Agent init integration | `agent/agent_init.py` |
| RHP native boot gate | `HERMES_RHP_NATIVE_BOOT` |
| RHP boot preflight gate | `HERMES_RHP_BOOT_PREFLIGHT` |
| RHP context gate | `HERMES_RHP_CONTEXT` |
| HRCN context gate | `HERMES_HRCN_CONTEXT` |
| Real write authority | `False` |
| CMS/memory authority | `False` |
| External ingestion authority | `False` |
| Autonomous authority | `False` |
| Latest RHP evidence | `docs/context-layer/ops/RHP-013-4-final-evidence.json` |

#### Failure-Learning Lock

| Lesson | Rule |
|---|---|
| RHP-L-029 | Runtime rehydration must be human-visible as a lock-by-lock startup sequence, not only an internal environment state. |
| RHP-L-030 | Operator-visible startup output must be ASCII-safe unless terminal encoding is explicitly verified. |
| RHP-L-031 | UI/dashboard surfaces should consume the same startup status packet as CLI startup to avoid divergent status truth. |
| RHP-L-032 | ASCII render guards must scope to managed RHP output blocks unless the operation explicitly cleans the full upstream file. |
| RHP-L-033 | When encoded banner text survives exact-string replacement, replace the whole managed hook region from markers instead of patching a single line. |
| RHP-L-034 | Managed-region replacement must use marker-safe or regex-safe block replacement; PowerShell Split is not safe for source surgery. |
| RHP-L-035 | Never commit raw broken-file debug captures unless they pass the same credential/trigger scan; prefer sanitized failure summaries. |
| RHP-L-036 | Every All-One, smoke, repair, and seal script must include progress telemetry with percent, branch, command, output, timeout, and copy-back failure block. |
| RHP-L-037 | Large generated scripts must run as files with `powershell.exe -NoProfile -ExecutionPolicy Bypass -File`, not as pasted interactive bodies. |
| RHP-L-038 | PowerShell script runners must avoid `$Args` / `$args` parameter names because they collide with automatic variables and can erase argv surfaces. |
| RHP-L-039 | Pytest absence is not a failing gate unless pytest is declared as a repo dependency; use focused direct smoke as the governed fallback. |
| RHP-L-040 | External command runners must print `argv_count`, command, output path, and timeout before execution. |
| RHP-L-041 | Scratch proof files must be either intentionally tracked or cleaned before the next RHP gate. |
| RHP-L-042 | Missing or invalid evidence must produce degraded visible startup status, not a crash, false-green state, or authority expansion. |
| RHP-L-043 | Safe boot negative controls must prove authority remains false while status degrades. |
| RHP-L-044 | Runtime evidence text must not remain stale after evidence version advances; operator-visible status, banner strip, and startup packet labels must align. |
| RHP-L-045 | Hermes has multiple banner surfaces; patches must bind both early boot stream and compact CLI gold banner renderer. |

AI lock: No future AI thread may claim write authority, tool authority, CMS authority, memory promotion, external ingestion, autonomous operation, AGI, consciousness, production readiness, or self-authorization from RHP-013.3.

Human lock: RHP may orient Hermes at boot only through read-only preflight and visible context packets. Apply/write remains separate and human-gated.

#### RHP-011.2 Geometry Closure

RHP-011.2 closes README geometry and evidence hygiene after the RHP-011.1 gold-interface Rehydration Protocol phase transition.

```text
RHP-011.1 made the runtime truth visible.
RHP-011.2 makes the repository truth agree everywhere.
```

Boundary: documentation/evidence alignment only. No provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.


#### RHP-012 Safe Boot Degraded Status

RHP-012 adds safe degraded startup status. Missing or invalid evidence, failed alignment, or unavailable boundary evidence must render visibly degraded startup state without granting authority.

```text
green evidence -> verified startup
missing evidence -> degraded startup
degraded startup -> authority remains false
```

Boundary: startup safety/status only. No provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.


#### RHP-012.1 CLI Visible Rehydration Text Alignment

RHP-012.1 repairs the live CLI surface after RHP-012 sealed. The operator-visible startup text now reports `evidence=RHP-012`, exposes the Rehydration Protocol strip in the CLI stream, and preserves degraded/verified status without authority expansion.

Boundary: display/text alignment only. No provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.


#### RHP-012.2 Compact CLI Gold Banner Strip

RHP-012.2 binds the compact `$NOUS HERMES - AI Agent Framework` banner in `cli.py` to the RHP Rehydration Protocol strip. The early boot stream was already correct after RHP-012.1; this patch closes the second visible surface.

Boundary: compact banner display only. No provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.

<!-- RHP_013_1_RUNTIMEBOOTSTATE_START -->
#### RHP-013.1 RuntimeBootState v0.1

RHP-013.1 adds the first typed `RuntimeBootState` packet in `rhp/startup_context_packet.py` and aligns boot preflight / alignment guard to the current RHP-013.1 evidence surface.

```text
StartupContextPacket -> RuntimeBootState -> future shared CLI/banner/operator truth
```

Boundary: RHP-013.1 adds a typed read-only state object and direct tests only. It does not wire new runtime consumers, call providers/models/tools, write CMS or memory, write APIs, perform external ingestion, grant autonomy, or self-authorize.
<!-- RHP_013_1_RUNTIMEBOOTSTATE_END -->

<!-- HERMES_RHP_RUNTIME_ACTIVATION_END -->









<!-- HRCN_OPS_OPERATIONAL_BRIDGE_STATUS_START -->
### HRCN OPS Operational Bridge Status

Human summary: HRCN OPS v0.3 remains sealed as the evidence boundary for read-only runtime/proposal orientation. OPS is the historical bridge ledger. RHP is the active runtime-threshold track and is current through RHP-013.3.

Current bridge status: HRCN v2.0 + OPS-027 + RHP-013.3 = read-only runtime-native boot orientation with persistent Rehydration Protocol visibility and safe degraded startup status through direct Hermes executable startup.

#### OPS / RHP Bridge Chart

| Stage | Meaning | Status |
|---|---|---:|
| OPS-027 | HRCN v0.3 seal and tag. | passed |
| RHP-004 | HRCN bridge evidence anchor aligned to OPS-027 / v0.3. | passed |
| RHP-005 | Generated-source and test-contract guard. | passed |
| RHP-006 | README/state/bridge/evidence alignment guard. | repaired |
| RHP-006.1 | Public metrics alignment closure. | passed |
| RHP-007 | Governed proposal-loop proof. | passed |
| RHP-008 | Apply-gate negative-control proof. | passed |
| RHP-009 | Runtime boot preflight integration. | passed |
| RHP-010 | Runtime-native boot interconnect. | passed |
| RHP-011 | Installed launcher smoke and operator-visible startup status. | passed |
| RHP-011.1 | Gold interface Rehydration Protocol strip. | passed |
| RHP-011.2 | README geometry and evidence hygiene closure. | passed |
| RHP-012 | Safe boot failure mode and degraded startup status. | passed |
| RHP-013.1 | RuntimeBootState v0.1 typed packet. | passed |
| RHP-013.2 | AI/agent preferences and CI stale-test repair. | passed |
| RHP-013.3 | Operational loop boxes and AI takeover runbook. | passed |
| next | RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run. | next |

#### Current Runtime Boundary

| Surface | Current state |
|---|---|
| Runtime code changed by RHP boot-orientation work | `True` |
| Default runtime authority changed | `False` |
| Runtime authority granted | `False` |
| Context injection default enabled by direct startup | `Read-only proposal orientation only` |
| Native boot gate | `HERMES_RHP_NATIVE_BOOT` |
| Boot preflight gate | `HERMES_RHP_BOOT_PREFLIGHT` |
| HRCN context injection gate | `HERMES_HRCN_CONTEXT` |
| RHP context injection gate | `HERMES_RHP_CONTEXT` |
| Latest OPS proof | `docs/context-layer/ops/OPS-027-final-evidence.json` |
| Latest RHP proof | `docs/context-layer/ops/RHP-013-4-final-evidence.json` |
| Current RHP status | `RHP-013.3 operational loop boxes and AI takeover runbook sealed` |
| Next gate | `RHP-014.3 CI red-job artifact extractor + autoheal executor dry-run` |

AI lock: No future AI thread may claim runtime authority, CMS write authority, memory write authority, API write authority, autonomous authority, production readiness, sentience, consciousness, AGI, ASI, or self-authorization from OPS-027/RHP-013.3.

Human lock: OPS v0.3 is sealed as evidence. RHP remains the active runtime-threshold track. Apply/write remains a separate human-gated transition.
<!-- HRCN_OPS_OPERATIONAL_BRIDGE_STATUS_END -->


<!-- HRCN_POST_SEAL_CYBERNETIC_TRACK_START -->
### Post-Seal Cybernetic-Memory Online Track

Current post-seal state: RHP-013.3 operational loop boxes and AI takeover runbook sealed. HRCN OPS v0.3 is sealed; RHP is the active runtime-threshold track.

OPS has served its role as the HRCN evidence ledger through v0.3. RHP carries the live boot-order, rehydration, generated-source, test-contract, alignment-guard, public-metrics, boot-preflight, startup-packet, and runtime-native entrypoint track.

| Stage | Meaning | Status |
|---|---|---:|
| OPS-027 | v0.3 seal and tag. | passed |
| RHP-001 | Hermes-local rehydration substrate. | passed |
| RHP-002 | Mini README and failure-learning lock. | passed |
| RHP-003 | Runtime startup/proposal smoke. | passed |
| RHP-004 | HRCN bridge anchor alignment and test-contract migration repair. | repaired |
| RHP-005 | Generated-source and test-contract guard. | passed |
| RHP-006 | README/state/bridge/evidence alignment guard and self-reference repair. | repaired |
| RHP-006.1 | Public metrics and post-seal README alignment closure. | passed |
| RHP-007 | First governed RHP -> HRCN -> Hermes proposal-loop proof. | passed |
| RHP-008 | Apply-gate negative-control proof. | passed |
| RHP-009 | Runtime boot preflight integration. | passed |
| RHP-010 | Runtime-native boot interconnect. | passed |
| RHP-011 | Installed launcher smoke and operator-visible startup status. | passed |
| RHP-011.1 | Gold interface Rehydration Protocol strip. | passed |
| RHP-011.2 | README geometry and evidence hygiene closure. | passed |
| RHP-012 | Safe boot failure mode and degraded startup status. | passed |
| RHP-013.1 | RuntimeBootState v0.1 typed packet. | passed |
| RHP-013.2 | AI/agent preferences and CI stale-test repair. | passed |
| RHP-013.3 | Operational loop boxes and AI takeover runbook. | passed |
| RHP-013.4 | Wire CLI/banner/operator surfaces to RuntimeBootState status. | passed |

Operational bridge target:

```text
Hermes executable
-> hermes_cli/main.py
-> RHP native boot hook
-> RHP boot preflight
-> startup context packet
-> read HRCN bounded-loop status
-> refuse authority drift
-> inject read-only RHP/HRCN orientation into proposal context
-> proposal/dry-run/apply only if separately human-gated
```

Post-seal lock: RHP-011.1 adds persistent gold-interface Rehydration Protocol visibility only. It does not execute CMS, write CMS, write memory, write APIs, change dependencies, call a provider/model, grant tool authority, operate autonomously, or self-authorize.
<!-- HRCN_POST_SEAL_CYBERNETIC_TRACK_END -->

















### Human Director Box

#### What this fork is

This fork is a local-first Hermes Agent workspace prepared for governed agent evolution:

```text
Hermes runtime -> repository orientation -> proposal classification
-> dry-run / evidence -> CMS permission boundary -> human authorization
```

Hermes already supplies CLI/TUI, model routing, tools, skills, memory hooks, terminal backends, gateway surfaces, scheduler, and documentation. HRCN adds a repository-governance map before any direct runtime bridge is attempted.

#### What this fork is not

This fork does not prove Hermes correctness, CMS correctness, code correctness, security, production readiness, external validation, AGI, ASI, consciousness, sentience, autonomy, or self-awareness. Through OPS-010, the fork has proven bounded local runtime smoke, a human-authorized provider gate, read-only HRCN context injection, read-only CMS/HRCN mirror packet rehearsal, negative-control authority refusal, replay/rollback evidence packaging, and operational release sealing. It still does not grant CMS write authority, memory write authority, API write authority, runtime mutation authority, dependency mutation authority, autonomous authority, production readiness, AGI, ASI, consciousness, sentience, or self-authorization.

### Current Public Metrics

| Surface | Result |
|---|---:|
| Current checkpoint | `HRCN v2.0` |
| Previous validated anchor | `HRCN v1.9` |
| Runtime code changed | `True - post-seal read-only bridge/proposal-context hook; default behavior remains false` |
| Dependency files changed by HRCN | `False` |
| README pointer present | `True` |
| Context layer doc | `docs/context-layer/rcc-cms-hrcn.md` |
| Context layer mini README | `docs/context-layer/README.md` |
| Rehydration protocol | `docs/context-layer/hermes-agent-rehydration-protocol.md` |
| Profile map | `docs/context-layer/hrcn-profile-map.json` |
| Runtime evolution boundary | `docs/context-layer/hrcn-runtime-evolution-boundary.md` |
| CMS root intake plan | `docs/context-layer/cms-root-intake-plan.md` |
| Surface boundary map | `docs/context-layer/hermes-surface-boundary-map.json` |
| Validation report | `docs/context-layer/hrcn-v2.0.validation.json` |
| Latest OPS bridge proof | `docs/context-layer/ops/OPS-027-final-evidence.json` |
| Current OPS status | `OPS-027 HRCN v0.3 seal and tag passed` |
| Release tag | `hrcn-ops-v0.1.0` |
| Bounded loop tag | `hrcn-ops-v0.2.0` |
| Latest post-seal proof | `docs/context-layer/ops/RHP-013-4-final-evidence.json` |
| Post-seal status | `RHP-013.3 operational loop boxes and AI takeover runbook sealed` |
| Next post-seal gate | `RHP-013.4 RuntimeBootState display wiring` |
| Mini README profiles | `full / compact / pointer` |
| Agent rehydration packet contract | `docs/context-layer/hrcn-v0.3-agent-rehydration-packet-contract.json` |
| CMS read-only bridge design | `docs/context-layer/hrcn-v0.4-cms-read-only-bridge-design.json` |
| Memory permission adapter design | `docs/context-layer/hrcn-v0.5-memory-permission-adapter-design.json` |
| Repair recommendation adapter design | `docs/context-layer/hrcn-v0.6-repair-recommendation-adapter-design.json` |
| Dry-run adapter design | `docs/context-layer/hrcn-v0.7-dry-run-adapter-design.json` |
| Apply-gate adapter design | `docs/context-layer/hrcn-v0.8-apply-gate-adapter-design.json` |
| Evidence package and benchmark harness | `docs/context-layer/hrcn-v0.9-evidence-package-benchmark-harness.json` |
| Governed Hermes-CMS nexus plan | `docs/context-layer/hrcn-v1.0-governed-hermes-cms-nexus-plan.json` |
| CMS read-only mirror authorization path | `docs/context-layer/hrcn-v1.0.1-cms-read-only-mirror-import-authorization-path.json` |
| CMS mirror preflight manifest | `docs/context-layer/hrcn-v1.0.2-cms-mirror-preflight-manifest.json` |
| CMS read-only mirror copy evidence | `docs/context-layer/hrcn-v1.0.3-cms-read-only-mirror-copy-evidence.json` |
| CMS mirror root | `cms/` |
| Bounded CMS context packet | `docs/context-layer/hrcn-v1.1-bounded-cms-context-packet.json` |
| Python format technique lock | `docs/context-layer/hrcn-v1.1.1-python-format-technique-lock.json` |
| Context surface coherence closure | `docs/context-layer/hrcn-v1.1.2-context-surface-coherence-closure.json` |
| Permission bridge dry-run design | `docs/context-layer/hrcn-v1.2-permission-bridge-dry-run-design.json` |
| CMS-Hermes read-only bridge prototype | `docs/context-layer/hrcn-v1.3-cms-hermes-read-only-bridge-prototype.json` |
| Dry-run execution harness contract | `docs/context-layer/hrcn-v1.4-dry-run-execution-harness-contract.json` |
| Apply-gate contract | `docs/context-layer/hrcn-v1.5-apply-gate-contract.json` |
| Limited apply executor | `docs/context-layer/hrcn-v1.6-limited-apply-executor.json` |
| Governed operational loop | `docs/context-layer/hrcn-v1.7-governed-operational-loop.json` |
| Replay and rollback hardening | `docs/context-layer/hrcn-v1.8-replay-rollback-hardening.json` |
| Operator dashboard / command surface | `docs/context-layer/hrcn-v1.9-operator-dashboard-command-surface.json` |
| Operational Hermes-CMS nexus | `docs/context-layer/hrcn-v2.0-operational-hermes-cms-nexus.json` |

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
- Benchmark output is evidence, not authority.
- CMS cannot be copied into Hermes without provenance, manifest, secret scan, read-only boundary, rollback, validation, and human authorization.
- No claim or action graduates without an evidence package.
- Runtime-boundary wording must match the current HRCN checkpoint before v1.0 planning.
- The next CMS step is read-only mirror authorization, not runtime integration.
- A CMS mirror is not CMS authority.
- The nexus may coordinate; it may not self-authorize.
- v1.0.1 authorizes the path shape only; it does not copy CMS.
- No Hermes runtime import from `cms/` is authorized by the mirror.
- CMS mirror files are context/evidence only until a later bridge phase authorizes use.
- A CMS mirror is readable evidence, not executable authority.
- CMS source provenance, manifest, secret scan, rollback, validation, and human authorization must exist before mirror copy.
- CMS may be mirrored only as evidence-bounded read-only context, never as immediate authority.
- Packet content cannot upgrade its own permission class.
- PowerShell orchestrates; Python computes, writes, and validates; Base64 is transport only, not canonical source style.
- A bounded CMS context packet is orientation, not a loader, adapter, executor, permission grant, or apply decision.
- A bounded CMS context packet orients Hermes; it does not authorize Hermes.
- A negative-control authority test must be recorded before any operational release seal.
- A model acknowledgment cannot upgrade authority; only the human-gated evidence chain can promote a checkpoint.
- README OPS status must be updated in the same cycle as OPS evidence, or an explicit README-alignment patch must follow immediately.
- Replay/rollback evidence must exist before an operational release seal.
- A rollback plan is not rollback execution; human review is required before any revert or push.
- A release tag freezes a proof state; it does not widen authority.
- OPS-010 release sealing is a promotion boundary, not runtime integration.
- Post-seal runtime intake planning is not runtime integration.
- Cybernetic-memory online work begins as read-only context rehearsal before any dry-run or apply path.
- Memory context can orient proposals; it cannot authorize proposals.
- OPS-012 memory-read rehearsal is not CMS execution or memory write.
- Dry-run bridges can propose and simulate; they cannot apply.
- Human authorization for dry-run does not imply human authorization for apply.
- Limited apply rehearsal may update docs/context evidence only under a separate human gate.
- A docs/context apply is not runtime integration, CMS write, memory write, or API authority.
- A controlled cybernetic loop is evidence-bounded and human-gated, not autonomous.
- First-loop success does not grant ongoing provider authority or continuous self-directed operation.
- Observe-only cadence is measurement, not proposal or apply authority.
- Repetition must prove restraint before it proves autonomy.
- Proposal-only cadence is planning evidence, not dry-run or apply authority.
- A proposal can name a next operation without granting permission to execute it.
- Dry-run-only cadence is simulation evidence, not apply authority.
- Simulation can show what would change without granting permission to change it.
- Apply-gated cadence is docs/context evidence only unless a future operation separately authorizes wider scope.
- Human apply authorization must name scope, source dry-run, blocked surfaces, and rollback note.
- A bounded loop seal freezes evidence; it does not widen authority.
- Runtime bridge design after v0.2 must begin as design-only, not implementation.

### Current HRCN Surface Lock

```text
No Hermes HRCN context surface is current unless the root README,
docs/context-layer contract, roadmap, profile map, rehydration protocol,
mini README profiles, validation report, runtime lock, and non-claim
boundaries agree.
```

<!-- HRCN_RUNTIME_EVOLUTION_BOUNDARY_START -->
### Current Runtime Boundary and Future Runtime Evolution

HRCN v1.1 keeps the current repository state docs/context plus CMS read-only mirror evidence under cms/ and a bounded CMS context packet, but it does not lock Hermes into docs-only forever.

Current boundary:

```text
HRCN v2.0 seals a bounded operational Hermes-CMS nexus; it does not change Hermes runtime.
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

<!-- HRCN_V09_EVIDENCE_BENCHMARK_START -->
### HRCN v0.9 Evidence Package and Benchmark Harness

HRCN v0.9 defines the evidence package and benchmark harness required before future governed Hermes-CMS nexus work or CMS import work.

Current rule:

```text
No claim or action graduates without an evidence package.
```

Evidence artifacts:

```text
docs/context-layer/hrcn-v0.9-evidence-package-benchmark-harness.json
docs/context-layer/hrcn-v0.9-evidence-package-benchmark-harness.md
docs/context-layer/hrcn-v0.9.validation.json
docs/context-layer/hrcn-v0.9.validation.md
```

v0.9 separates seven things that must not collapse into one another:

```text
claim/action
evidence package
benchmark contract
audit record
rollback binding
authorization record
promotion decision
```

CMS is now mirrored under cms/ as read-only context/evidence only. A future CMS copy must carry provenance, manifest, secret scan, read-only boundary, rollback/removal plan, validation commands, and human authorization.

Non-claim lock: HRCN v0.9 does not create a loader, adapter, benchmark executor, dry-run executor, apply executor, repair executor, runtime bridge, CMS folder, CMS writer, API writer, repair applier, or live integration.
<!-- HRCN_V09_EVIDENCE_BENCHMARK_END -->

<!-- HRCN_V10_GOVERNED_NEXUS_START -->
### HRCN v1.0 Governed Hermes-CMS Nexus Planning

HRCN v1.0 defines the governed nexus plan between Hermes, RCC, CMS, HRCN, evidence, rollback, and human authorization.

Current rule:

```text
The nexus may coordinate; it may not self-authorize.
```

Nexus artifacts:

```text
docs/context-layer/hrcn-v1.0-governed-hermes-cms-nexus-plan.json
docs/context-layer/hrcn-v1.0-governed-hermes-cms-nexus-plan.md
docs/context-layer/hrcn-v1.0.validation.json
docs/context-layer/hrcn-v1.0.validation.md
```

v1.0 separates seven things that must not collapse into one another:

```text
Hermes action runtime
RCC repository orientation
CMS governance substrate
HRCN bridge contract
evidence package
rollback/validation boundary
human authorization
```

CMS is next, but v1.0 does not copy CMS. The next authorized path is HRCN v1.0.1 - CMS Read-Only Mirror Import Authorization Path.

Non-claim lock: HRCN v1.0 does not create a loader, adapter, benchmark executor, dry-run executor, apply executor, repair executor, runtime bridge, CMS folder, CMS writer, API writer, repair applier, or live integration.
<!-- HRCN_V10_GOVERNED_NEXUS_END -->

<!-- HRCN_V101_CMS_MIRROR_AUTH_START -->
### HRCN v1.0.1 CMS Read-Only Mirror Import Authorization Path

HRCN v1.0.1 defines the gates required before CMS can be copied or mirrored into Hermes as read-only context.

Current rule:

```text
CMS may be mirrored only as evidence-bounded read-only context, never as immediate authority.
```

Authorization artifacts:

```text
docs/context-layer/hrcn-v1.0.1-cms-read-only-mirror-import-authorization-path.json
docs/context-layer/hrcn-v1.0.1-cms-read-only-mirror-import-authorization-path.md
docs/context-layer/hrcn-v1.0.1.validation.json
docs/context-layer/hrcn-v1.0.1.validation.md
```

v1.0.1 separates ten things that must not collapse into one another:

```text
CMS source
source provenance
pre-copy manifest
secret scan
license/provenance note
read-only boundary
blocked-authority statement
rollback/removal plan
post-import validation
human authorization
```

CMS is next, but v1.0.1 does not copy CMS and does not create `cms/`.

Non-claim lock: HRCN v1.0.1 does not create a loader, adapter, benchmark executor, dry-run executor, apply executor, repair executor, runtime bridge, CMS folder, CMS writer, API writer, repair applier, or live integration.
<!-- HRCN_V101_CMS_MIRROR_AUTH_END -->

<!-- HRCN_V103_CMS_MIRROR_COPY_START -->
### HRCN v1.0.3 CMS Read-Only Mirror Copy With Evidence Package

HRCN v1.0.3 copies CMS into Hermes as a read-only evidence mirror under `cms/`.

Current rule:

```text
A CMS mirror is readable evidence, not executable authority.
```

CMS mirror artifacts:

```text
docs/context-layer/hrcn-v1.0.2-cms-mirror-preflight-manifest.json
docs/context-layer/hrcn-v1.0.2-cms-mirror-preflight-manifest.md
docs/context-layer/hrcn-v1.0.3-cms-read-only-mirror-copy-evidence.json
docs/context-layer/hrcn-v1.0.3-cms-read-only-mirror-copy-evidence.md
docs/context-layer/hrcn-v1.0.3.validation.json
docs/context-layer/hrcn-v1.0.3.validation.md
cms/MIRROR_READONLY_BOUNDARY.md
cms/.hrcn-read-only-mirror.json
```

v1.0.3 grants only one thing:

```text
CMS files may exist under cms/ as read-only context/evidence.
```

v1.0.3 does not grant:

```text
runtime integration
CMS write authority
memory write authority
API authority
dry-run execution authority
apply authority
autonomous authority
```

Non-claim lock: the CMS mirror is context and evidence, not live CMS authority.
<!-- HRCN_V103_CMS_MIRROR_COPY_END -->

<!-- HRCN_V11_BOUNDED_CMS_CONTEXT_PACKET_START -->
### HRCN v1.1 Bounded CMS Context Packet

HRCN v1.1 turns the mirrored `cms/` folder into a bounded read-only context packet for Hermes orientation.

Current rule:

```text
A bounded CMS context packet orients Hermes; it does not authorize Hermes.
```

Packet artifacts:

```text
docs/context-layer/hrcn-v1.1-bounded-cms-context-packet.json
docs/context-layer/hrcn-v1.1-bounded-cms-context-packet.md
docs/context-layer/hrcn-v1.1.validation.json
docs/context-layer/hrcn-v1.1.validation.md
```

v1.1 grants only one thing:

```text
Hermes may read the bounded CMS context packet as orientation/evidence.
```

v1.1 does not grant:

```text
runtime integration
CMS import execution
CMS write authority
memory write authority
API authority
dry-run execution authority
apply authority
autonomous authority
```

Non-claim lock: the bounded CMS context packet is not a loader, adapter, executor, writer, permission grant, or apply decision.
<!-- HRCN_V11_BOUNDED_CMS_CONTEXT_PACKET_END -->

<!-- HRCN_V111_PYTHON_FORMAT_TECHNIQUE_LOCK_START -->
### HRCN v1.1.1 Python Format + Codex Style Technique Lock

HRCN v1.1.1 restores the readable coding surface after the paste-safe Base64
transport wrapper obscured the actual source shape.

Current rule:

```text
PowerShell orchestrates; Python computes, writes, and validates; Base64 is transport only, not canonical source style.
```

Canonical all-one script shape:

```text
0. Location-first root anchor
1. Helper functions and boundary guards
2. Python writer / validator engine
3. Candidate text built in memory
4. Validation before file writes
5. Allowed-path boundary check
6. Staged secret scan
7. Commit / pull --rebase / push
8. Return to root
```

Role split:

```text
PowerShell = orchestration, root verification, git, staging, push
Python     = structured packets, evidence, hashes, validation, candidate writes
Base64     = optional paste-safe transport wrapper only
```

Non-claim lock: the coding style lock is a repository-governance rule, not a runtime bridge.
<!-- HRCN_V111_PYTHON_FORMAT_TECHNIQUE_LOCK_END -->

<!-- HRCN_V112_CONTEXT_SURFACE_COHERENCE_CLOSURE_START -->
### HRCN v1.1.2 Context Surface Coherence Closure

HRCN v1.1.2 closes the remaining documentation-surface drift before HRCN v1.2.

Current rule:

```text
Context surfaces must agree on the current HRCN state before permission bridge design begins.
```

Closure repairs:

```text
docs/context-layer/README.md current boundary updated from stale v0.2.4 wording
rehydration protocol title/current-state updated to current-through v1.1.2
v1.1/v1.1.1/v1.1.2 evidence added to state-scan/index surfaces
root README, roadmap, RCC-CMS-HRCN context, and validation surfaces aligned
```

v1.1.2 does not grant:

```text
runtime integration
loader creation
adapter creation
CMS write authority
memory write authority
API authority
dry-run execution authority
apply authority
autonomous authority
```

Non-claim lock: this coherence closure is a documentation-surface alignment patch, not a runtime bridge.
<!-- HRCN_V112_CONTEXT_SURFACE_COHERENCE_CLOSURE_END -->

<!-- HRCN_V12_PERMISSION_BRIDGE_DRY_RUN_DESIGN_START -->
### HRCN v1.2 Permission Bridge Dry-Run Design

HRCN v1.2 defines the permission bridge design that classifies requested authority before action.

Current rule:

```text
Permission bridge design classifies requested authority before action; it does not execute CMS, run dry-runs, apply repairs, or grant authority.
```

Design artifacts:

```text
docs/context-layer/hrcn-v1.2-permission-bridge-dry-run-design.json
docs/context-layer/hrcn-v1.2-permission-bridge-dry-run-design.md
docs/context-layer/hrcn-v1.2.validation.json
docs/context-layer/hrcn-v1.2.validation.md
```

Decision classes:

```text
observe_only
read_only_context
summarize_evidence
dry_run_required
human_review_required
blocked
```

v1.2 does not grant:

```text
runtime integration
loader creation
adapter creation
dry-run execution
apply execution
CMS write authority
memory write authority
API authority
autonomous authority
```

Non-claim lock: the permission bridge is design-only; it is not a loader, adapter, executor, writer, permission grant, or apply decision.
<!-- HRCN_V12_PERMISSION_BRIDGE_DRY_RUN_DESIGN_END -->

<!-- HRCN_V13_READ_ONLY_BRIDGE_PROTOTYPE_START -->
### HRCN v1.3 CMS-Hermes Read-Only Bridge Prototype

HRCN v1.3 defines a read-only bridge prototype contract between Hermes and bounded CMS context.

Current rule:

```text
A read-only bridge may translate bounded CMS context into Hermes orientation; it may not command Hermes or execute CMS.
```

Prototype artifacts:

```text
docs/context-layer/hrcn-v1.3-cms-hermes-read-only-bridge-prototype.json
docs/context-layer/hrcn-v1.3-cms-hermes-read-only-bridge-prototype.md
docs/context-layer/hrcn-v1.3.validation.json
docs/context-layer/hrcn-v1.3.validation.md
```

Prototype flow:

```text
receive bridge request
classify requested authority using HRCN v1.2
allow only bounded read refs from HRCN v1.1 packet
resolve evidence/context summaries
return orientation packet with authority_granted=false
```

v1.3 does not grant:

```text
runtime integration
loader creation
adapter creation
CMS execution
dry-run execution
apply execution
CMS write authority
memory write authority
API authority
autonomous authority
```

Non-claim lock: the read-only bridge prototype is a reference contract, not a runtime bridge.
<!-- HRCN_V13_READ_ONLY_BRIDGE_PROTOTYPE_END -->

<!-- HRCN_V14_DRY_RUN_EXECUTION_HARNESS_CONTRACT_START -->
### HRCN v1.4 Dry-Run Execution Harness Contract

HRCN v1.4 defines the dry-run harness contract for future simulation.

Current rule:

```text
A dry-run harness may simulate and score a proposed change; it may not apply the change, mutate runtime, or grant authority.
```

Harness artifacts:

```text
docs/context-layer/hrcn-v1.4-dry-run-execution-harness-contract.json
docs/context-layer/hrcn-v1.4-dry-run-execution-harness-contract.md
docs/context-layer/hrcn-v1.4.validation.json
docs/context-layer/hrcn-v1.4.validation.md
```

Harness flow:

```text
receive permission-classified proposal
verify decision_class allows dry_run_required
construct sandbox plan
construct expected diff manifest
bind evidence requirements
bind rollback requirements
emit dry-run result with applied=false
```

v1.4 does not grant:

```text
runtime integration
loader creation
adapter creation
dry-run executor implementation
apply execution
CMS write authority
memory write authority
API authority
autonomous authority
```

Non-claim lock: the dry-run harness contract is a simulation contract, not a live executor.
<!-- HRCN_V14_DRY_RUN_EXECUTION_HARNESS_CONTRACT_END -->

<!-- HRCN_V15_APPLY_GATE_CONTRACT_START -->
### HRCN v1.5 Apply-Gate Contract

HRCN v1.5 defines the apply gate contract for future authorized transitions.

Current rule:

```text
Apply is a gated human-authorized transition, not an agent decision and not a dry-run result.
```

Apply-gate artifacts:

```text
docs/context-layer/hrcn-v1.5-apply-gate-contract.json
docs/context-layer/hrcn-v1.5-apply-gate-contract.md
docs/context-layer/hrcn-v1.5.validation.json
docs/context-layer/hrcn-v1.5.validation.md
```

Gate requirements:

```text
passed dry-run result
evidence package
rollback plan
human authorization record
scoped changed paths
validation plan
secret scan requirement
promotion decision
```

v1.5 does not grant:

```text
runtime integration
loader creation
adapter creation
dry-run executor implementation
apply executor implementation
apply execution
CMS write authority
memory write authority
API authority
autonomous authority
```

Non-claim lock: the apply gate contract is a future authorization boundary, not apply permission.
<!-- HRCN_V15_APPLY_GATE_CONTRACT_END -->

<!-- HRCN_V16_LIMITED_APPLY_EXECUTOR_START -->
### HRCN v1.6 Limited Apply Executor

HRCN v1.6 creates a bounded local executor tool for future human-authorized docs/context packets.

Current rule:

```text
A limited apply executor may apply only an explicitly authorized docs/context packet; creating the executor does not grant use.
```

Executor artifacts:

```text
docs/context-layer/hrcn-v1.6-limited-apply-executor.json
docs/context-layer/hrcn-v1.6-limited-apply-executor.md
docs/context-layer/hrcn-v1.6.validation.json
docs/context-layer/hrcn-v1.6.validation.md
scripts/hrcn/limited_apply_executor_v1_6.py
scripts/hrcn/README.md
```

Hard executor scope:

```text
README.md
docs/context-layer/**
```

Non-claim lock: executor creation is not apply permission; future execution still requires human authorization and a bounded packet.
<!-- HRCN_V16_LIMITED_APPLY_EXECUTOR_END -->

<!-- HRCN_V17_GOVERNED_OPERATIONAL_LOOP_START -->
### HRCN v1.7 Governed Operational Loop

HRCN v1.7 creates the governed operational loop controller for bounded docs/context operation.

Current rule:

```text
A governed operational loop may coordinate gates; it may not bypass them, self-authorize, or widen apply scope.
```

Loop artifacts:

```text
docs/context-layer/hrcn-v1.7-governed-operational-loop.json
docs/context-layer/hrcn-v1.7-governed-operational-loop.md
docs/context-layer/hrcn-v1.7.validation.json
docs/context-layer/hrcn-v1.7.validation.md
scripts/hrcn/governed_operational_loop_v1_7.py
```

Loop sequence:

```text
observe -> propose -> classify -> dry-run -> evidence -> authorize -> limited apply -> validate -> ledger
```

Hard scope inherited from v1.6:

```text
README.md
docs/context-layer/**
```

Non-claim lock: the loop coordinates gates only; it does not self-authorize or widen executor scope.
<!-- HRCN_V17_GOVERNED_OPERATIONAL_LOOP_END -->

<!-- HRCN_V18_REPLAY_ROLLBACK_HARDENING_START -->
### HRCN v1.8 Replay and Rollback Hardening

HRCN v1.8 hardens the governed docs/context loop with replay, audit, and rollback checks.

Current rule:

```text
A governed operation is not operationally safe until it can be replayed, audited, and rolled back within its authorized scope.
```

Hardening artifacts:

```text
docs/context-layer/hrcn-v1.8-replay-rollback-hardening.json
docs/context-layer/hrcn-v1.8-replay-rollback-hardening.md
docs/context-layer/hrcn-v1.8.validation.json
docs/context-layer/hrcn-v1.8.validation.md
scripts/hrcn/replay_rollback_hardening_v1_8.py
```

Hardening checks:

```text
expected_base_commit
operation hashes
allowed scope
ledger chain
limited-apply audit
rollback packet presence
replay manifest
post-apply validation evidence
```

Non-claim lock: replay and rollback hardening validates operational recoverability; it does not automatically rollback, self-authorize, or widen scope.
<!-- HRCN_V18_REPLAY_ROLLBACK_HARDENING_END -->

<!-- HRCN_V19_OPERATOR_COMMAND_SURFACE_START -->
### HRCN v1.9 Operator Dashboard / Command Surface

HRCN v1.9 adds the local human operator command surface for governed docs/context operations.

Current rule:

```text
An operator surface may make governed actions visible and selectable; it may not become the operator.
```

Operator artifacts:

```text
docs/context-layer/hrcn-v1.9-operator-dashboard-command-surface.json
docs/context-layer/hrcn-v1.9-operator-dashboard-command-surface.md
docs/context-layer/hrcn-v1.9.validation.json
docs/context-layer/hrcn-v1.9.validation.md
scripts/hrcn/operator_command_surface_v1_9.py
```

Operator commands:

```text
status
gates
make-packet-template
next-commands
```

Non-claim lock: the operator command surface presents and prepares governed actions; it does not apply, rollback, self-authorize, widen scope, or call APIs.
<!-- HRCN_V19_OPERATOR_COMMAND_SURFACE_END -->

<!-- HRCN_V20_OPERATIONAL_NEXUS_START -->
### HRCN v2.0 Operational Hermes-CMS Nexus

HRCN v2.0 seals the bounded operational Hermes-CMS nexus.

Current rule:

```text
Operational does not mean autonomous; operational means the full governed path is visible, bounded, auditable, and human-gated.
```

Operational nexus artifacts:

```text
docs/context-layer/hrcn-v2.0-operational-hermes-cms-nexus.json
docs/context-layer/hrcn-v2.0-operational-hermes-cms-nexus.md
docs/context-layer/hrcn-v2.0.validation.json
docs/context-layer/hrcn-v2.0.validation.md
scripts/hrcn/operational_nexus_status_v2_0.py
```

Operational scope:

```text
README.md
docs/context-layer/**
```

Operational chain:

```text
CMS mirror/context
bounded CMS packet
permission bridge
read-only bridge
dry-run contract
apply gate
limited apply executor
governed operational loop
replay/rollback hardening
operator command surface
```

Non-claim lock: operational means governed and bounded; it does not mean autonomous, runtime-integrated, or self-authorizing.
<!-- HRCN_V20_OPERATIONAL_NEXUS_END -->

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
| HRCN-L-013 | README render hygiene repairs repeatedly failed through PowerShell parser/string handling. | Complex Unicode/mojibake and quote replacement logic was embedded directly in PowerShell source. | For fragile text repair, use a paste-safe Base64 Python helper or connector-backed patch path; keep PowerShell as orchestration only. |
| HRCN-L-014 | OPS evidence advanced while README status could remain one checkpoint behind. | OPS scripts wrote evidence but did not always patch the public README OPS chart and metrics in the same cycle. | After each OPS pass, run README/lesson alignment before the next OPS gate unless the OPS script updates README itself. |
| HRCN-L-015 | A successful negative-control test proved the bridge must refuse false authority before release sealing. | Operational bridge proof is incomplete if it only accepts context and never tests denial of over-authority. | Before an operational seal, require at least one negative-control authority test with expected denial, no tool use, no forbidden grant, and all dangerous authority flags false. |
| HRCN-L-016 | Replay/rollback evidence was needed before release sealing. | A bridge can pass runtime/provider/context gates but still lack a recomputable evidence package and rollback path. | OPS release sealing requires evidence index, checksums, replay instructions, rollback notes, and a boundary matrix before tag creation. |
| HRCN-L-017 | Rollback plans can be mistaken for rollback execution. | A plan names a safe recovery path but does not itself perform a revert or validate a restored state. | Treat rollback notes as a human-reviewed plan only; any actual revert/push must be a separate authorized operation. |
| HRCN-L-018 | Release sealing and tag creation needed one bounded operation. | A release seal without a tag fails to freeze the proof state, while a tag without a manifest fails to explain what is frozen. | OPS-010 must create release manifest, release notes, final boundary matrix, tag plan, final evidence, README alignment, and then push the tag. |
| HRCN-L-019 | A release tag can be mistaken for production authority. | Tags make a repository state durable but do not validate security, correctness, runtime integration, CMS authority, or autonomy. | Every release tag must include a non-claim lock stating that the tag freezes evidence only and grants no new authority. |
| HRCN-L-020 | After the release tag, the system needed a controlled intake plan before any online work. | A sealed bridge proof can create pressure to jump straight into runtime integration. | Post-seal evolution must begin with OPS-011 controlled runtime intake planning, not runtime mutation. |
| HRCN-L-021 | Cybernetic-memory online language can be mistaken for autonomy. | Online operation sounds like continuous self-directed action unless bounded by authority classes. | Define online as observe, retrieve bounded context, classify authority, propose, dry-run, record evidence, and wait for human gate before apply/write. |
| HRCN-L-022 | Memory-read rehearsal needed to prove orientation without permission. | Reading memory context can be confused with granting action authority. | Every memory-read rehearsal must emit authority_granted=false and keep CMS write, memory write, API write, runtime mutation, dependency mutation, and self-authorization false. |
| HRCN-L-023 | Hash-verified bounded reads prevent silent context drift. | A memory adapter can accidentally ingest unbounded or changed surfaces. | Read adapters must compare declared and computed hashes for required bounded read files before producing orientation evidence. |
| HRCN-L-024 | Human-gated dry-run must not be mistaken for apply permission. | A successful dry-run can create pressure to execute the proposal immediately. | Dry-run authorization and apply authorization must remain separate gates with separate evidence. |
| HRCN-L-025 | Proposed diffs need a simulated manifest before apply rehearsal. | Without a simulated diff, the operator cannot see what would change before granting apply. | Every dry-run bridge must emit a simulated diff manifest, dry-run report, rollback preview, and authority matrix before OPS-014. |
| HRCN-L-026 | Limited apply needs a narrower gate than dry-run. | Dry-run evidence can show what would change, but apply changes repo state even when docs-only. | OPS-014 requires a new human phrase, apply packet, apply-gate evidence, applied manifest, rollback note, and final evidence. |
| HRCN-L-027 | Docs/context apply must remain visibly separate from runtime integration. | A successful apply rehearsal can be mistaken for code/runtime authority. | Every limited apply record must state runtime_source_mutation=false, cms_write=false, memory_write=false, api_write=false, and dependency_mutation_committed=false. |
| HRCN-L-028 | The first cybernetic loop must be evidence-bounded before it is automated. | A loop can appear operational once it observes, proposes, and applies docs/context evidence. | First-loop success must still require human gate, docs/context scope, all dangerous authority flags false, and no ongoing authority. |
| HRCN-L-029 | Loop continuity is not the same as autonomy. | Repeated observe/propose/apply cycles could be mistaken for self-directed agency. | Future cadence must start observe-only and require explicit authorization before any write or apply phase. |
| HRCN-L-030 | Observe-only cadence must be proven before proposal cadence. | A loop that immediately proposes or applies can hide whether observation alone is stable. | OPS-016 records repeated observations with proposal_generated=false, dry_run_executed=false, and apply_executed=false. |
| HRCN-L-031 | Repeated observation can create autonomy drift if not explicitly bounded. | Cadence language sounds like unattended agency. | Every cadence harness must state provider/model calls, runtime mutation, CMS write, memory write, API write, dependency mutation, autonomy, and self-authorization are false. |
| HRCN-L-032 | Proposal cadence must not collapse into dry-run cadence. | A repeated proposal can feel like an instruction pipeline. | OPS-017 generates proposals while keeping dry_run_executed=false and apply_executed=false. |
| HRCN-L-033 | Proposal authority must remain narrower than action authority. | Naming an operation can be mistaken for permission to run it. | Every proposal-only record must state the proposed next operation and explicitly deny dry-run/apply/runtime/CMS/memory/API/dependency/autonomous authority. |
| HRCN-L-034 | Dry-run cadence must not collapse into apply cadence. | Simulation can feel like permission once the intended changes are clear. | OPS-018 executes dry-runs while keeping apply_executed=false and all write/runtime authority flags false. |
| HRCN-L-035 | Dry-run manifests must preserve blocked-scope visibility. | A dry-run without explicit blocked scope can hide what must not be touched. | Every dry-run record must list would_create, would_update, and would_not_touch surfaces before any apply-gated operation. |
| HRCN-L-036 | Apply-gated cadence must remain docs/context-only until explicitly widened. | A successful apply cadence can be mistaken for runtime or CMS authority. | OPS-019 applies evidence only under docs_context_only scope and keeps runtime_source_mutation, cms_write, memory_write, api_write, and dependency_mutation_committed false. |
| HRCN-L-037 | Apply requires a source dry-run and rollback note. | Applying without a prior simulation and recovery path breaks the governed loop. | Every apply-gated cadence must cite source dry-runs, write apply records, write an apply manifest, and include a rollback note. |
| HRCN-L-038 | Bounded loop seals must freeze evidence, not widen authority. | After observe/propose/dry-run/apply cadence passes, it can be mistaken for autonomous operation. | OPS-020 tags the v0.2 proof while keeping runtime, CMS, memory, API, dependency, provider/model, autonomy, and self-authorization false. |
| HRCN-L-039 | Runtime bridge evolution must restart with design-only boundaries. | A sealed evidence loop can create pressure to mutate runtime immediately. | The next track must begin with OPS-021 governed runtime bridge interface design, not runtime implementation. |

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

HRCN v2.0 seals Hermes-CMS as operational only for bounded docs/context governance. The operational nexus can report status across the CMS mirror/context packet, permission bridge, read-only bridge, dry-run contract, apply gate, limited apply executor, governed loop, replay/rollback hardening, and operator surface. It does not grant runtime mutation, CMS write authority, memory write authority, API authority, dependency mutation, autonomous authority, or self-authorization.
<!-- HRCN_CONTEXT_LAYER_END -->
---

## Quick Install

### Linux, macOS, WSL2, Termux

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

### Windows (native, PowerShell)

> **Heads up:** Native Windows runs Hermes without WSL - CLI, gateway, TUI, and tools all work natively. If you'd rather use WSL2, the Linux/macOS one-liner above works there too. Found a bug? Please [file issues](https://github.com/NousResearch/hermes-agent/issues).

Run this in PowerShell:

```powershell
iex (irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1)
```

The installer handles everything: uv, Python 3.11, Node.js, ripgrep, ffmpeg, **and a portable Git Bash** (MinGit, unpacked to `%LOCALAPPDATA%\hermes\git` - no admin required, completely isolated from any system Git install). Hermes uses this bundled Git Bash to run shell commands.

If you already have Git installed, the installer detects it and uses that instead. Otherwise a ~45MB MinGit download is all you need - it won't touch or interfere with any system Git.

> **Android / Termux:** The tested manual path is documented in the [Termux guide](https://hermes-agent.nousresearch.com/docs/getting-started/termux). On Termux, Hermes installs a curated `.[termux]` extra because the full `.[all]` extra currently pulls Android-incompatible voice dependencies.
>
> **Windows:** Native Windows is fully supported - the PowerShell one-liner above installs everything. If you'd rather use WSL2, the Linux command works there too. Native Windows install lives under `%LOCALAPPDATA%\hermes`; WSL2 installs under `~/.hermes` as on Linux.  The only Hermes feature that currently needs WSL2 specifically is the browser-based dashboard chat pane (it uses a POSIX PTY - classic CLI and gateway both run natively).

After installation:

```bash
source ~/.bashrc    # reload shell (or: source ~/.zshrc)
hermes              # start chatting!
```

---

## Getting Started

```bash
hermes              # Interactive CLI - start a conversation
hermes model        # Choose your LLM provider and model
hermes tools        # Configure which tools are enabled
hermes config set   # Set individual config values
hermes gateway      # Start the messaging gateway (Telegram, Discord, etc.)
hermes setup        # Run the full setup wizard (configures everything at once)
hermes claw migrate # Migrate from OpenClaw (if coming from OpenClaw)
hermes update       # Update to the latest version
hermes doctor       # Diagnose any issues
```

**[Full documentation ->](https://hermes-agent.nousresearch.com/docs/)**

---

## Skip the API-key collection - Nous Portal

Hermes works with whatever provider you want - that's not changing. But if you'd rather not collect five separate API keys for the model, web search, image generation, TTS, and a cloud browser, **[Nous Portal](https://portal.nousresearch.com)** covers all of them under one subscription:

- **300+ models** - pick any of them with `/model <name>`
- **Tool Gateway** - web search (Firecrawl), image generation (FAL), text-to-speech (OpenAI), cloud browser (Browser Use), all routed through your sub. No extra accounts.

One command from a fresh install:

```bash
hermes setup --portal
```

That logs you in via OAuth, sets Nous as your provider, and turns on the Tool Gateway. Check what's wired up any time with `hermes portal info`. Full details on the [Tool Gateway docs page](https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-gateway).

You can still bring your own keys per-tool whenever you want - the gateway is per-backend, not all-or-nothing.

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
| [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)                 | Install -> setup -> first conversation in 2 minutes          |
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

- **SOUL.md** - persona file
- **Memories** - MEMORY.md and USER.md entries
- **Skills** - user-created skills -> `~/.hermes/skills/openclaw-imports/`
- **Command allowlist** - approval patterns
- **Messaging settings** - platform configs, allowed users, working directory
- **API keys** - allowlisted secrets (Telegram, OpenRouter, OpenAI, Anthropic, ElevenLabs)
- **TTS assets** - workspace audio files
- **Workspace instructions** - AGENTS.md (with `--workspace-target`)

See `hermes claw migrate --help` for all options, or use the `openclaw-migration` skill for an interactive agent-guided migration with dry-run previews.

---

## Contributing

We welcome contributions! See the [Contributing Guide](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) for development setup, code style, and PR process.

Quick start for contributors - clone and go with `setup-hermes.sh`:

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

- [Discord](https://discord.gg/NousResearch)
- [Skills Hub](https://agentskills.io)
- [Issues](https://github.com/NousResearch/hermes-agent/issues)
- [computer-use-linux](https://github.com/avifenesh/computer-use-linux) - Linux desktop-control MCP server for Hermes and other MCP hosts, with AT-SPI accessibility trees, Wayland/X11 input, screenshots, and compositor window targeting.
- [HermesClaw](https://github.com/AaronWong1999/hermesclaw) - Community WeChat bridge: Run Hermes Agent and OpenClaw on the same WeChat account.

---

## License

MIT - see [LICENSE](LICENSE).

Built by [Nous Research](https://nousresearch.com).


- Read-only HRCN runtime bridge modules may orient Hermes surfaces but cannot authorize actions.

- Self-improvement begins as evidence-gated proposal/dry-run/apply, not autonomous code mutation.

- Pytest config addopts must be neutralized for focused local bridge tests when optional pytest plugins are not installed.

| HRCN-L-042 | Runtime integration should start with a read-only module, not a broad interface patch. | Hermes has multiple surfaces, so patching only one GUI would create drift. | OPS-022 adds one importable bridge module that CLI, TUI, web, agent, and ACP surfaces can consume later. |

| HRCN-L-043 | Self-improvement must stay evidence-gated after runtime integration starts. | Runtime access can be mistaken for permission to mutate code autonomously. | The bridge exposes context and boundaries only; proposal, dry-run, and apply remain separate human-gated authority classes. |

| HRCN-L-044 | Focused local tests must not depend on optional pytest plugins. | The initial OPS-022 run failed because pyproject addopts referenced pytest-timeout flags unavailable in the local environment. | OPS-022 repair runs focused tests with -o addopts= and records direct Python bridge assertions. |

- Hermes status/startup surfaces may display HRCN bridge status only when read-only boundaries pass.

- Optional startup visibility must remain operator-enabled and off by default.

| HRCN-L-045 | Runtime status wiring must be visible but non-authorizing. | A status command can be mistaken for a control channel. | OPS-023 exposes `hermes hrcn status` and optional startup display while keeping all write/tool/provider/CMS/memory/API/autonomy flags false. |

| HRCN-L-046 | Startup bridge display should be opt-in at first. | Default startup changes can disrupt Hermes interfaces or scripts. | OPS-023 leaves normal behavior unchanged unless `HERMES_HRCN_BRIDGE=1` is set or an explicit HRCN status command is called. |

- HRCN runtime bridge status must fail closed when any forbidden authority flag is true.

- Negative-control refusal is mandatory before HRCN context can guide proposal paths.

| HRCN-L-047 | Runtime bridges must fail closed on forged authority. | Read-only status visibility is not enough unless forged CMS/memory/API/autonomy flags are rejected. | OPS-024 adds negative controls proving the bridge raises on forbidden authority flags. |

| HRCN-L-048 | Live read-only evidence and forged evidence must both be tested. | A bridge can pass live state while accepting bad packets in edge cases. | OPS-024 tests both live read-only acceptance and fake-repo forged-authority rejection. |

- HRCN proposal-path context injection must remain opt-in and read-only.

- HRCN context orientation cannot grant tools, writes, provider calls, CMS writes, memory writes, API writes, autonomy, or self-authorization.

- HRCN text assertions must match the bridge output surface: `READ ONLY` display plus read-only prose, not an internal enum spelling unless that enum is present.

| HRCN-L-049 | Proposal-path integration must be opt-in before default enablement. | Injecting governance context into every turn can alter behavior and surprise existing users/scripts. | OPS-025 uses `HERMES_HRCN_CONTEXT` as an explicit gate and leaves default behavior unchanged. |

| HRCN-L-050 | Read-only context must be appended only after bridge boundary verification. | Prompt context can become an authority channel if forged evidence is accepted. | OPS-025 calls the HRCN read-only boundary check before appending context and fails closed on bridge errors. |

| HRCN-L-051 | Tests should assert the public context surface, not an internal enum spelling. | OPS-025 initially expected `read_only`, while the prompt context emits `READ ONLY` and read-only prose. | OPS-025 repair aligns assertions to the real proposal-context text surface. |

- Post-seal runtime code has changed only for read-only bridge/status/proposal-context orientation.

- Default Hermes behavior remains unchanged unless `HERMES_HRCN_BRIDGE` or `HERMES_HRCN_CONTEXT` is explicitly set.

- Proposal-context HRCN orientation must fail closed on bridge boundary or formatter errors.

| HRCN-L-052 | Runtime-code-changed metrics must distinguish source mutation from authority mutation. | OPS-025 made a runtime hook, so `Runtime code changed=False` became stale even though authority remained false. | OPS-026 aligns README metrics to `runtime code changed=True` while preserving `default behavior=False` and `authority=False`. |

| HRCN-L-053 | Proposal-context injection needs its own negative controls after bridge negative controls. | A bridge can refuse forged evidence while the prompt-injection path still mishandles failures. | OPS-026 adds negative controls for bridge-boundary failure, formatter failure, unknown env values, non-authority lock, and duplicate injection. |


| RHP-L-021 | Direct proof scripts stored below docs must anchor the repository root into sys.path before importing repository packages. |
| RHP-L-022 | Final evidence closure should rebuild evidence as an ordered object instead of mutating a fixed ConvertFrom-Json PSCustomObject. |


RHP-L-034: Managed-region replacement should use regex over explicit start/end markers; PowerShell `.Split($marker, 2)` is not a safe delimiter split for block surgery.

<!-- RHP_014_8_CI_COHERENCE_DOCTOR -->
RHP-014.8 adds evidence_coherence_auditor, loop_state, and rhploop_doctor. Remote red CI is treated as a wound until a later green commit proves closure. Next: RHP-014.9 Autoheal executor dry-run v0.1.
<!-- /RHP_014_8_CI_COHERENCE_DOCTOR -->

<!-- RHP_014_9_AUTOHEAL_DRY_RUN -->
RHP-014.9 adds autoheal executor dry-run planning, RHPLOAD command headings, and RHPDIAG runtime diagnosis boxes. Autoheal execution remains disabled. Next: RHP-015.0 Autoheal proposal evaluator + CI log ingestion.
<!-- /RHP_014_9_AUTOHEAL_DRY_RUN -->

<!-- RHP_015_0_CI_BOOT_ALIGNMENT_REPAIR -->
RHP-015.0 repairs the CI boot/alignment wound by making `rhp/alignment_guard.py` pointer-aware while preserving legacy RHP-013.5 check keys: `latest_rhp0135_has_boundary_shape` and `latest_rhp0135_passed`. It also adds read-only CI log ingestion and autoheal proposal evaluation. Autoheal execution remains disabled. Next: RHP-015.1 CI green verification + autoheal proposal review.
<!-- /RHP_015_0_CI_BOOT_ALIGNMENT_REPAIR -->

<!-- RHP_015_1_AUTOHEAL_DRY_RUN_API_COMPATIBILITY -->
RHP-015.1 repairs the remote CI import wound by restoring the legacy `rhp.autoheal_executor_dry_run` API surface: `RHP_AUTOHEAL_DRY_RUN_SCHEMA` and `dry_run_for_packet`. The newer `build_plan`/Markdown dry-run surfaces remain, and autoheal execution stays disabled. Current loop status: RHP-015.1 sealed locally; remote CI remains the integration truth surface. Next: RHP-015.2 CI green verification and full RHP API surface audit.
<!-- /RHP_015_1_AUTOHEAL_DRY_RUN_API_COMPATIBILITY -->

<!-- RHP_015_2_API_SURFACE_AUDIT_COMPACT_SUMMARY -->
### RHP-015.2 API Surface Audit + Compact Command Summaries

RHP-015.2 makes the loop easier for any future AI or human operator to rehydrate. Stable imports, evidence keys, and output surfaces are now explicit contract surfaces. Repetitive command logs should no longer spam the terminal; use `RHPDROP [closed]` to summarize a command group and point to a raw-index file.

Operator rule:

```text
RHPLOAD = major gate/audit box
RHPWAIT = single-line fill/loading surface
RHPDROP [closed] = compact summary for repeated command groups
RHPDIAG = failure diagnosis box
```

Any AI continuing this repo must first read `docs/context-layer/latest-rhp.json`, `docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md`, `docs/context-layer/operator-dashboard.txt`, `AGENTS.md`, `README.md`, and `rhp/README.md`, then run the next All-One from Downloads with exact human authorization. The system does not self-authorize.
<!-- /RHP_015_2_API_SURFACE_AUDIT_COMPACT_SUMMARY -->

<!-- RHP_015_3_OPERATOR_QUICKSTART -->
### RHP-015.3 Operator Quickstart + CI Green Reconciliation

RHP-015.3 adds an explicit operator/AI quickstart surface so a fresh AI or human can understand the loop before proposing or running a script.

#### Required rehydration order

```text
1. docs/context-layer/latest-rhp.json
2. docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md
3. docs/context-layer/operator-dashboard.txt
4. docs/context-layer/hermes-operator-context.json
5. AGENTS.md
6. README.md
7. rhp/README.md
8. docs/context-layer/AI_OPERATOR_QUICKSTART.md
```

#### Output grammar

```text
RHPLOAD = major gate/audit box
RHPWAIT = single-line fill/loading surface
RHPDROP [closed] = compact summary for repeated command groups
RHPDIAG = failure diagnosis box
```

#### Operating law

```text
Hermes thinks and displays.
RHP gates.
All-One acts.
Evidence remembers.
Human authorizes.
```

Remote CI is the integration truth surface. Local focused tests prove bounded local repair; they do not prove remote integration closure until CI is green.
<!-- /RHP_015_3_OPERATOR_QUICKSTART -->

<!-- RHP_015_4_REMOTE_CI_GREEN_SEAL -->
### RHP-015.4 Remote CI Result Ingestion + Green-Seal Reconciliation

RHP-015.4 separates four surfaces that were starting to blur:

```text
local_validation = focused local proof from the All-One
operation_base_commit = HEAD before the current operation mutates the repo
previous_sealed_commit = already-published commit from the previous operation
remote_ci_status = unknown | pending | green | red | cancelled | skipped
```

A current operation cannot honestly embed its own final commit hash inside the same commit without a self-referential hash paradox. Therefore current-operation commit observation must come from the next operation or an external post-push observer.

Green seal law:

```text
integration_closed = local_validation_ok AND remote_ci_status == green
```

If CI is unknown or pending, the protocol must not claim green. If CI is red, create a wound packet before repair.
<!-- /RHP_015_4_REMOTE_CI_GREEN_SEAL -->

<!-- RHP_015_5_RENDER_HYGIENE_WAIT_STATE -->
### RHP-015.5 Render Hygiene + Wait-State Packet

RHP-015.5 fixes the render-hygiene wound exposed by RHP-015.4: text surfaces must contain real line breaks, not literal `\n` escape sequences.

It also records the CI branch without overclaiming:

```text
remote_ci_status = pending | unknown | green | red | cancelled | skipped
wait_state = remote_ci_status in {pending, unknown}
green_seal_ready = remote_ci_status == green
wound_packet_required = remote_ci_status == red
```

Rule: final JSON summaries should be compressed behind `RHPDROP [closed]`; full JSON belongs in evidence files or raw indexes.
<!-- /RHP_015_5_RENDER_HYGIENE_WAIT_STATE -->

<!-- RHP_015_6_EVIDENCE_API_CLAIM_REPLAY -->
### RHP-015.6 Evidence API Compatibility + Claim Ledger + Replay Scaffold

RHP-015.6 adds semantic accounting. Every protocol claim must name:

```text
claim = what is asserted
subject = commit/file/run/artifact being described
source = who or what observed it
observed_at = when it was observed
status = pending | green | red | unknown | skipped | cancelled
authority_granted = false unless explicitly and safely authorized
```

Remote CI status must always name the commit it describes. A previous green commit does not automatically make current HEAD green.

New tools:

```text
rhp/claim_ledger.py
rhp/ci_subject_resolver.py
rhp/evidence_api_compatibility_gate.py
rhp/rhpload_replay.py
```

Replay law:

```text
latest-rhp -> final evidence -> command summaries -> dashboard -> next legal operation
```
<!-- /RHP_015_6_EVIDENCE_API_CLAIM_REPLAY -->

<!-- RHP_015_7_DOCTOR_STATE_MACHINE -->
### RHP-015.7 RHP Doctor Cockpit + Explicit State Machine

RHP-015.7 adds a read-only operator cockpit and explicit state machine.

Doctor answers:

```text
What is latest?
Is worktree clean?
Is evidence API compatible?
Is replay complete?
What is current-head CI status?
What state is the loop in?
What is the next legal operation?
Can mutation happen?
```

State machine:

```text
NEW -> PREFLIGHT -> AUTHORIZED -> MUTATED -> VALIDATED -> SEALED_LOCAL -> PUSHED
PUSHED -> REMOTE_PENDING | REMOTE_GREEN | REMOTE_RED
REMOTE_GREEN -> RECONCILED
REMOTE_RED -> wound packet before repair
```

Doctor is read/classify/propose only. It does not mutate, rerun CI, call GitHub, execute autoheal, or grant authority.
<!-- /RHP_015_7_DOCTOR_STATE_MACHINE -->

<!-- RHP_015_8_WOUND_TAXONOMY_PROPOSAL -->
### RHP-015.8 Wound Taxonomy Registry + Proposal-Carrying Evidence

RHP-015.8 converts repeated failures into stable named wound classes and non-executing proposal packets.

Wound law:

```text
Failure -> WoundClass -> ProposalPacket -> Human-authorized All-One
```

Proposal packets carry:

```text
wound_class
subject
allowed_paths
blocked_paths
test_commands
risk_level
rollback
execution_enabled = false
authority_granted = false
```

This keeps autoheal dry-run/proposal-only while making future repairs sharper and replayable.
<!-- /RHP_015_8_WOUND_TAXONOMY_PROPOSAL -->

<!-- RHP_015_9_AUTOHEAL_PROPOSAL_WOUND_QUEUE -->
### RHP-015.9 Autoheal Proposal Planner + Doctor-Surfaced Wound Queue

RHP-015.9 connects wound taxonomy to non-executing autoheal proposal plans and a doctor-surfaced wound queue.

Planner law:

```text
WoundClass + Subject + Status -> ProposalPlan
ProposalPlan.execution_enabled = false
ProposalPlan.authority_granted = false
```

Queue law:

```text
Doctor surfaces wounds and proposal packets.
Doctor does not execute them.
Human-authorized All-One remains the only write boundary.
```

This is the bridge from classification to repair planning without crossing into autonomous mutation.
<!-- /RHP_015_9_AUTOHEAL_PROPOSAL_WOUND_QUEUE -->

<!-- RHP_016_0_GREEN_RECONCILIATION -->
### RHP-016.0 Green Reconciliation Seal

RHP-016.0 closes a specific commit-scoped CI claim.

Green reconciliation law:

```text
remote_ci_green(commit=X, source=github-actions-verified) -> integration_closed_for_commit(X) = true
```

The green claim applies only to the subject commit. The new reconciliation commit created by RHP-016.0 cannot claim its own remote CI state from inside itself.
<!-- /RHP_016_0_GREEN_RECONCILIATION -->

<!-- RHP_016_1_CURRENT_COMMIT_OBSERVATION_DOCTOR_CLI -->
### RHP-016.1 Current Commit CI Observation + Doctor CLI Wrapper

RHP-016.1 observes the RHP-016.0 commit's own CI status and exposes a small read-only doctor CLI wrapper.

Observation law:

```text
ci_status(commit=X, source=Y) must name X
```

Doctor CLI law:

```text
doctor_cli = read/classify/propose wrapper
doctor_cli does not mutate
doctor_cli does not grant authority
```
<!-- /RHP_016_1_CURRENT_COMMIT_OBSERVATION_DOCTOR_CLI -->

<!-- RHP_016_2_CI_WOUND_BROWSER_SUPERVISOR_WEBSOCKETS -->
### RHP-016.2 CI Wound Packet: Browser Supervisor Websockets Dependency/API Drift

RHP-016.2 records the remote CI failure as a typed wound packet and non-executing repair proposal.

```text
browser_supervisor_websockets_dependency_api_drift
tests/tools/test_browser_supervisor.py
python -m pytest tests/tools/test_browser_supervisor.py
```

Boundary: this operation records the wound and proposal only. It does not repair dependencies, patch code, rerun CI, or grant authority.
<!-- /RHP_016_2_CI_WOUND_BROWSER_SUPERVISOR_WEBSOCKETS -->

<!-- RHP_016_3_BROWSER_SUPERVISOR_WEBSOCKETS_COMPAT_REPAIR -->
### RHP-016.3 Bounded Browser Supervisor Websockets Dependency/API Repair

RHP-016.3 applies the bounded repair proposed by RHP-016.2.

Repair:

```text
tools/browser_supervisor.py
runtime import of websockets.asyncio.client.ClientConnection -> TYPE_CHECKING-only import
```

This keeps runtime use on `websockets.connect` while avoiding import-time dependency/API drift from newer websockets asyncio client internals.

Boundary: local repair only. Remote CI remains unknown until the new commit is observed after push.
<!-- /RHP_016_3_BROWSER_SUPERVISOR_WEBSOCKETS_COMPAT_REPAIR -->

<!-- RHP_016_4_REPAIR_COMMIT_CI_OBSERVATION -->
### RHP-016.4 Repair Commit CI Observation

RHP-016.4 observes the RHP-016.3 repair commit CI state and branches without overclaiming.

```text
subject_commit = cb5164265ef2df8ad894175bc56fc4b809ae5cea
observed_ci_status = pending
state = REPAIR_CI_PENDING
integration_closed = false
```

Boundary: observation/reconciliation only. It does not rerun CI, execute repair, or grant authority.
<!-- /RHP_016_4_REPAIR_COMMIT_CI_OBSERVATION -->
