from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]


OBSERVABLE_KEYS = ["R", "E", "V", "L", "D", "F", "N", "S", "C", "A"]


@dataclass(frozen=True)
class FeedbackItem:
    id: str
    source: str
    summary: str
    route: dict[str, Any]
    observables: dict[str, int]
    evidence: list[str]
    validator_binding: list[str]
    downgrade_path: str
    negative_control: str
    surrogate_or_dry_run: str
    falsification_condition: str
    non_claim_lock: str

    @property
    def score(self) -> float:
        values = [int(self.observables.get(key, 0)) for key in OBSERVABLE_KEYS]
        return sum(values) / len(OBSERVABLE_KEYS)

    @property
    def classification(self) -> str:
        score = self.score
        if score == 1.0:
            return "CMS-FB-A"
        if score >= 0.8:
            return "CMS-FB-B"
        if score >= 0.6:
            return "CMS-FB-C"
        if score >= 0.4:
            return "CMS-FB-D"
        return "CMS-FB-E"

    @property
    def lifecycle_state(self) -> str:
        cls = self.classification
        if cls == "CMS-FB-A":
            return "promotion_candidate"
        if cls == "CMS-FB-B":
            return "human_review_required"
        if cls == "CMS-FB-C":
            return "alternative_route"
        if cls == "CMS-FB-D":
            return "record_only"
        return "rejected"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "summary": self.summary,
            "route": self.route,
            "observables": self.observables,
            "score": self.score,
            "classification": self.classification,
            "lifecycle_state": self.lifecycle_state,
            "evidence": self.evidence,
            "validator_binding": self.validator_binding,
            "downgrade_path": self.downgrade_path,
            "negative_control": self.negative_control,
            "surrogate_or_dry_run": self.surrogate_or_dry_run,
            "falsification_condition": self.falsification_condition,
            "non_claim_lock": self.non_claim_lock,
        }


def default_feedback_items() -> list[FeedbackItem]:
    return [
        FeedbackItem(
            id="CMS-FB-001",
            source="v0.3a2 boundary",
            summary="Separate geometry emission from read-only geometry validation.",
            route={
                "shell": "middle",
                "meridian": "validation",
                "sector": "geometry",
                "files": [
                    "scripts/geometry/emit_reflective_git_geometry.py",
                    "scripts/validation/validate_reflective_git_geometry_v0_3.py",
                ],
            },
            observables={key: 1 for key in OBSERVABLE_KEYS},
            evidence=[
                "reports/geometry/latest_reflective_git_geometry_validation.json",
                "reports/public_sync/latest_public_sync_report.md",
            ],
            validator_binding=[
                "python scripts/geometry/emit_reflective_git_geometry.py",
                "python scripts/validation/validate_reflective_git_geometry_v0_3.py",
            ],
            downgrade_path="If read-only preservation fails, downgrade to CMS-FB-B and block API-readiness promotion.",
            negative_control="Report-refresh commits are excluded from semantic geometry nodes.",
            surrogate_or_dry_run="Run geometry validation after a report-refresh commit without re-emitting geometry.",
            falsification_condition="Validator changes outputs/geometry/latest_reflective_git_geometry.json or reports/geometry/latest_reflective_git_geometry.json.",
            non_claim_lock="This feedback item validates repository-bound geometry behavior only.",
        ),
        FeedbackItem(
            id="CMS-FB-002",
            source="PCE v3.5 integration",
            summary="Require scored lifecycle classification before feedback promotion.",
            route={
                "shell": "center",
                "meridian": "memory",
                "sector": "feedback",
                "files": [
                    "configs/feedback/feedback_lifecycle_contract.json",
                    "schemas/feedback_item.schema.json",
                ],
            },
            observables={key: 1 for key in OBSERVABLE_KEYS},
            evidence=[
                "configs/feedback/feedback_lifecycle_contract.json",
                "schemas/feedback_item.schema.json",
            ],
            validator_binding=[
                "python scripts/validation/validate_feedback_lifecycle_v0_3b.py",
            ],
            downgrade_path="If negative controls or falsification conditions are absent, downgrade to CMS-FB-B or CMS-FB-C.",
            negative_control="Feedback items lacking evidence or validator binding must not promote.",
            surrogate_or_dry_run="Construct a weak feedback item and verify classification downgrades.",
            falsification_condition="A feedback item promotes without required observables.",
            non_claim_lock="PCE-style scoring improves feedback governance; it does not prove external truth.",
        ),
        FeedbackItem(
            id="CMS-FB-003",
            source="two-way API readiness",
            summary="API observe/propose/write phases must remain separated.",
            route={
                "shell": "outer",
                "meridian": "safety",
                "sector": "api",
                "files": [
                    "README.md",
                    "docs/versions/v0_3b/cms_sa_v0_3b_feedback_lifecycle_engine.md",
                ],
            },
            observables={key: 1 for key in OBSERVABLE_KEYS},
            evidence=[
                "README.md",
                "configs/feedback/feedback_lifecycle_contract.json",
            ],
            validator_binding=[
                "python scripts/validation/validate_feedback_lifecycle_v0_3b.py",
                "python scripts/validate_release.py",
            ],
            downgrade_path="If API write authority is implied without authorization, downgrade or reject.",
            negative_control="An observe-only API action must not write repository files.",
            surrogate_or_dry_run="Generate a dry-run patch proposal without commit/push.",
            falsification_condition="An observe or classify phase mutates source, evidence, or Git state outside allowed reports.",
            non_claim_lock="API readiness is not autonomous write authority or production security.",
        ),
    ]


