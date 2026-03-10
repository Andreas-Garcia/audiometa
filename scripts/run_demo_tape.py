#!/usr/bin/env python3
"""Run a VHS tape and write the GIF to docs/demos/output/.
Usage: run_demo_tape.py [NAME] [--sample SAMPLE]. If NAME is omitted, select from tapes interactively."""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def _choose_tape(tapes_dir: Path) -> str | None:
    tapes = sorted(tapes_dir.glob("*.tape"))
    if not tapes:
        return None
    print("Available tapes:")
    for i, p in enumerate(tapes, 1):
        print(f"  {i}. {p.stem}")
    while True:
        try:
            raw = input("Select (number or name): ").strip()
            if not raw:
                return None
            if raw.isdigit():
                idx = int(raw)
                if 1 <= idx <= len(tapes):
                    return tapes[idx - 1].stem
            else:
                candidate = tapes_dir / f"{raw}.tape" if not raw.endswith(".tape") else tapes_dir / raw
                if candidate.is_file():
                    return candidate.stem
        except (EOFError, KeyboardInterrupt):
            return None
        print("Invalid choice. Try again.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a VHS tape from docs/demos/tapes/ and write the GIF to docs/demos/output/."
    )
    parser.add_argument(
        "name",
        nargs="?",
        default=None,
        help="Tape name (no .tape). Omit to select from available tapes interactively.",
    )
    parser.add_argument(
        "--sample",
        default="sample.mp3",
        help="Demo audio filename under docs/demos/ (default: sample.mp3).",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    tapes_dir = repo_root / "docs" / "demos" / "tapes"
    name = args.name
    if name is None:
        name = _choose_tape(tapes_dir)
        if name is None:
            print("No tape selected.", file=sys.stderr)
            sys.exit(1)
    tape_path = tapes_dir / f"{name}.tape"
    output_dir = repo_root / "docs" / "demos" / "output"
    output_gif = output_dir / f"{name}.gif"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not tape_path.is_file():
        print(f"Error: tape not found: {tape_path}", file=sys.stderr)
        sys.exit(1)

    tape_content = tape_path.read_text()
    tape_content = re.sub(
        r"^Output\s+.*$",
        f"Output docs/demos/output/{name}.gif",
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
