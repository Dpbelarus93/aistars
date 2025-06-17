#!/usr/bin/env python3
"""
extract_white_text.py

Utility script to isolate white text (or other nearly-white graphics) on a dark/black
background and export it as a transparent-background PNG.

How it works
------------
1. Converts each input image to RGBA.
2. For every pixel, if its RGB components are above a brightness threshold
   (default 200/255) it is kept as pure white (255,255,255,255).
3. Otherwise the pixel is made fully transparent (alpha = 0).

Resulting files are stored in the project-level folder «логотипы» with the same
basename and .png extension.

Usage
-----
$ python code/extract_white_text.py [SOURCE_DIR] [THRESHOLD]

• SOURCE_DIR   – directory with source images. Defaults to the current dir.
• THRESHOLD    – 0-255 brightness cutoff. Optional (default 200).

Example:
$ python code/extract_white_text.py ~/Desktop/хочу\ еще/logos_raw 220
"""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Tuple

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    print("[ERROR] Pillow is required: pip install pillow", file=sys.stderr)
    sys.exit(1)


def process_image(img_path: Path, out_dir: Path, threshold: int) -> None:
    """Convert black-bg image to transparent PNG containing only white text."""
    with Image.open(img_path) as im:
        im = im.convert("RGBA")
        pixels = im.getdata()

        def is_white(rgb: Tuple[int, int, int]) -> bool:
            r, g, b = rgb
            return r >= threshold and g >= threshold and b >= threshold

        new_pixels = [
            (255, 255, 255, 255) if is_white(rgb[:3]) else (255, 255, 255, 0)
            for rgb in pixels
        ]
        im.putdata(new_pixels)

        out_path = out_dir / f"{img_path.stem}.png"
        im.save(out_path, "PNG")
        print(f"[OK] Saved → {out_path}")


def main() -> None:
    src_dir = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else Path.cwd()
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 200

    # Determine project root (two levels up from this script) and output directory
    project_root = Path(__file__).resolve().parents[1]
    out_dir = project_root / "логотипы"
    out_dir.mkdir(exist_ok=True)

    supported_patterns = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tif", "*.tiff")
    to_process = [p for pattern in supported_patterns for p in src_dir.glob(pattern)]

    if not to_process:
        print(f"[INFO] No images found in {src_dir}")
        return

    print(f"[INFO] Processing {len(to_process)} image(s) → {out_dir}")
    for img_path in to_process:
        try:
            process_image(img_path, out_dir, threshold)
        except Exception as e:  # pragma: no cover
            print(f"[WARN] Failed on {img_path.name}: {e}")


if __name__ == "__main__":
    main() 