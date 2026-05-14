# MinerU + kimi-k2p6 Trial Notes

date: 2026-05-14
status: trial completed, output unusable

## Environment

| Item | Value |
| --- | --- |
| Python | 3.13 (brew-installed, 3.14 incompatible with pydantic-core) |
| venv | `.venv-mineru/` |
| MinerU version | 3.1.12 (GitHub: `opendatalab/MinerU`) |
| Backend | `vlm-http-client` |
| Model | `accounts/fireworks/models/kimi-k2p6` |
| API endpoint | `OPENAI_COMPAT_BASE_URL` (user environment) |
| PDF sample | `samples/GBT 13594-2025.pdf` (3 pages) |

## Installation

Two attempts required:

1. **PyPI `magic-pdf` v1.3.12 (FAILED for purpose)** — legacy version, only supports `auto/ocr/txt` backends, no `vlm-http-client`. Installed successfully but cannot use online VLM.

2. **GitHub `mineru` v3.1.12 (SUCCEEDED)** — `pip install 'git+https://github.com/opendatalab/MinerU.git'` provides `vlm-http-client` backend via `mineru-vl-utils` package.

Key dependencies: `torch` (2.12.0, 88MB wheel), `transformers` (4.57.6), `mineru-vl-utils`, `openai`, `httpx`.

Full log: `candidates/mineru-kimi/install.log`

## Run Command

```sh
mineru -p "samples/GBT 13594-2025.pdf" -o "outputs/mineru-kimi" -b vlm-http-client -u "$OPENAI_COMPAT_BASE_URL"
```

API key and model name read from environment: `MINERU_VL_API_KEY`, `MINERU_VL_MODEL_NAME` (set to match `OPENAI_COMPAT_API_KEY` and `OPENAI_COMPAT_MODEL`).

## Results

### Timing

| Phase | Duration |
| --- | --- |
| API startup | ~8s |
| Model init | ~3.5s |
| 3-page processing | ~14s |
| Total | ~31s |

### Output Status

All output files are **empty** (no content extracted):

| File | Content |
| --- | --- |
| `GBT 13594-2025.md` | Empty |
| `GBT 13594-2025_middle.json` | 3 pages, all `para_blocks: []` |
| `GBT 13594-2025_model.json` | `[[], [], []]` |
| `GBT 13594-2025_content_list.json` | `[]` |

### Root Cause: Format Mismatch

MinerU's `vlm-http-client` backend expects the VLM to output structured layout tokens:

```
<|box_start|>x1 y1 x2 y2<|box_end|><|ref_start|>text<|ref_end|>...
```

kimi-k2p6 outputs **natural language descriptions** instead. All 3 pages triggered:

```
WARNING | mineru_vl_utils.mineru_client:parse_layout_output:251 -
Layout output does not match expected format: Here is the layout
detection analysis for this standard document cover page...
```

The model correctly identified document content (standard number GB/T 13594-2025, title, TOC structure) but in narrative/markdown-table form, which MinerU's regex parser (`_layout_re`) cannot consume.

### Model Downloads

**None triggered.** The `vlm-http-client` backend skips `auto_download_and_get_model_root_path()` entirely (confirmed in `mineru/backend/vlm/vlm_analyze.py:80`).

### Token Usage

Not reported by MinerU for vlm-http-client backend. The API responses were not logged with token counts.

## Key Technical Details

- MinerU's `HttpVlmClient` sends images as `data:image/png;base64,...` in standard OpenAI-compatible `v1/chat/completions` format
- Prompts are hardcoded in `mineru_vl_utils/mineru_client.py`: `"\nLayout Detection:"` for layout, `"\nText Recognition:"` for content
- System prompt is generic: `"You are a helpful assistant."`
- The `vlm-http-client` backend was designed for `mineru-openai-server` (serving MinerU-fine-tuned Qwen2VL models with `MinerULogitsProcessor`), not arbitrary OpenAI-compatible endpoints
- kimi-k2p6 is a general reasoning model with chain-of-thought output behavior

## Stop Conditions

| Condition | Triggered? |
| --- | --- |
| Auth/routing/model call failure | No — all API calls returned HTTP 200 |
| Cannot configure online VLM | No — `vlm-http-client` backend configured successfully |
| Model download >500MB | No — zero model downloads |
| Run >60min with no output | No — completed in ~31s |
| No progress/cost cap | No — 3-page trial only |