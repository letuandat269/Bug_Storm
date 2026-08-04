#!/usr/bin/env python3
"""Convert the Bug_Storm `lcd d` shell dump into a pixel-perfect PNG."""

from __future__ import annotations

import argparse
import re
import struct
import zlib
from pathlib import Path

WIDTH = 128
HEIGHT = 64
FRAMEBUFFER_SIZE = WIDTH * HEIGHT // 8
START_MARKER = "[DUMP] frame buffer lcd => start"
END_MARKER = "[DUMP] frame buffer lcd => end"


def read_framebuffer(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if START_MARKER in text:
        text = text.split(START_MARKER, 1)[1]
    if END_MARKER in text:
        text = text.split(END_MARKER, 1)[0]

    values = [int(token, 16) for token in re.findall(r"0x([0-9A-Fa-f]{2})", text)]
    if len(values) != FRAMEBUFFER_SIZE:
        raise ValueError(
            f"expected {FRAMEBUFFER_SIZE} bytes for {WIDTH}x{HEIGHT}, got {len(values)}"
        )
    return bytes(values)


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body))


def write_png(framebuffer: bytes, output: Path, scale: int, invert: bool) -> None:
    scaled_width = WIDTH * scale
    scaled_height = HEIGHT * scale
    rows = bytearray()

    for y in range(HEIGHT):
        source_row = bytearray()
        page = y // 8
        mask = 1 << (y % 8)
        for x in range(WIDTH):
            pixel_on = bool(framebuffer[page * WIDTH + x] & mask)
            if invert:
                pixel_on = not pixel_on
            source_row.extend([255 if pixel_on else 0] * scale)
        encoded_row = b"\x00" + bytes(source_row)
        for _ in range(scale):
            rows.extend(encoded_row)

    png = bytearray(b"\x89PNG\r\n\x1a\n")
    png.extend(png_chunk(b"IHDR", struct.pack(">IIBBBBB", scaled_width, scaled_height, 8, 0, 0, 0, 0)))
    png.extend(png_chunk(b"IDAT", zlib.compress(bytes(rows), 9)))
    png.extend(png_chunk(b"IEND", b""))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(png)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert the 1024-byte output of the firmware command `lcd d` to PNG."
    )
    parser.add_argument("dump", type=Path, help="text file containing the `lcd d` output")
    parser.add_argument("output", type=Path, help="destination PNG file")
    parser.add_argument("--scale", type=int, default=6, help="nearest-neighbor scale (default: 6)")
    parser.add_argument("--invert", action="store_true", help="invert black and white pixels")
    args = parser.parse_args()

    if args.scale < 1:
        parser.error("--scale must be at least 1")

    framebuffer = read_framebuffer(args.dump)
    write_png(framebuffer, args.output, args.scale, args.invert)
    print(f"wrote {args.output} ({WIDTH * args.scale}x{HEIGHT * args.scale})")


if __name__ == "__main__":
    main()
