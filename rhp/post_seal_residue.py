from __future__ import annotations
import argparse, json
from dataclasses import dataclass, field
from typing import Any

RHP_POST_SEAL_RESIDUE_SCHEMA = "RHP-POST-SEAL-RESIDUE-v0.2"

SAFE_EXACT = {
    "docs/context-layer/ops/RHP-014-5-v6-residue-manager-error-box-zero-context/command-streams/commit.txt",
    "docs/context-layer/ops/RHP-014-5-v6-residue-manager-error-box-zero-context/command-streams/git-add.txt",
    "docs/context-layer/ops/RHP-014-5-v6-residue-manager-error-box-zero-context/command-streams/pull-rebase.txt",
    "docs/context-layer/ops/RHP-014-5-v6-residue-manager-error-box-zero-context/command-streams/push.txt",
}
SAFE_PREFIXES = [
    "docs/context-layer/ops/RHP-014-6-post-seal-residue-machine-reports/",
]

@dataclass(frozen=True)
class PostSealResidueReport:
    schema: str
    ok: bool
    cleanable: list[str] = field(default_factory=list)
    blocked: list[str] = field(default_factory=list)
    classification: str = "clean"
    non_claim_lock: str = "Post-seal residue classification only identifies bounded command residue. It does not mutate, commit, push, repair, or grant authority."

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def normalize(path: str) -> str:
    return path.replace("\\", "/").strip()

def classify_paths(paths: list[str]) -> PostSealResidueReport:
    cleanable: list[str] = []
    blocked: list[str] = []
    for raw in paths:
        path = normalize(raw)
        if not path:
            continue
        if path in SAFE_EXACT or any(path.startswith(prefix) for prefix in SAFE_PREFIXES):
            cleanable.append(path)
        else:
            blocked.append(path)
    if blocked:
        classification = "blocked_unknown_post_seal_residue"
    elif cleanable:
        classification = "bounded_post_seal_command_residue"
    else:
        classification = "clean"
    return PostSealResidueReport(RHP_POST_SEAL_RESIDUE_SCHEMA, not blocked, cleanable, blocked, classification)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Classify RHP post-seal residue paths")
    p.add_argument("paths", nargs="*")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    report = classify_paths(args.paths)
    print(json.dumps(report.as_dict(), indent=2, ensure_ascii=False))
    return 0 if report.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
