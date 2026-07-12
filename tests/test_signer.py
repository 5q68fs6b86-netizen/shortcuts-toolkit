"""sign 命令 --clean 测试（mock 签名，不依赖 macOS/联网）。"""

from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import MagicMock

from shortcuts_toolkit import signer


def _run_sign(unsigned: Path, signed: Path, *, clean: bool, monkeypatch) -> None:
    def fake_run(cmd, **kw):
        out = cmd[cmd.index("--output") + 1]
        Path(out).write_bytes(b"AEA1signed")
        r = MagicMock()
        r.returncode = 0
        r.stdout = ""
        r.stderr = ""
        return r

    monkeypatch.setattr(signer.subprocess, "run", fake_run)
    monkeypatch.setattr(signer.sys, "platform", "darwin")
    args = argparse.Namespace(input=str(unsigned), output=str(signed), mode="anyone", clean=clean)
    signer.cmd_sign(args)


def test_sign_clean_deletes_unsigned(tmp_path, monkeypatch):
    unsigned = tmp_path / "x.shortcut"
    unsigned.write_bytes(b"bplist00fake")
    signed = tmp_path / "x.signed.shortcut"
    _run_sign(unsigned, signed, clean=True, monkeypatch=monkeypatch)
    assert not unsigned.exists()
    assert signed.exists()


def test_sign_no_clean_keeps_unsigned(tmp_path, monkeypatch):
    unsigned = tmp_path / "x.shortcut"
    unsigned.write_bytes(b"bplist00fake")
    signed = tmp_path / "x.signed.shortcut"
    _run_sign(unsigned, signed, clean=False, monkeypatch=monkeypatch)
    assert unsigned.exists()
    assert signed.exists()
