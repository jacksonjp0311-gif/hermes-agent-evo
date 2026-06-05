
from __future__ import annotations
import json
from pathlib import Path
from cms.governance.agent_governance_kernel import build_bundle

ROOT = Path(__file__).resolve().parents[2]
def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True)+'\n', encoding='utf-8')
def main() -> int:
    bundle = build_bundle(load(ROOT/'outputs/version_registry/cms_version_registry.json'), load(ROOT/'reports/public_sync/latest_public_sync_report.json'), load(ROOT/'reports/loop/latest_loop_drift_pressure_validation.json'))
    write_json(ROOT/'outputs/agent_governance/latest_agent_governance_kernel_bundle.json', bundle)
    write_json(ROOT/'outputs/cms/hermes_cms_context.json', bundle['hermes_cms_context'])
    write_json(ROOT/'outputs/agent_governance/latest_rcc_cms_orientation_packet.json', bundle['rcc_cms_orientation_packet'])
    write_json(ROOT/'outputs/agent_governance/latest_agent_adapter_decisions.json', bundle['adapter_decisions'])
    write_json(ROOT/'reports/agent_governance/latest_agent_governance_kernel_bundle.json', bundle)
    write_json(ROOT/'reports/agent_governance/latest_hermes_cms_context.json', bundle['hermes_cms_context'])
    write_json(ROOT/'reports/agent_governance/latest_agent_proposal_classification.json', bundle['classification'])
    md = ['# CMS-SA v0.5.0 Agent Governance Kernel Bridge','',f'- mode: `{bundle["mode"]}`',f'- proposal count: `{bundle["classification"]["proposal_count"]}`',f'- classification count: `{bundle["classification"]["classification_count"]}`',f'- runtime code changes allowed: `{bundle["runtime_code_changes_allowed"]}`',f'- CMS write integration active: `{bundle["cms_write_integration_active"]}`',f'- write authority granted: `{bundle["write_authority_granted"]}`',f'- apply authority granted: `{bundle["apply_authority_granted"]}`','','## Division of Powers','','- RCC: orientation','- CMS: governed permission','- Hermes: action','- Human: write boundary','','## Primary Lock','',bundle['primary_lock'],'','## Non-Claim Lock','',bundle['non_claim_lock'],'']
    (ROOT/'reports/agent_governance/latest_agent_governance_kernel_bundle.md').write_text('\n'.join(md), encoding='utf-8')
    print(json.dumps({'schema':'CMS-SA-v0.5.0-agent-governance-kernel-emission','passed':True,'version':bundle['version'],'proposal_count':bundle['classification']['proposal_count'],'write_authority_granted':False,'apply_authority_granted':False,'bundle_hash':bundle['bundle_hash']}, indent=2, sort_keys=True))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
