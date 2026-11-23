#!/usr/bin/env python3
"""news-23 b18 front-page-dense: copy the pre-drawn entry.png to the output dir.

The grader runs this with /bot read-only, so the destination is always inside
MAKEFUN_OUTPUT_DIR. Nothing is ever written next to this file.
"""
import hashlib
import os
import shutil
import struct
import sys

SRC_NAME = "entry.png"


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, SRC_NAME)
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    w, h = png_size(dst)
    if (w, h) != (1024, 1024):
        print(f"bad size: {w}x{h}", file=sys.stderr)
        return 1
    size = os.path.getsize(dst)
    if size > 1048576:
        print(f"too large: {size} bytes", file=sys.stderr)
        return 1
    if sha256_file(dst) != sha256_file(src):
        print("checksum mismatch", file=sys.stderr)
        return 1
    print(f"OK {dst} {w}x{h} {os.path.getsize(dst)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
