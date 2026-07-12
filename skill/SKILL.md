---
name: shortcuts-toolkit
description: >
  Apple Shortcuts (.shortcut) parse / generate / sign / import toolkit.
  当用户需要解析(读懂)、生成(创建)、签名、从 iCloud 下载、或制作 Apple 快捷指令
  (Shortcuts / 快捷指令) 时调用。优先使用 shortcuts-toolkit CLI 的子命令
  (parse / inspect / preview / generate / build / sign / icloud / url / bookkeeping / build-rr / self-test)，
  而不是手写 plist——手写极易产生「能签名但导入为空」或「导入后无法找到此操作」的文件。
  内置 1155 个动作参考 (427 WF*Action + 728 AppIntent)。
allowed-tools: Bash, Read, Write
---

# Apple 快捷指令工具链 Skill

## 何时调用

当用户提到以下任何意图时，调用对应 CLI 子命令（**而非手写 plist**）：

| 意图 | 命令 |
|---|---|
| 读懂/分析 .shortcut | `shortcuts-toolkit parse <file>` |
| 看原始 plist 结构 | `shortcuts-toolkit inspect <file>` |
| **生成前预览（操作+模块+警告）** | `shortcuts-toolkit preview -i spec.json` |
| 按规格生成 unsigned | `shortcuts-toolkit generate -i spec.json -o out.shortcut` |
| **一键到正式成品（generate→sign→清理）** | `shortcuts-toolkit build -i spec.json -o out.signed.shortcut` |
| 签名（macOS，可 `--clean` 删中间文件） | `shortcuts-toolkit sign <file> -o signed.shortcut --mode anyone --clean` |
| 从 iCloud 分享链接下载 | `shortcuts-toolkit icloud <url>` |
| **生成调用链接（自动编码）** | `shortcuts-toolkit url -n <name> -i <输入>` |
| 记账成品（固定 JSON→CSV） | `shortcuts-toolkit bookkeeping -o out.shortcut` |
| App Intent→POST 回传工具 | `shortcuts-toolkit build-rr --bundle-id .. --intent-id .. --callback-url .. -o out.shortcut` |
| 验证工具链 | `shortcuts-toolkit self-test` |

> 已安装则直接 `shortcuts-toolkit ...`；未安装则 `uvx shortcuts-toolkit ...`。

## ⭐ 生成工作流（硬性流程，生成新快捷指令时必须按序，不得跳步）

1. **preview 确认** — `shortcuts-toolkit preview -i spec.json`，把输出的「操作清单 + 模块汇总 + 警告」**呈现给用户确认**。重点确认：
   - ⚠️ **第三方 App 动作**（模块显示 `App: <bundle>`）→ 用户设备必须装了对应 App，否则导入后报「无法找到此操作」。
   - ⚠️ **未知内置动作**（不在 427 清单）→ 可能拼错/过时，同样会「无法找到此操作」。
2. **规范命名** — 名字必须 URL-safe（见下「命名规则」）。不合法 CLI 会报错并给建议，**改到合法为止**。
3. **生成** — macOS 用 `shortcuts-toolkit build -i spec.json -o out/<name>.signed.shortcut`（一键 generate→sign→自动清理 unsigned 中间文件）；非 macOS 先 `generate`，再传到 macOS `sign --clean`。
4. **导入** — Finder 双击 `.signed.shortcut`，**确认非空、无红字「无法找到此操作」**。
5. **调用** — 用 `shortcuts-toolkit url -n <name> -i <输入>` 生成已编码的 `shortcuts://run-shortcut?name=...&input=...`，**禁止手拼 URL**。

## 命名规则（URL-safe，硬约束）

名字 = 快捷指令内部名（`WFWorkflowName`）= URL scheme 的 `name` 参数，三者是同一个，**必须 URL-safe**。

- **只允许** `[A-Za-z0-9_-]`。**禁止**空格、中文、`.` `&` `=` `+` `/` `?` `#` `%` 等特殊字符。
- **语义清晰英文**，不要拼音：`bookkeeping`（不要 `jizhang`）、`voice_bookkeeping`、`tool_<intent>`。
- **原因**：URL scheme `shortcuts://run-shortcut?name=<名字>` 的 name 就是内部名；空格/中文/特殊字符会破坏 URL 或需编码、且不同客户端容忍度不一（参见少数派/Apple 文档）。
- CLI（`generate`/`build`/`bookkeeping`/`url`）会自动校验，不合法报错并给 slug 建议。
- 名字里不要带 `.signed`（那是文件后缀，CLI 会自动剥离）。

## 生成前必查 reference/（硬规则）

快捷指令内部格式苹果不公开，**禁止凭记忆盲写 plist**。生成任何动作前先读对应文档：

- `reference/PLIST_FORMAT.md` — 根结构【必须扁平】（`WFWorkflowActions` 在顶层，禁止包 `WFWorkflow`，否则导入为空）
- `reference/ACTIONS.md` — 427 个 WF\*Action 标识符与参数
- `reference/APPINTENTS.md` — 728 个 AppIntent（系统/第三方 App 动作）
- `reference/VARIABLES.md` — 变量引用（`￼` U+FFFC + `attachmentsByRange` + `OutputUUID`）
- `reference/CONTROL_FLOW.md` — 循环/条件/菜单（`GroupingIdentifier` + `WFControlFlowMode` 整数）
- `reference/FILTERS.md` · `reference/PARAMETER_TYPES.md` · `reference/EXAMPLES.md`

## 规格（generate/build 输入，简化形式）

```json
{
  "name": "my_shortcut",
  "actions": [
    {"identifier": "is.workflow.actions.gettext", "parameters": {"WFTextActionText": "你好"}},
    {"identifier": "is.workflow.actions.showresult", "parameters": {}}
  ]
}
```

可选字段：`client_release` / `minimum_client_version` / `types` / `input_classes` / `icon{color,glyph}`。

## ⚠️ 已固化的踩坑（务必遵守）

1. **根结构扁平**：`WFWorkflowActions` 等必须在 plist 顶层；包进 `WFWorkflow` 会「签名成功但导入为空」。本工具 `generate`/`build` 已输出扁平结构。
2. **带变量的文本动作**（`WFTextActionText`）必须用包裹格式 `{Value:{string,attachmentsByRange},WFSerializationType:"WFTextTokenString"}`，否则运行时输出空文本。
3. **`WFControlFlowMode` 必须是整数**（0/1/2），写成字符串控制流失效。
4. 删除照片用 `photos` 不是 `WFInput`；截图筛选用「Is a Screenshot」布尔，不是 Media Type。
5. **导入后「无法找到此操作」** = 动作 identifier 拼错/过时，或第三方 App 没装。生成前用 `preview` 提前发现（会标红第三方/未知动作）。

## 能力边界

- 解析/生成/下载/预览/编码 URL：任意平台，无需联网。
- 签名：仅 macOS 12+（系统 `shortcuts` CLI）+ 联网（Apple 在线校验）。
- 自动静默导入：❌ iOS 安全模型硬边界，只能引导用户点 iCloud 链接。
- 解析已签名 `.shortcut`：❌ 签名后是 AEA1 加密容器；用 `icloud` 拉 unsigned 版再解析。
- **运行时行为验证**：❌ headless `shortcuts run` 传文件对象、交互动作受限，测不准；只能靠 `parse`（结构）+ `sign`（签名）+ 真机/URL scheme 文本输入运行。
