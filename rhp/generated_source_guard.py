# RHP generated-source and test-contract guard.
#
# This module is intentionally local and dependency-free. It is a reusable
# validation helper for future All-One scripts that emit Python source or
# mutate runtime/test contracts.

from __future__ import annotations

import argparse
import json
import py_compile
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


RUNTIME_PREFIXES = (
    "agent/",
    "hermes_cli/",
    "gateway/",
    "tools/",
    "skills/",
    "plugins/",
    "providers/",
    "tui_gateway/",
    "ui-tui/",
    "web/",
)

PYTHON_RUNTIME_SUFFIXES = (".py",)


@dataclass(frozen=True)
class GuardResult:
    ok: bool
    repo_root: str
    generated_python: list[str] = field(default_factory=list)
    touched_runtime_python: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    py_compile_passed: bool = False
    focused_tests_passed: bool = False
    failed_reason: str = ""
    pytest_output: str = ""

    def as_dict(self) -> dict:
        return {
            "ok": self.ok,
            "repo_root": self.repo_root,
            "generated_python": list(self.generated_python),
            "touched_runtime_python": list(self.touched_runtime_python),
            "tests": list(self.tests),
            "py_compile_passed": self.py_compile_passed,
            "focused_tests_passed": self.focused_tests_passed,
            "failed_reason": self.failed_reason,
            "pytest_output": self.pytest_output,
        }


def _posix(path: Path | str) -> str:
    return Path(path).as_posix()


def find_repo_root(start: str | Path | None = None) -> Path:
    current = Path(start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / ".git").exists():
            return candidate
    raise FileNotFoundError("Could not locate Hermes repository root")


def normalize_paths(paths: Iterable[str | Path]) -> list[str]:
    normalized: list[str] = []
    for value in paths:
        text = str(value).replace("\\", "/").strip()
        if not text:
            continue
        if text not in normalized:
            normalized.append(text)
    return normalized


def classify_runtime_python(paths: Iterable[str]) -> list[str]:
    out: list[str] = []
    for path in normalize_paths(paths):
        if not path.endswith(PYTHON_RUNTIME_SUFFIXES):
            continue
        if path.startswith("tests/"):
            continue
        if path.startswith(RUNTIME_PREFIXES) or path in {"hrcn_runtime_bridge.py", "rhp_runtime_bridge.py"}:
            out.append(path)
    return out


def classify_tests(paths: Iterable[str]) -> list[str]:
    return [path for path in normalize_paths(paths) if path.startswith("tests/") and path.endswith(".py")]


def compile_python(repo_root: Path, paths: Iterable[str]) -> tuple[bool, str]:
    targets = normalize_paths(paths)
    if not targets:
        return True, "No generated/touched Python targets supplied.\n"

    output: list[str] = []
    ok = True
    for rel in targets:
        path = repo_root / rel
        try:
            py_compile.compile(str(path), doraise=True)
            output.append(f"OK py_compile {rel}")
        except Exception as exc:  # pragma: no cover - message path tested through return
            ok = False
            output.append(f"FAIL py_compile {rel}: {exc}")
    return ok, "\n".join(output) + "\n"


def run_pytest(repo_root: Path, tests: Iterable[str]) -> tuple[bool, str]:
    selected = normalize_paths(tests)
    if not selected:
        return False, "No tests supplied for runtime/test-contract guard.\n"

    cmd = [sys.executable, "-m", "pytest", "-q", "-o", "addopts="] + selected
    proc = subprocess.run(cmd, cwd=str(repo_root), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode == 0, proc.stdout


def validate_guard(
    *,
    repo_root: str | Path | None = None,
    generated_python: Iterable[str] = (),
    touched_paths: Iterable[str] = (),
    tests: Iterable[str] = (),
) -> GuardResult:
    root = find_repo_root(repo_root)
    generated = normalize_paths(generated_python)
    touched = normalize_paths(touched_paths)
    runtime_python = classify_runtime_python([*generated, *touched])
    selected_tests = classify_tests(tests)

    compile_targets = normalize_paths([*generated, *runtime_python, *selected_tests])
    compile_ok, compile_output = compile_python(root, compile_targets)
    if not compile_ok:
        return GuardResult(
            ok=False,
            repo_root=str(root),
            generated_python=generated,
            touched_runtime_python=runtime_python,
            tests=selected_tests,
            py_compile_passed=False,
            focused_tests_passed=False,
            failed_reason=compile_output,
        )

    tests_ok, pytest_output = run_pytest(root, selected_tests)
    if not tests_ok:
        return GuardResult(
            ok=False,
            repo_root=str(root),
            generated_python=generated,
            touched_runtime_python=runtime_python,
            tests=selected_tests,
            py_compile_passed=True,
            focused_tests_passed=False,
            failed_reason="Focused tests failed; commit must be blocked.",
            pytest_output=pytest_output,
        )

    return GuardResult(
        ok=True,
        repo_root=str(root),
        generated_python=generated,
        touched_runtime_python=runtime_python,
        tests=selected_tests,
        py_compile_passed=True,
        focused_tests_passed=True,
        pytest_output=pytest_output,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="RHP generated-source and test-contract guard")
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--generated-python", nargs="*", default=[])
    parser.add_argument("--touched-paths", nargs="*", default=[])
    parser.add_argument("--tests", nargs="*", default=[])
    parser.add_argument("--json", action="store_true", help="emit JSON result")
    args = parser.parse_args(argv)

    result = validate_guard(
        repo_root=args.repo_root,
        generated_python=args.generated_python,
        touched_paths=args.touched_paths,
        tests=args.tests,
    )

    if args.json:
        print(json.dumps(result.as_dict(), indent=2))
    else:
        print(json.dumps(result.as_dict(), indent=2))

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
