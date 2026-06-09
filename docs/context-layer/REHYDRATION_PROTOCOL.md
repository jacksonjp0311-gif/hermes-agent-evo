# Rehydration Protocol

Status: read-only checklist.

Use this checklist when an agent must rehydrate against the Hermes Agent repository before continuing work.

## 1. Live Runtime Verification

Run:

```bash
echo hello
pwd
git branch --show-current
git log --oneline -5
git status --short
git rev-parse HEAD
```

Report:

- terminal execution worked: yes/no
- stdout returned correctly: yes/no
- current branch
- current HEAD
- working tree state

## 2. Repository Identity Verification

Inspect read-only:

- `README.md`
- `pyproject.toml`
- `cli.py`
- `hermes_cli/main.py`
- `hermes_cli/banner.py`
- `hermes_cli/skin_engine.py`
- `tools/environments/base.py`
- `tools/environments/local.py`
- `tools/terminal_tool.py`

Report what the repository is based on actual files, not memory.

## 3. RHP Surface Inspection

Check:

```bash
test -e rhp_runtime_bridge.py && echo present || echo missing
test -d docs/context-layer && echo present || echo missing
```

Classify RHP state:

- absent
- partial/stale
- present but inactive
- present and wired
- unknown

## 4. HRCN Surface Inspection

Check:

```bash
test -e hrcn_runtime_bridge.py && echo present || echo missing
test -d docs/context-layer && echo present || echo missing
```

Classify HRCN state:

- absent
- partial/stale
- present but inactive
- present and wired
- unknown

## 5. Drift / Risk Map

List only evidence-backed risks:

- stale docs
- missing context docs
- inactive RHP wiring
- inactive HRCN wiring
- encoding risk
- terminal backend risk
- branch/main cleanliness

## 6. Authority Boundary

End every rehydration report with:

Runtime source authority: read-only until authorized  
RHP authority: diagnostic only  
CMS write authority: false  
Memory promotion authority: false  
External ingestion authority: false  
Autonomous authority: false  
Human authorization required: true
