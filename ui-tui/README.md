# Hermes TUI

React + Ink terminal UI for Hermes. TypeScript owns the screen. Python owns sessions, tools, model calls, and most command logic.

```bash
hermes --tui
```

## What runs

The client entrypoint is `src/entry.tsx`. It exits early if `stdin` is not a TTY, starts `GatewayClient`, then renders `App`.

`GatewayClient` spawns:

```text
python -m tui_gateway.entry
```

Interpreter resolution order is: `HERMES_PYTHON` → `PYTHON` → `$VIRTUAL_ENV/bin/python` → `./.venv/bin/python` → `./venv/bin/python` → `python3` (or `python` on Windows).

The transport is newline-delimited JSON-RPC over stdio:

```text
ui-tui/src                  tui_gateway/
-----------                 -------------
entry.tsx                   entry.py
  -> GatewayClient            -> request loop
  -> App                      -> server.py RPC handlers

stdin/stdout: JSON-RPC requests, responses, events
stderr: captured into an in-memory log ring
```

Malformed stdout lines are treated as protocol noise and surfaced as `gateway.protocol_error`. Stderr lines become `gateway.stderr`. Neither writes directly into the terminal.

## Running it

From the repo root, the normal path is:

```bash
hermes --tui
```

The CLI expects `ui-tui/dist/entry.js` to exist, or the whole source code available in which to run `npm install` and `npm run dev`.

```bash
cd ui-tui
npm install
```

Local package commands:

```bash
npm run dev
npm start
npm run build
npm run lint
npm run fmt
npm run fix
```

Tests use vitest:

```bash
npm test         # single run
npm run test:watch
```

## App model

`src/app.tsx` is the center of the UI. Heavy logic is split into `src/app/`:

- `createGatewayEventHandler.ts` — maps gateway events to state updates
- `createSlashHandler.ts` — local slash command dispatch
- `useComposerState.ts` — draft, multiline buffer, queue editing
- `useInputHandlers.ts` — keypress routing
- `useTurnState.ts` — agent turn lifecycle
- `overlayStore.ts` / `uiStore.ts` — nanostores for overlay and UI state
- `gatewayContext.tsx` — React context for the gateway client
- `constants.ts`, `helpers.ts`, `interfaces.ts`

The top-level `app.tsx` composes these into the Ink tree with `Static` transcript output, a live streaming assistant row, prompt overlays, queue preview, status rule, input line, and completion list.

State managed at the top level includes:

- transcript and streaming state
- queued messages and input history
- session lifecycle
- tool progress and reasoning text
- prompt flows for approval, clarify, sudo, and secret input
- slash command routing
- tab completion and path completion
- theme state from gateway skin data

The UI renders as a normal Ink tree with `Static` transcript output, a live streaming assistant row, prompt overlays, queue preview, status rule, input line, and completion list.

The intro panel is driven by `session.info` and rendered through `branding.tsx`.

## Hotkeys and interactions

Current input behavior is split across `app.tsx`, `components/textInput.tsx`, and the prompt/picker components.

### Main chat input

