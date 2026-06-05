# OPS-002 Command Map

Purpose: make the HRCN v2.0 operating cadence repeatable without creating a new authority version.

Status commands:

  python.exe .\scripts\hrcn\operator_command_surface_v1_9.py --status
  python.exe .\scripts\hrcn\operational_nexus_status_v2_0.py --status

Gate commands:

  python.exe .\scripts\hrcn\operator_command_surface_v1_9.py --gates
  python.exe .\scripts\hrcn\operator_command_surface_v1_9.py --next-commands

Apply command shape:

  python.exe .\scripts\hrcn\limited_apply_executor_v1_6.py --packet PACKET.json --apply --authorization-phrase "I AUTHORIZE HRCN V1.6 LIMITED DOCS CONTEXT APPLY"

Replay command shape:

  python.exe .\scripts\hrcn\replay_rollback_hardening_v1_8.py --manifest MANIFEST.json --check --write-report

Rule: direct tool calls are preferred over wrapper functions until runtime readiness is closed.