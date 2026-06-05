from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
from typing import Any


IGNORED_DIRS = {".git", "__pycache__", ".venv", "venv", ".pytest_cache"}


@dataclass
class FileSurface:
    path: str
    suffix: str
    bytes: int
    sha256: str
    role: str


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify_file(path: Path) -> str:
    rel = path.as_posix().lower()
    name = path.name.lower()
    suffix = path.suffix.lower()

    if name == "readme.md":
        return "mini_readme"
    if name == "agents.md":
        return "ai_contract"
    if "route_map" in name or "rcc_nexus" in name:
        return "rcc_context"
    if "release_seal" in name:
        return "release_seal"
    if "injections" in rel or "injection" in name:
        return "injection_record"
    if "versions" in rel:
        return "version_document"
    if suffix == ".py":
        return "python_source"
    if suffix == ".json":
        return "json_artifact"
    if suffix in {".md", ".txt", ".tex"}:
        return "documentation"
    return "other"


class RepositoryObserver:
    """CMS-SA v0.2 repository observer.

    Emits a repository-bound file surface inventory. This does not prove code
    correctness or external validation.
    """

    def __init__(self, repo: str | Path) -> None:
        self.repo = Path(repo).resolve()

    def git_head(self) -> str | None:
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo,
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
        except Exception:
            return None

    def iter_files(self) -> list[Path]:
        files: list[Path] = []
        for path in self.repo.rglob("*"):
            if not path.is_file():
                continue
            parts = set(path.relative_to(self.repo).parts)
            if parts & IGNORED_DIRS:
                continue
            files.append(path)
        return sorted(files)

    def observe(self) -> dict[str, Any]:
        surfaces: list[FileSurface] = []
        for file_path in self.iter_files():
            rel = file_path.relative_to(self.repo).as_posix()
            try:
                surfaces.append(
                    FileSurface(
                        path=rel,
                        suffix=file_path.suffix.lower(),
                        bytes=file_path.stat().st_size,
                        sha256=sha256_file(file_path),
                        role=classify_file(Path(rel)),
                    )
                )
            except OSError:
                continue

        role_counts: dict[str, int] = {}
        suffix_counts: dict[str, int] = {}
        for surface in surfaces:
            role_counts[surface.role] = role_counts.get(surface.role, 0) + 1
            suffix_counts[surface.suffix or "<none>"] = suffix_counts.get(surface.suffix or "<none>", 0) + 1

        required_surfaces = {
            "README.md": (self.repo / "README.md").exists(),
            "README_90_SECONDS.md": (self.repo / "README_90_SECONDS.md").exists(),
            "AGENTS.md": (self.repo / "AGENTS.md").exists(),
            "docs/context/repository_context_index.json": (self.repo / "docs/context/repository_context_index.json").exists(),
            "docs/context/rcc_nexus_index.json": (self.repo / "docs/context/rcc_nexus_index.json").exists(),
            "rcc/nexus/route_map.json": (self.repo / "rcc/nexus/route_map.json").exists(),
            "outputs/version_registry/cms_version_registry.json": (self.repo / "outputs/version_registry/cms_version_registry.json").exists(),
        }

        return {
            "schema": "CMS-SA-v0.2-observation-manifest",
            "repository": self.repo.name,
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "git_head": self.git_head(),
            "file_count": len(surfaces),
            "role_counts": role_counts,
            "suffix_counts": suffix_counts,
            "required_surfaces": required_surfaces,
            "surfaces": [asdict(s) for s in surfaces],
            "non_claim_lock": "repository observation is not code correctness",
        }