from pathlib import Path
import importlib


def test_rhp_016_3_browser_supervisor_moves_clientconnection_to_type_checking_only():
    src = Path("tools/browser_supervisor.py").read_text(encoding="utf-8")
    assert "if TYPE_CHECKING:" in src
    assert "from typing import TYPE_CHECKING" in src or "TYPE_CHECKING, Any" in src

    before_guard = src.split("if TYPE_CHECKING:", 1)[0]
    after_guard = src.split("if TYPE_CHECKING:", 1)[1]
    assert "from websockets.asyncio.client import ClientConnection" not in before_guard
    assert "from websockets.asyncio.client import ClientConnection" in after_guard


def test_rhp_016_3_browser_supervisor_imports_without_installed_websockets():
    module = importlib.import_module("tools.browser_supervisor")
    assert hasattr(module, "CDPSupervisor")
    assert hasattr(module, "SUPERVISOR_REGISTRY")
    assert hasattr(module, "_require_websockets")


def test_rhp_016_3_browser_supervisor_has_lazy_websockets_guard():
    src = Path("tools/browser_supervisor.py").read_text(encoding="utf-8")
    assert "def _require_websockets()" in src
    assert "_require_websockets().connect" in src
    assert "websockets package is required for CDP supervisor" in src
