from __future__ import annotations
import argparse, json, traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

RHP_ERROR_BOX_SCHEMA = "RHP-ERROR-BOX-v0.1"

@dataclass(frozen=True)
class ErrorBox:
    schema: str
    ok: bool
    operation: str
    failure_class: str
    message: str
    raw_path: str = ""
    next_action: str = ""
    expandable_hint: str = "Open raw_path for full traceback/details."
    non_claim_lock: str = "Error box renders failure feedback only. It does not repair, mutate, commit, push, or grant authority."

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def classify_message(message: str) -> str:
    low = message.lower()
    if "eyist_ok" in low or "unexpected keyword argument" in low:
        return "python_helper_typo"
    if "missing_evidence" in low:
        return "current_script_gate_missing_evidence"
    if "pscommandpath" in low or "entrypoint" in low:
        return "entrypoint_invocation_surface"
    if "unknown dirty paths" in low:
        return "residue_classification_gap"
    if "modulenotfounderror" in low:
        return "module_path_execution_bug"
    return "unknown_failure"

def render(box: ErrorBox) -> str:
    glyph = "[FAIL]" if not box.ok else "[OK]"
    return "\n".join([
        f"RHPLOAD [ERR] loop=ERROR-BOX operation={box.operation} | status={'ok' if box.ok else 'failed'} {glyph}",
        "`- error feedback box",
        f"   +- class: {box.failure_class}",
        f"   +- message: {box.message[:220]}",
        f"   +- raw: {box.raw_path or 'not written'}",
        f"   +- expand: {box.expandable_hint}",
        f"   `- next: {box.next_action}",
    ])

def build(operation: str, message: str, raw_path: str = "", next_action: str = "") -> ErrorBox:
    return ErrorBox(RHP_ERROR_BOX_SCHEMA, False, operation, classify_message(message), message, raw_path, next_action)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render RHP error box")
    p.add_argument("--operation", required=True)
    p.add_argument("--message", required=True)
    p.add_argument("--raw-path", default="")
    p.add_argument("--next-action", default="classify, repair, rerun")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    box = build(args.operation, args.message, args.raw_path, args.next_action)
    print(json.dumps(box.as_dict(), indent=2, ensure_ascii=False) if args.json else render(box))
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
