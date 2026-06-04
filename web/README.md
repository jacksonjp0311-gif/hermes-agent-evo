# Hermes Agent — Web UI

Browser-based dashboard for managing Hermes Agent configuration, API keys, and monitoring active sessions.

## Stack

- **Vite** + **React 19** + **TypeScript**
- **Tailwind CSS v4** with custom dark theme
- **shadcn/ui**-style components (hand-rolled, no CLI dependency)

## Development

```bash
# Start the backend API server
cd ../
python -m hermes_cli.main web --no-open

# In another terminal, start the Vite dev server (with HMR + API proxy)
cd web/
npm install
npm run dev
```

Open the **Vite URL** printed in the terminal (usually `http://localhost:5173`). That is the live-reload UI.

`hermes dashboard` on port 9119 serves the **built** bundle from `hermes_cli/web_dist/`, not the Vite dev server — changes in `web/src/` will not appear there until you run `npm run build` and restart the dashboard (or use `web --no-open` + Vite as above).

The Vite dev server proxies `/api` requests to `http://127.0.0.1:9119` (the FastAPI backend).

## Build

```bash
npm run build
```

This outputs to `../hermes_cli/web_dist/`, which the FastAPI server serves as a static SPA. The built assets are included in the Python package via `pyproject.toml` package-data.

## Structure

```
src/
├── components/ui/   # Reusable UI primitives (Card, Badge, Button, Input, etc.)
├── lib/
│   ├── api.ts       # API client — typed fetch wrappers for all backend endpoints
│   └── utils.ts     # cn() helper for Tailwind class merging
├── pages/
│   ├── StatusPage   # Agent status, active/recent sessions
│   ├── ConfigPage   # Dynamic config editor (reads schema from backend)
│   └── EnvPage      # API key management with save/clear
├── App.tsx          # Main layout and navigation
├── main.tsx         # React entry point
└── index.css        # Tailwind imports and theme variables
```

## Typography & contrast rules

Read before adding or editing UI styles. These rules keep the dashboard legible across all built-in themes and stop drift back into the patterns the design system was just refactored out of.

### Text size floor

- **Minimum body size: `text-xs` (12px / 0.75rem).** Do not use arbitrary `text-[0.6rem]`, `text-[0.65rem]`, `text-[9px]`, `text-[10px]`, or `text-[11px]` on copy, hints, labels, counts, or badges. Use the standard scale: `text-xs`, `text-sm`, `text-base`.
- Smaller sizes are only acceptable on **decorative overlays** (chart stripes, empty-state icons) — never on text the user is meant to read.

### Opacity floor on text

- **Never apply opacity below 0.7 to text.** No `opacity-30`, `opacity-50`, `opacity-60` on `<span>`s, `<p>`s, labels, etc.
- **Do not stack opacity tokens.** Patterns like `text-muted-foreground/60`, `text-midground/70`, `text-foreground/50` create unpredictable WCAG failures because the parent token already has alpha.
- Use the **semantic text tokens** from `@nous-research/ui`'s `globals.css`:
  - `text-text-primary` — default body text.
  - `text-text-secondary` — subtitles, meta, inactive nav.
  - `text-text-tertiary` — small chrome labels, counts, footnotes.
  - `text-text-disabled` — disabled states.
  - `text-text-on-accent` — text on filled accent surfaces.

### Brand uppercase via `text-display`, not raw `uppercase`

- The dashboard preserves the Nous brand uppercase aesthetic, but it is **opt-in per element, not global**.
- Apply uppercase via the DS utility `text-display` on **brand chrome only** — page titles, nav section headings, badges, brand wordmark. DS components (`Button`, `Badge`, `Tabs`, `Segmented`, etc.) already self-apply `text-display`.
- **Do not introduce new `uppercase`** (the literal Tailwind class) in `hermes-agent/web/src`. Prefer `text-display` for new brand chrome. Legacy `uppercase` call sites (e.g. `components/ui/label.tsx`, `card.tsx`) remain until migrated.
- The app shell no longer forces uppercase globally, so blanket `normal-case` opt-outs are unnecessary. Use `normal-case` only where a DS component applies `text-display` but the label should stay sentence case — e.g. dynamic user content (model slugs, theme names) **or** fixed UI copy that is not brand chrome (EnvPage “not configured” toggle, sidebar “New chat”).

### Fonts

Typography is **opt-in per surface**, not global on layout shells — the app shell and page header keep their original theme/expanded fonts; Mondwest applies only where explicitly set.

| Tier | Classes | Use for |
|------|---------|---------|
| Brand chrome | `font-mondwest text-display` (or `themedChrome`) | Sidebar nav, card section headers (`CardTitle`), Segmented filter buttons, filter panel headings |
| Themed body | `font-mondwest normal-case` (or `themedBody`) | Card content (`Card`, `CardDescription`), session/platform rows, analytics tables — **scoped to the component** |
| Page chrome | `font-expanded` | Page header h1 (`PageHeaderProvider`) — sentence case, not `text-display` |
| Wordmark | `Typography` + size/tracking only | Sidebar/mobile “Hermes Agent” — mixed case, no Mondwest, no `text-display` |
| Technical | `font-mono-ui` / `font-mono` / `font-courier` | Model slugs, env keys, schedules, YAML, repo URLs |

- Do **not** put `themedBody` or `themedFont` on `<main>`, `App`, or other layout wrappers — it overrides component-scoped styles.
- **`Card`** applies `themedBody`; **`CardTitle`** uses `text-display` (uppercase chrome); **`CardDescription`** uses `themedBody`.
- **`NouiTypography`** defaults to `font-sans` unless a font prop is passed.
- Do **not** use raw `font-sans` or `font-display` (theme sans variable) on new dashboard UI — prefer Mondwest tiers above where brand-appropriate.

### Color tokens

- Prefer **semantic tokens** (`text-text-*`, `bg-card`, `border-border`, `text-foreground`, `text-destructive`, `text-success`, `text-warning`) over raw layer references (`text-midground`, `text-foreground`).
- `text-muted-foreground` is now wired to `--color-text-secondary`, so existing call sites stay correct, but new code should prefer the semantic name.
- When you genuinely need a non-token color (icon de-emphasis on a chart, terminal foreground via inline style), keep alpha at `≥ 0.7` for any text.

<!-- HRCN_MINI_README_START -->
# web

## Folder Purpose

Dashboard/frontend app surface.

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

- Shell: outer
- Meridian(s): web
- Sector: ui
- Version / TTL: HRCN-v0.2.4 boundary / inherits HRCN-v0.1.3 profile / 180 days
- Last Verified: 2026-06-04

Local Role:

- Dashboard/frontend app surface.

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
