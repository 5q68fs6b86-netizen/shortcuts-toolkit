"""url：生成已正确编码的 shortcuts://run-shortcut 调用链接（杜绝手拼 URL 出错）。

URL scheme `shortcuts://run-shortcut?name=<名>&input=<输入>`：
- name 必须 URL-safe（内部名即此），自动校验；
- input 会被 percent-encode（中文/特殊字符安全）。
"""

from __future__ import annotations

import argparse
import urllib.parse

from .naming import InvalidNameError, validate_name
from .plist_utils import die


def build_run_url(name: str, input_text: str | None = None) -> str:
    """生成已编码的 shortcuts://run-shortcut 链接。name 不合法抛 InvalidNameError。"""
    validated = validate_name(name)  # 校验 URL-safe 并去掉 .signed 后缀
    params: dict[str, str] = {"name": validated}
    if input_text is not None:
        params["input"] = input_text
    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    return f"shortcuts://run-shortcut?{query}"


def cmd_url(args: argparse.Namespace) -> None:
    try:
        url = build_run_url(args.name, args.input)
    except InvalidNameError as e:
        die(str(e))
    print(url)