def build_feedback_lifecycle_report() -> dict[str, Any]:
    items = [item.to_dict() for item in default_feedback_items()]
    class_counts: dict[str, int] = {}
    for item in items:
        class_counts[item["classification"]] = class_counts.get(item["classification"], 0) + 1

    return {
        "schema": "CMS-SA-v0.3b-feedback-lifecycle-report",
        "version": "v0.3b",
        "item_count": len(items),
        "class_counts": class_counts,
        "observables": OBSERVABLE_KEYS,
        "items": items,
        "api_boundary": {
            "observe": "read-only",
            "classify": "read-only plus report emission",
            "propose": "draft/diff/evidence only",
            "validate": "read-only over target artifacts except validation reports",
            "authorize": "human or constrained automation gate",
            "write": "explicit write phase only",
            "seal": "commit, push, tag, public sync",
        },
        "core_rule": "No feedback item may promote to memory, release, or API-write status without route classification, evidence, validator binding, lifecycle state, downgrade path, falsification condition, and non-claim lock.",
        "non_claim_lock": "Feedback lifecycle governance improves repository alignment and API-readiness. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.",
    }


def report_to_markdown(report: dict[str, Any]) -> str:
    rows = [
        "# CMS-SA v0.3b Feedback Lifecycle Report",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| schema | `{report['schema']}` |",
        f"| version | `{report['version']}` |",
        f"| item count | `{report['item_count']}` |",
        f"| class counts | `{json.dumps(report['class_counts'], sort_keys=True)}` |",
        "",
        "## Feedback Items",
        "",
        "| ID | Classification | Lifecycle state | Score | Summary |",
        "|---|---|---|---:|---|",
    ]

    for item in report["items"]:
        summary = str(item["summary"]).replace("|", "/")
        rows.append(
            f"| `{item['id']}` | `{item['classification']}` | `{item['lifecycle_state']}` | `{item['score']}` | {summary} |"
        )

    rows.extend([
        "",
        "## API Boundary",
        "",
        "| Phase | Rule |",
        "|---|---|",
    ])

    for phase, rule in report["api_boundary"].items():
        rows.append(f"| `{phase}` | {rule} |")

    rows.extend([
        "",
        "## Core Rule",
        "",
        report["core_rule"],
        "",
        "## Non-claim Lock",
        "",
        report["non_claim_lock"],
        "",
    ])

    return "\n".join(rows)


def write_feedback_lifecycle_report() -> dict[str, Any]:
    report = build_feedback_lifecycle_report()

    out_json = ROOT / "outputs" / "feedback" / "latest_feedback_lifecycle_report.json"
    report_json = ROOT / "reports" / "feedback" / "latest_feedback_lifecycle_report.json"
    report_md = ROOT / "reports" / "feedback" / "latest_feedback_lifecycle_report.md"

    out_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.parent.mkdir(parents=True, exist_ok=True)

    text = json.dumps(report, indent=2) + "\n"
    out_json.write_text(text, encoding="utf-8")
    report_json.write_text(text, encoding="utf-8")
    report_md.write_text(report_to_markdown(report), encoding="utf-8")

    return report


if __name__ == "__main__":
    print(json.dumps(write_feedback_lifecycle_report(), indent=2))