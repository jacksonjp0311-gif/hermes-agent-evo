from __future__ import annotations

import argparse
import ast
import importlib
import json
from pathlib import Path
from typing import Any

from rhp.contract_registry import STABLE_SYMBOLS, registry

RHP_API_SURFACE_AUDITOR_SCHEMA = "RHP-API-SURFACE-AUDITOR-v0.1"


def _iter_py_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for base in ("tests", "rhp"):
        directory = root / base
        if directory.exists():
            paths.extend(path for path in directory.rglob("*.py") if "__pycache__" not in path.parts)
    return sorted(paths)


def discover_imports(root: str | Path = ".") -> dict[str, list[dict[str, str]]]:
    root_path = Path(root)
    imports: dict[str, list[dict[str, str]]] = {}
    for path in _iter_py_files(root_path):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("rhp."):
                for alias in node.names:
                    if alias.name == "*":
                        continue
                    imports.setdefault(node.module, []).append({"symbol": alias.name, "file": str(path.relative_to(root_path))})
    return imports


def _symbol_exists(module_name: str, symbol: str) -> tuple[bool, str]:
    try:
        module = importlib.import_module(module_name)
    except Exception as exc:
        return False, f"import failed: {type(exc).__name__}: {exc}"
    return hasattr(module, symbol), "ok" if hasattr(module, symbol) else "missing"


def audit_contract(root: str | Path = ".", include_discovered: bool = True) -> dict[str, Any]:
    root_path = Path(root)
    checks: list[dict[str, Any]] = []
    for module_name, symbols in STABLE_SYMBOLS.items():
        for symbol in symbols:
            ok, detail = _symbol_exists(module_name, symbol)
            checks.append({"kind": "registry", "module": module_name, "symbol": symbol, "ok": ok, "detail": detail})

    discovered = discover_imports(root_path) if include_discovered else {}
    for module_name, refs in discovered.items():
        for ref in refs:
            ok, detail = _symbol_exists(module_name, ref["symbol"])
            checks.append({"kind": "discovered_import", "module": module_name, "symbol": ref["symbol"], "file": ref["file"], "ok": ok, "detail": detail})

    missing = [check for check in checks if check["ok"] is not True]
    return {
        "schema": RHP_API_SURFACE_AUDITOR_SCHEMA,
        "ok": len(missing) == 0,
        "registry_schema": registry()["schema"],
        "checks": checks,
        "missing": missing,
        "summary": {
            "total": len(checks),
            "missing": len(missing),
            "registry_symbols": sum(1 for check in checks if check["kind"] == "registry"),
            "discovered_imports": sum(1 for check in checks if check["kind"] == "discovered_import"),
        },
        "non_claim_lock": "API auditor inspects/imports local Python surfaces only. It does not mutate files, execute repairs, rerun CI, call remote APIs, or grant authority.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Audit RHP stable API/import surfaces")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="")
    parser.add_argument("--registry-only", action="store_true")
    args = parser.parse_args(argv)
    result = audit_contract(args.repo_root, include_discovered=not args.registry_only)
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
