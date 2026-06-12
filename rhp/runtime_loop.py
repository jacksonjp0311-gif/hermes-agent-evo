from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

from rhp.visible_console import ConsoleField, ConsolePanel, render_panel


RUNTIME_LOOP_ORDER = (
    "ENTRYPOINT-GATE",
    "ROOT-ANCHOR",
    "RESIDUE-MANAGER",
    "PREAUTH-PULL",
    "HUMAN-AUTHORIZATION",
    "RHPREADY",
    "OPERATION-START",
    "RHPLOOP-DOCTOR",
    "RHPLOOP-SELF-LEARNING",
    "VALIDATION",
    "SECRET-SCAN",
    "COMMIT-SEAL",
    "PUSH-SEAL",
    "RHPDROP",
    "RHPREFLECT",
    "POST-SEAL-RESIDUE",
    "RETURN-ROOT",
    "HUMAN-UI-SUMMARY",
)


DIAGNOSTIC_NONZERO_STAGES = {
    "doctor-cli-readonly",
    "doctor-cli-readonly-runtime",
    "rhpready-diagnostic",
    "rhpready-diagnostic-runtime",
}


@dataclass(frozen=True)
class CommandRecord:
    stage: str
    exit: int
    raw: str = ""
    diagnostic_nonzero_allowed: bool = False


@dataclass(frozen=True)
class RuntimeLoopSummary:
    hard_failed: int
    diagnostic_nonzero: int
    ok: int
    total: int
    records: Sequence[CommandRecord] = field(default_factory=tuple)


def classify_command_records(records: Iterable[dict[str, Any]]) -> RuntimeLoopSummary:
    normalized: list[CommandRecord] = []
    hard_failed = 0
    diagnostic_nonzero = 0
    ok = 0
    for item in records:
        stage = str(item.get("stage", ""))
        code = int(item.get("exit", 0))
        diagnostic_allowed = (
            code != 0
            and (
                stage in DIAGNOSTIC_NONZERO_STAGES
                or stage.startswith("doctor-cli-readonly")
                or stage.startswith("rhpready-diagnostic")
            )
        )
        normalized.append(CommandRecord(
            stage=stage,
            exit=code,
            raw=str(item.get("raw", "")),
            diagnostic_nonzero_allowed=diagnostic_allowed,
        ))
        if code == 0:
            ok += 1
        elif diagnostic_allowed:
            diagnostic_nonzero += 1
        else:
            hard_failed += 1
    return RuntimeLoopSummary(
        hard_failed=hard_failed,
        diagnostic_nonzero=diagnostic_nonzero,
        ok=ok,
        total=len(normalized),
        records=tuple(normalized),
    )


def render_runtime_loop_order_panel() -> str:
    fields = [ConsoleField(f"{idx:02d}", stage) for idx, stage in enumerate(RUNTIME_LOOP_ORDER, start=1)]
    return render_panel(ConsolePanel(
        tag="RHPLOOP-RUNTIME [GOLD]",
        title="canonical runtime loop order",
        status="aligned",
        tone="gold",
        fields=fields,
        footer="doctor and self-learning run before reflection and human summary",
    ))


def render_command_summary_panel(records: Iterable[dict[str, Any]]) -> str:
    summary = classify_command_records(records)
    status = "ok" if summary.hard_failed == 0 else "failed"
    fields = [
        ConsoleField("total", str(summary.total)),
        ConsoleField("ok", str(summary.ok)),
        ConsoleField("diagnostic-nonzero", str(summary.diagnostic_nonzero)),
        ConsoleField("hard-failed", str(summary.hard_failed)),
    ]
    return render_panel(ConsolePanel(
        tag="RHPDROP [closed]",
        title="runtime-aware command summary",
        status=status,
        tone="gold" if status == "ok" else "red",
        fields=fields,
        footer="diagnostic nonzero is not hard failure when valid evidence exists",
    ))


def render_self_learning_runtime_panel(
    *,
    observed_event: str,
    evidence_path: str,
    lesson: str,
    future_behavior_change: str,
    authority_boundary: str = "no authority grant",
) -> str:
    fields = [
        ConsoleField("observed-event", observed_event),
        ConsoleField("evidence", evidence_path),
        ConsoleField("lesson", lesson),
        ConsoleField("future-behavior", future_behavior_change),
        ConsoleField("authority", authority_boundary),
    ]
    return render_panel(ConsolePanel(
        tag="RHPLOOP-SELF-LEARNING [GOLD]",
        title="runtime lesson checkpoint before final summary",
        status="observed",
        tone="gold",
        fields=fields,
        footer="promotion: evidence-gated / human-authorized [LOCKED]",
    ))
