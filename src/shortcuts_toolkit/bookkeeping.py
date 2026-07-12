"""记账快捷指令：固定 JSON 输入 → 提取字段 → 追加到 CSV/Numbers。⭐ 已实测可用。"""

import argparse
import uuid
from typing import Any

from .generator import normalize_spec, write_shortcut


def _var_ref_out(uuid_str: str, name: str) -> dict[str, Any]:
    return {"OutputUUID": uuid_str.upper(), "Type": "ActionOutput", "OutputName": name}


def _wf_input(ref: dict[str, Any]) -> dict[str, Any]:
    return {"Value": ref, "WFSerializationType": "WFTextTokenAttachment"}


def _record_text(label_map):
    """label_map: list of (label, var_ref) -> (string, attachmentsByRange)."""
    s = []
    atts = {}
    pos = 0
    for label, ref in label_map:
        s.append(label + ": ")
        pos += len(label) + 2
        s.append("\ufffc")
        atts[f"{{{pos}, 1}}"] = ref
        pos += 1
        s.append("  |  ")
        pos += 5
    return "".join(s).rstrip().rstrip("|").rstrip(), atts


def _csv_line(field_refs):
    """field_refs: list of (key, var_ref) -> (csv string, attachments)。
    生成 "￼,￼,￼,￼,￼" 逗号分隔，每个 ￼ 是一个字段变量。"""
    s = []
    atts = {}
    pos = 0
    for i, (_, ref) in enumerate(field_refs):
        if i > 0:
            s.append(",")
            pos += 1
        s.append("\ufffc")
        atts[f"{{{pos}, 1}}"] = ref
        pos += 1
    return "".join(s), atts


def build_bookkeeping_spec(args: argparse.Namespace):
    keys = [k.strip() for k in args.keys.split(",") if k.strip()]
    data_uuid = str(uuid.uuid4()).upper()
    data_ref = _var_ref_out(data_uuid, "数据")
    actions = [
        {
            "WFWorkflowActionIdentifier": "is.workflow.actions.detect.dictionary",
            "WFWorkflowActionParameters": {
                "UUID": data_uuid,
                "CustomOutputName": "数据",
                "WFInput": {
                    "Value": {"Type": "ExtensionInput"},
                    "WFSerializationType": "WFTextTokenAttachment",
                },
            },
        },
    ]
    field_refs = []
    for key in keys:
        k_uuid = str(uuid.uuid4()).upper()
        actions.append(
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.getvalueforkey",
                "WFWorkflowActionParameters": {
                    "WFDictionaryKey": key,
                    "WFGetDictionaryValueType": "Value",
                    "WFInput": _wf_input(data_ref),
                    "UUID": k_uuid,
                    "CustomOutputName": key,
                },
            }
        )
        field_refs.append((key, _var_ref_out(k_uuid, key)))

    if args.save == "numbers":
        values = []
        for _, ref in field_refs:
            values.append(
                {
                    "Value": {"string": "\ufffc", "attachmentsByRange": {"{0, 1}": ref}},
                    "WFSerializationType": "WFTextTokenString",
                }
            )
        spreadsheet = {
            "fileLocation": {
                "relativeSubpath": "com~apple~Numbers/Documents/" + args.numbers_file,
                "fileProviderDomainID": "REPLACE_WITH_YOUR_ICLOUD_FILEPROVIDER_ID",
                "WFFileLocationType": "iCloud",
                "appContainerBundleIdentifier": "com.apple.Numbers",
            },
            "filename": args.numbers_file,
            "displayName": args.numbers_file.replace(".numbers", ""),
        }
        actions.append(
            {
                "WFWorkflowActionIdentifier": "com.apple.Numbers.TNiOSAddValuesToFormIntent",
                "WFWorkflowActionParameters": {
                    "spreadsheet": spreadsheet,
                    "formName": args.table_name,
                    "values": values,
                    "UUID": str(uuid.uuid4()).upper(),
                },
            }
        )
        flow = (
            f"解析JSON→提取{keys}→往Numbers表格「{args.table_name}」追加一行"
            f"(文件{args.numbers_file})"
        )
    else:
        csv_str, csv_atts = _csv_line(field_refs)
        actions.append(
            {
                "WFWorkflowActionIdentifier": "is.workflow.actions.file.append",
                "WFWorkflowActionParameters": {
                    "WFFilePath": args.csv_file,
                    "WFAppendFileLineBreak": True,
                    "WFInput": {
                        "Value": {"string": csv_str, "attachmentsByRange": csv_atts},
                        "WFSerializationType": "WFTextTokenString",
                    },
                    "UUID": str(uuid.uuid4()).upper(),
                },
            }
        )
        flow = (
            f"解析JSON→提取{keys}→拼成CSV记录行→追加到文件「{args.csv_file}」"
            f"(iCloud云盘，不存在则自动建)"
        )

    return {
        "name": args.name or "记账",
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
    }, flow


def cmd_bookkeeping(args: argparse.Namespace) -> None:
    spec, flow = build_bookkeeping_spec(args)
    keys = [k.strip() for k in args.keys.split(",") if k.strip()]
    plist = normalize_spec(spec)
    write_shortcut(plist, args.output)
    n = len(plist.get("WFWorkflowActions", []))
    print(f"[OK] 已生成记账快捷指令: {args.output}  (动作 {n} 个)")
    print(f"     流程: {flow}")
    print(f"     JSON 字段(将逐个提取): {keys}")
    print("     示例输入:")
    print(
        '       {"date":"2026-07-10","type":"支出","amount":38.5,"category":"餐饮","note":"午餐"}'
    )
    if args.save == "numbers":
        print("     ⚠️ Numbers 文件引用是占位符：导入后在该动作里重选你的 .numbers 文件，")
        print(f"        并确保表格「{args.table_name}」列数与字段数一致。")
    else:
        print(f"     ℹ️ CSV 模式：记录追加到 iCloud 云盘的「{args.csv_file}」，")
        print("        不存在则自动创建；可直接用 Numbers/Excel 打开成表格。")
        print(f"        首行如需表头，可自行在文件里加：{','.join(keys)}")
    print("     下一步: sign 签名 → 在 Finder 双击 .signed.shortcut 导入 → 带 JSON 运行。")
