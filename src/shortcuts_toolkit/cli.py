"""CLI 子命令调度 + 往返自测(self-test)。"""

import argparse
import plistlib
import subprocess
import sys
import tempfile
from pathlib import Path

from .bookkeeping import cmd_bookkeeping
from .generator import cmd_build_rr, cmd_generate, normalize_spec
from .icloud import cmd_icloud
from .parser import (
    cmd_inspect,
    cmd_parse,
    describe_action,
    extract_actions,
    extract_workflow,
    load_plist,
)
from .signer import cmd_sign


def cmd_self_test(args: argparse.Namespace) -> None:
    print("=" * 60)
    print("自测：生成 → 解析 → inspect 往返")
    print("=" * 60)
    spec = {
        "name": "SelfTest",
        "actions": [
            {
                "identifier": "is.workflow.actions.gettext",
                "parameters": {"WFTextActionText": "你好，世界"},
            },
            {"identifier": "is.workflow.actions.showresult", "parameters": {}},
        ],
    }
    plist = normalize_spec(spec)
    with tempfile.TemporaryDirectory() as d:
        sc = Path(d) / "selftest.shortcut"
        with open(sc, "wb") as f:
            plistlib.dump(plist, f, fmt=plistlib.FMT_BINARY)
        print(
            f"[1/4] 生成 unsigned .shortcut -> {sc.name} "
            f"({sc.stat().st_size} 字节, 头={open(sc, 'rb').read(8)!r})"
        )

        data = load_plist(str(sc))
        wf = extract_workflow(data)
        actions = extract_actions(wf)
        ok_roundtrip = len(actions) == 2
        print(f"[2/4] 解析回读: 动作数={len(actions)}  往返一致={'是' if ok_roundtrip else '否'}")
        for i, a in enumerate(actions, 1):
            _, label, _ = describe_action(a)
            print(f"        {i}. {label}")
        if not ok_roundtrip:
            print("[错误] 往返不一致，生成/解析有问题。", file=sys.stderr)
            sys.exit(1)

        xml = plistlib.dumps(data, fmt=plistlib.FMT_XML).decode("utf-8")
        ok_xml = "WFWorkflowActions" in xml
        print(f"[3/4] inspect -> XML plist 合法={'是' if ok_xml else '否'}")

        print("[4/4] 签名测试 (仅 macOS):")
        if sys.platform != "darwin":
            print("        跳过（非 macOS 平台）")
        else:
            signed = Path(d) / "selftest.signed.shortcut"
            cmd = [
                "shortcuts",
                "sign",
                "--mode",
                "anyone",
                "--input",
                str(sc),
                "--output",
                str(signed),
            ]
            print(f"        运行: {' '.join(cmd)}")
            try:
                r = subprocess.run(cmd, capture_output=True, text=True)
            except FileNotFoundError:
                print("        找不到 shortcuts CLI，跳过。")
                r = None
            if r is not None:
                if r.returncode == 0 and signed.exists():
                    print(
                        f"        [通过] 签名成功 -> {signed.name} ({signed.stat().st_size} 字节)"
                    )
                else:
                    print(f"        [信息] 签名未通过 (exit {r.returncode})。")
                    out = (r.stdout + r.stderr).strip()
                    if out:
                        print("        输出:", out[:300])
                    print(
                        "        （常见原因：未联网/未登录 Apple ID/Apple 在线校验。"
                        "解析与生成功能不受影响。）"
                    )
    print("-" * 60)
    print("自测完成。生成、解析、inspect 均正常。")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="shortcuts-toolkit",
        description="快捷指令 解析·生成·签名·导入 工具链",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("parse", help="解析 .shortcut 输出可读动作清单")
    sp.add_argument("file", help=".shortcut 文件路径")
    sp.set_defaults(func=cmd_parse)

    sp = sub.add_parser("inspect", help="转成 XML plist 输出原始结构")
    sp.add_argument("file", help=".shortcut 文件路径")
    sp.set_defaults(func=cmd_inspect)

    sp = sub.add_parser("generate", help="由 JSON 规格生成 unsigned .shortcut")
    sp.add_argument("-i", "--input", required=True, help="JSON 规格文件")
    sp.add_argument("-o", "--output", required=True, help="输出 .shortcut 路径")
    sp.set_defaults(func=cmd_generate)

    sp = sub.add_parser("sign", help="用 macOS shortcuts sign 签名")
    sp.add_argument("input", help="待签名的 unsigned .shortcut")
    sp.add_argument("-o", "--output", help="签名后输出路径(默认 *.signed.shortcut)")
    sp.add_argument(
        "--mode",
        default="anyone",
        choices=["anyone", "people-who-know-me"],
        help="签名模式(默认 anyone)",
    )
    sp.set_defaults(func=cmd_sign)

    sp = sub.add_parser("icloud", help="从 iCloud 分享链接下载 .shortcut")
    sp.add_argument("url", help="iCloud 分享链接或 GUID")
    sp.add_argument("-o", "--output", help="保存路径(默认用快捷指令名)")
    sp.set_defaults(func=cmd_icloud)

    sp = sub.add_parser("build-rr", help="生成一扫「App Intent+回传」工具模板")
    sp.add_argument("--bundle-id", required=True, help="App Bundle Identifier")
    sp.add_argument("--intent-id", required=True, help="App Intent 标识符")
    sp.add_argument("--team-id", default="", help="Team Identifier(可从 codesign -dv 取)")
    sp.add_argument("--callback-url", required=True, help="结果回传 URL(POST)")
    sp.add_argument("--name", help="快捷指令名(默认 tool-<intent>)")
    sp.add_argument("--include-gettext", action="store_true", help="首步加「获取文本」")
    sp.add_argument("--client-release", default="18.0")
    sp.add_argument("--min-version", type=int, default=900)
    sp.add_argument("-o", "--output", required=True, help="输出 .shortcut 路径")
    sp.set_defaults(func=cmd_build_rr)

    sp = sub.add_parser("self-test", help="生成→解析→inspect 往返自测+签名尝试")
    sp.set_defaults(func=cmd_self_test)

    sp = sub.add_parser("bookkeeping", help="生成记账快捷指令: 固定JSON→表格/备忘录")
    sp.add_argument(
        "--save",
        default="csv",
        choices=["csv", "numbers"],
        help="保存方式：csv(追加CSV，默认) 或 numbers(追加Numbers表格行)",
    )
    sp.add_argument(
        "--keys",
        default="date,type,amount,category,note",
        help="JSON 字段键，逗号分隔(默认 date,type,amount,category,note)",
    )
    sp.add_argument("--name", default="记账", help="快捷指令名")
    sp.add_argument(
        "--csv-file",
        default="账本.csv",
        help="csv 模式: 追加的目标文件名(iCloud 云盘，不存在自动建)",
    )
    sp.add_argument(
        "--numbers-file", default="记账本.numbers", help="numbers 模式: .numbers 文件名"
    )
    sp.add_argument("--table-name", default="表单", help="numbers 模式: 表格名")
    sp.add_argument("--client-release", default="18.0")
    sp.add_argument("--min-version", type=int, default=900)
    sp.add_argument("-o", "--output", required=True, help="输出 .shortcut 路径")
    sp.set_defaults(func=cmd_bookkeeping)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
