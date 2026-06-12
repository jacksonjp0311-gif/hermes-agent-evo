from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DEFAULT_HARD_LIMIT_BYTES = 95_000_000
DEFAULT_WARNING_LIMIT_BYTES = 10_000_000

TRACKED_GOVERNANCE_FILES = (
    "AGENTS.md",
    "README.md",
    "docs/context-layer/latest-rhp.json",
    "docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md",
    "docs/context-layer/rhp_zero_context_rebuild.json",
)


@dataclass(frozen=True)
class FileSizeFinding:
    path: str
    size_bytes: int
    severity: str
    limit_bytes: int
    message: str

    def to_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "size_bytes": self.size_bytes,
            "severity": self.severity,
            "limit_bytes": self.limit_bytes,
            "message": self.message,
        }


def audit_file_sizes(
    repo_root: str | Path,
    *,
    hard_limit_bytes: int = DEFAULT_HARD_LIMIT_BYTES,
    warning_limit_bytes: int = DEFAULT_WARNING_LIMIT_BYTES,
    paths: tuple[str, ...] = TRACKED_GOVERNANCE_FILES,
) -> dict[str, object]:
    root = Path(repo_root)
    findings: list[FileSizeFinding] = []

    for rel in paths:
        target = root / rel
        if not target.exists():
            continue
        size = target.stat().st_size
        if size >= hard_limit_bytes:
            findings.append(FileSizeFinding(
                path=rel,
                size_bytes=size,
                severity="error",
                limit_bytes=hard_limit_bytes,
                message="file exceeds hard repository file-size guard",
            ))
        elif size >= warning_limit_bytes:
            findings.append(FileSizeFinding(
                path=rel,
                size_bytes=size,
                severity="warning",
                limit_bytes=warning_limit_bytes,
                message="file exceeds governance warning threshold and should be compressed",
            ))

    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]

    return {
        "schema": "RHP-REPOSITORY-FILE-SIZE-AUDIT-v0.1",
        "ok": len(errors) == 0,
        "hard_limit_bytes": hard_limit_bytes,
        "warning_limit_bytes": warning_limit_bytes,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "findings": [item.to_dict() for item in findings],
        "non_claim_lock": "File-size audit is a repository hygiene guard only. It does not claim green, close wounds, release, promote, or grant authority.",
    }