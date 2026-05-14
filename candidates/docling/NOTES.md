# docling

status: converted

## Basic Info

- source: https://github.com/docling-project/docling
- package tested: `docling==2.93.0`
- environment: `.venv-docling`
- input: `samples/GBT 13594-2025.pdf`
- output: `outputs/docling/GBT-13594-2025.md`

## Install

```sh
python3 -m venv .venv-docling
.venv-docling/bin/python -m pip install docling
```

Installation log:

```text
candidates/docling/install.log
```

## Run

```sh
.venv-docling/bin/docling --from pdf --to md --image-export-mode referenced --table-mode accurate --no-ocr --device cpu --output outputs/docling 'samples/GBT 13594-2025.pdf' > candidates/docling/run.log 2>&1
cp 'outputs/docling/GBT 13594-2025.md' outputs/docling/GBT-13594-2025.md
```

## Status

- install: success, heavy dependency set
- conversion: success
- markdown lines: 1,006
- assets: 11 referenced images
- runtime: roughly 3 minutes for first conversion

## Initial Observations

- Structure and headings are better than `markitdown`.
- Table 1 is preserved as a Markdown table.
- Fatal issue: digits and Latin letters are heavily spaced, e.g. `GB / T 1 3 5 9 4 - 2 0 2 5`.
- Many technical symbols are split: `F b R A L`, `0. 8`, `4 0k m / h`.
- Some headings are still broken or duplicated.
