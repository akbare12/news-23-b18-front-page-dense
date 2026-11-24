#!/usr/bin/env python3
"""news-23 b18 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it works from a read-only copy with MAKEFUN_OUTPUT_DIR pointed elsewhere.
Validates the PNG header (signature + IHDR) before copying.
"""
import os
import shutil
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        head = f.read(33)
    if head[:8] != PNG_SIGNATURE:
        sys.exit("entry.png: bad PNG signature")
    (length,) = struct.unpack(">I", head[8:12])
    if head[12:16] != b"IHDR" or length != 13:
        sys.exit("entry.png: bad IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != (1024, 1024):
        sys.exit("entry.png: expected 1024x1024, got %dx%d" % (width, height))
    if os.path.getsize(src) > 1024 * 1024:
        sys.exit("entry.png: over 1 MiB")
    with open(src, "rb") as f:
        data = f.read()
    # IEND trailer: 4-byte length (0) + "IEND" + 4-byte CRC = 12 bytes.
    if len(data) < 12 or data[-12:-8] != b"\x00\x00\x00\x00" or data[-8:-4] != b"IEND":
        sys.exit("entry.png: missing well-formed IEND trailer")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main()
