from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

from rhp.visible_console import ConsoleField, ConsolePanel, render_panel

SPINNERS = ("|", "/", "-", "\\")

PROGRESS_STAGE_ORDER: tuple[tuple[str, int], ...] = (
    ("ENTRYPOINT-GATE", 5),
    ("ROOT-ANCHOR", 10),
    ("RESIDUE-MANAGER", 15),
    ("PREAUTH-PULL", 20),
    ("RHPLOOP-RUNTIME", 25),
    ("HUMAN-AUTHORIZATION", 30),
    ("RHPREADY", 35),
    ("OPERATION-START", 40),
    ("RHPLOOP-DOCTOR", 50),
    ("RHPLOOP-SELF-LEARNING", 60),
    ("VALIDATION", 70),
    ("SECRET-SCAN", 78),
    ("COMMIT-SEAL", 84),
    ("PUSH-SEAL", 90),
    ("RHPDROP", 94),
    ("RHPREFLECT", 97),
    ("POST-SEAL-RESIDUE", 98),
    ("RETURN-ROOT", 99),
    ("HUMAN-UI-SUMMARY", 100),
)

PROGRESS_STAGE_PERCENT: Mapping[str, int] = dict(PROGRESS_STAGE_ORDER)


@dataclass(frozen=True)
class ProgressFrame:
    stage: str
    percent: int
    spinner: str
    status: str
    detail: str
    tone: str = "green"


def progress_bar(percent: int, width: int = 20) -> str:
    """Backward-compatible bar renderer for evidence files/tests.

    Operator body output should not print this inline. Use render_settled_stage()
    for clean body panels and PowerShell Write-Progress for motion.
    """
    clamped = max(0, min(100, int(percent)))
    filled = round((clamped / 100) * width)
    return "[" + ("#" * filled) + ("-" * (width - filled)) + "]"


def spinner_for(stage: str, tick: int = 0) -> str:
    index = (len(stage) + tick) % len(SPINNERS)
    return SPINNERS[index]


def frame_for(stage: str, *, status: str = "ok", detail: str = "", tick: int = 0, tone: str = "green") -> ProgressFrame:
    percent = PROGRESS_STAGE_PERCENT.get(stage, 0)
    return ProgressFrame(
        stage=stage,
        percent=percent,
        spinner=spinner_for(stage, tick=tick),
        status=status,
        detail=detail,
        tone=tone,
    )


def render_progress_frame(frame: ProgressFrame, *, operation: str) -> str:
    """Legacy evidence renderer.

    Kept for compatibility with RHP-018.11 tests/evidence. Runtime body output
    should use render_settled_stage() so no inline [#---] bars or spin= spam
    appear in the operator console body.
    """
    return "\n".join([
        f"RHPLOAD [{frame.percent:03d}%] spin={frame.spinner} loop={frame.stage} operation={operation} | status={frame.status} tone={frame.tone}",
        f"`- {progress_bar(frame.percent)} {frame.detail}",
    ])


def render_settled_stage(stage: str, *, operation: str, status: str, detail: str, tone: str = "green") -> str:
    percent = PROGRESS_STAGE_PERCENT.get(stage, 0)
    return "\n".join([
        f"RHPLOAD [{percent:03d}%] loop={stage} operation={operation} | status={status} tone={tone}",
        f"`- {detail}",
    ])


def render_progress_sequence(operation: str) -> str:
    lines: list[str] = []
    for stage, _percent in PROGRESS_STAGE_ORDER:
        tone = "gold" if stage.startswith("RHPLOOP") or stage in {"RHPREADY", "RHPDROP", "RHPREFLECT", "HUMAN-UI-SUMMARY"} else "green"
        lines.append(render_settled_stage(
            stage,
            operation=operation,
            status="checkpoint",
            detail="settled checkpoint; motion is top progress only",
            tone=tone,
        ))
    return "\n".join(lines)


def animation_frames(start_percent: int, end_percent: int, *, stage: str, status: str, detail: str, operation: str) -> tuple[str, ...]:
    """Compatibility surface: returns synthetic frames for tests/evidence.

    Do not print these as runtime body output.
    """
    start = max(0, min(100, int(start_percent)))
    end = max(start, min(100, int(end_percent)))
    if end == start:
        steps = [end]
    else:
        step = max(1, (end - start) // 5 or 1)
        steps = list(range(start, end + 1, step))
        if steps[-1] != end:
            steps.append(end)
    frames: list[str] = []
    for tick, percent in enumerate(steps):
        frame = ProgressFrame(
            stage=stage,
            percent=percent,
            spinner=spinner_for(stage, tick=tick),
            status=status,
            detail=detail,
            tone="gold" if stage.startswith("RHPLOOP") or stage in {"RHPREADY", "RHPDROP", "RHPREFLECT", "HUMAN-UI-SUMMARY"} else "green",
        )
        frames.append(render_progress_frame(frame, operation=operation))
    return tuple(frames)


def required_progress_stages() -> tuple[str, ...]:
    return tuple(stage for stage, _ in PROGRESS_STAGE_ORDER)


def progress_contract() -> dict[str, Any]:
    return {
        "schema": "RHP-RUNTIME-PROGRESS-CONSOLE-CONTRACT-v0.5",
        "requires_percent": True,
        "requires_global_top_progress": True,
        "requires_concise_settled_sections": True,
        "body_inline_bars_allowed": False,
        "body_spinner_allowed": False,
        "body_frame_spam_allowed": False,
        "preferred_runtime_surface": "PowerShell Write-Progress",
        "motion_rule": "Use one global top progress surface, then emit concise settled loop panels. Do not print inline [#---] bars or spin= frames in the body.",
        "stage_order": [
            {"stage": stage, "percent": percent}
            for stage, percent in PROGRESS_STAGE_ORDER
        ],
        "non_claim_lock": "Progress console contract changes operator visibility only and grants no authority.",
    }


def global_progress_contract() -> dict[str, Any]:
    return {
        "schema": "RHP-GLOBAL-TOP-PROGRESS-CONTRACT-v0.2",
        "preferred_runtime_surface": "PowerShell Write-Progress",
        "console_rule": "One moving top progress bar plus concise settled panels; no inline body bars; no spin= body spam.",
        "requires_percent": True,
        "requires_current_stage": True,
        "requires_status": True,
        "requires_concise_settled_sections": True,
        "body_inline_bars_allowed": False,
        "body_spinner_allowed": False,
        "non_claim_lock": "Global top progress is operator UX only and grants no authority.",
    }
