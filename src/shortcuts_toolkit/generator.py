"""生成 unsigned .shortcut：generate(通用规格) + build-rr(一扫工具模板)。"""

import argparse
import json
import uuid
from pathlib import Path
from typing import Any

from .naming import InvalidNameError, validate_name
from .plist_utils import die


def normalize_spec(spec: dict[str, Any]) -> dict[str, Any]:
    """统一 JSON 规格为完整 plist dict（【扁平结构】，WFWorkflow* 键在顶层，
    不再包裹 WFWorkflow——否则签名虽过但导入会是空快捷指令）。"""
    if "WFWorkflowActions" in spec:
        return spec
    if "WFWorkflow" in spec:
        return spec["WFWorkflow"]
    icon = spec.get("icon", {}) or {}
    actions = []
    for a in spec.get("actions", []):
        actions.append(
            {
                "WFWorkflowActionIdentifier": a["identifier"],
                "WFWorkflowActionParameters": a.get("parameters", {}),
            }
        )
    return {
        "WFWorkflowClientVersion": spec.get("client_version", "3300.7.1"),
        "WFWorkflowIcon": {
            "WFWorkflowIconStartColor": icon.get("color", 4282601983),
            "WFWorkflowIconGlyphNumber": icon.get("glyph", 61440),
        },
        "WFWorkflowImportQuestions": spec.get("import_questions", []),
        "WFWorkflowInputContentItemClasses": spec.get("input_classes", ["WFTextContentItem"]),
        "WFWorkflowMinimumClientVersion": spec.get("minimum_client_version", 900),
        "WFWorkflowMinimumClientVersionString": str(spec.get("minimum_client_version", 900)),
        "WFWorkflowName": spec.get("name", ""),
        "WFWorkflowOutputContentItemClasses": spec.get("output_classes", []),
        "WFWorkflowHasOutputFallback": spec.get("has_output_fallback", False),
        "WFWorkflowTypes": spec.get("types", ["NC"]),
        "WFWorkflowHasShortcutInputVariables": spec.get("has_input_variables", True),
        "WFWorkflowActions": actions,
    }


def write_shortcut(plist: dict[str, Any], out_path: str) -> Path:
    import plistlib

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        plistlib.dump(plist, f, fmt=plistlib.FMT_BINARY)
    return out


def cmd_generate(args: argparse.Namespace) -> None:
    spec_path = Path(args.input)
    if not spec_path.exists():
        die(f"规格文件不存在: {args.input}")
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    try:
        spec["name"] = validate_name(spec.get("name", ""))
    except InvalidNameError as e:
        die(str(e))
    plist = normalize_spec(spec)
    write_shortcut(plist, args.output)
    wf = plist.get("WFWorkflow", plist)
    n = len(wf.get("WFWorkflowActions", []))
    print(f"[OK] 已生成: {args.output}  (动作 {n} 个, 二进制 plist)")


def build_receive_result_spec(args: argparse.Namespace) -> dict[str, Any]:
    bundle = args.bundle_id
    intent = args.intent_id
    team = args.team_id
    callback = args.callback_url
    if not (bundle and intent and callback):
        die("build-rr 需要 --bundle-id --intent-id --callback-url")

    app_intent_action = {
        "WFWorkflowActionIdentifier": f"{bundle}.{intent}",
        "WFWorkflowActionParameters": {
            "AppIntentDescriptor": {
                "BundleIdentifier": bundle,
                "TeamIdentifier": team or "",
                "AppIntentIdentifier": intent,
                "Name": intent,
            },
            "ShowWhenRun": False,
            "UUID": str(uuid.uuid4()).upper(),
        },
    }
    post_action = {
        "WFWorkflowActionIdentifier": "is.workflow.actions.getcontentofurl",
        "WFWorkflowActionParameters": {
            "WFHTTPMethod": "POST",
            "WFHTTPHeaders": {"Content-Type": "application/json"},
            "WFHTTPBodyType": "JSON",
            "WFJSONBody": {"result": "{ShortcutInput}"},
            "WFURLActionURL": callback,
        },
    }
    actions = [app_intent_action, post_action]
    if args.include_gettext:
        actions = [
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.gettext",
                "WFWorkflowActionParameters": {"WFTextActionText": ""},
            }
        ] + actions
    return {
        "name": args.name or f"tool-{intent}",
        "client_release": args.client_release,
        "minimum_client_version": args.min_version,
        "types": ["NC"],
        "input_classes": ["WFTextContentItem"],
        "actions": [
            {
                "identifier": a["WFWorkflowActionIdentifier"],
                "parameters": a["WFWorkflowActionParameters"],
            }
            for a in actions
        ],
    }


def cmd_build_rr(args: argparse.Namespace) -> None:
    spec = build_receive_result_spec(args)
    try:
        spec["name"] = validate_name(spec.get("name", ""))
    except InvalidNameError as e:
        die(str(e))
    plist = normalize_spec(spec)
    write_shortcut(plist, args.output)
    n = len(plist.get("WFWorkflowActions", []))
    print(f"[OK] 已生成一扫工具模板: {args.output}  (动作 {n} 个)")
    print(
        f"     流程: 运行 App Intent {args.bundle_id}.{args.intent_id} "
        f"→ POST 结果到 {args.callback_url}"
    )
    print("     提示: 接下来用 `sign` 签名后即可导入。")
