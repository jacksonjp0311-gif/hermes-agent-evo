# HRCN OPS v0.1.0 Tag Plan

Tag name: `hrcn-ops-v0.1.0`

## Tag purpose

Freeze the OPS-010 operational bridge proof state after the release-seal commit is created and pushed.

## Local command used by the seal script

```powershell
git tag -a hrcn-ops-v0.1.0 -m "HRCN OPS v0.1.0 operational bridge proof seal"
git push origin hrcn-ops-v0.1.0
```

## Tag boundary

The tag freezes evidence. It does not grant new authority.

## Required before tag

- OPS-009 final evidence passed.
- OPS-010 release manifest written.
- OPS-010 release notes written.
- OPS-010 final boundary matrix written.
- OPS-010 final evidence written.
- README aligned to OPS-010.

## Non-claim lock

The tag is a repository proof checkpoint, not production readiness, security proof, runtime integration, CMS authority, memory authority, API authority, autonomous authority, or self-authorization.
