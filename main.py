#!/usr/bin/env python3
"""
Poster Entry Validator and Copier

This script validates a poster.png file (must be a 1024x1024 PNG under 1 MiB)
and optionally copies it to /output/entry.png.

Modes:
  python3 main.py        # Normal mode: validates and copies to /output/entry.png
  python3 main.py --check  # Check mode: validates only, prints info, no output written
"""
import os
import struct
import sys
import argparse


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate and copy a 1024x1024 PNG poster."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate poster.png without writing output",
    )
    return parser.parse_args()


def validate_png(data: bytes) -> tuple[int, int]:
    """Validate PNG data and return (width, height). Raises ValueError on failure."""
    if len(data) < 25 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a valid PNG")
    if data[12:16] != b"IHDR":
        raise ValueError("IHDR chunk not found")
    width, height = struct.unpack(">II", data[16:24])
    if width != 1024 or height != 1024:
        raise ValueError(f"dimensions {width}x{height} != 1024x1024")
    return width, height


def main() -> int:
    args = parse_args()

    src = os.path.join(os.path.dirname(__file__), "poster.png")
    try:
        with open(src, "rb") as f:
            data = f.read()
    except OSError as e:
        print(f"Error reading {src}: {e}", file=sys.stderr)
        return 1

    if len(data) > 1048576:
        print(f"Error: file size {len(data)} exceeds 1048576 bytes", file=sys.stderr)
        return 1

    try:
        width, height = validate_png(data)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.check:
        print(f"OK: {width}x{height}, {len(data)} bytes")
        return 0

    os.makedirs("/output", exist_ok=True)
    try:
        with open("/output/entry.png", "wb") as f:
            f.write(data)
    except OSError as e:
        print(f"Error writing /output/entry.png: {e}", file=sys.stderr)
        return 1

    print("OK: copied poster.png -> /output/entry.png (1024x1024)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
