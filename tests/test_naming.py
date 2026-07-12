"""naming（URL-safe 命名校验）测试。"""

from __future__ import annotations

import pytest

from shortcuts_toolkit.naming import (
    InvalidNameError,
    is_valid_name,
    slugify,
    validate_name,
)

# ---------- is_valid_name ----------


@pytest.mark.parametrize("name", ["bookkeeping", "voice_bookkeeping", "tool-1", "A1_b-2"])
def test_is_valid_name_good(name):
    assert is_valid_name(name)


@pytest.mark.parametrize("name", ["", "记账", "a b", "a.b", "a+b", "a/b", "a#b", "account.signed"])
def test_is_valid_name_bad(name):
    assert not is_valid_name(name)


# ---------- slugify ----------


def test_slugify_spaces_to_underscore():
    assert slugify("voice bookkeeping") == "voice_bookkeeping"


def test_slugify_lowercases():
    assert slugify("Bookkeeping") == "bookkeeping"


def test_slugify_special_chars():
    assert slugify("a.b") == "a_b"
    assert slugify("a+b/c") == "a_b_c"


def test_slugify_drops_chinese():
    # 中文被丢弃 → 空
    assert slugify("记账") == ""


def test_slugify_strips_signed_suffix():
    assert slugify("account.signed") == "account"


def test_slugify_collapses_repeats():
    assert slugify("a---b") == "a---b"  # 连字符合法，保留
    assert slugify("a...b") == "a_b"  # 非法点合并为单 _


# ---------- validate_name ----------


def test_validate_name_ok():
    assert validate_name("bookkeeping") == "bookkeeping"


def test_validate_name_strips_signed():
    assert validate_name("account.signed") == "account"


def test_validate_name_rejects_empty():
    with pytest.raises(InvalidNameError):
        validate_name("")


def test_validate_name_rejects_chinese_with_suggestion():
    with pytest.raises(InvalidNameError) as ei:
        validate_name("记账")
    # 中文无 ASCII → suggestion 为空，提示用英文
    assert "英文" in str(ei.value)


def test_validate_name_rejects_spaces_with_slug_suggestion():
    with pytest.raises(InvalidNameError) as ei:
        validate_name("Voice Bookkeeping")
    assert ei.value.suggestion == "voice_bookkeeping"


def test_validate_name_rejects_dot():
    with pytest.raises(InvalidNameError):
        validate_name("a.b")
