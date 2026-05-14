# markitdown Review

## 基本信息

- 工具名称：`markitdown`
- 来源：https://github.com/microsoft/markitdown
- 版本：`0.1.5`
- 运行日期：2026-05-14
- 输入文件：`samples/GBT 13594-2025.pdf`
- 输出目录：`outputs/markitdown/`
- 运行命令：

```sh
.venv-markitdown/bin/markitdown 'samples/GBT 13594-2025.pdf' > outputs/markitdown/GBT-13594-2025.md 2> candidates/markitdown/run.log
```

## 结果摘要

- 是否成功生成 Markdown：是，但更接近纯文本抽取
- 输出文件：`outputs/markitdown/GBT-13594-2025.md`
- Markdown 行数：9,943
- 是否生成图片 / assets：否
- 是否需要 OCR：否
- 是否需要人工修复：需要，且修复成本较高

## 评分

| 维度 | 分值 | 备注 |
| --- | --- | --- |
| 标题层级 | 1 | 未生成 Markdown 标题结构 |
| 正文准确性 | 3 | 文本相对干净，但被切成大量短行 |
| 表格保真 | 1 | 表格结构基本丢失 |
| 图像处理 | 0 | 未输出图片或公式 assets |
| 噪声清理 | 2 | 页眉页脚和分页符仍在，结构噪声明显 |
| 自动化适配 | 3 | 安装简单，但需 `[pdf]` extra，结果不适合作为主方案 |

## 主要问题

- 输出没有 Markdown heading，后续 agent 难以直接识别章节层级。
- 大量中文字符和短语被拆为单独行，阅读连续性差。
- 目录、表格、附录结构没有被可靠保留。
- 未提取图片、公式或图形。
- 输出包含分页控制字符和重复页眉。

## 值得保留的优点

- 标准号、部分正文符号比 `pymupdf4llm` 更干净。
- 安装和命令行使用简单。
- 可以作为“纯文本抽取”对照组。

## 结论

- 建议：暂不作为主方案，保留为对照组。
- 原因：它能成功抽文本，但结构化 Markdown 能力不足，后处理成本高于 `pymupdf4llm`。

