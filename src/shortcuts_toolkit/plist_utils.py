"""共享工具：错误退出、plist 常量、文本截断。"""

import json
import sys
from typing import NoReturn

SIGNED_MAGIC = b"AEA1"


def die(msg: str, code: int = 1) -> NoReturn:
    print(f"[错误] {msg}", file=sys.stderr)
    sys.exit(code)


def truncate(v: object, n: int = 80) -> str:
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s if len(s) <= n else s[:n] + "…"
