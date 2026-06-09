# HRCN v0.1 — Hermes Rehydration Context Notes

Status: documentation-only.

HRCN is a proposed documentation convention for durable, human-readable context surfaces inside the Hermes Agent repository.

It is subordinate to Hermes Agent identity. It is not a new product identity.

## Current State

- `hrcn_runtime_bridge.py`: absent
- Runtime wiring: absent
- Memory integration: absent
- CMS integration: absent
- External ingestion authority: false

## What HRCN Is

HRCN is:

- a context note convention
- a rehydration support surface
- a documentation scaffold for future repo orientation
- a way to preserve boundaries and verification rules

## What HRCN Is Not

HRCN is not:

- a runtime injector
- a memory system
- a CMS
- a startup hook
- a prompt-construction layer
- a tool registry
- an autonomous authority layer

## Relationship to Hermes

HRCN may document how Hermes should rehydrate against repository state.

It must not claim Hermes is HRCN-native, HRCN-powered, or runtime-wired unless future code and tests establish that fact.

## Future Integration Gates

Runtime integration requires:

- explicit human authorization
- a branch
- design notes
- tests
- failure-mode documentation
- no default behavior change
- no write authority by default
