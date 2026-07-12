"""预览：生成前列出将用到的操作 + 模块 + 警告，供用户确认（不写文件）。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .actions_catalog import ActionInfo, classify_action
from .generator import normalize_spec
from .plist_utils import die


def preview_spec(spec: dict[str, Any]) -> list[ActionInfo]:
    """解析规格，返回每个动作的分类信息（不生成文件）。"""
    plist = normalize_spec(spec)
    actions = plist.get("WFWorkflowActions", [])
    infos: list[ActionInfo] = []
    for a in actions:
        ident = a.get("WFWorkflowActionIdentifier", "?")
        params = a.get("WFWorkflowActionParameters", {}) or {}
        infos.append(classify_action(ident, params))
    return infos


def format_preview(infos: list[ActionInfo], name: str) -> str:
    lines = [f"快捷指令名: {name}", f"动作数: {len(infos)}"]

    modules: dict[str, int] = {}
    for info in infos:
        modules[info.module] = modules.get(info.module, 0) + 1
    lines.append("")
    lines.append("模块汇总:")
    for mod, cnt in sorted(modules.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"  - {mod}: {cnt}")

    lines.append("")
    lines.append("操作清单:")
    warnings: list[ActionInfo] = []
    for i, info in enumerate(infos, 1):
        lines.append(f"  {i}. {info.label}")
        lines.append(f"     模块: {info.module}  类型: {info.kind}")
        if info.source_app:
            lines.append(f"     来源App: {info.source_app}")
        if info.note:
            lines.append(f"     注意: {info.note}")
            warnings.append(info)

    if warnings:
        lines.append("")
        lines.append(f"⚠️ {len(warnings)} 个动作需确认（未知/第三方，导入后可能「无法找到此操作」）")
    else:
        lines.append("")
        lines.append("✓ 所有动作均为已知内置，无警告")
    return "\n".join(lines)


def cmd_preview(args: argparse.Namespace) -> None:
    spec_path = Path(args.input)
    if not spec_path.exists():
        die(f"规格文件不存在: {args.input}")
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    infos = preview_spec(spec)
    print(format_preview(infos, spec.get("name", "(未命名)")))
