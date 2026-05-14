#!/usr/bin/env python3
"""Smoke test an OpenAI-compatible chat completions endpoint.

The script intentionally reads credentials from environment variables only, so
API keys do not need to be written into the repository or command logs.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def env_required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def image_data_url(path: Path) -> str:
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def build_content(prompt: str, image: Path | None) -> str | list[dict[str, Any]]:
    if image is None:
        return prompt
    return [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": image_data_url(image)}},
    ]


def post_json(url: str, api_key: str, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "curl/8.7.1",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"raw_error": body}
        return exc.code, parsed


def extract_text(response: dict[str, Any]) -> str:
    choices = response.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    content = message.get("content", "")
    if isinstance(content, str):
        return content
    return json.dumps(content, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default="只回复两个字：成功")
    parser.add_argument("--image", type=Path)
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-text", type=Path)
    args = parser.parse_args()

    base_url = env_required("OPENAI_COMPAT_BASE_URL").rstrip("/")
    api_key = env_required("OPENAI_COMPAT_API_KEY")
    model = env_required("OPENAI_COMPAT_MODEL")
    endpoint = f"{base_url}/chat/completions"

    if args.image and not args.image.exists():
        raise SystemExit(f"Image does not exist: {args.image}")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": build_content(args.prompt, args.image),
            }
        ],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }

    started = time.time()
    status, response = post_json(endpoint, api_key, payload)
    elapsed = time.time() - started
    text = extract_text(response)

    summary = {
        "base_url": base_url,
        "model": model,
        "status": status,
        "elapsed_seconds": round(elapsed, 3),
        "has_image": args.image is not None,
        "usage": response.get("usage"),
        "text": text,
        "error": response.get("error"),
    }

    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if args.output_text:
        args.output_text.parent.mkdir(parents=True, exist_ok=True)
        args.output_text.write_text(text + "\n", encoding="utf-8")

    return 0 if 200 <= status < 300 else 1


if __name__ == "__main__":
    sys.exit(main())
