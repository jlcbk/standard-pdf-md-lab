# marker Review

## 基本信息

- 工具名称：`marker`
- 来源：https://github.com/datalab-to/marker
- 版本：`marker-pdf==1.10.2`
- 运行日期：2026-05-14
- 输入文件：`samples/GBT 13594-2025.pdf`
- 输出目录：`outputs/marker/`
- 运行命令：

```sh
.venv-marker/bin/marker_single 'samples/GBT 13594-2025.pdf' --output_dir outputs/marker --output_format markdown --disable_ocr > candidates/marker/run.log 2>&1
```

## 结果摘要

- 是否成功生成 Markdown：否
- 是否生成图片 / assets：否
- 是否需要 OCR：本次尝试传入 `--disable_ocr`
- 是否需要人工修复：未生成结果，无法评估文本质量

## 评分

| 维度 | 分值 | 备注 |
| --- | --- | --- |
| 标题层级 | N/A | 未生成输出 |
| 正文准确性 | N/A | 未生成输出 |
| 表格保真 | N/A | 未生成输出 |
| 图像处理 | N/A | 未生成输出 |
| 噪声清理 | N/A | 未生成输出 |
| 自动化适配 | 1 | 本地 CPU 首次运行成本过高，不适合作为批量默认方案 |

## 主要问题

- 模型下载很重，首次运行拉取约 1.35GB 和 258MB 级别模型。
- 在本机 CPU 上，布局识别约 `1/27` 页耗时 112 秒。
- 估算单个 28 页 PDF 可能需要 45-60 分钟，无法满足批量调试效率。
- `deepseek-v4-pro` 执行模型调用仍然预算超限且未落盘，实际安装与测试由 `gpt-5.5` 接手。

## 值得保留的优点

- 仍可能在 GPU 或更快推理环境中表现较好。
- 工具定位和功能覆盖适合复杂 PDF，但本轮本地 CPU 不适合继续消耗。

## 结论

- 建议：暂缓，不进入本地 CPU 主方案。
- 原因：不是质量失败，而是运行成本失败。除非后续有 GPU / 远端推理环境，否则不继续作为第一批候选。

