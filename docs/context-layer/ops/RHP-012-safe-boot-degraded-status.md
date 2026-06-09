# RHP-012 Safe Boot Failure Mode and Degraded Startup Status

RHP-012 proves that Hermes RHP boot orientation can degrade visibly without crashing, false-green reporting, or authority expansion.

## Repair notes

First run exposed a valid alignment error: the startup packet schema advanced toward v0.4 but explicit degraded fields were not inserted.

Second repair exposed a process-level smoke timeout. RHP-012 Repair V2 avoids stdout/stderr pipe deadlock by redirecting child process output to proof files through `cmd.exe`, and it uses compact smoke output.

## Target behavior

```text
green evidence -> verified startup
missing evidence -> degraded startup
degraded startup -> authority remains false
```

Boundary: startup safety/status only. No provider call, model call, tool call, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.