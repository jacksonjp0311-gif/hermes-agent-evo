from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence


@dataclass(frozen=True)
class ConsoleField:
    key: str
    value: str


@dataclass(frozen=True)
class ConsolePanel:
    tag: str
    title: str
    status: str = "ok"
    tone: str = "cyan"
    fields: Sequence[ConsoleField] = field(default_factory=tuple)
    footer: str = ""


TONE_GUIDE = {
    "green": "success / pass / sealed",
    "gold": "diagnostic / attention / reflection / readiness",
    "cyan": "information / orientation",
    "magenta": "diagnosis / failure class",
    "red": "blocked / failed / unsafe",
    "gray": "raw artifact / low-priority detail",
}


def render_panel(panel: ConsolePanel) -> str:
    lines = [f"{panel.tag} status={panel.status} tone={panel.tone}", f"`- {panel.title}"]
    for item in panel.fields:
        lines.append(f"   +- {item.key}: {item.value}")
    if panel.footer:
        lines.append(f"   `- {panel.footer}")
    return "\n".join(lines)


def render_reflection_panel(
    *,
    operation: str,
    state: str,
    active_wound: str,
    subject_commit: str,
    repair_basis: bool,
    next_operation: str,
    learned: Iterable[str],
) -> str:
    fields = [
        ConsoleField("operation", operation),
        ConsoleField("state", state),
        ConsoleField("active-wound", active_wound),
        ConsoleField("subject", subject_commit),
        ConsoleField("repair-basis", str(repair_basis).lower()),
        ConsoleField("next", next_operation),
    ]
    lines = [render_panel(ConsolePanel(
        tag="RHPREFLECT [GOLD]",
        title="operator reflection summary",
        status="aligned",
        tone="gold",
        fields=fields,
        footer="authority: no grant [LOCKED]",
    ))]
    lines.append("   +- learned:")
    for item in learned:
        lines.append(f"      - {item}")
    return "\n".join(lines)


def required_uncompressed_stages() -> tuple[str, ...]:
    return (
        "ENTRYPOINT-GATE",
        "ROOT-ANCHOR",
        "RESIDUE-MANAGER",
        "PREAUTH-PULL",
        "HUMAN-AUTHORIZATION",
        "RHPREADY",
        "OPERATION-START",
        "RHPDROP",
        "RHPDIAG",
        "VALIDATION",
        "SECRET-SCAN",
        "COMMIT-SEAL",
        "PUSH-SEAL",
        "POST-SEAL-RESIDUE",
        "RETURN-ROOT",
        "HUMAN-UI-SUMMARY",
        "RHPREFLECT",
    )


def minimum_panel_fields() -> tuple[str, ...]:
    return (
        "stage",
        "decision",
        "state",
        "evidence",
        "authority",
        "next",
    )
