"""The Long Roast: Lawmakers and the File They Cannot Convert — make.fun entry.

Writes one satirical sentence (<= 320 characters) roasting lawmakers who
regulate AI, crypto or the internet but cannot convert a file to PDF.
Output goes to /output/entry.txt by default, or to
$MAKEFUN_OUTPUT_DIR/entry.txt when that variable is set.
"""

import os
import sys

# The roast (one sentence, one line, no trailing newline).
# Setup: the senator wrote the law telling AI companies how to behave.
# Turn: he cannot convert his own bill to PDF. The punch lands on the
# last few words — printing it, scanning it back in, and faxing the
# scan to himself — a specific, unexpected detail instead of the worn
# "can't open a PDF" cliche.
LINE = ("The senator who wrote the law telling AI companies how to behave "
        "asked his aide to convert the bill to PDF by printing it out, "
        "scanning it back in, and faxing the scan to himself.")


def output_path():
    """Resolve the output file path from the environment."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def verify(path):
    """Read the file back and enforce the competition gate: UTF-8 text,
    1 to 320 characters, not only whitespace, exactly one line.

    Reads raw bytes first so the check is byte-exact: a stray BOM,
    a CRLF ending, or a trailing newline all fail here instead of
    slipping through a forgiving text-mode read.
    """
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")  # strict: invalid UTF-8 raises
    assert raw == LINE.encode("utf-8"), "entry bytes do not match the chosen line"
    assert 1 <= len(text) <= 320, "entry must be 1-320 chars, got %d" % len(text)
    assert text.strip(), "entry must not be only whitespace"
    assert "\n" not in text, "entry must be a single line"
    # The judge brief says one sentence only, and it must stand alone:
    # exactly one sentence-terminating period, at the very end.
    assert text.endswith("."), "entry must end with a period"
    assert text.count(".") == 1, "entry must be exactly one sentence"
    return text


def main():
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE)
    text = verify(path)
    print("wrote %s (%d chars)" % (path, len(text)))
    return path


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print("verification failed: %s" % exc, file=sys.stderr)
        sys.exit(1)
