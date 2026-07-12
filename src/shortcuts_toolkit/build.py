"""build：一键工作流 generate → sign → 只留正式成品（unsigned 中间文件自动清理）。"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from .generator import normalize_spec, write_shortcut
from .naming import InvalidNameError, validate_name
from .plist_utils import die


def cmd_build(args: argparse.Namespace) -> None:
    spec_path = Path(args.input)
    if not spec_path.exists():
        die(f"规格文件不存在: {args.input}")
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    try:
        spec["name"] = validate_name(spec.get("name", ""))
    except InvalidNameError as e:
        die(str(e))
    plist = normalize_spec(spec)
    name = spec["name"]
    final_out = Path(args.output)

    if sys.platform == "darwin":
        # unsigned 写临时目录，签名到 final_out，临时目录退出即清理
        with tempfile.TemporaryDirectory() as d:
            unsigned = Path(d) / f"{name}.shortcut"
            write_shortcut(plist, str(unsigned))
            cmd = [
                "shortcuts",
                "sign",
                "--mode",
                args.mode,
                "--input",
                str(unsigned),
                "--output",
                str(final_out),
            ]
            print(f"[build] 签名: {' '.join(cmd)}")
            try:
                r = subprocess.run(cmd, capture_output=True, text=True)
            except FileNotFoundError:
                die("找不到 `shortcuts` 命令（仅 macOS 12+ 自带）。")
            if r.returncode != 0:
                print(r.stdout, end="")
                print(r.stderr, end="", file=sys.stderr)
                die(f"签名失败 (exit {r.returncode})。")
            print(r.stdout, end="")
        sz = final_out.stat().st_size if final_out.exists() else 0
        print(f"[OK] 正式快捷指令(已签名): {final_out}  ({sz} 字节)")
        print("     (unsigned 中间文件已随临时目录自动清理)")
    else:
        write_shortcut(plist, str(final_out))
        print(f"[OK] 已生成 unsigned: {final_out}  (非 macOS，未签名)")
        print("     签名需 macOS：传到 macOS 后跑 `shortcuts-toolkit sign <file> --clean`")
