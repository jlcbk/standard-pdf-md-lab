# Task Card: kimi-k2p6 JSON Page-Set Experiment

任务目标：

用已验证可用的 `scripts/openai_compat_smoke.py`，对固定页面集做低成本 JSON 抽取实验，验证 `kimi-k2p6` 是否能稳定识别标准页面结构。

输入文件：

- `samples/GBT 13594-2025.pdf`
- `outputs/kimi-k2p6/page-01.png`

允许写入：

- `outputs/kimi-k2p6/page-03.png`
- `outputs/kimi-k2p6/page-07.png`
- `outputs/kimi-k2p6/page-10.png`
- `outputs/kimi-k2p6/page-03-json.json`
- `outputs/kimi-k2p6/page-07-json.json`
- `outputs/kimi-k2p6/page-10-json.json`
- `outputs/kimi-k2p6/page-03-json.txt`
- `outputs/kimi-k2p6/page-07-json.txt`
- `outputs/kimi-k2p6/page-10-json.txt`
- `candidates/kimi-k2p6/page-set.log`
- `reviews/kimi-k2p6-page-set.md`

禁止修改：

- `samples/`
- `outputs/pymupdf4llm/`
- `outputs/markitdown/`
- `outputs/docling/`
- `reviews/round-1-summary.md`
- `reviews/kimi-k2p6-smoke.md`
- `README.md`
- `MODEL_COLLAB_PLAN.md`

执行命令建议：

1. 用 PyMuPDF 将第 3、7、10 页渲染为 PNG，分辨率可沿用当前 `page-01.png` 的 1.5x 缩放。
2. 对每页运行 `scripts/openai_compat_smoke.py`，提示词必须要求 JSON-only。
3. 使用环境变量传入 API 配置，不要把 API key 写进任何文件。

推荐 JSON schema：

```json
{
  "page_no": 0,
  "page_type": "",
  "standard_no": "",
  "headings": [],
  "clause_numbers": [],
  "tables": [],
  "figures": [],
  "notable_text": []
}
```

需要记录：

- 每页 HTTP status。
- 每页 elapsed_seconds。
- 每页 token usage。
- 输出是否能被 `jq` 解析。
- 是否识别出真实章节标题。
- 是否出现 reasoning-like 文本。

停止条件：

- 任一请求返回认证、路由或图片输入错误。
- 单页请求超过 10000 total tokens。
- 输出无法解析为 JSON，且重试一次仍失败。

交付物：

- `candidates/kimi-k2p6/page-set.log`
- `reviews/kimi-k2p6-page-set.md`

默认护栏：

你只负责执行、记录和生成草稿，不做最终方案判断。不得删除或覆盖已有文件。新增文件必须放在任务卡指定目录。不得把 API key 写入仓库文件或日志。失败时保留完整错误信息并停止，不要自行扩大任务范围。不要使用 git add、git commit、git push。
