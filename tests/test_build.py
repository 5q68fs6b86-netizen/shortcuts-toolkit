"""build 一键工作流测试（mock 签名）。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from shortcuts_toolkit import build as build_mod
from shortcuts_toolkit.build import cmd_build


def _spec(path: Path, name: str) -> None:
    path.write_text(
        json.dumps(
            {
                "name": name,
                "actions": [{"identifier": "is.workflow.actions.showresult", "parameters": {}}],
            }
        ),
        encoding="utf-8",
    )


def test_build_macos_produces_signed(tmp_path, monkeypatch):
    spec = tmp_path / "s.json"
    _spec(spec, "mytool")
    out = tmp_path / "mytool.signed.shortcut"

    def fake_run(cmd, **kw):
        Path(cmd[cmd.index("--output") + 1]).write_bytes(b"AEA1signed")
        r = MagicMock()
        r.returncode = 0
        r.stdout = ""
        r.stderr = ""
        return r

    monkeypatch.setattr(build_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(build_mod.sys, "platform", "darwin")
    cmd_build(argparse.Namespace(input=str(spec), output=str(out), mode="anyone"))
    assert out.exists()


def test_build_rejects_bad_name(tmp_path):
    spec = tmp_path / "s.json"
    _spec(spec, "记账")
    with pytest.raises(SystemExit):
        cmd_build(
            argparse.Namespace(input=str(spec), output=str(tmp_path / "o.shortcut"), mode="anyone")
        )


def test_build_non_macos_produces_unsigned(tmp_path, monkeypatch):
    spec = tmp_path / "s.json"
    _spec(spec, "mytool")
    out = tmp_path / "mytool.shortcut"
    monkeypatch.setattr(build_mod.sys, "platform", "linux")
    cmd_build(argparse.Namespace(input=str(spec), output=str(out), mode="anyone"))
    assert out.exists()
