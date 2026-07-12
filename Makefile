.PHONY: install install-all install-claude install-copilot install-cursor install-codex install-kilo install-opencode test lint format check self-test clean

SKILL_NAME := shortcuts-toolkit
SKILL_SRC := skill

## 一键把 skill/ 安装到本机检测到的各 agent 平台目录
install: install-all

install-all: install-claude install-copilot install-cursor install-codex install-kilo install-opencode
	@echo ""
	@echo "==> $(SKILL_NAME) skill 安装完成（已装到所有检测到的平台）。"

# 各目标：若该 agent 配置目录存在则安装，否则跳过
install-claude:
	@if [ -d ~/.claude ] || [ -d ~/.claude/skills ]; then mkdir -p ~/.claude/skills && rm -rf ~/.claude/skills/$(SKILL_NAME) && cp -r $(SKILL_SRC) ~/.claude/skills/$(SKILL_NAME) && echo "  ✓ Claude Code:    ~/.claude/skills/$(SKILL_NAME)"; else echo "  · Claude Code:    未检测到 ~/.claude，跳过"; fi

install-copilot:
	@if [ -d ~/.copilot ] || [ -d .github/skills ]; then mkdir -p .github/skills && rm -rf .github/skills/$(SKILL_NAME) && cp -r $(SKILL_SRC) .github/skills/$(SKILL_NAME) && echo "  ✓ GitHub Copilot: .github/skills/$(SKILL_NAME)"; else echo "  · GitHub Copilot: 未检测到，跳过"; fi

install-cursor:
	@if [ -d ~/.cursor ] || [ -d .cursor ]; then mkdir -p .cursor/rules && rm -rf .cursor/rules/$(SKILL_NAME) && cp -r $(SKILL_SRC) .cursor/rules/$(SKILL_NAME) && echo "  ✓ Cursor:         .cursor/rules/$(SKILL_NAME)"; else echo "  · Cursor:         未检测到 ~/.cursor，跳过"; fi

install-codex:
	@if [ -d ~/.codex ]; then mkdir -p ~/.codex/skills && rm -rf ~/.codex/skills/$(SKILL_NAME) && cp -r $(SKILL_SRC) ~/.codex/skills/$(SKILL_NAME) && echo "  ✓ Codex CLI:      ~/.codex/skills/$(SKILL_NAME)"; else echo "  · Codex CLI:      未检测到 ~/.codex，跳过"; fi

install-kilo:
	@if [ -d ~/.kilo ] || [ -d .kilo ]; then mkdir -p .kilo/skills && rm -rf .kilo/skills/$(SKILL_NAME) && cp -r $(SKILL_SRC) .kilo/skills/$(SKILL_NAME) && echo "  ✓ Kilo:           .kilo/skills/$(SKILL_NAME)"; else echo "  · Kilo:           未检测到 ~/.kilo，跳过"; fi

install-opencode:
	@if [ -d .opencode ] || [ -d ~/.config/opencode ]; then mkdir -p .opencode/skills && rm -rf .opencode/skills/$(SKILL_NAME) && cp -r $(SKILL_SRC) .opencode/skills/$(SKILL_NAME) && echo "  ✓ OpenCode:       .opencode/skills/$(SKILL_NAME)"; else echo "  · OpenCode:       未检测到 .opencode，跳过"; fi

## 开发任务
test:
	uv run pytest -q

lint:
	uv run ruff check .

format:
	uv run ruff format .

check: lint
	uv run ruff format --check .
	uv run mypy
	uv run pytest -q

self-test:
	uv run shortcuts-toolkit self-test

clean:
	rm -rf build dist *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
