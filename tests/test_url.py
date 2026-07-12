"""url 子命令测试。"""

from __future__ import annotations

import urllib.parse

import pytest

from shortcuts_toolkit.naming import InvalidNameError
from shortcuts_toolkit.url import build_run_url


def test_url_simple_name():
    assert build_run_url("mytool") == "shortcuts://run-shortcut?name=mytool"


def test_url_encodes_chinese_input():
    u = build_run_url("mytool", "你好 world")
    assert "name=mytool" in u
    assert "input=" in u
    assert "你好" not in u  # 中文不应裸出现
    # 空格 → %20，中文 → %E4%BD%A0...
    assert "%20" in u or urllib.parse.quote(" ") in u


def test_url_strips_signed_suffix():
    u = build_run_url("mytool.signed")
    assert "name=mytool" in u
    assert "signed" not in u


def test_url_no_input_param_when_none():
    u = build_run_url("mytool")
    assert "input" not in u


def test_url_rejects_invalid_name():
    with pytest.raises(InvalidNameError):
        build_run_url("记 账")
