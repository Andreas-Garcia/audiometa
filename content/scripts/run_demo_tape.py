#!/usr/bin/env python3
"""Run a VHS tape from content/articles/<article>/tapes/ and write the GIF to that article's output/.
Lists the 5 most recently modified tape files; user selects one. Output is written to the same article's output dir.
Usage: run_demo_tape.py [ARTICLE/NAME]. Omit to select from the 5 most recent tapes interactively."""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def _find_all_tapes(articles_dir: Path) -> list[tuple[Path, str, str]]:
    result = []
    for tapes_dir in articles_dir.glob("*/tapes"):
        article = tapes_dir.parent.name
        for tape_path in tapes_dir.glob("*.tape"):
            result.append((tape_path, article, tape_path.stem))
    return result


def _five_most_recent(tapes: list[tuple[Path, str, str]]) -> list[tuple[Path, str, str]]:
    sorted_tapes = sorted(tapes, key=lambda x: x[0].stat().st_mtime, reverse=True)
    return sorted_tapes[:5]


def _choose_tape(
    recent: list[tuple[Path, str, str]], articles_dir: Path
) -> tuple[Path, str, str] | None:
    if not recent:
        return None
    print("Recent tapes (select by number or article/name):")
    for i, (tape_path, article, name) in enumerate(recent, 1):
        rel = tape_path.relative_to(articles_dir.parent)
        print(f"  {i}. {article}/{name}")
    while True:
        try:
            raw = input("Select: ").strip()
            if not raw:
                return None
            if raw.isdigit():
                idx = int(raw)
                if 1 <= idx <= len(recent):
                    return recent[idx - 1]
            else:
                if "/" in raw:
                    part_article, part_name = raw.split("/", 1)
                    part_name = part_name.replace(".tape", "")
                else:
                    part_article = None
                    part_name = raw.replace(".tape", "")
                for tape_path, article, name in recent:
                    if name == part_name and (part_article is None or article == part_article):
                        return (tape_path, article, name)
                for tape_path, article, name in _find_all_tapes(articles_dir):
                    if name == part_name and (part_article is None or article == part_article):
                        return (tape_path, article, name)
            print("Invalid choice. Try again.")
        except (EOFError, KeyboardInterrupt):
            return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a VHS tape from content/articles/ and write the GIF to that article's output/."
    )
    parser.add_argument(
        "tape",
        nargs="?",
        default=None,
        help="Tape as article/name or name. Omit to select from the 5 most recent tapes.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent.parent
    articles_dir = repo_root / "content" / "articles"
    if not articles_dir.is_dir():
        print("Error: content/articles/ not found.", file=sys.stderr)
        sys.exit(1)

    all_tapes = _find_all_tapes(articles_dir)
    if not all_tapes:
        print("No .tape files found under content/articles/*/tapes/.", file=sys.stderr)
        sys.exit(1)

    recent = _five_most_recent(all_tapes)
    if args.tape is None:
        chosen = _choose_tape(recent, articles_dir)
        if chosen is None:
            print("No tape selected.", file=sys.stderr)
            sys.exit(1)
        tape_path, article, name = chosen
    else:
        part = args.tape.strip()
        if "/" in part:
            part_article, part_name = part.split("/", 1)
            part_name = part_name.replace(".tape", "")
        else:
            part_article = None
            part_name = part.replace(".tape", "")
        found = None
        for tape_path, article, name in all_tapes:
            if name == part_name and (part_article is None or article == part_article):
                found = (tape_path, article, name)
                break
        if found is None:
            print(f"Error: tape not found: {args.tape}", file=sys.stderr)
            sys.exit(1)
        tape_path, article, name = found

    output_dir = articles_dir / article / "output"
    output_gif = output_dir / f"{name}.gif"
    output_dir.mkdir(parents=True, exist_ok=True)

    tape_content = tape_path.read_text()
    output_path_str = str(output_gif.relative_to(repo_root)).replace("\\", "/")
    tape_content = re.sub(
        r"^Output\s+.*$",
        f"Output {output_path_str}",
        tape_content,
        count=1,
        flags=re.MULTILINE,
    )

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
