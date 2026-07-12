"""shortcuts-toolkit 核心单元测试 + 生成/解析往返测试。

覆盖：normalize_spec（扁平结构）、解析抽取、动作描述、iCloud GUID、
记账/工具回传规格构建、变量引用工具、生成→解析往返、已签名文件拒绝。
不依赖联网或 macOS 签名。
"""

from __future__ import annotations

import argparse

import pytest

from shortcuts_toolkit.bookkeeping import (
    _csv_line,
    _record_text,
    _var_ref_out,
    build_bookkeeping_spec,
)
from shortcuts_toolkit.generator import (
    build_receive_result_spec,
    normalize_spec,
    write_shortcut,
)
from shortcuts_toolkit.icloud import extract_guid
from shortcuts_toolkit.parser import (
    describe_action,
    extract_actions,
    extract_workflow,
    load_plist,
)

# ---------- normalize_spec ----------


def test_normalize_spec_flat_structure():
    spec = {
        "name": "T",
        "actions": [
            {"identifier": "is.workflow.actions.gettext", "parameters": {}},
        ],
    }
    out = normalize_spec(spec)
    assert "WFWorkflowActions" in out
    assert "WFWorkflow" not in out  # 扁平：不包裹
    assert out["WFWorkflowName"] == "T"
    assert len(out["WFWorkflowActions"]) == 1
    a = out["WFWorkflowActions"][0]
    assert a["WFWorkflowActionIdentifier"] == "is.workflow.actions.gettext"


def test_normalize_spec_passthrough_when_actions_present():
    spec = {"WFWorkflowActions": [{"x": 1}], "WFWorkflowName": "keep"}
    assert normalize_spec(spec) is spec


def test_normalize_spec_unwrap_workflow():
    spec = {"WFWorkflow": {"WFWorkflowActions": [{"y": 2}], "WFWorkflowName": "w"}}
    out = normalize_spec(spec)
    assert out["WFWorkflowName"] == "w"
    assert out["WFWorkflowActions"] == [{"y": 2}]


def test_normalize_spec_defaults():
    out = normalize_spec({"name": "n", "actions": []})
    assert out["WFWorkflowTypes"] == ["NC"]
    assert out["WFWorkflowInputContentItemClasses"] == ["WFTextContentItem"]
    assert out["WFWorkflowMinimumClientVersion"] == 900


# ---------- 解析抽取 ----------


def test_extract_workflow_flat():
    data = {"WFWorkflowActions": [1], "WFWorkflowName": "x"}
    wf = extract_workflow(data)
    assert wf is data


def test_extract_workflow_wrapped():
    data = {"WFWorkflow": {"WFWorkflowActions": [1]}}
    assert extract_workflow(data) == {"WFWorkflowActions": [1]}


def test_extract_actions():
    assert extract_actions({"WFWorkflowActions": [{"a": 1}]}) == [{"a": 1}]
    assert extract_actions({}) == []


# ---------- describe_action ----------


def test_describe_action_known_cn():
    ident, label, _ = describe_action(
        {
            "WFWorkflowActionIdentifier": "is.workflow.actions.gettext",
            "WFWorkflowActionParameters": {"WFTextActionText": "hi"},
        }
    )
    assert ident == "is.workflow.actions.gettext"
    assert "获取文本" in label


def test_describe_action_app_intent():
    ident, label, _ = describe_action(
        {
            "WFWorkflowActionIdentifier": "com.foo.RunThing",
            "WFWorkflowActionParameters": {
                "AppIntentDescriptor": {"AppIntentIdentifier": "RunThing"}
            },
        }
    )
    assert "运行 App Intent" in label
    assert "RunThing" in label


# ---------- iCloud GUID ----------


def test_extract_guid_icloud_url():
    assert extract_guid("https://www.icloud.com/shortcuts/abc123XYZ") == "abc123XYZ"


def test_extract_guid_hex():
    assert extract_guid("deadbeefcafe") == "deadbeefcafe"


# ---------- 变量引用工具 ----------


def test_var_ref_out_uppercases_uuid():
    ref = _var_ref_out("low-uuid", "数据")
    assert ref["OutputUUID"] == "LOW-UUID"
    assert ref["OutputName"] == "数据"
    assert ref["Type"] == "ActionOutput"


def test_csv_line_three_fields():
    refs = [("a", {"OutputUUID": "A"}), ("b", {"OutputUUID": "B"}), ("c", {"OutputUUID": "C"})]
    s, atts = _csv_line(refs)
    assert s.count("\ufffc") == 3
    assert s == "\ufffc,\ufffc,\ufffc"
    assert len(atts) == 3


