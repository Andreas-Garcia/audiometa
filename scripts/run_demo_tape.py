#!/usr/bin/env python3
"""Run a VHS tape and write the GIF to docs/demos/output/. Usage: run_demo_tape.py NAME [--sample SAMPLE]."""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a VHS tape from docs/demos/tapes/ and write the GIF to docs/demos/output/."
    )
    parser.add_argument(
        "name",
        help="Tape name (no .tape). Same name used for the generated GIF (e.g. get_full_metadata).",
    )
    parser.add_argument(
        "--sample",
        default="sample.mp3",
        help="Demo audio filename under docs/demos/ (default: sample.mp3).",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    tapes_dir = repo_root / "docs" / "demos" / "tapes"
    tape_path = tapes_dir / f"{args.name}.tape"
    output_dir = repo_root / "docs" / "demos" / "output"
    output_gif = output_dir / f"{args.name}.gif"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not tape_path.is_file():
        print(f"Error: tape not found: {tape_path}", file=sys.stderr)
        sys.exit(1)

    tape_content = tape_path.read_text()
    tape_content = re.sub(
        r"^Output\s+.*$",
        f"Output docs/demos/output/{args.name}.gif",
        tape_content,
        count=1,
        flags=re.MULTILINE,
    )
    if args.sample != "sample.mp3":
        tape_content = tape_content.replace("docs/demos/sample.mp3", f"docs/demos/{args.sample}")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".tape", delete=False) as f:
        f.write(tape_content)
        tmp_tape = Path(f.name)

    try:
        subprocess.run(
            ["vhs", str(tmp_tape)],
            cwd=repo_root,
            check=True,
        )
    finally:
        tmp_tape.unlink(missing_ok=True)

    print(f"Output: {output_gif}")


if __name__ == "__main__":
    main()
