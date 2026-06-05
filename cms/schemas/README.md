# CMS Schemas

Echo Location:

| Field | Value |
|---|---|
| Shell | middle |
| Meridian | feedback, validation, evidence |
| Sector | feedback |
| Version / TTL | CMS-RCC-N-v0.3b1a / 180 days |
| Last verified | 2026-06-02 |

## Purpose

Stores machine-readable JSON schemas for typed CMS objects including feedback items and reflective geometry nodes.

## Inputs

Runtime contract requirements.

## Outputs

feedback_item.schema.json and reflective_git_node.schema.json.

## Validation

``powershell
python scripts/validation/validate_surface_alignment_v0_3b1a.py
``

## Alignment Rule

This mini README must update when this folder's purpose, files, routing meaning, evidence role, validation command, or public interpretation changes.

## Non-claim Lock

This folder supports repository-bound reflective feedback alignment. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.