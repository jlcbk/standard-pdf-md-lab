# pymupdf4llm

## Basic Info

- source: https://github.com/pymupdf/pymupdf4llm
- package tested: `pymupdf4llm==1.27.2.3`
- environment: `.venv-pymupdf4llm`
- input: `samples/GBT 13594-2025.pdf`
- output: `outputs/pymupdf4llm/GBT-13594-2025.md`

## Install

```sh
python3 -m venv .venv-pymupdf4llm
.venv-pymupdf4llm/bin/python -m pip install pymupdf4llm
```

Installation log:

```text
candidates/pymupdf4llm/install.log
```

## Run

```sh
.venv-pymupdf4llm/bin/python candidates/pymupdf4llm/convert.py > candidates/pymupdf4llm/run.log 2>&1
```

## Status

- install: success
- conversion: success
- markdown length: 30,304 characters
- markdown lines: 1,062
- extracted assets: 27 PNG files

## Initial Observations

- Very fast local conversion after installation.
- Extracts many formulas / page graphic fragments as images.
- Markdown is readable enough for rough agent ingestion.
- Significant bracket artifacts appear around Chinese punctuation and symbols, for example `GB[/] T` and `1[范围]`.
- Heading detection is inconsistent; some body fragments become headings.
- Tables are present but need review and likely cleanup.

