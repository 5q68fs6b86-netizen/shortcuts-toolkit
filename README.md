# shortcuts-toolkit

> 🇨🇳 中文 · 🇬🇧 [English](#english)

[![CI](https://github.com/moonhorsemmy/shortcuts-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/moonhorsemmy/shortcuts-toolkit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Apple 快捷指令（`.shortcut`）的**解析 / 生成 / 签名 / 导入**命令行工具链 —— 纯 Python 标准库实现（零第三方依赖），并附带一份可被主流 AI 智能体直接调用的 **Agent Skill**。

把「快捷指令」当成**可读、可造、可签、可分发**的对象来处理。

> 快捷指令本质是**二进制 plist**，核心字段 `WFWorkflowActions`（动作数组）。本工具围绕它实现解析 / 生成 / 签名 / 下载。

---

## ✨ 特性

- **解析** `parse` / `inspect`：`.shortcut` → 可读动作清单 / 原始 XML plist
- **生成** `generate` / `build-rr` / `bookkeeping`：JSON 规格 → unsigned `.shortcut`（**扁平结构**，确保导入非空）
- **签名** `sign`：macOS `shortcuts sign`（导入前必需）
- **下载** `icloud`：iCloud 分享链接 → unsigned `.shortcut`
- **实测成品**：记账快捷指令（固定 JSON → CSV/Numbers）
- **AI Skill**：一份 `SKILL.md`，Claude Code / GitHub Copilot / Cursor / Codex / Kilo / Antigravity 等 agent 自动调用 CLI

## 🆚 与 erik-agens/shortcuts-skill 的区别

|  | erik-agens/shortcuts-skill | **shortcuts-toolkit** |
|---|---|---|
| 形态 | 纯知识库（SKILL.md）让 agent 手写 plist | 知识库 **+ 完整 CLI** |
| 签名 / 导入 | 无 | ✅ `sign` + 导入流程 |
| 成品模板 | 无 | ✅ 记账 / 工具回传 |
| agent 调用 | 手写 plist 易出错 | ✅ 直接调命令 |

`reference/` 源自该项目（MIT 署名），见 [`reference/NOTICE.md`](reference/NOTICE.md)。

## 📦 安装

```bash
# 直接运行（推荐，无需安装）
uvx shortcuts-toolkit --help

# 或安装
pip install shortcuts-toolkit
# uv add shortcuts-toolkit
```

**环境**：Python ≥ 3.10；签名额外需 macOS 12+（系统自带 `shortcuts` CLI）+ 联网。解析/生成/下载任意平台可用、无需联网。

## 🚀 快速开始

```bash
# 1) 自测：生成 → 解析 → inspect 往返 + macOS 签名尝试
uvx shortcuts-toolkit self-test

# 2) 由 JSON 规格生成 unsigned .shortcut
uvx shortcuts-toolkit generate -i templates/simple_example.json -o out/example.shortcut

# 3) 解析它
uvx shortcuts-toolkit parse out/example.shortcut

# 4) 签名（macOS）
uvx shortcuts-toolkit sign out/example.shortcut -o out/example.signed.shortcut --mode anyone

# 5) 记账成品（固定 JSON → CSV，已实测）
uvx shortcuts-toolkit bookkeeping -o out/记账.shortcut
```

简化规格示例：
```json
{
  "name": "我的快捷指令",
  "actions": [
    { "identifier": "is.workflow.actions.gettext",
      "parameters": { "WFTextActionText": "你好" } },
    { "identifier": "is.workflow.actions.showresult", "parameters": {} }
  ]
}
```

## 🤖 作为 AI Agent Skill 使用

本仓库附带 `skill/SKILL.md`（带 YAML frontmatter，遵循跨 agent 标准）。各平台安装：

| 平台 | 安装方式 |
|---|---|
| Claude Code | `cp -r skill/ ~/.claude/skills/shortcuts-toolkit` |
| GitHub Copilot | `cp -r skill/ .github/skills/shortcuts-toolkit` |
| Cursor | `cp -r skill/ .cursor/rules/shortcuts-toolkit` |
| Codex CLI | `cp -r skill/ .codex/skills/shortcuts-toolkit` |
| Kilo | `cp -r skill/ .kilo/skills/shortcuts-toolkit` |
| OpenCode | `cp -r skill/ .opencode/skills/shortcuts-toolkit`（也兼容 `~/.config/opencode/skills/`、`.claude/skills/`、`.agents/skills/`） |
| 通用 | `cp skill/SKILL.md AGENTS.md`（30+ agent 读 AGENTS.md，含 Gemini CLI/Jules/Devin/Aider） |

安装后，agent 在你提到「快捷指令 / 解析 / 生成 / 签名」时会自动调用 `shortcuts-toolkit` CLI（解析/生成/签名/导入），**无需手写 plist**。

> 一键安装（跨工具）：`npx skills add https://github.com/moonhorsemmy/shortcuts-toolkit`

## 💬 用于 ChatGPT / Gemini（网页版）

本工具是 CLI + 文本知识库，网页版 GPT/Gem 没有 bash，但可这样用：

1. 复制 `skill/SKILL.md` 全文 → 作为 **Custom GPT** 的 Instructions（或 Gemini Gem 的指令）。
2. 让它按你的需求**生成 JSON 规格**（动作数组），你把 JSON 存为文件。
3. 在本地终端跑 `uvx shortcuts-toolkit generate -i spec.json -o out.shortcut` → `sign` → 导入。

## 📚 子命令

| 命令 | 作用 |
|---|---|
| `parse <file>` | 解析 .shortcut → 可读动作清单（常见动作映射中文） |
| `inspect <file>` | 转成 XML plist 查看原始结构 |
| `preview -i <spec.json>` | ⭐ 生成前预览：操作清单 + 模块 + 警告（防导入后「无法找到此操作」） |
| `generate -i <spec.json> -o <out>` | 由 JSON 规格生成 unsigned .shortcut |
| `build -i <spec.json> -o <out>` | ⭐ 一键 generate→sign→清理中间文件 |
| `sign <file> -o <out> [--mode] [--clean]` | macOS 签名；`--clean` 签后删 unsigned |
| `url -n <name> [-i <input>]` | 生成已编码的 shortcuts://run-shortcut 调用链接 |
| `icloud <url\|GUID>` | 从 iCloud 分享链接下载 unsigned .shortcut |
| `build-rr --bundle-id ...` | 生成「运行 App Intent → POST 回传」工具模板 |
| `bookkeeping --keys ... -o <out>` | 生成记账快捷指令（JSON → CSV/Numbers） |
| `self-test` | 生成→解析→inspect 往返自测 + 签名尝试 |

**生成前必查 `reference/`**（动作标识符/参数/变量/控制流，逆向自苹果未公开格式）：`reference/ACTIONS.md`（427 WF*Action）、`reference/APPINTENTS.md`（728 AppIntent）、`reference/PLIST_FORMAT.md`（**根结构必须扁平**）、`reference/VARIABLES.md`、`reference/CONTROL_FLOW.md`。

## 🏷️ 命名规则（URL-safe，硬约束）

名字（=内部名 `WFWorkflowName` = URL scheme 的 `name` 参数，三者同一个）必须 **URL-safe**：只允许 `[A-Za-z0-9_-]`，禁空格/中文/特殊字符（`. & = + /` 等）。

原因：`shortcuts://run-shortcut?name=<名字>` 里中文/空格/特殊字符会破坏 URL 或需编码、不同客户端容忍度不一（[Apple 文档](https://support.apple.com/zh-cn/guide/shortcuts/apd624386f42/ios)）。CLI 自动校验，不合法报错并给 slug 建议。

## ⚙️ 生成工作流（推荐顺序）

1. `shortcuts-toolkit preview -i spec.json` — 确认动作清单、模块、第三方/未知警告
2. `shortcuts-toolkit build -i spec.json -o out/<name>.signed.shortcut` — macOS 一键到正式成品（generate→sign→清理）
3. Finder 双击 `.signed.shortcut` 导入，确认非空、无「无法找到此操作」
4. `shortcuts-toolkit url -n <name> -i <输入>` — 生成已编码的调用链接（禁止手拼）

## ⚠️ 能力边界

| 能力 | 支持 | 说明 |
|---|---|---|
| 生成 unsigned `.shortcut` | ✅ | 写二进制 plist（扁平结构） |
| 解析 unsigned `.shortcut` | ✅ | 读 plist + 动作清单 |
| 签名（macOS） | ✅ | `shortcuts sign` |
| 签名（Linux） | ❌ | 另用 [shortcut-sign](https://github.com/0xilis/shortcut-sign) |
| **自动静默导入** | ❌ | iOS 安全模型硬边界；只能引导用户点 iCloud 链接 |
| **解析已签名 `.shortcut`** | ❌ | 签名后是 AEA1 加密容器，连 `plutil` 也读不出；用 `icloud` 拉 unsigned 版再解析 |

### 关键踩坑（已固化）
- `WFWorkflowActions` 等 `WFWorkflow*` 键必须在 plist **顶层**（**不能**包 `WFWorkflow`），否则 `shortcuts sign` 仍签名成功但**导入为空快捷指令**。
- 带变量的「文本」动作必须用包裹格式 `{Value:{string,attachmentsByRange},WFSerializationType:"WFTextTokenString"}`，否则运行时输出空文本。

## 📁 目录结构

```
shortcuts-toolkit/
├── src/shortcuts_toolkit/   CLI 实现（parser/generator/signer/icloud/bookkeeping/cli）
├── skill/SKILL.md           AI Agent Skill（跨平台）
├── reference/               格式文档（MIT，源自 erik-agens/shortcuts-skill）
├── templates/               JSON 规格示例
├── tests/                   pytest 套件
└── AGENTS.md                30+ agent 项目上下文
```

## 📄 License

MIT © moonhorsemmy。`reference/` 文档 MIT © openclaw/skills contributors (erik-agens)，见 `reference/LICENSE`。

## 🙏 致谢

- [erik-agens/shortcuts-skill](https://github.com/openclaw/skills/tree/main/skills/erik-agens/shortcuts-skill)（reference/ 格式文档来源）
- [0xdevalias · Decompile Apple Shortcuts](https://gist.github.com/0xdevalias/27d9aea9529be7b6ce59055332a94477)
- [zachary7829 · Shortcuts File Format](https://zachary7829.github.io/blog/shortcuts/fileformat)
- [0xilis/shortcut-sign](https://github.com/0xilis/shortcut-sign)

---

## English

A CLI toolkit for **Apple Shortcuts (`.shortcut`)** — parse / generate / sign / import — built on the Python standard library only (no third-party deps), plus an **AI Agent Skill** so agents like Claude Code, GitHub Copilot, Cursor, Codex, and Kilo can drive it directly.

**Why vs `erik-agens/shortcuts-skill`**: that project is a pure knowledge base (an `SKILL.md` telling agents to hand-write plist). `shortcuts-toolkit` is that knowledge base **plus a complete CLI** — agents call commands instead of hand-writing error-prone plist, and you get signing, iCloud download, and ready-made templates (bookkeeping, App-Intent callback).

**Install**: `uvx shortcuts-toolkit --help` · `pip install shortcuts-toolkit`

**As an agent skill**: copy `skill/` into your agent's skill dir (`.claude/skills/`, `.github/skills/`, `.cursor/rules/`, `.codex/skills/`, `.kilo/skills/`) or `npx skills add https://github.com/moonhorsemmy/shortcuts-toolkit`. See the Chinese section above for full details and the ChatGPT/Gemini web usage recipe.

**License**: MIT. The `reference/` docs are MIT © openclaw/skills contributors (erik-agens).
