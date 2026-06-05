
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from typing import Any

VERSION = 'v0.5.0'
NON_CLAIM_LOCK = ('CMS-SA v0.5.0 agent governance outputs are repository-bound governance evidence and do not prove '
'Hermes correctness, CMS correctness, code correctness, truth, AGI, consciousness, security, production readiness, '
'external validation, autonomous patch safety, or autonomous write authority.')
PRIMARY_LOCK = ('No agent proposal may become memory, skill, repair authority, dry-run authority, apply authority, '
'or write authority unless CMS classifies the proposal, records evidence, preserves blocked actions, and emits a non-claim boundary.')
DIVISION_OF_POWERS = {'rcc':'orientation','cms':'governed_permission','hermes':'action','human':'write_boundary'}
BLOCKED_ACTIONS = ['runtime_code_patch','memory_promotion_without_cms_decision','skill_trust_without_evidence',
'repair_apply_without_dry_run','target_surface_write','api_write','git_commit','git_push','release_tag_creation',
'autonomous_patch','production_apply']
ALLOWED_READ_ONLY_ACTIONS = ['read_docs','read_rcc_map','read_cms_checkpoint','read_loop_pressure',
'read_repair_recommendations','read_dry_run_state','read_apply_gate_state','emit_read_only_context_packet',
'emit_candidate_classification']
PROPOSAL_TYPES = ['memory_proposal','repair_proposal','skill_proposal','tool_action_proposal',
'repo_write_proposal','documentation_update_proposal','dry_apply_result']

def now_iso() -> str: return datetime.now(timezone.utc).isoformat()
def stable_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',',':')).encode('utf-8')).hexdigest()

def default_agent_proposals() -> list[dict[str, Any]]:
    return [
      {'proposal_id':'HRCN-MEMORY-001','proposal_type':'memory_proposal','risk':'medium','requests_write_authority':False,'evidence_refs':['reports/loop/latest_v0_4_8_final_evidence_commit_report.json']},
      {'proposal_id':'HRCN-REPAIR-001','proposal_type':'repair_proposal','risk':'high','requests_write_authority':False,'evidence_refs':['reports/loop/latest_authorized_dry_apply_sandbox_validation.json']},
      {'proposal_id':'HRCN-SKILL-001','proposal_type':'skill_proposal','risk':'high','requests_write_authority':False,'evidence_refs':[]},
      {'proposal_id':'HRCN-WRITE-001','proposal_type':'repo_write_proposal','risk':'critical','requests_write_authority':True,'evidence_refs':['reports/loop/latest_authorized_repair_apply_gate_validation.json']},
    ]

def decide(ptype: str, risk: str, evidence_count: int, wants_write: bool) -> str:
    if ptype not in PROPOSAL_TYPES: return 'reject'
    if wants_write: return 'dry_run_required' if evidence_count > 0 else 'human_review_required'
    if risk in {'critical','high'}: return 'human_review_required' if ptype != 'repair_proposal' else 'dry_run_required'
    if ptype in {'memory_proposal','skill_proposal'} and evidence_count <= 0: return 'observe_only'
    if ptype == 'repair_proposal': return 'dry_run_required'
    if ptype == 'dry_apply_result': return 'observe_only'
    return 'promote_candidate'

