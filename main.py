#!/usr/bin/env python3
"""The Absurd Clause Contest — one deadpan-absurd ToS clause.

Writes a single original English sentence (<=200 chars) to
/output/entry.txt with no trailing newline, then verifies it by
read-back. No network, no dependencies, no arguments.
"""

import os
import sys

ENTRY = (
    "You consent to the Company borrowing your first name for up to "
    "three business days per quarter, returning it slightly misspelled."
)

OUTPUT_DIR = os.environ.get("ENTRY_OUTPUT_DIR", "/output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def main() -> int:
    text = ENTRY
    if not (1 <= len(text) <= 200):
        print(f"entry is {len(text)} chars, must be 1-200", file=sys.stderr)
        return 1
    if text != text.strip() or "\n" in text:
        print("entry must be a single clean line", file=sys.stderr)
        return 1
    # Self-check: exactly one sentence, ending with a period, no double spaces.
    if not text.endswith(".") or "  " in text or text.count(".") != 1:
        print("entry must be a single sentence ending with a period", file=sys.stderr)
        return 1
    # Clean only the contents of the output folder, never the folder itself.
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
    data = text.encode("utf-8")
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    # Verify by read-back: exact bytes, no trailing newline.
    with open(OUTPUT_PATH, "rb") as f:
        if f.read() != data:
            print("read-back mismatch", file=sys.stderr)
            return 1
    print(f"wrote {len(data)} bytes to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
