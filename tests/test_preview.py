"""preview 子命令测试。"""

from __future__ import annotations

from shortcuts_toolkit.preview import format_preview, preview_spec


def test_preview_classifies_mixed_actions():
    spec = {
        "name": "t",
        "actions": [
            {"identifier": "is.workflow.actions.gettext", "parameters": {}},
            {"identifier": "com.apple.Numbers.SomeIntent", "parameters": {}},
            {"identifier": "is.workflow.actions.totallyfake", "parameters": {}},
        ],
    }
    infos = preview_spec(spec)
    assert len(infos) == 3
    assert infos[0].kind == "builtin"
    assert infos[1].kind == "third_party"
    assert infos[2].kind == "unknown_builtin"


def test_format_preview_has_modules_and_warning():
    spec = {
        "name": "t",
        "actions": [
            {"identifier": "is.workflow.actions.gettext", "parameters": {}},
            {"identifier": "is.workflow.actions.fakefake", "parameters": {}},
        ],
    }
    out = format_preview(preview_spec(spec), "t")
    assert "模块汇总" in out
    assert "需确认" in out  # fakefake 触发警告
    assert "动作数: 2" in out


def test_format_preview_no_warning_when_all_valid():
    spec = {
        "name": "t",
        "actions": [{"identifier": "is.workflow.actions.gettext", "parameters": {}}],
    }
    out = format_preview(preview_spec(spec), "t")
    assert "无警告" in out
    assert "需确认" not in out


def test_format_preview_lists_third_party_source_app():
    spec = {"name": "t", "actions": [
        {"identifier": "com.foo.RunThing", "parameters": {}}]}
    out = format_preview(preview_spec(spec), "t")
    assert "com.foo" in out


def test_preview_verify_system_flags_not_in_system(monkeypatch):
    from shortcuts_toolkit import verify as verify_mod

    monkeypatch.setattr(
        verify_mod, "load_builtin_table",
        lambda: ({"is.workflow.actions.showresult"}, "test"),
    )
    spec = {"name": "t", "actions": [
        {"identifier": "is.workflow.actions.generatemachinereadablecode", "parameters": {}}]}
    infos = preview_spec(spec, verify_system=True)
    assert "not_in_system" in infos[0].kind
