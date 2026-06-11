from rhp.claim_ledger import build_ledger, make_claim, validate_claim


def test_rhp_015_6_claim_requires_subject_and_no_authority():
    claim = make_claim(
        claim="remote_ci_green",
        subject_type="git_commit",
        subject_id="abc",
        status="green",
        source="github-actions-verified",
        applies_to_current_head=False,
    )
    assert validate_claim(claim)["ok"] is True
    ledger = build_ledger([claim])
    assert ledger["ok"] is True
    assert ledger["claim_precision"] == 1.0
