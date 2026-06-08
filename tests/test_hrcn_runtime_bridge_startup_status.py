import importlib.util
from pathlib import Path


def _load_main_module():
    path = Path.cwd() / "hermes_cli" / "main.py"
    spec = importlib.util.spec_from_file_location("hermes_cli_main_for_hrcn_test", path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)  # type: ignore[union-attr]
    except SystemExit:
        pass
    return module


def test_hrcn_status_command_predicate_rejects_unrelated():
    mod = _load_main_module()
    assert mod._try_hrcn_bridge_status_command(["not-hrcn"]) is False


def test_hrcn_bridge_status_prints_read_only(capsys):
    mod = _load_main_module()
    assert mod._print_hrcn_bridge_status(compact=True) is True
    out = capsys.readouterr().out
    assert "HRCN bridge: read_only / hrcn-ops-v0.3.0" in out


def test_hrcn_startup_status_respects_env(monkeypatch, capsys):
    mod = _load_main_module()
    monkeypatch.setenv("HERMES_HRCN_BRIDGE", "1")
    monkeypatch.setattr(mod.sys, "argv", ["hermes"])
    mod._maybe_print_hrcn_bridge_startup_status()
    out = capsys.readouterr().out
    assert "HRCN bridge: read_only / hrcn-ops-v0.3.0" in out
