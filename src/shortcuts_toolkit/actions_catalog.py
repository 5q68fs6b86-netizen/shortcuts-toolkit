"""动作目录：解析 reference/ 建标识符→模块映射，用于 preview（生成前列出操作+模块）与有效性校验。

分类规则：
- 内置 WF*Action（is.workflow.actions.<name>）：查 ACTIONS.md 的 427 清单与 16 类别
- 系统 AppIntent（appintentexecution 包装）：查 APPINTENTS.md 的 728 清单
- 第三方 App 动作（<bundle>.<intent>）：标注来源 App，提示需设备安装
- 不在任何清单：警告可能拼错/过时
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from .actions_cn import ACTION_CN

_BUILTIN_PREFIX = "is.workflow.actions."
_APPINTENT_WRAPPER = "is.workflow.actions.appintentexecution"


@dataclass(frozen=True)
class ActionInfo:
    identifier: str
    label: str  # 可读名
    module: str  # 类别 / 来源 App（"模块"）
    kind: str  # builtin | system_appintent | third_party | unknown_builtin | unknown_appintent
    source_app: str | None
    note: str  # 提示/警告


def _find_reference_dir() -> Path | None:
    env = os.environ.get("SHORTCUTS_TOOLKIT_REFERENCE")
    candidates: list[Path] = []
    if env:
        candidates.append(Path(env))
    candidates.append(Path.cwd() / "reference")
    here = Path(__file__).resolve()
    # editable install: src/shortcuts_toolkit/x.py -> 项目根 = parent.parent.parent
    candidates.append(here.parent.parent.parent / "reference")
    candidates.append(here.parent.parent / "reference")
    for c in candidates:
        if (c / "ACTIONS.md").exists():
            return c
    return None


def _sections_by_h2(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for sec in re.split(r"(?m)^##\s+", text):
        lines = sec.splitlines()
        if not lines:
            continue
        out[lines[0].strip().lower()] = sec
    return out


def _parse_actions_md(text: str) -> tuple[dict[str, str], set[str]]:
    categories: dict[str, str] = {}
    all_names: set[str] = set()
    secs = _sections_by_h2(text)
    cat_section = next((v for k, v in secs.items() if k.startswith("actions by category")), "")
    list_section = next(
        (v for k, v in secs.items() if k.startswith("complete identifier list")), ""
    )

    current_cat: str | None = None
    for line in cat_section.splitlines():
        m = re.match(r"^###\s+(.+?)\s*$", line)
        if m:
            current_cat = m.group(1).strip()
            continue
        if current_cat:
            for tok in re.findall(r"`([a-z][a-z0-9.]*)`", line):
                categories.setdefault(tok, current_cat)
            for tok in re.findall(r"\|\s*`?([a-z][a-z0-9.]*)`?\s*\|", line):
                if tok and tok not in {"identifier", "class", "description"}:
                    categories.setdefault(tok, current_cat)

    in_block = False
    for line in list_section.splitlines():
        if line.strip().startswith("```"):
            in_block = not in_block
            continue
        if in_block:
            for tok in re.findall(r"([a-z][a-z0-9.]*)", line):
                all_names.add(tok)
    all_names |= set(categories)
    return categories, all_names


def _parse_appintents_md(text: str) -> tuple[dict[str, str], set[str]]:
    categories: dict[str, str] = {}
    all_names: set[str] = set()
    secs = _sections_by_h2(text)
    cat_section = next((v for k, v in secs.items() if k.startswith("appintents by category")), "")

    current_cat: str | None = None
    for line in cat_section.splitlines():
        m = re.match(r"^###\s+(.+?)\s*(?:\(\d+\))?\s*$", line)
        if m:
            current_cat = m.group(1).strip()
            continue
        if current_cat:
            for tok in re.findall(r"`?([A-Z][A-Za-z0-9]+Intent)`?", line):
                categories.setdefault(tok, current_cat)
                all_names.add(tok)
    return categories, all_names


@lru_cache(maxsize=1)
def get_catalog() -> tuple[dict[str, str], set[str], dict[str, str], set[str]]:
    """返回 (内置短名→类别, 内置短名全集, AppIntent名→类别, AppIntent名全集)。"""
    ref = _find_reference_dir()
    cn_names = {k[len(_BUILTIN_PREFIX) :] for k in ACTION_CN if k.startswith(_BUILTIN_PREFIX)}
    if ref is None:
        return {}, cn_names, {}, set()
    cat, names = _parse_actions_md((ref / "ACTIONS.md").read_text("utf-8"))
    acat, anames = _parse_appintents_md((ref / "APPINTENTS.md").read_text("utf-8"))
    names |= cn_names
    return cat, names, acat, anames


def classify_action(identifier: str, params: dict[str, Any] | None = None) -> ActionInfo:
    params = params or {}
    cat, names, acat, anames = get_catalog()

    if identifier == _APPINTENT_WRAPPER:
        desc = params.get("AppIntentDescriptor") or {}
        intent_id = desc.get("AppIntentIdentifier", "?") if isinstance(desc, dict) else "?"
        bundle = desc.get("BundleIdentifier", "?") if isinstance(desc, dict) else "?"
        if intent_id in anames:
            return ActionInfo(
                identifier,
                f"系统动作: {intent_id}",
                acat.get(intent_id, "系统集成"),
                "system_appintent",
                bundle,
                "",
            )
        return ActionInfo(
            identifier,
            f"AppIntent: {intent_id}",
            "第三方/未知",
            "unknown_appintent",
            bundle,
            f"AppIntent「{intent_id}」不在已知清单，需设备支持",
        )

    if identifier.startswith(_BUILTIN_PREFIX):
        short = identifier[len(_BUILTIN_PREFIX) :]
        cn = ACTION_CN.get(identifier)
        label = f"{cn}（{identifier}）" if cn else identifier
        if short in names:
            return ActionInfo(
                identifier, label, cat.get(short, "内置（未分类）"), "builtin", None, ""
            )
        return ActionInfo(
            identifier,
            label,
            "未知内置动作",
            "unknown_builtin",
            None,
            f"内置动作「{short}」不在已知清单，可能拼错/过时",
        )

    if "." in identifier:
        bundle, intent = identifier.rsplit(".", 1)
        cn = ACTION_CN.get(identifier)
        label = f"{cn}（{identifier}）" if cn else f"第三方动作: {intent}（{identifier}）"
        return ActionInfo(
            identifier,
            label,
            f"App: {bundle}",
            "third_party",
            bundle,
            f"需目标设备装有 App「{bundle}」才可用",
        )

    return ActionInfo(
        identifier, identifier, "未知", "unknown_builtin", None, "无法识别的动作标识符"
    )
