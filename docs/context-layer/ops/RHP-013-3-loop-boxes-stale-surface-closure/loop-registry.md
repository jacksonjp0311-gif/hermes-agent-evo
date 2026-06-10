# RHP-013.3 Loop Registry

## Purpose

This registry makes the repository teach future AI agents what loop to run before editing.

## Loop boxes

- Rehydration Loop
- Diagnosis Loop
- Mutation Loop
- Evidence Loop
- CI Watch Loop
- CI Repair Loop
- Learning Loop
- Runtime Status Loop
- Security Boundary Loop
- No-Op Loop

## Key improvement

The system now separates observation, diagnosis, mutation, evidence, CI watch, repair, and learning. This prevents a future agent from treating every prompt as an edit request.

## Boundary

Loop boxes are procedure and orientation only. They grant no runtime/provider/tool/CMS/memory/API/external-ingestion/autonomy authority.
