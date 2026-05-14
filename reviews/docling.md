# docling Review

## 基本信息

- 工具名称：`docling`
- 来源：https://github.com/docling-project/docling
- 版本：`2.93.0`
- 运行日期：2026-05-14
- 输入文件：`samples/GBT 13594-2025.pdf`
- 输出目录：`outputs/docling/`
- 运行命令：

```sh
.venv-docling/bin/docling --from pdf --to md --image-export-mode referenced --table-mode accurate --no-ocr --device cpu --output outputs/docling 'samples/GBT 13594-2025.pdf' > candidates/docling/run.log 2>&1
```

## 结果摘要

- 是否成功生成 Markdown：是
- 输出文件：`outputs/docling/GBT-13594-2025.md`
- Markdown 行数：1,006
- 是否生成图片 / assets：是，11 个图片
- 是否需要 OCR：本次未启用 OCR
- 是否需要人工修复：需要，且数字 / 英文拆分问题严重

## 评分

| 维度 | 分值 | 备注 |
| --- | --- | --- |
| 标题层级 | 3 | 章节结构比前两个工具更清楚，但仍有断裂和误判 |
| 正文准确性 | 2 | 中文主体可读，但数字、标准号、英文、符号拆分严重 |
| 表格保真 | 3 | 表 1 能保留为 Markdown 表格，目录表格仍混乱 |
| 图像处理 | 3 | 能引用图片 assets，但路径嵌套不理想 |
| 噪声清理 | 2 | 页眉仍会进入标题，重复图像和页眉存在 |
| 自动化适配 | 2 | 安装重、首次运行慢，质量未达到投入成本 |

## 主要问题

- 标准号被拆为 `GB / T 1 3 5 9 4 - 2 0 2 5`，不满足最低验收线。
- 英文标题被拆成字符级间隔：`P e r f o r m a n c e...`。
- 数字和单位被拆散，例如 `GB / T1 5 0 8 9`、`4 0k m / h`、`0. 8`。
- 符号表中变量名被拆散，例如 `F b R A L`。
- 部分标题断裂，例如 `## 5` 和 `## 分类` 分开。
- 输出 assets 路径出现 `outputs/docling/outputs/docling/...` 嵌套。

## 值得保留的优点

- 章节层级和表格识别强于 `markitdown`。
- 表 1 形成了三列表格，结构上比第一轮更接近目标。
- 中文正文段落比 `markitdown` 连续。

## 结论

- 建议：暂不作为主方案。
- 原因：结构能力有提升，但标准号、数字、英文和单位拆分是标准文档转换的核心失败。除非后续能通过配置显著改善字符间距，否则不值得进入二轮。

