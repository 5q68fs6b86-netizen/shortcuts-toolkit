# Contributing to shortcuts-toolkit

感谢你的贡献！这个项目欢迎 PR（修 bug、加动作映射、补测试、改文档）。

## 开发流程

```bash
git clone <fork-url> && cd shortcuts-toolkit
uv sync                       # 安装依赖（pytest/ruff/mypy，走清华源）
```

改代码后，提交前确保质量门全绿：

```bash
make check                    # = ruff check + format --check + mypy + pytest
# 或单独：
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest -q
```

端到端自测（含 macOS 签名）：

```bash
uv run shortcuts-toolkit self-test
```

## 规范

- **纯标准库优先**：运行时不引入第三方依赖。如确需引入，必须用 **uv + 国内源**（清华，见 `pyproject.toml` `[tool.uv]`）。
- **新功能配测试**：在 `tests/test_core.py` 增加用例，覆盖核心纯函数与往返。
- **遵循现有风格**：ruff 已配置（line-length 100，规则 E/F/W/I/UP/B）；格式化用 `uv run ruff format .`。
- **类型注解**：新增公开函数补 type hints（mypy 已启用）。
- **生成快捷指令前必查 `reference/`**：见 `AGENTS.md` 的强制查阅顺序——禁止凭记忆盲写 plist。
- **版权**：`reference/` 是第三方（erik-agens/shortcuts-skill，MIT），保持署名不删。

## 提交

- commit message 用中文或英文均可，建议带类型前缀（`feat:` / `fix:` / `docs:` / `test:` / `chore:`）。
- PR 描述写清改了什么、为什么、如何验证。

## 发布（维护者）

1. 更新 `CHANGELOG.md` 的 `[Unreleased]` → 新版本段。
2. 改 `pyproject.toml` 的 `version`。
3. commit + tag：`git tag v0.x.0 && git push --tags`。
4. `publish.yml` 自动 build + 发布到 PyPI（需先在 PyPI 配置 Trusted Publisher，见 `.github/workflows/publish.yml` 注释）。
