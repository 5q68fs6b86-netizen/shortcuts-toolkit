"""verify：用系统真实 identifier 校验 spec，生成前拦截「导入后无法找到此操作」。

数据源（权威优先）：
- macOS：实时 grep dyld 共享缓存（WorkflowKit.framework 注册的 identifier），跟系统版本走，最准
- 非 macOS：读包内 data/known_actions.txt（dump 自 macOS 的内置表，作 fallback）

校验规则：
- 内置动作 identifier（is.workflow.actions.*）不在系统真实集合 → ❌ 导入后会「无法找到此操作」
- 第三方 App 动作（<bundle>.<intent>）→ 无法静态判定，提示需设备装 App
"""

from __future__ import annotations

import argparse
import glob
import json
import subprocess
import sys
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any

from .actions_catalog import ActionInfo, classify_action
from .generator import normalize_spec
from .plist_utils import die

_BUILTIN_PREFIX = "is.workflow.actions."


def _find_dyld_cache() -> str:
    for pat in (
        "/System/Cryptexes/OS/System/Library/dyld/dyld_shared_cache_x86_64h",
        "/System/Cryptexes/OS/System/Library/dyld/dyld_shared_cache_arm64e",
    ):
        if Path(pat).exists():
            return pat
    return ""


def _dump_system_actions() -> tuple[set[str], str]:
    """macOS：grep 共享缓存 dump 真实 identifier。失败返回 (set(), '')."""
    cache = _find_dyld_cache()
    if not cache:
        return set(), ""
    files = [cache] + sorted(
        glob.glob(cache + ".0[0-9]") + glob.glob(cache + ".[12][0-9]")
    )
    ids: set[str] = set()
    for f in files:
        if not Path(f).exists():
            continue
        try:
            r = subprocess.run(
                ["grep", "-aoE", r"is\.workflow\.actions\.[a-z0-9.]+", f],
                capture_output=True, text=True, timeout=180,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return set(), ""
        for line in r.stdout.splitlines():
            tok = line.strip()
            if tok:
                ids.add(tok)
    if ids:
        return ids, f"系统共享缓存实时 dump（{len(ids)} 个，{sys.platform}）"
    return set(), ""


def _load_bundled_table() -> set[str]:
    """读包内 data/known_actions.txt（非 macOS fallback）。"""
    ids: set[str] = set()
    text = (
        resources.files("shortcuts_toolkit")
        .joinpath("data/known_actions.txt")
        .read_text("utf-8")
    )
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            ids.add(line)
    return ids


@lru_cache(maxsize=1)
def load_builtin_table() -> tuple[set[str], str]:
    """返回 (内置 identifier 全集, 来源说明)。macOS 优先实时 dump（结果缓存）。"""
    if sys.platform == "darwin":
        ids, note = _dump_system_actions()
        if ids:
            return ids, note
    return _load_bundled_table(), "内置表（dump 自 macOS 2026-07-12，非实时）"


def verify_spec(spec: dict[str, Any]) -> tuple[list[ActionInfo], str]:
    """校验规格里每个动作 identifier 是否系统可识别。返回 (infos, 数据来源)。"""
    plist = normalize_spec(spec)
    actions = plist.get("WFWorkflowActions", [])
    builtin, source = load_builtin_table()
    infos: list[ActionInfo] = []
    for a in actions:
        ident = a.get("WFWorkflowActionIdentifier", "?")
        params = a.get("WFWorkflowActionParameters", {}) or {}
        info = classify_action(ident, params)
        # 权威复核：内置前缀动作用系统真实集合判定（系统是权威，reference 可能滞后）
        if ident.startswith(_BUILTIN_PREFIX):
            if ident not in builtin:
                info = ActionInfo(
                    ident, info.label, info.module, "builtin_not_in_system", None,
                    f"系统（{source}）未注册此 identifier，导入后大概率「无法找到此操作」",
                )
            else:
                # 系统已注册 → 放行（即便 reference 未收录也认作合法内置）
                info = ActionInfo(ident, info.label, info.module, "builtin", info.source_app, "")
        infos.append(info)
    return infos, source


def cmd_verify(args: argparse.Namespace) -> None:
    spec_path = Path(args.input)
    if not spec_path.exists():
        die(f"规格文件不存在: {args.input}")
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    infos, source = verify_spec(spec)
    print(f"数据来源: {source}")
    print(f"动作数: {len(infos)}")
    bad = [
        i for i in infos
        if i.kind == "builtin_not_in_system" or i.kind == "unknown_builtin"
    ]
    for i, info in enumerate(infos, 1):
        flag = "❌" if info in bad else "✓"
        print(f"  {flag} {i}. {info.label}")
        if info.note:
            print(f"     {info.note}")
    if bad:
        print(f"\n❌ {len(bad)} 个动作系统未注册，导入后会「无法找到此操作」。")
        sys.exit(1)
    print("\n✓ 全部动作系统可识别")
