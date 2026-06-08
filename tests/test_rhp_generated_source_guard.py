from pathlib import Path

from rhp.generated_source_guard import (
    classify_runtime_python,
    classify_tests,
    compile_python,
    validate_guard,
)


def test_classify_runtime_python_includes_runtime_surfaces():
    paths = [
        "agent/agent_init.py",
        "hrcn_runtime_bridge.py",
        "rhp_runtime_bridge.py",
        "README.md",
        "tests/test_example.py",
    ]
    assert classify_runtime_python(paths) == [
        "agent/agent_init.py",
        "hrcn_runtime_bridge.py",
        "rhp_runtime_bridge.py",
    ]


def test_classify_tests_keeps_only_python_tests():
    assert classify_tests(["tests/test_a.py", "tests/data.json", "agent/x.py"]) == ["tests/test_a.py"]


def test_compile_python_reports_syntax_error(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    (root / ".git").mkdir()
    (root / "pyproject.toml").write_text("[project]\nname='fake'\n", encoding="utf-8")
    bad = root / "bad.py"
    bad.write_text("x = \"unterminated\n", encoding="utf-8")

    ok, output = compile_python(root, ["bad.py"])

    assert ok is False
    assert "FAIL py_compile bad.py" in output


def test_validate_guard_blocks_missing_tests():
    result = validate_guard(
        repo_root=Path.cwd(),
        generated_python=[],
        touched_paths=["hrcn_runtime_bridge.py"],
        tests=[],
    )

    assert result.ok is False
    assert result.py_compile_passed is True
    assert result.focused_tests_passed is False
    assert "No tests supplied" in result.pytest_output or "Focused tests failed" in result.failed_reason


def test_validate_guard_accepts_current_rhp_bridge_contract():
    result = validate_guard(
        repo_root=Path.cwd(),
        generated_python=["rhp/generated_source_guard.py"],
        touched_paths=["rhp_runtime_bridge.py"],
        tests=[
            "tests/test_rhp_runtime_bridge.py",
            "tests/test_rhp_context_injection.py",
            "tests/test_rhp_hrcn_order.py",
            "tests/test_rhp_runtime_startup_smoke.py",
        ],
    )

    assert result.ok is True
    assert result.py_compile_passed is True
    assert result.focused_tests_passed is True
