from __future__ import annotations

from dataclasses import dataclass
from typing import Any

STORY_START = "<!-- HERMES_RHP_STORY_START -->"
STORY_END = "<!-- HERMES_RHP_STORY_END -->"
GUARD_START = "<!-- RHP_README_EVIDENCE_STORY_COHERENCE_AUDITOR_START -->"
GUARD_END = "<!-- RHP_README_EVIDENCE_STORY_COHERENCE_AUDITOR_END -->"

REQUIRED_STORY_PHRASES = (
    "Hermes thinks and displays.",
    "RHP gates.",
    "All-One scripts act.",
    "Evidence remembers.",
    "The human authorizes.",
    "governed proof-state machine",
)

CLAIM_PATTERNS = (
    ("ci_green_claim", "ci is green"),
    ("ci_green_claim", "ci green"),
    ("green_status_claim", "green status achieved"),
    ("wound_closure_claim", "wound closed"),
    ("wound_closure_claim", "wounds closed"),
    ("release_claim", "release complete"),
    ("promotion_claim", "promotion complete"),
    ("authority_claim", "has autonomous authority"),
    ("authority_claim", "grants autonomous authority"),
    ("self_authorization_claim", "self-authorizing"),
    ("self_authorization_claim", "self-authorized"),
    ("full_autonomy_claim", "fully autonomous"),
)

NEGATION_TOKENS = (
    "not ",
    "no ",
    "cannot ",
    "can't ",
    "must not ",
    "does not ",
    "do not ",
    "without ",
    "unless ",
    "forbid ",
    "forbidden ",
    "blocked ",
    "never ",
)


@dataclass(frozen=True)
class StoryFinding:
    code: str
    severity: str
    message: str
    phrase: str

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "phrase": self.phrase,
        }


def extract_between(text: str, start_marker: str, end_marker: str) -> str:
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1 or end < start:
        return ""
    return text[start + len(start_marker):end]


def _same_sentence_prefix(text: str, start: int) -> str:
    last_stop = max(text.rfind(".", 0, start), text.rfind("\n", 0, start), text.rfind(";", 0, start), text.rfind(":", 0, start))
    return text[last_stop + 1:start]


def _is_negated(text: str, start: int) -> bool:
    prefix = _same_sentence_prefix(text, start)
    return any(token in prefix for token in NEGATION_TOKENS)


def _iter_positive_claims(text: str) -> list[tuple[str, str]]:
    lower = text.lower()
    hits: list[tuple[str, str]] = []
    for code, phrase in CLAIM_PATTERNS:
        idx = lower.find(phrase)
        while idx != -1:
            if not _is_negated(lower, idx):
                hits.append((code, phrase))
            idx = lower.find(phrase, idx + len(phrase))
    return hits


def audit_readme_story(readme_text: str, latest_pointer: dict[str, Any], final_evidence: dict[str, Any]) -> dict[str, Any]:
    findings: list[StoryFinding] = []

    story_block = extract_between(readme_text, STORY_START, STORY_END)
    guard_block = extract_between(readme_text, GUARD_START, GUARD_END)
    scoped_text = story_block + "\n" + guard_block

    if not story_block:
        findings.append(StoryFinding(
            code="missing_story_block",
            severity="error",
            message="README is missing the bounded Hermes/RHP story block.",
            phrase=STORY_START,
        ))

    for phrase in REQUIRED_STORY_PHRASES:
        if phrase not in story_block:
            findings.append(StoryFinding(
                code="missing_story_phrase",
                severity="error",
                message="README story block is missing a required bounded identity phrase.",
                phrase=phrase,
            ))

    for code, phrase in _iter_positive_claims(scoped_text):
        findings.append(StoryFinding(
            code=code,
            severity="error",
            message="README scoped story surface contains a positive status/authority claim that must be backed by named evidence or removed.",
            phrase=phrase,
        ))

    if latest_pointer.get("integration_closed") is True:
        findings.append(StoryFinding(
            code="integration_closed_pointer",
            severity="warning",
            message="Latest pointer says integration is closed; README story audit should ensure closure claim is evidence-backed.",
            phrase="integration_closed",
        ))

    if final_evidence.get("active_subject_closed") is True:
        findings.append(StoryFinding(
            code="active_subject_closed_evidence",
            severity="warning",
            message="Final evidence says subject closed; README story audit should ensure closure language is bounded.",
            phrase="active_subject_closed",
        ))

    if final_evidence.get("autonomous_authority") is not False:
        findings.append(StoryFinding(
            code="authority_lock_not_false",
            severity="error",
            message="Final evidence must keep autonomous_authority false for the public story to remain bounded.",
            phrase="autonomous_authority",
        ))

    if final_evidence.get("self_authorization") is not False:
        findings.append(StoryFinding(
            code="self_authorization_not_false",
            severity="error",
            message="Final evidence must keep self_authorization false for the public story to remain bounded.",
            phrase="self_authorization",
        ))

    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]

    return {
        "schema": "RHP-README-EVIDENCE-STORY-COHERENCE-AUDIT-v0.4",
        "ok": len(errors) == 0,
        "section_scoped": True,
        "negation_aware": True,
        "sentence_bounded_negation": True,
        "story_block_present": bool(story_block),
        "guard_block_present": bool(guard_block),
        "finding_count": len(findings),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "findings": [f.to_dict() for f in findings],
        "latest_operation": latest_pointer.get("latest_operation"),
        "latest_evidence": latest_pointer.get("latest_evidence"),
        "evidence_operation": final_evidence.get("operation"),
        "non_claim_lock": "README story audit is scoped observability only. It does not repair, close wounds, claim green, or grant authority.",
    }