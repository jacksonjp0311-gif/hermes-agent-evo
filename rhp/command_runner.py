# RHP-014.2 V3 command runner.
from __future__ import annotations
import argparse, json, subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from rhp.stream_collapse import collapse

RHP_COMMAND_RUNNER_SCHEMA = "RHP-COMMAND-RUNNER-v0.1"

@dataclass(frozen=True)
class CommandRun:
    schema: str
    command: list[str]
    return_code: int
    raw_path: str
    collapsed: dict[str, Any]
    ok: bool
    non_claim_lock: str = "Command runner captures display streams only. It does not alter command semantics, hide nonzero exits, mutate files by itself, or grant authority."

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def run_captured(command: list[str], *, cwd: str | Path = ".", raw_path: str | Path) -> CommandRun:
    raw = Path(raw_path)
    raw.parent.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(command, cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    raw.write_text(p.stdout, encoding="utf-8", newline="\n")
    summary, _rendered = collapse(p.stdout, p.returncode)
    return CommandRun(RHP_COMMAND_RUNNER_SCHEMA, command, p.returncode, str(raw), summary.as_dict(), p.returncode == 0)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Run a command with captured/collapsed stream")
    p.add_argument("--cwd", default=".")
    p.add_argument("--raw-path", required=True)
    p.add_argument("--json", action="store_true")
    p.add_argument("command", nargs=argparse.REMAINDER)
    args = p.parse_args(argv)
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise SystemExit("missing command")
    result = run_captured(command, cwd=args.cwd, raw_path=args.raw_path)
    print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False))
    return 0 if result.ok else result.return_code

if __name__ == "__main__":
    raise SystemExit(main())
