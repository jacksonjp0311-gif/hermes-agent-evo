# OPS-003 to OPS-004 Run Plan

OPS-004 may perform the first local smoke run if OPS-003 passes.

Candidate OPS-004 commands:

    python.exe -m venv .venv
    .\.venv\Scripts\python.exe -m pip install --upgrade pip
    .\.venv\Scripts\python.exe -m pip install -e .
    .\.venv\Scripts\hermes.exe --help
    .\.venv\Scripts\hermes-agent.exe --help
    .\.venv\Scripts\hermes-acp.exe --help

OPS-004 boundary:

- .venv may be created locally but must not be committed.
- no .env commit
- no API key commit
- no provider call
- no CMS write
- no runtime source mutation
- no dependency file mutation commit
- evidence only under docs/context-layer/ops/
