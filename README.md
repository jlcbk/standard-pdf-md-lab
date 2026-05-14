# standard-pdf-md-lab

本项目用于调试和评估“标准 PDF 转 Markdown”的方案。目标不是马上锁定某一个工具，而是用同一份标准 PDF 对多种开源项目或命令行工具做可复现实验，让人工审查转换结果后再确定最终方案。

## 当前样本

- `samples/GBT 13594-2025.pdf`
  - 来源：国家标准全文公开系统
  - 标准号：`GB/T 13594-2025`
  - 页数：28 页
  - MD5：`9b6b4557825c1d43e25d420415fd6a38`

## 目录结构

```text
standard-pdf-md-lab/
  README.md
  WORKPLAN.md
  MODEL_COLLAB_PLAN.md
  samples/      # 输入 PDF 样本，当前使用软链接指向上级目录已下载文件
  candidates/   # 候选工具记录、安装说明、适配脚本或子模块
  outputs/      # 每个候选工具生成的 Markdown / 图片 / 中间文件
  reviews/      # 人工审查记录和评分
  scripts/      # 后续沉淀的统一转换、对比、校验脚本
```

## 协作方式

- 总体工作计划见 `WORKPLAN.md`。
- `gpt-5.5` 与 Claude Code 中 `deepseek-v4-pro` 的任务拆分见 `MODEL_COLLAB_PLAN.md`。

## 评估目标

标准 PDF 的转换结果至少要能支持后续 agent 理解和处理，因此重点看：

- 标题层级是否清晰。
- 条款编号、表格编号、图题、脚注是否保留。
- 表格是否能被 Markdown 或 HTML 表格表达，并且不丢列、不错行。
- 页眉、页脚、水印、版权提示是否被合理清理。
- 中英文、单位、公式、符号是否尽量不乱码。
- 图片、流程图、结构图是否能被提取或用占位说明保留。
- 输出是否稳定可复现，适合批量处理更多标准。
