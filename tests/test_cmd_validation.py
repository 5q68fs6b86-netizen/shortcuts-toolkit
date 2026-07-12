"""cmd 层命名校验测试：非法名应报错退出，合法名正常生成。"""

from __future__ import annotations

import argparse
import json

import pytest

from shortcuts_toolkit.bookkeeping import cmd_bookkeeping
from shortcuts_toolkit.generator import cmd_generate


def test_cmd_generate_rejects_non_url_safe_name(tmp_path):
    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps({"name": "记账", "actions": []}), encoding="utf-8")
    args = argparse.Namespace(input=str(spec), output=str(tmp_path / "o.shortcut"))
    with pytest.raises(SystemExit):
        cmd_generate(args)


def test_cmd_generate_accepts_url_safe_name(tmp_path):
    spec = tmp_path / "spec.json"
    spec.write_text(
        json.dumps(
            {
                "name": "hello",
                "actions": [{"identifier": "is.workflow.actions.showresult", "parameters": {}}],
            }
        ),
        encoding="utf-8",
    )
    out = tmp_path / "o.shortcut"
    cmd_generate(argparse.Namespace(input=str(spec), output=str(out)))
    assert out.exists()


def test_cmd_bookkeeping_rejects_invalid_name(tmp_path):
    args = argparse.Namespace(
        save="csv",
        keys="a",
        name="记账",
        csv_file="x.csv",
        numbers_file="x.numbers",
        table_name="t",
        client_release="18.0",
        min_version=900,
        output=str(tmp_path / "o.shortcut"),
    )
    with pytest.raises(SystemExit):
        cmd_bookkeeping(args)


def test_cmd_bookkeeping_accepts_url_safe_name(tmp_path):
    out = tmp_path / "o.shortcut"
    args = argparse.Namespace(
        save="csv",
        keys="a",
        name="my_books",
        csv_file="x.csv",
        numbers_file="x.numbers",
        table_name="t",
        client_release="18.0",
        min_version=900,
        output=str(out),
    )
    cmd_bookkeeping(args)
    assert out.exists()
