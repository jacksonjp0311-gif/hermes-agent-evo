# Feedback Lifecycle Contracts

Echo Location:

| Field | Value |
|---|---|
| Shell | middle |
| Meridian | feedback, validation, evidence |
| Sector | feedback |
| Version / TTL | CMS-RCC-N-v0.3b1a / 180 days |
| Last verified | 2026-06-02 |

## Purpose

Stores the feedback lifecycle contract that defines scoring, classification, downgrade, negative-control, surrogate/dry-run, and non-claim lock requirements.

## Inputs

Feedback governance rules and promotion constraints.

## Outputs

Machine-readable feedback lifecycle contract JSON.

## Validation

``powershell
python scripts/validation/validate_feedback_lifecycle_v0_3b.py
``

## Alignment Rule

This mini README must update when this folder's purpose, files, routing meaning, evidence role, validation command, or public interpretation changes.

## Non-claim Lock

This folder supports repository-bound reflective feedback alignment. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.