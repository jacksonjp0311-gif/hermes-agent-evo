from rhp.readme_story_coherence_auditor import audit_readme_story


GOOD_README = """
<!-- HERMES_RHP_STORY_START -->
Hermes thinks and displays.
RHP gates.
All-One scripts act.
Evidence remembers.
The human authorizes.
This repository is a governed proof-state machine.
<!-- HERMES_RHP_STORY_END -->

<!-- RHP_README_EVIDENCE_STORY_COHERENCE_AUDITOR_START -->
The README must not say CI is green.
The system does not grant autonomous authority.
<!-- RHP_README_EVIDENCE_STORY_COHERENCE_AUDITOR_END -->
"""


def test_good_story_passes_when_authority_locks_false():
    latest = {"latest_operation": "RHP-X", "latest_evidence": "docs/x.json", "integration_closed": False}
    evidence = {"operation": "RHP-X", "active_subject_closed": False, "autonomous_authority": False, "self_authorization": False}
    result = audit_readme_story(GOOD_README, latest, evidence)
    assert result["ok"]
    assert result["error_count"] == 0
    assert result["section_scoped"] is True


def test_missing_story_block_fails():
    latest = {"latest_operation": "RHP-X", "latest_evidence": "docs/x.json"}
    evidence = {"operation": "RHP-X", "autonomous_authority": False, "self_authorization": False}
    result = audit_readme_story("RHP gates.", latest, evidence)
    assert not result["ok"]
    assert any(f["code"] == "missing_story_block" for f in result["findings"])


def test_positive_green_claim_inside_scoped_block_fails():
    latest = {"latest_operation": "RHP-X", "latest_evidence": "docs/x.json"}
    evidence = {"operation": "RHP-X", "autonomous_authority": False, "self_authorization": False}
    readme = GOOD_README.replace("The README must not say CI is green.", "CI is green.")
    result = audit_readme_story(readme, latest, evidence)
    assert not result["ok"]
    assert any(f["code"] == "ci_green_claim" for f in result["findings"])


def test_positive_claim_outside_scoped_blocks_is_not_a_live_story_claim():
    latest = {"latest_operation": "RHP-X", "latest_evidence": "docs/x.json"}
    evidence = {"operation": "RHP-X", "autonomous_authority": False, "self_authorization": False}
    readme = GOOD_README + "\nArchived text: CI is green."
    result = audit_readme_story(readme, latest, evidence)
    assert result["ok"]


def test_authority_locks_not_false_fails():
    latest = {"latest_operation": "RHP-X", "latest_evidence": "docs/x.json"}
    evidence = {"operation": "RHP-X", "autonomous_authority": True, "self_authorization": False}
    result = audit_readme_story(GOOD_README, latest, evidence)
    assert not result["ok"]
    assert any(f["code"] == "authority_lock_not_false" for f in result["findings"])