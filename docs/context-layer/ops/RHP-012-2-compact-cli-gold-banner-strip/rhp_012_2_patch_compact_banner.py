from __future__ import annotations

import json
from pathlib import Path

root = Path(r"C:\Users\jacks\OneDrive\Desktop\hermes-agent-evo")
cli_path = root / "cli.py"
readme_path = root / "README.md"
rhp_readme_path = root / "rhp" / "README.md"

cli = cli_path.read_text(encoding="utf-8", errors="replace")
readme = readme_path.read_text(encoding="utf-8", errors="replace")
rhp_readme = rhp_readme_path.read_text(encoding="utf-8", errors="replace")

orig_cli = cli
orig_readme = readme
orig_rhp = rhp_readme

old = """    # Truncate and pad to fit
    line1 = line1[:content_width].ljust(content_width)
    line2 = version_line[:content_width].ljust(content_width)

    return (
        f"\\n[bold {border_color}]╔{bar}╗[/]\\n"
        f"[bold {border_color}]║[/] [{title_color}]{line1}[/] [bold {border_color}]║[/]\\n"
        f"[bold {border_color}]║[/] [dim {dim_color}]{line2}[/] [bold {border_color}]║[/]\\n"
        f"[bold {border_color}]╚{bar}╝[/]\\n"
    )
"""

new = """    # Truncate and pad to fit
    line1 = line1[:content_width].ljust(content_width)
    line2 = version_line[:content_width].ljust(content_width)

    rhp_strip = (os.environ.get("HERMES_RHP_PROTOCOL_STRIP") or "").strip()
    rhp_locks = (os.environ.get("HERMES_RHP_PROTOCOL_LOCKS") or "").strip()
    rhp_box_lines = []
    if rhp_strip:
        rhp_box_lines.append(rhp_strip[:content_width].ljust(content_width))
    if rhp_locks:
        rhp_box_lines.append(rhp_locks[:content_width].ljust(content_width))

    boxed_lines = [
        f"[bold {border_color}]║[/] [{title_color}]{line1}[/] [bold {border_color}]║[/]",
        f"[bold {border_color}]║[/] [dim {dim_color}]{line2}[/] [bold {border_color}]║[/]",
    ]
    for rhp_line in rhp_box_lines:
        boxed_lines.append(
            f"[bold {border_color}]║[/] [#7DF9FF]{rhp_line}[/] [bold {border_color}]║[/]"
        )

    return (
        f"\\n[bold {border_color}]╔{bar}╗[/]\\n"
        + "\\n".join(boxed_lines)
        + f"\\n[bold {border_color}]╚{bar}╝[/]\\n"
    )
"""

if "rhp_box_lines" not in cli:
    if old not in cli:
        raise SystemExit("Could not find compact banner return block in cli.py")
    cli = cli.replace(old, new)

readme = readme.replace("| Latest RHP proof | `docs/context-layer/ops/RHP-012-1-final-evidence.json` |", "| Latest RHP proof | `docs/context-layer/ops/RHP-012-2-final-evidence.json` |")
readme = readme.replace("| Current RHP status | `RHP-012.1 CLI visible Rehydration Protocol text alignment passed` |", "| Current RHP status | `RHP-012.2 compact CLI gold banner Rehydration Protocol strip passed` |")
if "RHP-L-045" not in readme:
    readme = readme.replace(
        "| RHP-L-044 | Runtime evidence text must not remain stale after evidence version advances; operator-visible status, banner strip, and startup packet labels must align. |",
        "| RHP-L-044 | Runtime evidence text must not remain stale after evidence version advances; operator-visible status, banner strip, and startup packet labels must align. |\n| RHP-L-045 | Hermes has multiple banner surfaces; patches must bind both early boot stream and compact CLI gold banner renderer. |",
    )

note = """
#### RHP-012.2 Compact CLI Gold Banner Strip

RHP-012.2 binds the compact `$NOUS HERMES - AI Agent Framework` banner in `cli.py` to the RHP Rehydration Protocol strip. The early boot stream was already correct after RHP-012.1; this patch closes the second visible surface.

Boundary: compact banner display only. No provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.
"""
if "#### RHP-012.2 Compact CLI Gold Banner Strip" not in readme:
    readme = readme.replace("<!-- HERMES_RHP_RUNTIME_ACTIVATION_END -->", note + "\n<!-- HERMES_RHP_RUNTIME_ACTIVATION_END -->")

if "RHP-012.2 compact CLI gold banner Rehydration Protocol strip" not in rhp_readme:
    rhp_readme += """

## RHP-012.2 compact CLI gold banner Rehydration Protocol strip

RHP-012.2 binds the compact `$NOUS HERMES - AI Agent Framework` banner renderer in `cli.py` to the RHP Rehydration Protocol environment strip.

Boundary: compact banner display only. It does not grant provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.
"""

cli_path.write_text(cli, encoding="utf-8")
readme_path.write_text(readme, encoding="utf-8")
rhp_readme_path.write_text(rhp_readme, encoding="utf-8")

report = {
    "ok": True,
    "cli_changed": cli != orig_cli,
    "readme_changed": readme != orig_readme,
    "rhp_readme_changed": rhp_readme != orig_rhp,
    "rhp_box_lines_present": "rhp_box_lines" in cli,
    "protocol_strip_env_present": "HERMES_RHP_PROTOCOL_STRIP" in cli,
    "protocol_locks_env_present": "HERMES_RHP_PROTOCOL_LOCKS" in cli,
    "compact_banner_target_present": "_build_compact_banner" in cli and "NOUS HERMES" in cli,
    "latest_evidence_readme_present": "docs/context-layer/ops/RHP-012-2-final-evidence.json" in readme,
    "lesson_045_present": "RHP-L-045" in readme,
}
print(json.dumps(report, indent=2))