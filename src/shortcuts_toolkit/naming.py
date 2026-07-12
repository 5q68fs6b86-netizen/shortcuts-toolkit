"""快捷指令命名规范：URL-safe 校验与 slug 转换。

URL scheme `shortcuts://run-shortcut?name=<名字>` 的 name 就是内部名（WFWorkflowName），
故内部名必须 URL-safe：只允许 [A-Za-z0-9_-]，禁止空格/中文/特殊字符。
社区最佳实践：用语义清晰的英文（非拼音乱 slug）。
"""

from __future__ import annotations

import re

_SAFE_RE = re.compile(r"^[A-Za-z0-9_-]+$")
_INVALID_RE = re.compile(r"[^A-Za-z0-9_-]+")
_SIGNED_SUFFIX = ".signed"


class InvalidNameError(ValueError):
    """名字不符合 URL-safe 规范。"""

    def __init__(self, name: str, suggestion: str | None = None) -> None:
        msg = f"名字「{name}」不合法：URL scheme 要求只含 [A-Za-z0-9_-]（禁空格/中文/特殊字符）。"
        if suggestion:
            msg += f" 建议改为：{suggestion}"
        else:
            msg += " 请用语义清晰的英文重命名。"
        super().__init__(msg)
        self.name = name
        self.suggestion = suggestion


def is_valid_name(name: str) -> bool:
    """名字是否 URL-safe 合法（非空且只含 [A-Za-z0-9_-]）。"""
    return bool(name) and bool(_SAFE_RE.match(name))


def slugify(name: str) -> str:
    """把任意名字尽力转成 URL-safe slug：非 ASCII（含中文）丢弃，非法字符段替为单个 _。

    注意：中文会被丢弃（slug 无法表达中文语义）——此时应提示人工起英文名。
    """
    ascii_only = name.encode("ascii", "ignore").decode("ascii")
    if ascii_only.endswith(_SIGNED_SUFFIX):
        ascii_only = ascii_only[: -len(_SIGNED_SUFFIX)]
    slug = _INVALID_RE.sub("_", ascii_only)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug.lower()


def validate_name(name: str) -> str:
    """校验并返回清理后的合法名字（去掉 `.signed` 后缀）；不合法抛 InvalidNameError（含建议）。"""
    if not name:
        raise InvalidNameError(name, "名字不能为空")
    cleaned = name[: -len(_SIGNED_SUFFIX)] if name.endswith(_SIGNED_SUFFIX) else name
    if is_valid_name(cleaned):
        return cleaned
    suggestion = slugify(name)
    raise InvalidNameError(name, suggestion or None)
