# Round 1 Summary

## Tested Tools

| Tool | Status | Verdict |
| --- | --- | --- |
| `pymupdf4llm` | 成功生成 Markdown 和 27 个 assets | 保留为轻量基线，不作为主方案 |
| `markitdown` | 成功生成文本型 Markdown | 淘汰为主方案，仅保留对照 |
| `docling` | 成功生成 Markdown 和 11 个 assets | 结构更好，但字符拆分严重，暂不作为主方案 |
| `marker` | 安装成功，转换被中止 | 本地 CPU 成本过高，暂缓 |

## Overall Judgment

第一轮和补充测试结果整体偏差，不能直接满足“给后续 agent 理解和处理标准”的目标。

`pymupdf4llm` 的优点是输出完整、速度快、能抽取图片和表格轮廓；但 bracket artifact 太严重，例如 `GB[/] T 13594[—] 2025`、`1[范围]`、`GB[/] T20716.1[道路车辆]`。这些污染不仅影响阅读，也会影响后续 agent 做标准号、条款号、引用文件和章节标题的可靠识别。

`markitdown` 的文本符号更干净一些，但输出基本不是结构化 Markdown。它把中文、类别符号、表格和目录拆成大量短行，章节层级和表格行列关系基本丢失。后处理要做的不是清洗，而是重建文档结构，成本过高。

`docling` 的结构能力强于 `markitdown`，表 1 能转成 Markdown 表格，章节标题也较完整。但它把标准号、数字、英文和单位拆成字符级间隔，例如 `GB / T 1 3 5 9 4 - 2 0 2 5`、`4 0k m / h`，这对标准号和条款引用场景是核心失败。

`marker` 没有生成可评审 Markdown。本地 CPU 首次运行下载了大型模型，进入布局识别后 `1/27` 页耗时约 112 秒，估算单个 PDF 接近 45-60 分钟，不适合作为批量默认方案。

## Failure Modes

- 标题层级不可信：正文片段可能被提升为标题、断裂为多个标题，或完全没有标题。
- 标准号和引用文件污染：`GB/T`、破折号、括号、标点被错误拆分或包裹。
- 数字和英文拆分：`docling` 将标准号、年份、单位和英文标题拆成字符级间隔。
- 表格不可直接使用：`pymupdf4llm` 保留了表格外形但有换行污染；`markitdown` 基本丢失表格结构。
- 页眉页脚和页码污染：重复进入正文，尤其影响条款连续性。
- 英文标题和专有名词断词：英文标题空格丢失，中文类别符号上下文分离。
- 重型模型成本：`marker` 在本地 CPU 上运行成本过高。

## Decision

第一轮不进入最终方案选择。下一步应测试更强的文档版面理解工具：

1. `MinerU`：下一优先。目标是验证中文标准 PDF 的版面、表格和公式是否明显优于当前工具。
2. 混合后处理方案：以 `pymupdf4llm` 或 `docling` 作为底稿，写规则修复标准号、条款号、页眉页脚和表格。
3. 远端 / GPU 方案：如果要继续 `marker`，应换到 GPU 或更快推理环境。

## Updated Acceptance Bar

后续工具只有满足以下最低要求，才值得进入二轮：

- 标准号能保持为 `GB/T 13594-2025` 或等价清晰格式。
- 一级章节至少能输出为稳定 Markdown 标题。
- 条款编号如 `6.3.3.2` 不应和正文混成无法拆分的一段。
- 表 1 至少能保持三列表格结构。
- 页眉页脚不能频繁被识别为正文标题。

## VLM Preparation Update

`kimi-k2p6` 在线模型接口已完成 smoke test，见 `reviews/kimi-k2p6-smoke.md`：

- 文本请求成功：HTTP `200`，总 token `77`。
- 单页图片请求成功：HTTP `200`，总 token `2028`。
- 模型能识别封面页中的 `GB/T 13594-2025` 和中文标题。
- 主要风险是普通提示会输出 reasoning-like 解释文本，并且在 `max_tokens=512` 下被截断。
- 追加 JSON-only 小测成功返回可解析 JSON，说明严格提示下可以做受控单页结构抽取。

因此，`kimi-k2p6` 可以进入下一步小范围 VLM 实验，但不能直接进入整份 PDF 批量转换。下一步应测试固定页面集 JSON 抽取、schema 校验和成本上限。

## MinerU + kimi-k2p6 Trial Update

`deepseek-v4-pro` 已按任务卡执行 `MinerU v3.1.12 + vlm-http-client + kimi-k2p6` 小样本试跑，见 `reviews/mineru-kimi.md`：

- MinerU 可以连接在线 OpenAI-compatible endpoint，接口返回 HTTP `200`。
- 未触发本地大模型下载，符合“暂缓本地模型部署”的约束。
- 试跑限制为 3 页，运行完成但 Markdown、content list、model JSON 产物为空。
- 根因是 MinerU 的 `vlm-http-client` 需要 MinerU 专用结构化输出 token，例如 `<|box_start|>...<|box_end|><|ref_start|>...<|ref_end|>`；`kimi-k2p6` 输出的是自然语言版面描述，无法被 MinerU 的解析器消费。

因此，当前证据显示：`kimi-k2p6` 可以作为自定义 VLM 页面理解组件继续测试，但不适合作为 MinerU `vlm-http-client` 的直接替换模型。
