"""从 iCloud 分享链接下载 unsigned .shortcut。"""

import argparse
import json
import re
import urllib.request

from .plist_utils import die


def extract_guid(url: str) -> str:
    m = re.search(r"icloud\.com/shortcuts/([A-Za-z0-9]+)", url)
    if m:
        return m.group(1)
    m = re.search(r"\b([0-9a-fA-F]{8,})\b", url)
    return m.group(1) if m else url.strip()


def cmd_icloud(args: argparse.Namespace) -> None:
    guid = extract_guid(args.url)
    api = f"https://www.icloud.com/shortcuts/api/records/{guid}"
    print(f"[下载] 请求 {api}")
    try:
        with urllib.request.urlopen(api, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        die(f"获取 iCloud 记录失败: {e}\n(api/records 为非官方接口，可能变动/限流)")
    try:
        fields = payload["fields"]
        name = fields.get("name", {}).get("value", "(未知)")
        dl = fields["shortcut"]["value"]["downloadURL"]
    except (KeyError, TypeError):
        die(f"返回结构异常，未找到 downloadURL。原始:\n{json.dumps(payload)[:400]}")
    print(f"[下载] 名称: {name}")
    print(f"[下载] 地址: {dl}")
    out_path = args.output or f"{name}.shortcut"
    try:
        with urllib.request.urlopen(dl, timeout=60) as resp:
            data = resp.read()
    except Exception as e:
        die(f"下载 .shortcut 失败: {e}")
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"[OK] 已保存: {out_path}  ({len(data)} 字节)")
