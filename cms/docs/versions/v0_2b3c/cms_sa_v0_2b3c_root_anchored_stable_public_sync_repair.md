# CMS-SA v0.2b3c - Root-Anchored Stable Public Sync Repair

## Purpose

Repair the failed v0.2b3b attempt without rewriting history.

## Problem

v0.2b3b was tagged, but its intended validator and document writes did not land because file writes were not root-anchored. The old HEAD-bound public-sync validator remained active.

## Repair

- Root-anchor every file write.
- Preserve v0.2b3b as failed-but-useful.
- Replace committed public-sync report semantics with stable fields.
- Omit volatile commit hashes from committed latest report.
- Keep runtime HEAD/origin/tag checks active.

## Lessons

- CMS-L-008: committed public-sync reports must not store volatile commit hashes.
- CMS-L-009: all orchestrator writes must be root-anchored and run as a file.

## Non-claim lock

This improves repository-state traceability only.