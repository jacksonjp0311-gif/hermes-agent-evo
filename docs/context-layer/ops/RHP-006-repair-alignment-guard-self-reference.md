# RHP-006 Repair — Alignment Guard Self-Reference Fix

- operation: RHP-006 repair
- previous failure: alignment guard required final evidence to be green before the script reached final evidence-writing phase
- second failure: manual continuation committed red evidence after the guard stopped
- repair lesson: RHP-L-008
- preflight alignment mode: true
- final alignment mode: true
- py_compile passed: true
- focused tests passed: true
- final alignment guard passed: true
- next: RHP-007 first governed RHP to HRCN to Hermes proposal-loop proof

## RHP-L-008

A guard can stop correctly, but manual continuation can still commit red evidence. After any guard failure, run a repair seal and do not manually stage, commit, or push post-failure artifacts.

## Boundary

RHP-006 repair fixes guard sequencing and state coherence only. It does not execute CMS, write CMS, write memory, write APIs, change dependencies, call a provider/model, grant tool authority, operate autonomously, or self-authorize.
