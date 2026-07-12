"""签名：调用 macOS `shortcuts sign` 给 unsigned .shortcut 签名。"""

import argparse
import subprocess
import sys
from pathlib import Path

from .plist_utils import die


def cmd_sign(args: argparse.Namespace) -> None:
    if sys.platform != "darwin":
        die("签名仅支持 macOS（需系统自带 `shortcuts` CLI）。当前平台: " + sys.platform)
    in_path = Path(args.input)
    if not in_path.exists():
        die(f"输入文件不存在: {args.input}")
    out_path = args.output or str(in_path.with_suffix(".signed.shortcut"))
    mode = args.mode
    if mode not in ("anyone", "people-who-know-me"):
        die(f"未知签名模式: {mode}（应为 anyone 或 people-who-know-me）")
    cmd = [
        "shortcuts",
        "sign",
        "--mode",
        mode,
        "--input",
        str(in_path),
        "--output",
        out_path,
    ]
    print(f"[签名] {' '.join(cmd)}")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        die("找不到 `shortcuts` 命令（仅 macOS 12+ 自带）。")
    if r.returncode != 0:
        print(r.stdout, end="")
        print(r.stderr, end="", file=sys.stderr)
        die(
            f"签名失败 (exit {r.returncode})。常见原因：未联网(Apple 在线校验)、"
            f"输入 plist 结构不被接受、或 Apple ID 未登录。"
        )
    print(r.stdout, end="")
    sz = Path(out_path).stat().st_size if Path(out_path).exists() else 0
    print(f"[OK] 已签名: {out_path}  ({sz} 字节)")
    if getattr(args, "clean", False) and Path(out_path) != in_path:
        try:
            in_path.unlink()
            print(f"[清理] 已删除 unsigned 输入: {in_path}")
        except OSError as e:
            print(f"[清理] 删除失败: {e}", file=sys.stderr)
