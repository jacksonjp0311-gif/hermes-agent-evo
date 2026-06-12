from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

ALLOWED_PREFIXES: tuple[str, ...] = (
    "docs/context-layer/ops/RHP-021-2-current-operation-ci-wound-packet/",
    "docs/context-layer/ops/RHP-021-2-final-evidence.json",
    "rhp/current_operation_ci_wound_packet.py",
    "tests/test_rhp_021_2_current_operation_ci_wound_packet.py",
)

ALLOWED_CONTEXT_FILES: tuple[str, ...] = (
    "docs/context-layer/latest-rhp.json",
    "docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md",
    "docs/context-layer/rhp_zero_context_rebuild.json",
    "README.md",
    "AGENTS.md",
)


@dataclass(frozen=True)
class ResidueClassification:
    ok: bool
    residue_count: int
    bounded_count: int
    unbounded_count: int
    bounded_paths: tuple[str, ...]
    unbounded_paths: tuple[str, ...]
    classification: str
    next_action: str


def parse_git_status_lines(lines: Iterable[str]) -> tuple[str, ...]:
    paths: list[str] = []
    for raw in lines:
        line = raw.strip("\n\r")
        if not line.strip():
            continue
        path = line[3:].strip() if len(line) >= 4 else line.strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        paths.append(path.replace("\\", "/"))
    return tuple(paths)


def is_bounded_path(path: str) -> bool:
    p = path.replace("\\", "/")
    if p in ALLOWED_CONTEXT_FILES:
        return True
    return any(p.startswith(prefix) for prefix in ALLOWED_PREFIXES)


def classify_residue(lines: Iterable[str]) -> ResidueClassification:
    paths = parse_git_status_lines(lines)
    bounded = tuple(p for p in paths if is_bounded_path(p))
    unbounded = tuple(p for p in paths if not is_bounded_path(p))
    ok = len(unbounded) == 0
    classification = "bounded_rhp_021_2_residue" if ok else "unbounded_residue_requires_operator_review"
    next_action = "clean_bounded_residue_and_reseal" if ok else "stop_and_classify_unbounded_paths"
    return ResidueClassification(
        ok=ok,
        residue_count=len(paths),
        bounded_count=len(bounded),
        unbounded_count=len(unbounded),
        bounded_paths=bounded,
        unbounded_paths=unbounded,
        classification=classification,
        next_action=next_action,
    )


def to_dict(result: ResidueClassification) -> dict:
    return {
        "ok": result.ok,
        "residue_count": result.residue_count,
        "bounded_count": result.bounded_count,
        "unbounded_count": result.unbounded_count,
        "bounded_paths": list(result.bounded_paths),
        "unbounded_paths": list(result.unbounded_paths),
        "classification": result.classification,
        "next_action": result.next_action,
    }


def render_panel(result: ResidueClassification) -> str:
    status = "classified" if result.ok else "blocked"
    return "\n".join([
        f"RHPRESIDUE [GOLD] status={status}",
        "`- post-seal residue classification",
        f"   +- residue-count: {result.residue_count}",
        f"   +- bounded-count: {result.bounded_count}",
        f"   +- unbounded-count: {result.unbounded_count}",
        f"   +- classification: {result.classification}",
        f"   +- next-action: {result.next_action}",
        "   `- authority: no grant [LOCKED]",
    ])
