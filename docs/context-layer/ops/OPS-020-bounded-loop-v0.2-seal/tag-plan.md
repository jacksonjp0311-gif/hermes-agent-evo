# HRCN OPS v0.2.0 Tag Plan

Tag name: `hrcn-ops-v0.2.0`

## Purpose

Freeze the bounded loop v0.2 proof after the OPS-020 seal commit.

## Local commands used by the shell script

```powershell
git tag -a hrcn-ops-v0.2.0 -m "HRCN OPS v0.2.0 bounded loop proof seal"
git push origin hrcn-ops-v0.2.0
```

## Required before tag

- OPS-019 final evidence passed.
- OPS-020 release manifest written.
- OPS-020 final boundary matrix written.
- OPS-020 release notes written.
- OPS-020 proof graph written.
- README aligned to OPS-020.

## Non-claim lock

The tag freezes evidence only. It does not grant runtime, CMS, memory, API, dependency, provider/model, autonomous, production, or self-authorization authority.
