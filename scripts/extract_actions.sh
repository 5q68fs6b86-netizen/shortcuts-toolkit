#!/usr/bin/env bash
# 从 macOS dyld 共享缓存 dump 所有 Apple 快捷指令内置动作 identifier（最权威来源）。
# 这些 identifier 是 WorkflowKit.framework 在系统里注册的字符串常量，直接反映当前系统版本支持哪些动作。
#
# 用法:
#   bash scripts/extract_actions.sh > src/shortcuts_toolkit/data/known_actions.txt
#
# 仅 macOS 可用。Intel / Apple Silicon 路径自动兜底。
# 注意: 此表仅含「系统内置动作」；第三方 App 动作（<bundle>.<intent>）由各自 App 注册，不在此。
set -euo pipefail

CACHE=""
for pat in \
  "/System/Cryptexes/OS/System/Library/dyld/dyld_shared_cache_x86_64h" \
  "/System/Cryptexes/OS/System/Library/dyld/dyld_shared_cache_arm64e"; do
  if [ -f "$pat" ]; then CACHE="${pat%.*}"; break; fi
done

if [ -z "$CACHE" ]; then
  echo "错误: 未找到 dyld 共享缓存（此脚本仅 macOS 可用）。" >&2
  exit 1
fi

# 遍历主缓存 + 各子缓存，提取所有 is.workflow.actions.* identifier，去重排序
for f in "$CACHE" "$CACHE".0[1-9] "$CACHE".1[0-9] "$CACHE".2[0-9]; do
  [ -f "$f" ] && grep -aoE "is\.workflow\.actions\.[a-z0-9.]+" "$f"
done | sort -u