def test_record_text_attachments():
    refs = [("金额", {"OutputUUID": "X"})]
    s, atts = _record_text(refs)
    assert "\ufffc" in s
    assert "金额" in s
    assert len(atts) == 1


# ---------- 记账 / 工具回传规格 ----------


def _ns(**kw) -> argparse.Namespace:
    base = dict(
        save="csv",
        keys="date,type,amount",
        name="记账",
        csv_file="账本.csv",
        numbers_file="记账本.numbers",
        table_name="表单",
        client_release="18.0",
        min_version=900,
    )
    base.update(kw)
    return argparse.Namespace(**base)


def test_build_bookkeeping_csv_action_count():
    spec, flow = build_bookkeeping_spec(_ns())
    # detect.dictionary + 3 getvalueforkey + file.append = 5
    assert len(spec["actions"]) == 5
    assert "CSV" in flow or "csv" in flow
    idents = [a["identifier"] for a in spec["actions"]]
    assert idents[0] == "is.workflow.actions.detect.dictionary"
    assert idents[-1] == "is.workflow.actions.file.append"


def test_build_bookkeeping_numbers_action_count():
    spec, flow = build_bookkeeping_spec(_ns(save="numbers"))
    # detect.dictionary + 3 getvalueforkey + Numbers intent = 5
    assert len(spec["actions"]) == 5
    assert spec["actions"][-1]["identifier"] == "com.apple.Numbers.TNiOSAddValuesToFormIntent"
    assert "Numbers" in flow


def test_build_receive_result_spec():
    args = argparse.Namespace(
        bundle_id="com.example.app",
        intent_id="ReceiveToolResult",
        team_id="TEAM1",
        callback_url="https://srv/cb",
        name=None,
        include_gettext=False,
        client_release="18.0",
        min_version=900,
    )
    spec = build_receive_result_spec(args)
    assert len(spec["actions"]) == 2
    assert spec["actions"][0]["identifier"] == "com.example.app.ReceiveToolResult"
    assert spec["actions"][1]["identifier"] == "is.workflow.actions.getcontentofurl"


def test_build_receive_result_spec_with_gettext():
    args = argparse.Namespace(
        bundle_id="com.example.app",
        intent_id="R",
        team_id="",
        callback_url="u",
        name=None,
        include_gettext=True,
        client_release="18.0",
        min_version=900,
    )
    spec = build_receive_result_spec(args)
    assert len(spec["actions"]) == 3
    assert spec["actions"][0]["identifier"] == "is.workflow.actions.gettext"


# ---------- 生成 → 解析 往返 ----------


def test_roundtrip_generate_parse(tmp_path):
    spec = {
        "name": "Roundtrip",
        "actions": [
            {
                "identifier": "is.workflow.actions.gettext",
                "parameters": {"WFTextActionText": "你好，世界"},
            },
            {"identifier": "is.workflow.actions.showresult", "parameters": {}},
        ],
    }
    plist = normalize_spec(spec)
    out = tmp_path / "rt.shortcut"
    write_shortcut(plist, str(out))
    assert out.exists()

    data = load_plist(str(out))
    # 扁平结构：顶层即 WFWorkflow*
    assert "WFWorkflowActions" in data
    actions = extract_actions(extract_workflow(data))
    assert len(actions) == 2
    assert actions[0]["WFWorkflowActionIdentifier"] == "is.workflow.actions.gettext"


def test_generated_file_is_binary_plist(tmp_path):
    plist = normalize_spec({"name": "x", "actions": []})
    out = tmp_path / "x.shortcut"
    write_shortcut(plist, str(out))
    head = out.read_bytes()[:8]
    assert head.startswith(b"bplist00")


# ---------- 边界 ----------


def test_load_plist_rejects_signed_file(tmp_path):
    f = tmp_path / "signed.shortcut"
    f.write_bytes(b"AEA1" + b"\x00" * 32)
    with pytest.raises(SystemExit):
        load_plist(str(f))


def test_load_plist_missing_file(tmp_path):
    with pytest.raises(SystemExit):
        load_plist(str(tmp_path / "nope.shortcut"))


def test_bookkeeping_spec_normalizes_to_flat():
    spec, _ = build_bookkeeping_spec(_ns())
    plist = normalize_spec(spec)
    assert "WFWorkflowActions" in plist
    assert "WFWorkflow" not in plist


def test_build_bookkeeping_spec_requires_keys_via_normalize():
    spec, _ = build_bookkeeping_spec(_ns(keys="a"))
    plist = normalize_spec(spec)
    # detect.dictionary + 1 getvalueforkey + file.append = 3
    assert len(plist["WFWorkflowActions"]) == 3
