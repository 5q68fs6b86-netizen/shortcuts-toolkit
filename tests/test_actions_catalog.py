"""actions_catalog 解析与分类测试。"""

from __future__ import annotations

from shortcuts_toolkit.actions_catalog import classify_action, get_catalog


def test_catalog_builtin_loaded():
    _, names, _, _ = get_catalog()
    assert "gettext" in names
    assert "showresult" in names
    assert "file.append" in names


def test_catalog_appintent_loaded():
    _, _, _, anames = get_catalog()
    assert "CreateAlarmIntent" in anames


def test_classify_builtin_has_category():
    info = classify_action("is.workflow.actions.gettext")
    assert info.kind == "builtin"
    assert info.module  # 有类别
    assert "获取文本" in info.label


def test_classify_unknown_builtin():
    info = classify_action("is.workflow.actions.totallymadeupxyz")
    assert info.kind == "unknown_builtin"
    assert info.note  # 有警告


def test_classify_third_party():
    info = classify_action("com.apple.Numbers.TNiOSAddValuesToFormIntent")
    assert info.kind == "third_party"
    assert info.source_app == "com.apple.Numbers"
    assert "Numbers" in info.note


def test_classify_appintent_wrapper_known():
    info = classify_action(
        "is.workflow.actions.appintentexecution",
        {
            "AppIntentDescriptor": {
                "AppIntentIdentifier": "CreateAlarmIntent",
                "BundleIdentifier": "com.apple.mobiletimer",
            }
        },
    )
    assert info.kind == "system_appintent"
    assert info.module  # 有类别


def test_classify_appintent_wrapper_unknown():
    info = classify_action(
        "is.workflow.actions.appintentexecution",
        {"AppIntentDescriptor": {"AppIntentIdentifier": "FooBarBaz", "BundleIdentifier": "com.x"}},
    )
    assert info.kind == "unknown_appintent"
    assert info.note
