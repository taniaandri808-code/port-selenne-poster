#!/usr/bin/env python3
import os, struct, sys

def main():
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

    if len(data) < 25 or data[:8] != b"\x89PNG\r\n\x1a\n":
        print("Error: not a valid PNG", file=sys.stderr)
        return 1

    if data[12:16] != b"IHDR":
        print("Error: IHDR chunk not found", file=sys.stderr)
        return 1

    width, height = struct.unpack(">II", data[16:24])
    if width != 1024 or height != 1024:
        print(f"Error: dimensions {width}x{height} != 1024x1024", file=sys.stderr)
        return 1

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
