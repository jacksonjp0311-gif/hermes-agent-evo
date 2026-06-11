from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

RHP_RENDER_HYGIENE_AUDITOR_SCHEMA = "RHP-RENDER-HYGIENE-AUDITOR-v0.2"

STRICT_GENERATED_SURFACES = [
    "docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md",
    "docs/context-layer/operator-dashboard.txt",
]

DOC_SURFACES = [
    "README.md",
    "AGENTS.md",
    "rhp/README.md",
]


def _count_allowed_doc_mentions(text: str) -> int:
    patterns = [
        r"`\\\\n`",
        r"literal `\\\\n`",
        r"literal \\\\n",
        r"escaped newline",
    ]
    return sum(len(re.findall(pattern, text)) for pattern in patterns)


def _audit_strict(path: Path, rel: str) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    literal_newline_count = text.count("\\\\n")
    physical_lines = len(text.splitlines())
    ok = literal_newline_count == 0 and physical_lines >= 2
    return {
        "file": rel,
        "surface": "generated_context",
        "severity": "error" if not ok else "ok",
        "ok": ok,
        "literal_backslash_n_count": literal_newline_count,
        "physical_lines": physical_lines,
        "rule": "Generated operator/context surfaces must use physical line breaks, not literal escaped newline payloads.",
    }


def _audit_doc(path: Path, rel: str) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    literal_newline_count = text.count("\\\\n")
    allowed_mentions = _count_allowed_doc_mentions(text)
    unexpected = max(0, literal_newline_count - allowed_mentions)
    ok = unexpected == 0
    return {
        "file": rel,
        "surface": "documentation",
        "severity": "warning" if literal_newline_count else "ok",
        "ok": ok,
        "literal_backslash_n_count": literal_newline_count,
        "allowed_doc_mentions": allowed_mentions,
        "unexpected_literal_backslash_n_count": unexpected,
        "physical_lines": len(text.splitlines()),
        "rule": "Documentation may mention literal `\\\\n`; generated context surfaces may not contain literal newline payload drift.",
    }


def audit(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    checks: list[dict[str, Any]] = []
    for rel in STRICT_GENERATED_SURFACES:
        checks.append(_audit_strict(root / rel, rel))
    for rel in DOC_SURFACES:
        checks.append(_audit_doc(root / rel, rel))
    errors = [check for check in checks if check["severity"] == "error" or check.get("ok") is not True]
    warnings = [check for check in checks if check["severity"] == "warning" and check.get("ok") is True]
    return {
        "schema": RHP_RENDER_HYGIENE_AUDITOR_SCHEMA,
        "ok": len(errors) == 0,
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
        "non_claim_lock": "Render hygiene auditor reads local text surfaces only. It does not mutate files, call remote APIs, rerun CI, or grant authority.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Audit RHP text surfaces for literal escaped newline render drift")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = audit(args.repo_root)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\\n", encoding="utf-8")
    print(text)
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
