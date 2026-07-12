"""verify 子命令测试（mock 系统表，不依赖共享缓存）。"""

from __future__ import annotations

import argparse
import json
from unittest.mock import patch

import pytest

from shortcuts_toolkit import verify
from shortcuts_toolkit.verify import cmd_verify, verify_spec


def test_verify_flags_builtin_not_in_system():
    spec = {"name": "t", "actions": [
        {"identifier": "is.workflow.actions.showresult", "parameters": {}},
        {"identifier": "is.workflow.actions.generatemachinereadablecode", "parameters": {}},
    ]}
    fake = {"is.workflow.actions.showresult"}
    with patch.object(verify, "load_builtin_table", return_value=(fake, "test")):
        infos, source = verify_spec(spec)
    assert source == "test"
    assert infos[0].kind == "builtin"
    assert "not_in_system" in infos[1].kind


def test_verify_third_party_not_flagged():
    spec = {"name": "t", "actions": [
        {"identifier": "com.apple.Numbers.SomeIntent", "parameters": {}}]}
    with patch.object(verify, "load_builtin_table", return_value=(set(), "test")):
        infos, _ = verify_spec(spec)
    assert "not_in_system" not in infos[0].kind
    assert infos[0].kind == "third_party"


def test_cmd_verify_exits_on_bad(tmp_path):
    spec = tmp_path / "s.json"
    spec.write_text(
        json.dumps({"name": "t", "actions": [
            {"identifier": "is.workflow.actions.totallyfake", "parameters": {}}]}),
        encoding="utf-8",
    )
    with patch.object(
        verify, "load_builtin_table",
        return_value=({"is.workflow.actions.showresult"}, "test"),
    ):
        with pytest.raises(SystemExit):
            cmd_verify(argparse.Namespace(input=str(spec)))


def test_cmd_verify_passes_when_all_known(tmp_path, capsys):
    spec = tmp_path / "s.json"
    spec.write_text(
        json.dumps({"name": "t", "actions": [
            {"identifier": "is.workflow.actions.showresult", "parameters": {}}]}),
        encoding="utf-8",
    )
    with patch.object(
        verify, "load_builtin_table",
        return_value=({"is.workflow.actions.showresult"}, "test"),
    ):
        cmd_verify(argparse.Namespace(input=str(spec)))
    assert "全部动作系统可识别" in capsys.readouterr().out


def test_verify_system_known_but_not_in_reference():
    """系统有但 reference 未收录的新动作 → 应放行（不误判坏）。"""
    fake = {"is.workflow.actions.brandnewaction"}  # reference 没有，但系统有
    with patch.object(verify, "load_builtin_table", return_value=(fake, "test")):
        infos, _ = verify_spec({"name": "t", "actions": [
            {"identifier": "is.workflow.actions.brandnewaction", "parameters": {}}]})
    assert infos[0].kind == "builtin"  # 系统有 → 放行，不误判 unknown_builtin
