# Candidate Shortlist

候选工具按第一轮优先级排列。第一轮目标是用同一份 `GB/T 13594-2025` 快速得到可审查 Markdown，而不是马上做复杂调参。

## 1. pymupdf4llm

- source: https://github.com/pymupdf/pymupdf4llm
- type: lightweight local PDF extraction
- why first:
  - 安装简单，通常只需要 `pip install pymupdf4llm`。
  - 官方定位是把 PDF 转为 LLM-ready Markdown / JSON / text。
  - 支持表格、图片、页块和 OCR 选项。
  - 适合作为速度和可控性的基线。
- risk:
  - 对复杂表格和页眉页脚清理可能需要后处理。

## 2. docling

- source: https://github.com/docling-project/docling
- type: document understanding / structured conversion
- why:
  - 支持 PDF 到 Markdown / JSON。
  - 有版面、阅读顺序、表格结构等能力。
  - 适合检查标准 PDF 的条款和表格保留效果。
- risk:
  - 安装和首次模型下载可能比 PyMuPDF4LLM 慢。

## 3. marker

- source: https://github.com/datalab-to/marker
- type: PDF / document to Markdown / JSON converter
- why:
  - 面向高精度 Markdown 和 JSON 转换。
  - 对复杂文档、表格、图片通常比纯文本抽取更强。
- risk:
  - 依赖较重，可能下载模型或需要更长运行时间。
  - 对本地机器资源更敏感。

## 4. markitdown

- source: https://github.com/microsoft/markitdown
- type: general file-to-Markdown converter
- why:
  - Microsoft 维护，安装和调用相对直接。
  - 可作为轻量通用转换基线。
- risk:
  - PDF 结构化能力可能不如专门的 PDF 版面分析工具。

## Second-round candidate: MinerU

- source: https://github.com/opendatalab/MinerU
- type: OCR / layout analysis / document parsing
- why later:
  - 对复杂中文文档和版面解析很有潜力。
  - 支持 Markdown / JSON 输出。
- reason not first:
  - 工具链和模型较重，适合在第一轮轻量工具效果不足时投入。

