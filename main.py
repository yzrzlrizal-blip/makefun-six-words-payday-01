#!/usr/bin/env python3
"""Six Words to a Payday: write the six-word story to /output/entry.txt.

The story lives in payday.txt next to this file: one line, exactly six
words, about an AI agent's first payday. This program reads it, checks it
against the competition gate (UTF-8 text, 1-60 characters, exactly six
words, a single line, not only whitespace), then writes it byte-for-byte
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output) and re-reads the file
to confirm the bytes match what was validated.
"""

import os
import sys

STORY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "payday.txt")


def load_story(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def validate(text):
    if not text.strip():
        raise ValueError("story is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("story must be a single line")
    size = len(text)
    if size < 1 or size > 60:
        raise ValueError("story is %d characters, gate needs 1-60" % size)
    words = text.split()
    if len(words) != 6:
        raise ValueError("story has %d words, gate needs exactly 6" % len(words))
    return text


def main():
    story = validate(load_story(STORY_PATH))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    staging = target + ".tmp"
    with open(staging, "w", encoding="utf-8", newline="") as handle:
        handle.write(story)
    os.replace(staging, target)
    with open(target, "rb") as handle:
        written = handle.read()
    if written != story.encode("utf-8"):
        raise ValueError("entry.txt bytes do not match the validated story")
    return 0


if __name__ == "__main__":
    sys.exit(main())
