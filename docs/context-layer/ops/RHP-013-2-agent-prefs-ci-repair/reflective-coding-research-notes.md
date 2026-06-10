# RHP-013.2 AI/Agent Preferences + Reflective Coding Status Notes

## External signals

- Progress indicators are useful because they tell operators that work is ongoing and can show percentage or phase in CLI/TUI environments.
- AGENTS.md-style context files can reduce runtime/token waste when concise and operational.
- AGENTS.md-style context files can hurt task success when they over-specify behavior or create unnecessary requirements.
- Agent context files tend to prioritize build commands, implementation details, and architecture; security/performance guardrails are often under-specified.
- Coding agents have action bias; explicitly allowing no-op diagnostics helps avoid unnecessary code churn.

## Applied design

RHP-013.2 adds:

```text
README AI/Agent Preferences section
+ appendable preference chart
+ AGENTS.md load-status contract
+ stale alignment-guard test repair
+ evidence-backed next gate
```

## Runtime boundary

No runtime status bar is wired in this operation. Runtime wiring is deferred to RHP-013.3.
