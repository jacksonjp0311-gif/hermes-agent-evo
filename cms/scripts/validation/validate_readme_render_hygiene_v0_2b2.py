
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
REGISTRY = ROOT / "outputs" / "version_registry" / "cms_version_registry.json"
text = README.read_text(encoding="utf-8", errors="replace") if README.exists() else ""


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


registry = load_json(REGISTRY)
version = registry.get("current_version") or registry.get("latest_version") or "v0.3b3"
version = str(version).strip()
version_badge = f"CMS--SA-{version}"

errors = []
required_badges = [
    version_badge,
    "RCC--N-passing",
    "architecture-passing",
    "lineage-recorded",
    "README%20audit-passing",
    "directory%20box-passing",
    "render%20hygiene-passing",
    "markdown%20structure-passing",
    "public%20sync-stable--guard",
    "K__CMS-1.0",
    "D__CMS-0.0",
    "non--claim--locks-active",
]
for badge in required_badges:
    if badge not in text:
        errors.append(f"missing_badge:{badge}")

for stale in ["CMS--SA-v0.1.2", "RCC--N-scaffolded", "README%20audit-local--ready"]:
    if stale in text:
        errors.append(f"stale_status:{stale}")

for idx, ch in enumerate(text):
    code = ord(ch)
    if code < 32 and ch not in ("\n", "\r", "\t"):
        errors.append(f"control_character:{idx}:{code}")
        break

bad_fragments = ["\ncc/nexus", "\neports/", "$GitHead", "$Kcms", "$Dcms", "$Class", "$ReleaseAllowed"]
for frag in bad_fragments:
    if frag in text:
        errors.append(f"bad_fragment:{frag.encode('unicode_escape').decode('ascii')}")

required_sections = [
    "## Repository Layers",
    "## Historical Report Archive",
    "### Gap Classes the AI Must Detect",
    "## Law of Sufficient Form",
    "## AI Failure Learning Ledger",
]
for section in required_sections:
    if section not in text:
        errors.append(f"missing_section:{section}")

passed = not errors
report = {
    "schema": f"CMS-SA-{version}-readme-render-hygiene",
    "passed": passed,
    "errors": len(errors),
    "findings": errors,
    "checked_badges": len(required_badges),
    "version": version,
    "non_claim_lock": "README render hygiene is not runtime correctness.",
}

out_json = ROOT / "reports" / "render_hygiene" / "latest_readme_render_hygiene.json"
out_md = ROOT / "reports" / "render_hygiene" / "latest_readme_render_hygiene.md"
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
out_md.write_text(
    f"# CMS-SA {version} README Render Hygiene\n\n"
    f"- passed: `{passed}`\n"
    f"- errors: `{len(errors)}`\n"
    f"- checked_badges: `{len(required_badges)}`\n\n"
    "## Findings\n\n"
    + ("\n".join(f"- `{e}`" for e in errors) if errors else "- none\n")
    + "\n\nNon-claim lock: render hygiene is not runtime correctness.\n",
    encoding="utf-8",
)
print(json.dumps(report, indent=2))
raise SystemExit(0 if passed else 1)
