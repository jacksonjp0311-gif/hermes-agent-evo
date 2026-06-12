from pathlib import Path

from rhp.repository_file_size_guard import audit_file_sizes


def test_small_file_passes(tmp_path: Path):
    (tmp_path / "AGENTS.md").write_text("small", encoding="utf-8")
    result = audit_file_sizes(tmp_path, hard_limit_bytes=100, warning_limit_bytes=50, paths=("AGENTS.md",))
    assert result["ok"]
    assert result["error_count"] == 0


def test_warning_threshold_does_not_fail(tmp_path: Path):
    (tmp_path / "AGENTS.md").write_text("x" * 75, encoding="utf-8")
    result = audit_file_sizes(tmp_path, hard_limit_bytes=100, warning_limit_bytes=50, paths=("AGENTS.md",))
    assert result["ok"]
    assert result["warning_count"] == 1


def test_hard_threshold_fails(tmp_path: Path):
    (tmp_path / "AGENTS.md").write_text("x" * 101, encoding="utf-8")
    result = audit_file_sizes(tmp_path, hard_limit_bytes=100, warning_limit_bytes=50, paths=("AGENTS.md",))
    assert not result["ok"]
    assert result["error_count"] == 1


def test_missing_file_is_ignored(tmp_path: Path):
    result = audit_file_sizes(tmp_path, hard_limit_bytes=100, warning_limit_bytes=50, paths=("AGENTS.md",))
    assert result["ok"]
    assert result["finding_count"] if "finding_count" in result else True