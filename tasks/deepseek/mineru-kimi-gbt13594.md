# Task Card: MinerU + kimi-k2p6 GBT13594 Trial

任务目标：

尝试用 MinerU 方案转换 `samples/GBT 13594-2025.pdf`，优先使用在线 `kimi-k2p6` 模型接口，不部署本地大模型，不下载大体积模型权重。你只负责执行、记录和生成草稿，不做最终方案判断。

输入文件：

- `samples/GBT 13594-2025.pdf`
- `scripts/openai_compat_smoke.py`
- `candidates/kimi-k2p6/NOTES.md`
- `reviews/kimi-k2p6-smoke.md`

允许写入：

- `.venv-mineru/`
- `candidates/mineru-kimi/`
- `outputs/mineru-kimi/`
- `reviews/mineru-kimi.md`

禁止修改：

- `samples/`
- `outputs/pymupdf4llm/`
- `outputs/markitdown/`
- `outputs/docling/`
- `outputs/kimi-k2p6/`
- `reviews/round-1-summary.md`
- `reviews/kimi-k2p6-smoke.md`
- `README.md`
- `MODEL_COLLAB_PLAN.md`

必须遵守：

- 不要把 API key 写入仓库文件、日志、Markdown 或命令记录。
- 使用已经存在于运行环境中的 `OPENAI_COMPAT_BASE_URL`、`OPENAI_COMPAT_MODEL`、`OPENAI_COMPAT_API_KEY` 环境变量。
- 不要使用 `git add`、`git commit`、`git push`。
- 不要删除或覆盖已有候选工具输出。
- 不要安装或下载本地大模型权重。如果 MinerU 必须下载大于 500 MB 的模型权重才能继续，请停止并记录原因。
- 如果 MinerU 不能直接接入 OpenAI-compatible VLM，请停止并记录官方文档或 CLI 帮助中的证据；不要改用本地大模型。

执行建议：

1. 建立目录：

```sh
mkdir -p candidates/mineru-kimi outputs/mineru-kimi reviews
```

2. 记录环境和 MinerU 安装尝试到：

```text
candidates/mineru-kimi/install.log
candidates/mineru-kimi/run.log
candidates/mineru-kimi/NOTES.md
```

3. 先查看 MinerU 官方 CLI 帮助或包文档，确认是否能使用远端 OpenAI-compatible VLM。

4. 如果确认可行，再尝试转换整份 PDF，输出到：

```text
outputs/mineru-kimi/
```

5. 如果整份 PDF 运行成本明显过高，可以改为 1 到 3 页的小样本试跑，但必须在 `run.log` 里写清楚原因。

需要记录：

- MinerU 版本。
- 安装命令和主要依赖。
- 是否使用了在线模型。
- 是否触发本地模型下载。
- 是否生成 Markdown / JSON / assets。
- 输出路径。
- 耗时。
- 错误信息。
- token 用量或可见费用信号，如接口返回中存在。

停止条件：

- 认证、路由或模型调用失败。
- MinerU 无法配置在线 VLM。
- 需要下载大于 500 MB 的本地模型权重。
- 单次运行超过 60 分钟仍无可评审产物。
- 工具开始批量调用在线模型但没有可见进度或成本上限。

交付物：

- `candidates/mineru-kimi/NOTES.md`
- `candidates/mineru-kimi/install.log`
- `candidates/mineru-kimi/run.log`
- `outputs/mineru-kimi/` 中的原始产物，若有
- `reviews/mineru-kimi.md`，只写客观结果和初步风险，不写最终采用结论