| Key                             | Behavior                                                                                                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Enter`                         | Submit the current draft                                                                                                                                |
| empty `Enter` twice             | If queued messages exist and the agent is busy, interrupt the current run. If queued messages exist and the agent is idle, send the next queued message |
| `Shift+Enter` / `Alt+Enter`     | Insert a newline in the current draft                                                                                                                   |
| `\` + `Enter`                   | Append the line to the multiline buffer (fallback for terminals without modifier support)                                                               |
| `Ctrl+C`                        | Interrupt active run, or clear the current draft, or exit if nothing is pending                                                                         |
| `Ctrl+D`                        | Exit                                                                                                                                                    |
| `Cmd/Ctrl+G` / `Alt+G`          | Open `$EDITOR` with the current draft (use `Alt+G` in VSCode/Cursor — they bind the primary keystroke to Find Next)                                     |
| `Ctrl+L`                        | New session (same as `/clear`)                                                                                                                          |
| `Ctrl+V` / `Alt+V`              | Paste text first, then fall back to image/path attachment when applicable                                                                               |
| `Tab`                           | Apply the active completion                                                                                                                             |
| `Up/Down`                       | Cycle completions if the completion list is open; otherwise edit queued messages first, then walk input history                                         |
| `Left/Right`                    | Move the cursor                                                                                                                                         |
| modified `Left/Right`           | Move by word when the terminal sends `Ctrl` or `Meta` with the arrow key                                                                                |
| `Home` / `Ctrl+A`               | Start of line                                                                                                                                           |
| `End` / `Ctrl+E`                | End of line                                                                                                                                             |
| `Backspace`                     | Delete the character to the left of the cursor                                                                                                          |
| `Delete`                        | Delete the character to the right of the cursor                                                                                                         |
| modified `Backspace`            | Delete the previous word                                                                                                                                |
| modified `Delete`               | Delete the next word                                                                                                                                    |
| `Ctrl+W`                        | Delete the previous word                                                                                                                                |
| `Ctrl+U`                        | Delete from the cursor back to the start of the line                                                                                                    |
| `Ctrl+K`                        | Delete from the cursor to the end of the line                                                                                                           |
| `Meta+B` / `Meta+F`             | Move by word                                                                                                                                            |
| `!cmd`                          | Run a shell command through the gateway                                                                                                                 |
| `{!cmd}`                        | Inline shell interpolation before send; queued drafts keep the raw text until they are sent                                                            |

Notes:

- `Tab` only applies completions when completions are present and you are not in multiline mode.
- Queue/history navigation only applies when you are not in multiline mode.
- `PgUp` / `PgDn` are left to the terminal emulator; the TUI does not handle them.

### Prompt and picker modes

| Context                     | Keys                | Behavior                                          |
| --------------------------- | ------------------- | ------------------------------------------------- |
| approval prompt             | `Up/Down`, `Enter`  | Move and confirm the selected approval choice     |
| approval prompt             | `o`, `s`, `a`, `d`  | Quick-pick `once`, `session`, `always`, `deny`    |
| approval prompt             | `Esc`, `Ctrl+C`     | Deny                                              |
| clarify prompt with choices | `Up/Down`, `Enter`  | Move and confirm the selected choice              |
| clarify prompt with choices | single-digit number | Quick-pick the matching numbered choice           |
| clarify prompt with choices | `Enter` on "Other"  | Switch into free-text entry                       |
| clarify free-text mode      | `Enter`             | Submit typed answer                               |
| sudo / secret prompt        | `Enter`             | Submit typed value                                |
| sudo / secret prompt        | `Ctrl+C`            | Cancel by sending an empty response               |
| resume picker               | `Up/Down`, `Enter`  | Move and resume the selected session              |
| resume picker               | `1-9`               | Quick-pick one of the first nine visible sessions |
| resume picker               | `Esc`, `Ctrl+C`     | Close the picker                                  |

Notes:

- Clarify free-text mode and masked prompts use `ink-text-input`, so text editing there follows the library's default bindings rather than `components/textInput.tsx`.
- When a blocking prompt is open, the main chat input hotkeys are suspended.
- Clarify mode has no dedicated cancel shortcut in the current client. Sudo and secret prompts only expose `Ctrl+C` cancellation from the app-level blocked handler.

### Interaction rules

- Plain text entered while the agent is busy is queued instead of sent immediately.
- Slash commands and `!cmd` do not queue; they execute immediately even while a run is active.
- Queue auto-drains after each assistant response, unless a queued item is currently being edited.
- `Up/Down` prioritizes queued-message editing over history. History only activates when there is no queue to edit.
- Queued drafts keep their original `!cmd` and `{!cmd}` text while you edit them. Shell commands and interpolation run when the queued item is actually sent.
- If you load a queued item into the input and resubmit plain text, that queue item is replaced, removed from the queue preview, and promoted to send next. If the agent is still busy, the edited item is moved to the front of the queue and sent after the current run completes.
- Completion requests are debounced by 60 ms. Input starting with `/` uses `complete.slash`. A trailing token that starts with `./`, `../`, `~/`, `/`, or `@` uses `complete.path`.
- Text pastes are inserted inline directly into the draft. Nothing is newline-flattened.
- `Cmd/Ctrl+G` (or `Alt+G` in VSCode/Cursor, which intercept the primary keystroke for Find Next) writes the current draft, including any multiline buffer, to a temp file, suspends Ink, launches `$EDITOR`, then restores the TUI and submits the saved text if the editor exits cleanly.
- Input history is stored in `~/.hermes/.hermes_history` or under `HERMES_HOME`.

## Rendering

Assistant output is rendered in one of two ways:

- if the payload already contains ANSI, `messageLine.tsx` prints it directly
- otherwise `components/markdown.tsx` renders a small Markdown subset into Ink components

The Markdown renderer handles headings, lists, block quotes, tables, fenced code blocks, diff coloring, inline code, emphasis, links, and plain URLs.

Tool/status activity is shown in a live activity lane. Transcript rows stay focused on user/assistant turns.

## Prompt flows

The Python gateway can pause the main loop and request structured input:

- `approval.request`: allow once, allow for session, allow always, or deny
- `clarify.request`: pick from choices or type a custom answer
- `sudo.request`: masked password entry
- `secret.request`: masked value entry for a named env var
- `session.list`: used by `SessionPicker` for `/resume`

These are stateful UI branches in `app.tsx`, not separate screens.

## Commands

The local slash handler covers the built-ins that need direct client behavior:

- `/help`
- `/quit`, `/exit`, `/q`
- `/clear`
- `/new`
- `/compact`
- `/resume`
- `/copy`
- `/paste`
- `/details`
- `/logs`
- `/statusbar`, `/sb`
- `/queue`
- `/undo`
- `/retry`

Notes:

- `/copy` sends the selected assistant response through OSC 52.
- `/paste` with no args asks the gateway to attach a clipboard image.
- Text paste remains inline-only; `Cmd+V` / `Ctrl+V` handle layered text/OSC52/image fallback before `/paste` is needed.
- `/details [hidden|collapsed|expanded|cycle]` controls thinking/tool-detail visibility.
- `/statusbar` toggles the status rule on/off.

Anything else falls through to:

1. `slash.exec`
2. `command.dispatch`

That lets Python own aliases, plugins, skills, and registry-backed commands without duplicating the logic in the TUI.

## Event surface

Primary event types the client handles today:

| Event                    | Payload                                         |
| ------------------------ | ----------------------------------------------- |
| `gateway.ready`          | `{ skin? }`                                     |
| `session.info`           | session metadata for banner + tool/skill panels |
| `message.start`          | start assistant streaming                       |
| `message.delta`          | `{ text, rendered? }`                           |
| `message.complete`       | `{ text, rendered?, usage, status }`            |
| `thinking.delta`         | `{ text }`                                      |
| `reasoning.delta`        | `{ text }`                                      |
| `reasoning.available`    | `{ text }`                                      |
| `status.update`          | `{ kind, text }`                                |
| `tool.start`             | `{ tool_id, name, context? }`                   |
| `tool.progress`          | `{ name, preview }`                             |
| `tool.complete`          | `{ tool_id, name }`                             |
| `clarify.request`        | `{ question, choices?, request_id }`            |
| `approval.request`       | `{ command, description }`                      |
| `sudo.request`           | `{ request_id }`                                |
| `secret.request`         | `{ prompt, env_var, request_id }`               |
| `background.complete`    | `{ task_id, text }`                             |
| `error`                  | `{ message }`                                   |
| `gateway.stderr`         | synthesized from child stderr                   |
| `gateway.protocol_error` | synthesized from malformed stdout               |

## Theme model

The client starts with `DEFAULT_THEME` from `theme.ts`, then merges in gateway skin data from `gateway.ready`.

Current branding overrides:

- agent name
- prompt symbol
- welcome text
- goodbye text

Current color overrides:

- banner title, accent, border, body, dim
- label, ok, error, warn

`branding.tsx` uses those values for the logo, session panel, and update notice.

## File map

```text
ui-tui/
  packages/hermes-ink/   forked Ink renderer (local dep)
  src/
    entry.tsx            TTY gate + render()
    app.tsx              top-level Ink tree, composes src/app/*
    gatewayClient.ts     child process + JSON-RPC bridge
    theme.ts             default palette + skin merge
    constants.ts         display constants, hotkeys, tool labels
    types.ts             shared client-side types
    banner.ts            ASCII art data

    app/
      createGatewayEventHandler.ts  event → state mapping
      createSlashHandler.ts         local slash dispatch
      useComposerState.ts           draft + multiline + queue editing
      useInputHandlers.ts           keypress routing
      useTurnState.ts               agent turn lifecycle
      overlayStore.ts               nanostores for overlays
      uiStore.ts                    nanostores for UI flags
      gatewayContext.tsx             React context for gateway client
      constants.ts                  app-level constants
      helpers.ts                    pure helpers
      interfaces.ts                 internal interfaces

    components/
      appChrome.tsx      status bar, input row, completions
      appLayout.tsx      top-level layout composition
      appOverlays.tsx    overlay routing (pickers, prompts)
      branding.tsx       banner + session summary
      markdown.tsx       Markdown-to-Ink renderer
      maskedPrompt.tsx   masked input for sudo / secrets
      messageLine.tsx    transcript rows
      modelPicker.tsx    model switch picker
      prompts.tsx        approval + clarify flows
      queuedMessages.tsx queued input preview
      sessionPicker.tsx  session resume picker
      textInput.tsx      custom line editor
      thinking.tsx       spinner, reasoning, tool activity

    hooks/
      useCompletion.ts   tab completion (slash + path)
      useInputHistory.ts persistent history navigation
      useQueue.ts        queued message management
      useVirtualHistory.ts in-memory history for pickers

    lib/
      history.ts         persistent input history
      messages.ts        message formatting helpers
      osc52.ts           OSC 52 clipboard copy
      rpc.ts             JSON-RPC type helpers
      text.ts            text helpers, ANSI detection, previews

    types/
      hermes-ink.d.ts    type declarations for @hermes/ink

    __tests__/           vitest suite
```

Related Python side:

```text
tui_gateway/
  entry.py               stdio entrypoint
  server.py              RPC handlers and session logic
  render.py              optional rich/ANSI bridge
  slash_worker.py        persistent HermesCLI subprocess for slash commands
```

<!-- HRCN_MINI_README_START -->
# ui-tui

## Folder Purpose

Ink/React terminal UI.

## S - Specification

This folder participates in the Hermes repository according to its local role. Profile source: HRCN v0.1.3. Current repository boundary: HRCN v0.2.4. This README remains a navigation and context surface only.

## HRCN Boundary Note

Profile source: HRCN v0.1.3.
Current repository boundary: HRCN v0.2.4.
This README is a navigation/context surface only.
Runtime, dependency, CMS, API-write, or apply/write authority is not granted by this README.

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

Profile inherited from HRCN v0.1.3. Current repository boundary is HRCN v0.2.4, with RCC repository orientation, CMS permission discipline, RCC-N profile-gated governance, and Hermes upstream development boundaries.

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

For current docs/context work, expected validation is:

```powershell
git status --short
```

## RCC Nexus Echo Location

Sphere Position:

- Shell: middle
- Meridian(s): ui
- Sector: runtime
- Version / TTL: HRCN-v0.2.4 boundary / inherits HRCN-v0.1.3 profile / 180 days
- Last Verified: 2026-06-04

Local Role:

- Ink/React terminal UI.

Evidence Surface:

- `docs/context-layer/hrcn-v0.1.3.validation.json` (profile source)
- `docs/context-layer/hermes-surface-boundary-map.json` (current boundary)
- `docs/context-layer/hrcn-v0.2.4.public-surface-coherence.validation.json` (current public-surface validation)

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
