
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
def main() -> int:
    findings = []
    bundle = load(ROOT/'outputs/agent_governance/latest_agent_governance_kernel_bundle.json')
    context = load(ROOT/'outputs/cms/hermes_cms_context.json')
    report = load(ROOT/'reports/agent_governance/latest_agent_governance_kernel_bundle.json')
    classification = load(ROOT/'reports/agent_governance/latest_agent_proposal_classification.json')
    if not bundle: findings.append('missing_bundle')
    if bundle != report: findings.append('bundle_report_copy_mismatch')
    if not context: findings.append('missing_hermes_cms_context')
    if not classification: findings.append('missing_classification')
    if bundle.get('schema') != 'CMS-SA-v0.5.0-agent-governance-kernel-bridge': findings.append('schema_mismatch')
    if bundle.get('version') != 'v0.5.0': findings.append('version_mismatch')
    for key in ['runtime_code_changes_allowed','cms_write_integration_active','write_authority_granted','apply_authority_granted','memory_authority_granted','skill_trust_authority_granted']:
        if bundle.get(key) is not False: findings.append(f'{key}_not_false')
    if context.get('mode') != 'read_only': findings.append('context_not_read_only')
    if context.get('runtime_code_changes_allowed') is not False: findings.append('context_runtime_mutation_allowed')
    if context.get('cms_write_integration_active') is not False: findings.append('context_write_integration_active')
    expected = {'rcc':'orientation','cms':'governed_permission','hermes':'action','human':'write_boundary'}
    if bundle.get('division_of_powers') != expected: findings.append('division_of_powers_mismatch')
    required = ['target_surface_write','api_write','git_commit','git_push','release_tag_creation','autonomous_patch','production_apply']
    for action in required:
        if action not in context.get('blocked_actions', []): findings.append(f'missing_blocked_action:{action}')
    for row in classification.get('decisions', []):
        for key in ['write_authority','memory_authority','skill_trust_authority','apply_authority']:
            if row.get(key) is not False: findings.append(f'{key}_granted:{row.get("proposal_id")}')
    validation = {'schema':'CMS-SA-v0.5.0-agent-governance-kernel-validation','version':'v0.5.0','passed':len(findings)==0,'errors':len(findings),'findings':findings,'proposal_count':classification.get('proposal_count',0),'classification_count':classification.get('classification_count',0),'runtime_code_changes_allowed':bundle.get('runtime_code_changes_allowed'),'cms_write_integration_active':bundle.get('cms_write_integration_active'),'write_authority_granted':bundle.get('write_authority_granted'),'apply_authority_granted':bundle.get('apply_authority_granted'),'memory_authority_granted':bundle.get('memory_authority_granted'),'skill_trust_authority_granted':bundle.get('skill_trust_authority_granted'),'primary_lock':bundle.get('primary_lock'),'non_claim_lock':'Agent governance kernel validation is repository-bound and does not prove code correctness.'}
    out = ROOT/'reports/agent_governance/latest_agent_governance_kernel_validation.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(validation, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    md = '# CMS-SA v0.5.0 Agent Governance Kernel Validation\n\n' + '\n'.join([f'- passed: `{str(validation["passed"]).lower()}`',f'- errors: `{validation["errors"]}`',f'- proposal count: `{validation["proposal_count"]}`',f'- classification count: `{validation["classification_count"]}`',f'- write authority granted: `{validation["write_authority_granted"]}`',f'- apply authority granted: `{validation["apply_authority_granted"]}`','','## Findings',''] + [f'- `{x}`' for x in (findings or ['none'])] + ['', '## Primary Lock','', str(validation['primary_lock']), ''])
    (ROOT/'reports/agent_governance/latest_agent_governance_kernel_validation.md').write_text(md, encoding='utf-8')
    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation['passed'] else 1
if __name__ == '__main__':
    raise SystemExit(main())
