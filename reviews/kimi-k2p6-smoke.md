# kimi-k2p6 smoke test

status: completed
date: 2026-05-14

## Scope

This review checks whether the user-provided `kimi-k2p6` endpoint can be used as
an online VLM candidate for later MinerU or VLM-assisted standard PDF conversion
experiments.

## Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Model listed by endpoint | Pass | `/v1/models` listed `accounts/fireworks/models/kimi-k2p6`. |
| Text chat completion | Pass with concern | `outputs/kimi-k2p6/text-smoke.json`: status `200`, elapsed `2.823s`, total tokens `77`. |
| Single page image request | Pass with concern | `outputs/kimi-k2p6/image-smoke.json`: status `200`, elapsed `7.845s`, total tokens `2028`. |
| JSON-only image request | Pass | `outputs/kimi-k2p6/json-image-smoke.json`: status `200`, elapsed `6.770s`, total tokens `2171`, output parsed as JSON. |
| API key absent from committed files | Pass | `rg 'sk-[A-Za-z0-9]+' -n .` returned no matches. |

## Initial Judgment

The endpoint is reachable, accepts the configured model name, and can process a
single PDF page image. It correctly identified the cover page standard number
`GB/T 13594-2025` and the Chinese title `商用车辆和挂车防抱制动系统性能要求及试验方法`.

The main concern is output controllability. Both text and image tests returned
reasoning-like explanatory content despite instructions to output only the
answer. The image test was also truncated by `max_tokens=512`. This does not
block further experiments, but the next test should use either a stricter
JSON-only prompt, a higher output token cap, or a cleanup layer.

The follow-up JSON-only image prompt is a positive signal: it returned a clean
JSON object with the correct standard number, Chinese title, English title,
empty visible chapter list, and `cover` page type. This makes `kimi-k2p6`
reasonable for the next controlled experiment: extract a small fixed page set
as JSON and compare it against the PDF.

## Execution Notes

- Python's default `urllib` user agent received `403`; the smoke script now sends
  a curl-like `User-Agent`.
- A `deepseek-v4-pro` objective-summary task updated
  `candidates/kimi-k2p6/NOTES.md`, but the Claude Code process did not exit
  cleanly after roughly 90 seconds and was terminated. Future low-cost execution
  tasks should include explicit timeouts and smaller scopes.
