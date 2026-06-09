from __future__ import annotations
import json
from pathlib import Path

root = Path(r"C:\Users\jacks\OneDrive\Desktop\hermes-agent-evo")
main_path = root / "hermes_cli" / "main.py"
banner_path = root / "hermes_cli" / "banner.py"
readme_path = root / "README.md"
rhp_readme_path = root / "rhp" / "README.md"

main = main_path.read_text(encoding="utf-8", errors="replace")
banner = banner_path.read_text(encoding="utf-8", errors="replace")
readme = readme_path.read_text(encoding="utf-8", errors="replace")
rhp_readme = rhp_readme_path.read_text(encoding="utf-8", errors="replace")

orig_main, orig_banner, orig_readme, orig_rhp = main, banner, readme, rhp_readme

main = main.replace('return render_operator_startup_status(packet, evidence="RHP-010")', 'return render_operator_startup_status(packet, evidence="RHP-012")')
main = main.replace("[OK] RHP-010 evidence green", "[OK] RHP evidence green")
main = main.replace("evidence=RHP-010", "evidence=RHP-012")
main = main.replace('os.environ["HERMES_RHP_BOOT_PREFLIGHT_STATUS"] = "ok" if packet.ok else "blocked"', 'os.environ["HERMES_RHP_BOOT_PREFLIGHT_STATUS"] = "ok" if packet.ok else "degraded"')
main = main.replace('os.environ["HERMES_RHP_BOOT_PREFLIGHT_PACKET"] = "RHP-BOOT-PREFLIGHT-PACKET-v0.1"', 'os.environ["HERMES_RHP_BOOT_PREFLIGHT_PACKET"] = "RHP-BOOT-PREFLIGHT-PACKET-v0.3"')

needle = 'os.environ["HERMES_RHP_OPERATOR_STATUS"] = _rhp_render_operator_status(packet)\n\n        if ('
insert = """os.environ["HERMES_RHP_OPERATOR_STATUS"] = _rhp_render_operator_status(packet)
        os.environ["HERMES_RHP_PROTOCOL_STRIP"] = (
            "Rehydration Protocol - "
            + ("verified" if packet.ok else "degraded")
            + " - phase=pre-interaction - evidence=RHP-012 - authority=false"
        )
        os.environ["HERMES_RHP_PROTOCOL_LOCKS"] = (
            "locks: repo ok - evidence "
            + ("ok" if packet.rhp_evidence_green else "degraded")
            + " - HRCN "
            + ("ok" if packet.hrcn_boundary_green else "degraded")
            + " - alignment "
            + ("ok" if packet.alignment_guard_green else "degraded")
            + " - startup ok"
        )

        if ("""
if needle in main and "HERMES_RHP_PROTOCOL_STRIP" not in main:
    main = main.replace(needle, insert)

print_block = """            print(os.environ["HERMES_RHP_OPERATOR_STATUS"], file=sys.stderr)
            protocol_strip = os.environ.get("HERMES_RHP_PROTOCOL_STRIP")
            protocol_locks = os.environ.get("HERMES_RHP_PROTOCOL_LOCKS")
            if protocol_strip:
                print(protocol_strip, file=sys.stderr)
            if protocol_locks:
                print(protocol_locks, file=sys.stderr)"""
main = main.replace('            print(os.environ["HERMES_RHP_OPERATOR_STATUS"], file=sys.stderr)', print_block)

banner = banner.replace('evidence = "RHP-011.1" if verified else "RHP-011"', 'evidence = "RHP-012"')
banner = banner.replace('status in {"blocked", "error"}', 'status in {"blocked", "error", "degraded"}')

readme = readme.replace("| Latest RHP proof | `docs/context-layer/ops/RHP-012-final-evidence.json` |", "| Latest RHP proof | `docs/context-layer/ops/RHP-012-1-final-evidence.json` |")
readme = readme.replace("| Current RHP status | `RHP-012 safe boot failure mode and degraded startup status passed` |", "| Current RHP status | `RHP-012.1 CLI visible Rehydration Protocol text alignment passed` |")
if "RHP-L-044" not in readme:
    readme = readme.replace(
        "| RHP-L-043 | Safe boot negative controls must prove authority remains false while status degrades. |",
        "| RHP-L-043 | Safe boot negative controls must prove authority remains false while status degrades. |\n| RHP-L-044 | Runtime evidence text must not remain stale after evidence version advances; operator-visible status, banner strip, and startup packet labels must align. |",
    )
note = """
#### RHP-012.1 CLI Visible Rehydration Text Alignment

RHP-012.1 repairs the live CLI surface after RHP-012 sealed. The operator-visible startup text now reports `evidence=RHP-012`, exposes the Rehydration Protocol strip in the CLI stream, and preserves degraded/verified status without authority expansion.

Boundary: display/text alignment only. No provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.
"""
if "#### RHP-012.1 CLI Visible Rehydration Text Alignment" not in readme:
    readme = readme.replace("<!-- HERMES_RHP_RUNTIME_ACTIVATION_END -->", note + "\n<!-- HERMES_RHP_RUNTIME_ACTIVATION_END -->")

if "RHP-012.1 CLI visible Rehydration Protocol text alignment" not in rhp_readme:
    rhp_readme += """

## RHP-012.1 CLI visible Rehydration Protocol text alignment

RHP-012.1 aligns the live operator-visible CLI text with the RHP-012 evidence state. It removes stale `evidence=RHP-010` startup text and surfaces the Rehydration Protocol strip directly in the CLI stream.

Boundary: display/text alignment only. It does not grant provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.
"""

main_path.write_text(main, encoding="utf-8")
banner_path.write_text(banner, encoding="utf-8")
readme_path.write_text(readme, encoding="utf-8")
rhp_readme_path.write_text(rhp_readme, encoding="utf-8")

report = {
    "ok": True,
    "main_changed": main != orig_main,
    "banner_changed": banner != orig_banner,
    "readme_changed": readme != orig_readme,
    "rhp_readme_changed": rhp_readme != orig_rhp,
    "main_evidence_rhp012": 'evidence="RHP-012"' in main and "evidence=RHP-012" in main,
    "protocol_strip_env_present": "HERMES_RHP_PROTOCOL_STRIP" in main,
    "boot_packet_v03_present": "RHP-BOOT-PREFLIGHT-PACKET-v0.3" in main,
    "banner_evidence_rhp012": 'evidence = "RHP-012"' in banner,
    "lesson_044_present": "RHP-L-044" in readme,
}
print(json.dumps(report, indent=2))