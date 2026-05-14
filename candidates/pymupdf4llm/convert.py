from pathlib import Path

import pymupdf4llm


ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "samples" / "GBT 13594-2025.pdf"
OUT_DIR = ROOT / "outputs" / "pymupdf4llm"
ASSET_DIR = OUT_DIR / "assets"
OUT = OUT_DIR / "GBT-13594-2025.md"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    markdown = pymupdf4llm.to_markdown(
        str(PDF),
        write_images=True,
        image_path=str(ASSET_DIR),
        image_format="png",
        dpi=150,
    )
    OUT.write_text(markdown, encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"characters {len(markdown)}")


if __name__ == "__main__":
    main()
