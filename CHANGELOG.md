# Changelog

本文件记录 shortcuts-toolkit 的所有显著变更。格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [0.1.0] - 2026-07-12

### Added
- CLI 入口 `shortcuts-toolkit`（pyproject `[project.scripts]`），8 个子命令：
  - `parse` / `inspect`：解析 .shortcut 为可读动作清单 / XML plist
  - `generate`：JSON 规格 → unsigned .shortcut（扁平结构）
  - `sign`：macOS `shortcuts sign` 签名
  - `icloud`：从 iCloud 分享链接下载 unsigned .shortcut
  - `build-rr`：生成「运行 App Intent → POST 回传」工具模板
  - `bookkeeping`：记账成品（固定 JSON → CSV/Numbers，已实测）
  - `self-test`：生成→解析→inspect 往返自测 + 签名尝试
- 包化结构（`src/shortcuts_toolkit/`，8 模块拆分，纯标准库）
- pytest 测试套件（24 用例，覆盖 normalize_spec/解析/动作描述/GUID/记账规格/往返/边界）
- 质量门：ruff（check + format）+ mypy + py.typed marker
- GitHub Actions：`ci.yml`（macOS/ubuntu × Python 3.10–3.13）+ `publish.yml`（Trusted Publisher）
- AI Agent Skill（`skill/SKILL.md`，跨平台 SKILL.md 标准）+ `Makefile` 一键安装到各平台
- `reference/` 格式文档（1155 动作：427 WF\*Action + 728 AppIntent，源自 erik-agens/shortcuts-skill，MIT 署名）
- 双语 README（中文为主 + 英文摘要），含 ChatGPT/Gemini 网页用法
- `AGENTS.md`（30+ agent 项目上下文）+ `CLAUDE.md`（@AGENTS.md import）
