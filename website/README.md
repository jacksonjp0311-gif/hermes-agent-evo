# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Installation

```bash
yarn
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## Diagram Linting

CI runs `ascii-guard` to lint docs for ASCII box diagrams. Use Mermaid (````mermaid`) or plain lists/tables instead of ASCII boxes to avoid CI failures.

<!-- HRCN_MINI_README_START -->
# website

## Folder Purpose

Public Docusaurus documentation site.

Profile: `compact`

## HRCN Position

- Shell: outer
- Meridian(s): documentation
- Sector: public
- Version / TTL: HRCN-v0.1.3 / 180 days
- Last Verified: 2026-06-04

## Read Before Editing

- `README.md`
- `AGENTS.md`
- `docs/context-layer/rcc-cms-hrcn.md`
- `docs/context-layer/hermes-agent-rehydration-protocol.md`
- this README

## Boundary

This folder README is navigation only. It does not prove correctness, safety, production readiness, security, consciousness, sentience, autonomy, AGI/ASI, or external validation.

## Update Rule

If this folder's purpose, files, routes, evidence surfaces, validation commands, or claim boundaries change, update this mini README and the root HRCN README block in the same commit.

Non-claim locks:

- navigation_is_not_validation
- documentation_is_not_correctness
- profile_adoption_is_not_validation
- rehydration_is_not_authority
<!-- HRCN_MINI_README_END -->
