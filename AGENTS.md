# AGENTS.md — shortcuts-toolkit

> 给 AI agent（Claude Code / Codex / Copilot / Cursor / Kilo 等）的硬性约定。
> 这是**代码项目**：`src/shortcuts_toolkit/` 是 CLI 实现，`reference/` 是格式参考，`skill/SKILL.md` 是 agent 调用说明。

## 核心约定：生成前必读 reference/

**每次生成、改写、或排查快捷指令时，必须先查阅 `reference/` 下的相关文档，确认格式无误后再动手。** 禁止凭记忆盲写 plist——快捷指令内部格式苹果不公开，盲写极易产生「能签名但导入为空 / 动作不生效」的文件。

### 强制查阅顺序
1. **任何生成动作前** → 读 `reference/PLIST_FORMAT.md` 确认**根结构扁平**（`WFWorkflowActions` 在顶层，**禁止**包 `WFWorkflow`，否则导入为空）。
2. **用具体动作时** → 查 `reference/ACTIONS.md`（427 个 WF\*Action）或 `reference/APPINTENTS.md`（728 个 AppIntent）确认标识符与参数键名。
3. **连接变量/输出时** → 查 `reference/VARIABLES.md`（`￼` U+FFFC 占位 + `attachmentsByRange` + `OutputUUID` + `WFSerializationType`）。
4. **用循环/条件/菜单时** → 查 `reference/CONTROL_FLOW.md`（`GroupingIdentifier` + `WFControlFlowMode` 整数 0/1/2）。
5. **用查找/筛选时** → 查 `reference/FILTERS.md`。
6. **不确定参数类型时** → 查 `reference/PARAMETER_TYPES.md`。

### 已踩的坑（务必避免）
- ❌ 把动作包在 `WFWorkflow` 里 → `shortcuts sign` 仍签名成功，但**导入为空快捷指令**。
- ❌ `WFControlFlowMode` 写成字符串 → 控制流失效（必须 `<integer>`）。
- ❌ 删除照片用 `WFInput` → 应该用 `photos`（小写）。
- ❌ 截图筛选用 `Media Type=Screenshot` → 应该用 `Is a Screenshot` 布尔过滤。

### ⭐ 实测验证过的关键格式
1. **根结构扁平**：`WFWorkflowActions` 在顶层，不包 `WFWorkflow`。
2. **带变量的文本动作**（`WFTextActionText`）必须用包裹格式 `{Value:{string,attachmentsByRange},WFSerializationType:"WFTextTokenString"}`，否则运行时产出空文本。
3. `detect.dictionary` + `getvalueforkey` 的 `WFInput` 用 `WFTextTokenAttachment` 正常工作。
4. `file.append` 的内容走 `WFInput` 且必须是 `WFTextTokenString`（把记录行内嵌），不是 `WFTextTokenAttachment`。

## 工具运行规范
- CLI 入口：`shortcuts-toolkit <子命令>`（开发时 `uv run shortcuts-toolkit ...`）。
- 纯标准库，无运行时第三方依赖；开发依赖（pytest/ruff/mypy）用 **uv + 国内源**（清华，见 `pyproject.toml` `[tool.uv]`）。
- 签名：macOS 用 `shortcuts sign --mode anyone`；非 macOS 另用开源 `shortcut-sign`（本工具不含）。

## 构建 / 测试 / 质量门
```bash
uv sync                                    # 安装依赖
uv run pytest -q                           # 测试（24 用例）
uv run ruff check . && uv run ruff format --check . && uv run mypy   # 质量门
uv run shortcuts-toolkit self-test         # 端到端自测（含 macOS 签名）
```

## Skill 分发
- canonical：`skill/SKILL.md`
- 安装到本机各 agent 平台：`make install`（见 `Makefile`）

## 生成工作流 + 命名规则（硬约束）
1. **preview 确认**：`shortcuts-toolkit preview -i spec.json`，把「操作+模块+警告」呈现给用户确认。第三方 App 动作 / 未知内置动作会导致导入后「无法找到此操作」，必须提前发现。
2. **URL-safe 命名**：名字必须 `[A-Za-z0-9_-]`（禁空格/中文/特殊字符/拼音），因为 URL scheme 的 `name` 就是内部名。不合法 CLI 报错并给建议。
3. **build 一键**：`shortcuts-toolkit build -i spec.json -o out/<name>.signed.shortcut`（generate→sign→自动清理 unsigned）；或 `generate` + `sign --clean`。
4. **调用**：用 `shortcuts-toolkit url -n <name> -i <输入>` 生成调用链接，**禁止手拼 URL**。

## 验证流程（生成后必做）
1. `shortcuts-toolkit parse <生成文件>` — 确认动作链、变量引用正确。
2. `shortcuts-toolkit sign <文件> -o <signed> --mode anyone` — macOS 签名成功。
3. Finder 双击 `.signed.shortcut` 导入，**确认非空**。

## 文档来源与版权
- `reference/` 缓存自 [openclaw/skills · shortcuts-skill](https://github.com/openclaw/skills/tree/main/skills/erik-agens/shortcuts-skill)（作者 erik-agens，MIT，见 `reference/LICENSE` / `reference/NOTICE.md`）。社区逆向整理，**非苹果官方**；系统更新后格式可能变动。
