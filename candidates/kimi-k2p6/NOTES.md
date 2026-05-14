# kimi-k2p6

source: user-provided OpenAI-compatible endpoint
model: `accounts/fireworks/models/kimi-k2p6`
endpoint: configured at runtime with `OPENAI_COMPAT_BASE_URL`
status: smoke test passed (both text and image requests returned HTTP 200)

## Purpose

This candidate records low-cost connectivity and capability checks for the
online `kimi-k2p6` model service before using it in a MinerU or VLM-assisted PDF
conversion workflow.

## Credential Handling

Do not write API keys into this file, shell logs, committed scripts, or review
notes. Use environment variables:

```sh
export OPENAI_COMPAT_BASE_URL="https://example.com/v1"
export OPENAI_COMPAT_MODEL="accounts/fireworks/models/kimi-k2p6"
export OPENAI_COMPAT_API_KEY="..."
```

## Smoke Test Commands

Text-only request:

```sh
scripts/openai_compat_smoke.py \
  --output-json outputs/kimi-k2p6/text-smoke.json \
  --output-text outputs/kimi-k2p6/text-smoke.txt
```

Single-image request:

```sh
scripts/openai_compat_smoke.py \
  --image outputs/kimi-k2p6/page-01.png \
  --prompt "请识别这页标准 PDF 的标准号、标题和可见章节标题，用 Markdown 列表输出。" \
  --output-json outputs/kimi-k2p6/image-smoke.json \
  --output-text outputs/kimi-k2p6/image-smoke.md
```

## Stop Conditions

- Authentication or model routing fails.
- The model accepts text but rejects image input.
- A single page request is unexpectedly expensive or slow.
- Output contains obvious hallucinated standard numbers or titles.

## Smoke Test Results (2026-05-14)

### Text-Only Request

| Item | Value |
| --- | --- |
| HTTP status | 200 |
| Elapsed | 2.823s |
| prompt_tokens | 13 |
| completion_tokens | 64 |
| total_tokens | 77 |
| cached_tokens | 12 |
| Error | null |

Raw output: `outputs/kimi-k2p6/text-smoke.json`

The model received a prompt asking for the two-character reply "成功". The
response was truncated at 64 completion tokens mid-reasoning, with the actual
"成功" answer never emitted. The output is entirely chain-of-thought text.

### Single-Image Request

| Item | Value |
| --- | --- |
| HTTP status | 200 |
| Elapsed | 7.845s |
| prompt_tokens | 1516 |
| completion_tokens | 512 |
| total_tokens | 2028 |
| cached_tokens | 3 |
| Error | null |

Raw output: `outputs/kimi-k2p6/image-smoke.json`

The model correctly identified:
- Standard number: **GB/T 13594-2025** (with note: replaces GB/T 13594-2003)
- Title: **商用车辆和挂车防抱制动系统性能要求及试验方法**
- Visible chapter titles: **none** (the page is a cover/title page)

The response was truncated at 512 completion tokens. Nearly all of the output
is chain-of-thought reasoning; the model never emitted a clean final answer
before hitting the token limit.

### Preliminary Risk Notes

- **Token limit truncation**: both responses hit the completion token limit
  (default 512), cutting off before emitting a clean answer. Increasing
  `max_tokens` is necessary for production use.
- **Chain-of-thought leakage**: the model outputs extensive reasoning text
  before the actual answer. This consumes tokens and makes structured output
  parsing harder. A stricter system prompt or post-processing may be needed.
- **Image recognition accuracy**: standard number and title were recognized
  correctly from the cover page. No hallucination observed in this single
  sample.

### JSON-Only Single-Image Request

| Item | Value |
| --- | --- |
| HTTP status | 200 |
| Elapsed | 6.770s |
| prompt_tokens | 1554 |
| completion_tokens | 617 |
| total_tokens | 2171 |
| cached_tokens | 3 |
| Error | null |

Raw output: `outputs/kimi-k2p6/json-image-smoke.json`

The stricter JSON-only prompt produced clean parseable JSON:

```json
{
  "standard_no": "GB/T 13594-2025",
  "title_zh": "商用车辆和挂车防抱制动系统性能要求及试验方法",
  "title_en": "Performance requirements and test methods of anti-lock braking system for commercial vehicle and trailer",
  "visible_chapter_titles": [],
  "page_type": "cover"
}
```

This suggests the endpoint is viable for controlled single-page structured
extraction tests, provided prompts are strict and outputs are validated.
