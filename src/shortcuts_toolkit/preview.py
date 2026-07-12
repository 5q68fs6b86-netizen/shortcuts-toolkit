"""预览：生成前列出将用到的操作 + 模块 + 警告，供用户确认（不写文件）。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .actions_catalog import ActionInfo, classify_action
from .generator import normalize_spec
from .plist_utils import die

_BUILTIN_PREFIX = "is.workflow.actions."


def preview_spec(spec: dict[str, Any], verify_system: bool = False) -> list[ActionInfo]:
    """解析规格，返回每个动作的分类信息（不生成文件）。

    verify_system=True 时（macOS），用系统真实 identifier 复核：reference 判为内置
    但系统未注册的，标为 builtin_not_in_system（拦截导入后「无法找到此操作」）。
    """
    plist = normalize_spec(spec)
    actions = plist.get("WFWorkflowActions", [])
    builtin: set[str] | None = None
    source = ""
    if verify_system:
        from .verify import load_builtin_table

        builtin, source = load_builtin_table()
    infos: list[ActionInfo] = []
    for a in actions:
        ident = a.get("WFWorkflowActionIdentifier", "?")
        params = a.get("WFWorkflowActionParameters", {}) or {}
        info = classify_action(ident, params)
        if builtin is not None and ident.startswith(_BUILTIN_PREFIX):
            if ident not in builtin:
                info = ActionInfo(
                    ident, info.label, info.module, "builtin_not_in_system", None,
                    f"系统未注册（{source}），导入后会「无法找到此操作」",
                )
            elif info.kind == "unknown_builtin":
                # 系统已注册但 reference 未收录 → 放行
                info = ActionInfo(ident, info.label, info.module, "builtin", None, "")
        infos.append(info)
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
    infos = preview_spec(spec, verify_system=getattr(args, "verify", False))
    print(format_preview(infos, spec.get("name", "(未命名)")))
    if getattr(args, "verify", False):
        from .verify import load_builtin_table

        _, source = load_builtin_table()
        print(f"\n(系统复核: {source})")
