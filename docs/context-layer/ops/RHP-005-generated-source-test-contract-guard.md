# RHP-005 Generated Source + Test Contract Guard

- operation: RHP-005
- guard: `rhp/generated_source_guard.py`
- tests: `tests/test_rhp_generated_source_guard.py`
- generated Python requires py_compile: true
- runtime touch requires focused tests: true
- test contract migration required: true
- failed tests are commit blockers: true
- RHP-L-006 logged: true
- next: RHP-006 README/state/bridge/evidence alignment guard

## RHP-L-006

A repo can shape AI behavior through local evidence, tests, and README geometry, but shape must remain bounded by compile/test/evidence gates.

## Boundary

RHP-005 installs a local validation helper only. It does not execute CMS, write CMS, write memory, write APIs, change dependencies, call a provider/model, grant tool authority, operate autonomously, or self-authorize.
