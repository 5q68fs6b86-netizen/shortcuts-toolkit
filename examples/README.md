# Markdown 剪贴板转 Word

`md_clipboard_to_word.json` 是一个可由 `shortcuts-toolkit` 生成的 Apple 快捷指令规格：

1. 读取剪贴板 Markdown。
2. 调用 OpenAI 兼容接口 `https://nnnn.114514heihei.eu.org/v1/chat/completions`，使用 `fast` 模型生成安全的中文文件名。
3. 调用 `https://md2word.ciallo0d000721.cc.cd/api/markdown-to-word` 生成 DOCX。服务支持原生 Word 公式（OMML）和真实表格。
4. 保存为 AI 标题命名的 `.docx` 文件。

模板中的 `YOUR_API_KEY` 只是占位符，不能直接运行。请在本地副本中替换为自己的密钥；不要把真实密钥提交到 GitHub。

```bash
uv run shortcuts-toolkit preview --verify -i examples/md_clipboard_to_word.json
uv run shortcuts-toolkit generate -i examples/md_clipboard_to_word.json -o out/md_clipboard_to_word.shortcut
uv run shortcuts-toolkit parse out/md_clipboard_to_word.shortcut
```

Linux 无法执行 Apple 的 `shortcuts sign`。在 macOS 上运行：

```bash
shortcuts sign --mode anyone --input out/md_clipboard_to_word.shortcut --output out/md_clipboard_to_word.signed.shortcut
```

快捷指令的 `Save File` 已设置为不弹出保存位置对话框，并使用标题作为文件名。如果设备要求指定文件夹，可在导入后给最后一个“存储文件”动作选择 iCloud Drive/快捷指令文件夹。
