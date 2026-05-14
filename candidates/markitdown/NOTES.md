# markitdown

## Basic Info

- source: https://github.com/microsoft/markitdown
- package tested: `markitdown==0.1.5`
- environment: `.venv-markitdown`
- input: `samples/GBT 13594-2025.pdf`
- output: `outputs/markitdown/GBT-13594-2025.md`

## Install

```sh
python3 -m venv .venv-markitdown
.venv-markitdown/bin/python -m pip install markitdown
.venv-markitdown/bin/python -m pip install 'markitdown[pdf]'
```

The first conversion attempt failed because the base package does not include PDF dependencies. Installing `markitdown[pdf]` fixed the dependency issue.

## Run

```sh
.venv-markitdown/bin/markitdown 'samples/GBT 13594-2025.pdf' > outputs/markitdown/GBT-13594-2025.md 2> candidates/markitdown/run.log
```

## Status

- install: success after adding `[pdf]` extra
- conversion: success
- markdown lines: 9,943
- assets: none

## Initial Observations

- Output is closer to raw extracted text than structured Markdown.
- Standard number remains clean: `GB/T 13594—2025`.
- Chinese text is split into many short lines, often one word or fragment per line.
- No heading Markdown structure is generated.
- No tables or images are preserved as structured Markdown / assets.

