---
name: shortcuts-toolkit
description: >
  Apple Shortcuts (.shortcut) parse / generate / sign / import toolkit.
  当用户需要解析(读懂)、生成(创建)、签名、从 iCloud 下载、或制作 Apple 快捷指令
  (Shortcuts / 快捷指令) 时调用。优先使用 shortcuts-toolkit CLI 的子命令
  (parse / generate / sign / icloud / build-rr / bookkeeping / self-test)，
  而不是手写 plist——手写极易产生「能签名但导入为空」的文件。
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
| 按动作清单生成新快捷指令 | `shortcuts-toolkit generate -i spec.json -o out.shortcut` |
| 签名（导入前必需，macOS） | `shortcuts-toolkit sign <file> -o signed.shortcut --mode anyone` |
| 从 iCloud 分享链接下载 | `shortcuts-toolkit icloud <url>` |
| 记账成品（固定 JSON→CSV） | `shortcuts-toolkit bookkeeping -o out.shortcut` |
| App Intent→POST 回传工具 | `shortcuts-toolkit build-rr --bundle-id .. --intent-id .. --callback-url .. -o out.shortcut` |
| 验证工具链 | `shortcuts-toolkit self-test` |

> 已安装则直接 `shortcuts-toolkit ...`；未安装则 `uvx shortcuts-toolkit ...`。

## 生成前必查 reference/（硬规则）

快捷指令内部格式苹果不公开，**禁止凭记忆盲写 plist**。生成任何动作前先读对应文档：

- `reference/PLIST_FORMAT.md` — 根结构【必须扁平】（`WFWorkflowActions` 在顶层，禁止包 `WFWorkflow`，否则导入为空）
- `reference/ACTIONS.md` — 427 个 WF\*Action 标识符与参数
- `reference/APPINTENTS.md` — 728 个 AppIntent（第三方/系统 App 动作）
- `reference/VARIABLES.md` — 变量引用（`￼` U+FFFC + `attachmentsByRange` + `OutputUUID`）
- `reference/CONTROL_FLOW.md` — 循环/条件/菜单（`GroupingIdentifier` + `WFControlFlowMode` 整数）
- `reference/FILTERS.md` · `reference/PARAMETER_TYPES.md` · `reference/EXAMPLES.md`

## 规格（generate 输入，简化形式）

```json
{
  "name": "我的快捷指令",
  "actions": [
    {"identifier": "is.workflow.actions.gettext", "parameters": {"WFTextActionText": "你好"}},
    {"identifier": "is.workflow.actions.showresult", "parameters": {}}
  ]
}
```

可选字段：`client_release` / `minimum_client_version` / `types` / `input_classes` / `icon{color,glyph}`。

## ⚠️ 已固化的踩坑（务必遵守）

1. **根结构扁平**：`WFWorkflowActions` 等必须在 plist 顶层；包进 `WFWorkflow` 会「签名成功但导入为空」。本工具 `generate` 已输出扁平结构。
2. **带变量的文本动作**（`WFTextActionText`）必须用包裹格式 `{Value:{string,attachmentsByRange},WFSerializationType:"WFTextTokenString"}`，否则运行时输出空文本。
3. **`WFControlFlowMode` 必须是整数**（0/1/2），写成字符串控制流失效。
4. 删除照片用 `photos` 不是 `WFInput`；截图筛选用「Is a Screenshot」布尔，不是 Media Type。

## 能力边界

- 解析/生成/下载：任意平台，无需联网。
- 签名：仅 macOS 12+（系统 `shortcuts` CLI）+ 联网（Apple 在线校验）。
- 自动静默导入：❌ iOS 安全模型硬边界，只能引导用户点 iCloud 链接。
- 解析已签名 `.shortcut`：❌ 签名后是 AEA1 加密容器；用 `icloud` 拉 unsigned 版再解析。

## 验证流程（生成后必做）

1. `shortcuts-toolkit parse <生成文件>` 确认动作链、变量引用正确。
2. `shortcuts-toolkit sign ... -o signed.shortcut`（macOS）签名成功。
3. Finder 双击 `.signed.shortcut` 导入，**确认非空**。
