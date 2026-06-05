from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from cms.geometry.git_geometry import write_geometry  # noqa: E402


def main() -> int:
    geometry = write_geometry(limit=12)

    report = {
        "schema": "CMS-SA-v0.3a2-reflective-git-geometry-emission",
        "passed": True,
        "version": geometry.get("version"),
        "node_count": geometry.get("node_count"),
        "wrote": [
            "outputs/geometry/latest_reflective_git_geometry.json",
            "reports/geometry/latest_reflective_git_geometry.json",
            "reports/geometry/latest_reflective_git_geometry.md",
        ],
        "non_claim_lock": "Geometry emission writes repository evidence artifacts; it does not prove correctness.",
    }

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())