"""解析 .shortcut 文件：可读动作清单(parse) + XML plist 原始结构(inspect)。"""

import argparse
import plistlib
from pathlib import Path
from typing import Any

from .actions_cn import ACTION_CN
from .plist_utils import SIGNED_MAGIC, die, truncate


def load_plist(path: str) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        die(f"文件不存在: {path}")
    with open(p, "rb") as f:
        head = f.read(8)
    if head.startswith(SIGNED_MAGIC):
        die(
            "该 .shortcut 是【已签名/加密】格式(AEA1 容器)，工作流被加密，无法明文读取——"
            "这是 Apple 的安全设计，连系统 plutil 也读不出。只能【导入】，不能解析。\n"
            "如需解析内容：用 `icloud <链接>` 从 iCloud 下载 unsigned 版本，"
            "或在快捷指令 App 里导出后再处理。"
        )
    with open(p, "rb") as f:
        data = f.read()
    try:
        return plistlib.loads(data)
    except Exception:
        die(f"不是有效的二进制 plist / .shortcut 文件: {path}")


def extract_workflow(data: Any) -> dict[str, Any]:
    """从 plist 顶层解析出 workflow 字典，兼容包裹与扁平两种结构。"""
    if isinstance(data, dict) and "WFWorkflow" in data:
        wf = data["WFWorkflow"]
        if isinstance(wf, dict):
            return wf
    return data if isinstance(data, dict) else {}


def extract_actions(wf: Any) -> list[dict[str, Any]]:
    return wf.get("WFWorkflowActions", []) if isinstance(wf, dict) else []


def describe_action(action: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    ident = action.get("WFWorkflowActionIdentifier", "?")
    params = action.get("WFWorkflowActionParameters", {}) or {}
    cn = ACTION_CN.get(ident)
    if cn:
        label = f"{cn}  ({ident})"
    elif "." in ident and not ident.startswith("is.workflow.actions."):
        tail = ident.rsplit(".", 1)[-1]
        label = f"运行 App Intent  ({ident})"
        desc = params.get("AppIntentDescriptor") or {}
        if isinstance(desc, dict) and desc.get("AppIntentIdentifier"):
            label += f"  [intent={desc['AppIntentIdentifier']}]"
        _ = tail
    else:
        label = ident
    return ident, label, params


def cmd_parse(args: argparse.Namespace) -> None:
    data = load_plist(args.file)
    wf = extract_workflow(data)
    actions = extract_actions(wf)
    name = wf.get("WFWorkflowName") or args.file
    types = wf.get("WFWorkflowTypes", [])
    minver = wf.get("WFWorkflowMinimumClientVersion", "?")
    print(f"快捷指令: {name}")
    print(f"类型: {types}    最低客户端版本: {minver}")
    print(f"动作数: {len(actions)}")
    print("-" * 60)
    if not actions:
        print("(未发现 WFWorkflowActions，可能结构不同。可用 inspect 查看原始 plist)")
        return
    for i, action in enumerate(actions, 1):
        _, label, params = describe_action(action)
        print(f"{i:>2}. {label}")
        if params:
            for k, val in params.items():
                if k in ("UUID", "CustomOutputName"):
                    continue
                print(f"      {k} = {truncate(val)}")


def cmd_inspect(args: argparse.Namespace) -> None:
    data = load_plist(args.file)
    text = plistlib.dumps(data, fmt=plistlib.FMT_XML).decode("utf-8")
    print(text)