def classify_agent_proposals(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    decisions = []
    for i, p in enumerate(proposals):
        ptype = str(p.get('proposal_type','unknown'))
        evidence = p.get('evidence_refs', [])
        if not isinstance(evidence, list): evidence = []
        risk = str(p.get('risk','medium'))
        wants_write = bool(p.get('requests_write_authority', False))
        row = {
          'proposal_id': p.get('proposal_id', f'AGENT-PROPOSAL-{i+1:03d}'),
          'proposal_type': ptype,
          'risk': risk,
          'requests_write_authority': wants_write,
          'evidence_ref_count': len(evidence),
          'decision': decide(ptype, risk, len(evidence), wants_write),
          'allowed_actions': ALLOWED_READ_ONLY_ACTIONS,
          'blocked_actions_preserved': BLOCKED_ACTIONS,
          'write_authority': False,
          'memory_authority': False,
          'skill_trust_authority': False,
          'apply_authority': False,
          'human_authorization_required': wants_write or risk in {'critical','high'},
          'non_claim_lock': NON_CLAIM_LOCK,
        }
        row['classification_hash'] = stable_hash(row)
        decisions.append(row)
    out = {
      'schema':'CMS-SA-v0.5.0-agent-proposal-classification',
      'version':VERSION,
      'created_at':now_iso(),
      'proposal_count':len(proposals),
      'classification_count':len(decisions),
      'decisions':decisions,
      'write_authority_granted':False,
      'memory_authority_granted':False,
      'skill_trust_authority_granted':False,
      'apply_authority_granted':False,
      'primary_lock':PRIMARY_LOCK,
      'non_claim_lock':NON_CLAIM_LOCK,
    }
    out['classification_report_hash'] = stable_hash(out)
    return out

def build_bundle(cms_registry: dict[str, Any], public_sync: dict[str, Any], pressure: dict[str, Any]) -> dict[str, Any]:
    classification = classify_agent_proposals(default_agent_proposals())
    context = {
      'schema':'HRCN-v1.0-hermes-cms-context',
      'cms_schema':'CMS-SA-v0.5.0-agent-governance-context',
      'mode':'read_only',
      'hermes_repo':'jacksonjp0311-gif/hermes-agent-evo',
      'cms_repo':'jacksonjp0311-gif/cybernetic-memory-system',
      'rcc_alignment_active':True,
      'runtime_code_changes_allowed':False,
      'cms_write_integration_active':False,
      'cms_current_version':cms_registry.get('current_version'),
      'cms_current_checkpoint':cms_registry.get('current_checkpoint'),
      'cms_previous_seal':cms_registry.get('previous_seal'),
      'cms_next_anchor':cms_registry.get('next_anchor'),
      'public_sync_passed':public_sync.get('passed'),
      'release_tag_status':public_sync.get('release_tag_status'),
      'loop_drift_pressure':pressure.get('loop_drift_pressure'),
      'stability_state':pressure.get('stability_state'),
      'candidate_decisions_ref':'reports/agent_governance/latest_agent_proposal_classification_validation.md',
      'dry_apply_sandbox_ref':'reports/loop/latest_authorized_dry_apply_sandbox_validation.md',
      'blocked_actions':BLOCKED_ACTIONS,
      'allowed_current_actions':ALLOWED_READ_ONLY_ACTIONS,
      'division_of_powers':DIVISION_OF_POWERS,
      'primary_lock':PRIMARY_LOCK,
      'non_claim_lock':NON_CLAIM_LOCK,
      'created_at':now_iso(),
    }
    context['context_hash'] = stable_hash(context)
    orientation = {
      'schema':'CMS-SA-v0.5.0-rcc-cms-repository-orientation-packet',
      'mode':'read_only',
      'repository':'cybernetic-memory-system',
      'orientation':{'rcc':'map_and_route_boundary','cms':'memory_repair_permission_governor','hermes':'future_actor_runtime','human':'write_boundary'},
      'high_risk_surfaces':['agent loop','tool execution','skill creation / skill update','memory implementation','provider routing','messaging gateway','terminal backends','dependency pins','install/update scripts','auth/config/secrets'],
      'safe_current_surfaces':['README.md','AGENTS.md','RCC.md','docs/rcc/*.md','reports/agent_governance/*.json','outputs/cms/hermes_cms_context.json'],
      'non_claim_lock':NON_CLAIM_LOCK,
      'created_at':now_iso(),
    }
    orientation['orientation_hash'] = stable_hash(orientation)
    adapters = {
      'schema':'CMS-SA-v0.5.0-agent-adapter-decisions',
      'version':VERSION,
      'memory_candidate_adapter':[{'decision':'cms_decides_memory_status','future_influence_authority':False}],
      'repair_proposal_adapter':[{'decision':'cms_decides_repair_class_and_dry_run_boundary','write_authority':False}],
      'skill_candidate_adapter':[{'decision':'observe_only_until_evidence_and_tests','trusted_skill_authority':False}],
      'write_authority_granted':False,
      'non_claim_lock':NON_CLAIM_LOCK,
      'created_at':now_iso(),
    }
    adapters['adapter_hash'] = stable_hash(adapters)
    bundle = {
      'schema':'CMS-SA-v0.5.0-agent-governance-kernel-bridge',
      'version':VERSION,
      'mode':'read_only_agent_governance_kernel',
      'created_at':now_iso(),
      'division_of_powers':DIVISION_OF_POWERS,
      'classification':classification,
      'hermes_cms_context':context,
      'rcc_cms_orientation_packet':orientation,
      'adapter_decisions':adapters,
      'runtime_code_changes_allowed':False,
      'cms_write_integration_active':False,
      'write_authority_granted':False,
      'apply_authority_granted':False,
      'memory_authority_granted':False,
      'skill_trust_authority_granted':False,
      'primary_lock':PRIMARY_LOCK,
      'non_claim_lock':NON_CLAIM_LOCK,
    }
    bundle['bundle_hash'] = stable_hash(bundle)
    return bundle
