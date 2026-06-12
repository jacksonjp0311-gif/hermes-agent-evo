from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence
import re


FULL_RUNTIME_GEOMETRY: tuple[str, ...] = (
    "ENTRYPOINT-GATE",
    "ROOT-ANCHOR",
    "RESIDUE-MANAGER",
    "PREAUTH-PULL",
    "RHPLOOP-RUNTIME",
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

VISIBLE_BODY_GEOMETRY: tuple[str, ...] = (
    "RHPREADY",
    "RHPLOOP-DOCTOR",
    "RHPLOOP-SELF-LEARNING",
    "RHPDROP",
    "RHPREFLECT",
    "POST-SEAL-RESIDUE",
    "RETURN-ROOT",
    "HUMAN-UI-SUMMARY",
)

GEOMETRY_SOURCE_MARKER_START = "<!-- RHP_CANONICAL_RUNTIME_RUN_BLOCK_START -->"
GEOMETRY_SOURCE_MARKER_END = "<!-- RHP_CANONICAL_RUNTIME_RUN_BLOCK_END -->"


@dataclass(frozen=True)
class GeometryReport:
    expected: tuple[str, ...]
    observed: tuple[str, ...]
    missing: tuple[str, ...]
    unexpected: tuple[str, ...]
    order_ok: bool
    ok: bool


def _unique_preserve_order(items: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return tuple(out)


def extract_readme_run_block(readme_text: str) -> str:
    start = readme_text.find(GEOMETRY_SOURCE_MARKER_START)
    end = readme_text.find(GEOMETRY_SOURCE_MARKER_END)
    if start < 0 or end < 0 or end <= start:
        return ""
    return readme_text[start:end]


def extract_loop_geometry_from_text(text: str) -> tuple[str, ...]:
    loops: list[str] = []
    for line in text.splitlines():
        loop_match = re.search(r"\bloop=([A-Z0-9-]+)", line)
        if loop_match:
            loops.append(loop_match.group(1))
            continue
        direct_match = re.match(r"^\s*(RHPREADY|RHPDROP|RHPREFLECT|RHPLOOP-[A-Z0-9-]+)\b", line)
        if direct_match:
            loops.append(direct_match.group(1))
    return _unique_preserve_order(loops)


def ordered_subset_ok(expected: Sequence[str], observed: Sequence[str]) -> bool:
    positions = {stage: idx for idx, stage in enumerate(observed)}
    last = -1
    for stage in expected:
        if stage not in positions:
            return False
        current = positions[stage]
        if current < last:
            return False
        last = current
    return True


def geometry_report(expected: Sequence[str], observed: Sequence[str]) -> GeometryReport:
    expected_t = tuple(expected)
    observed_t = tuple(observed)
    expected_set = set(expected_t)
    observed_set = set(observed_t)
    missing = tuple(stage for stage in expected_t if stage not in observed_set)
    unexpected = tuple(stage for stage in observed_t if stage not in expected_set)
    order_ok = ordered_subset_ok(expected_t, observed_t)
    return GeometryReport(
        expected=expected_t,
        observed=observed_t,
        missing=missing,
        unexpected=unexpected,
        order_ok=order_ok,
        ok=(not missing and not unexpected and order_ok),
    )


def validate_full_runtime_geometry(observed: Sequence[str]) -> GeometryReport:
    return geometry_report(FULL_RUNTIME_GEOMETRY, observed)


def validate_visible_body_geometry(observed: Sequence[str]) -> GeometryReport:
    return geometry_report(VISIBLE_BODY_GEOMETRY, observed)


def validate_readme_geometry(readme_text: str) -> GeometryReport:
    block = extract_readme_run_block(readme_text)
    observed = extract_loop_geometry_from_text(block)
    return validate_full_runtime_geometry(observed)


def report_to_dict(report: GeometryReport) -> dict:
    return {
        "expected": list(report.expected),
        "observed": list(report.observed),
        "missing": list(report.missing),
        "unexpected": list(report.unexpected),
        "order_ok": report.order_ok,
        "ok": report.ok,
    }


def render_geometry_panel(report: GeometryReport, *, operation: str) -> str:
    status = "aligned" if report.ok else "blocked"
    lines = [
        f"RHPLOOP-GEOMETRY [GOLD] operation={operation} status={status}",
        "`- runtime geometry alignment",
        f"   +- expected-count: {len(report.expected)}",
        f"   +- observed-count: {len(report.observed)}",
        f"   +- missing: {','.join(report.missing) if report.missing else 'none'}",
        f"   +- unexpected: {','.join(report.unexpected) if report.unexpected else 'none'}",
        f"   +- order-ok: {str(report.order_ok).lower()}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\n".join(lines)
def geometry() -> dict:
    """Legacy compatibility surface for pre-runtime-geometry tests."""
    return {
        "schema": "RHP-LOOP-GEOMETRY-v0.1",
        "axes": [
            "evidence",
            "authority",
            "runtime",
            "residue",
            "reflection",
        ],
        "boundary": "human authorization",
        "adaptation_rule": "AI may propose bounded tools; only human authorization may cross the boundary.",
    }
