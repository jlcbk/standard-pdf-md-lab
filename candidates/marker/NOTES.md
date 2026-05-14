# marker

status: aborted

## Basic Info

- source: https://github.com/datalab-to/marker
- package tested: `marker-pdf==1.10.2`
- environment: `.venv-marker`
- input: `samples/GBT 13594-2025.pdf`
- intended output: `outputs/marker/`

## Install

```sh
python3 -m venv .venv-marker
.venv-marker/bin/python -m pip install marker-pdf
```

Installation log:

```text
candidates/marker/install.log
```

## Run Attempt

```sh
.venv-marker/bin/marker_single 'samples/GBT 13594-2025.pdf' --output_dir outputs/marker --output_format markdown --disable_ocr > candidates/marker/run.log 2>&1
```

## Status

- install: success
- conversion: aborted manually
- output: none
- reason: local CPU run time was not practical

## Runtime Notes

- First run downloaded a large layout model around 1.35GB.
- It then downloaded an OCR error detection model around 258MB.
- After model downloads, layout recognition reached only `1/27` pages after about 112 seconds.
- Extrapolated full conversion time on this machine was roughly 45-60 minutes for one 28-page PDF.
- Because the goal is batch conversion of standards, this is too expensive for the first-pass pipeline.

## Decision

Keep as a possible heavyweight fallback only if a GPU or faster inference environment is available. Do not continue with local CPU testing as the main path.
