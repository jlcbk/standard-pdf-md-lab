# MinerU + kimi-k2p6 Trial Review

date: 2026-05-14
type: objective results and preliminary risk assessment
**No final adoption conclusions.**

## Trial Summary

Attempted to convert `samples/GBT 13594-2025.pdf` (3 pages) using MinerU v3.1.12 with `vlm-http-client` backend pointing to the kimi-k2p6 OpenAI-compatible endpoint.

## Objective Results

### What Worked

- **Installation**: MinerU v3.1.12 installed successfully from GitHub source (PyPI `magic-pdf` is legacy and lacks `vlm-http-client` support).
- **Connectivity**: `vlm-http-client` backend successfully connected to the OpenAI-compatible endpoint. All HTTP requests returned 200.
- **No local model downloads**: The backend correctly skipped `auto_download_and_get_model_root_path()` — confirmed zero model weight downloads.
- **Run completed**: 3 pages processed in ~14 seconds (31 seconds total including API startup).
- **Model recognition quality**: kimi-k2p6 correctly identified the document's standard number, titles (Chinese and English), TOC structure, and page types from the cover, blank, and TOC pages.

### What Didn't Work

- **Zero content extracted**: All output files (`.md`, `_middle.json`, `_model.json`, `_content_list.json`) are empty.
- **Format incompatibility**: kimi-k2p6 outputs natural language descriptions. MinerU's parser (`_layout_re` in `mineru_vl_utils/mineru_client.py`) expects structured tokens: `<|box_start|>x1 y1 x2 y2<|box_end|><|ref_start|>type<|ref_end|>`.
- **Hardcoded prompts**: MinerU uses simple prompts (`"\nLayout Detection:"`, `"\nText Recognition:"`) with a generic system prompt (`"You are a helpful assistant."`). These are not configurable via CLI.

## Preliminary Risk Assessment

### Blocking Issues

1. **Model fine-tuning dependency**: MinerU's VLM pipeline is designed for models fine-tuned with `MinerULogitsProcessor` (typically Qwen2VL-family). The `vlm-http-client` backend was built for `mineru-openai-server` serving these specialized models, not general-purpose OpenAI-compatible endpoints.

2. **No prompt customization**: MinerU does not expose prompt configuration via CLI or environment variables. The layout detection prompt is hardcoded at `mineru_vl_utils/mineru_client.py:33-35`. Without the ability to instruct kimi-k2p6 to output the required token format, the format mismatch cannot be resolved at the integration layer.

3. **Chain-of-thought behavior**: kimi-k2p6 outputs extensive reasoning text before answers (documented in `candidates/kimi-k2p6/NOTES.md`). Even if prompt customization were available, the model's tendency toward narrative output makes structured token generation unlikely without fine-tuning.

### Non-Issues

- No local model downloads triggered (confirmed safe for environments with disk constraints).
- API connectivity and authentication worked correctly.
- Cost appears contained for small-scale trials (3 pages, ~3 API calls).

### Architecture Observation

The two-step extraction flow (layout detection → content extraction per block) is a reasonable design, but the tight coupling between the parser regex and a specific model family's output format makes the pipeline fragile when used with non-MinerU models. The `vlm-http-client` backend name suggests general OpenAI compatibility, but in practice it expects a MinerU-specific served model.

## Related Candidates

- `candidates/kimi-k2p6/NOTES.md` — kimi-k2p6 smoke test results
- `reviews/kimi-k2p6-smoke.md` — kimi-k2p6 connectivity and capability review