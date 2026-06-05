
from __future__ import annotations
import unittest
from cms.governance.agent_governance_kernel import build_bundle, classify_agent_proposals, default_agent_proposals, BLOCKED_ACTIONS

class AgentGovernanceKernelTests(unittest.TestCase):
    def test_authorities_never_granted(self):
        report = classify_agent_proposals(default_agent_proposals())
        self.assertEqual(report['proposal_count'], 4)
        for key in ['write_authority_granted','memory_authority_granted','skill_trust_authority_granted','apply_authority_granted']:
            self.assertFalse(report[key])
        for row in report['decisions']:
            self.assertFalse(row['write_authority'])
            self.assertFalse(row['memory_authority'])
            self.assertFalse(row['skill_trust_authority'])
            self.assertFalse(row['apply_authority'])
            for action in BLOCKED_ACTIONS:
                self.assertIn(action, row['blocked_actions_preserved'])
    def test_context_is_read_only(self):
        bundle = build_bundle({'current_version':'v0.5.0','current_checkpoint':'CMS-SA v0.5.0 - Agent Governance Kernel Bridge','previous_seal':'v0.4.8','next_anchor':'HRCN v0.1'}, {'passed':True,'release_tag_status':'present_and_ancestor_of_head'}, {'loop_drift_pressure':0.14,'stability_state':'stable_green_loop'})
        self.assertEqual(bundle['hermes_cms_context']['mode'], 'read_only')
        self.assertFalse(bundle['runtime_code_changes_allowed'])
        self.assertFalse(bundle['cms_write_integration_active'])
        self.assertFalse(bundle['write_authority_granted'])
        self.assertEqual(bundle['division_of_powers']['cms'], 'governed_permission')
if __name__ == '__main__':
    unittest.main()
