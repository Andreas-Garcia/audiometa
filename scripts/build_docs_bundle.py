#!/usr/bin/env python3
"""
Build a JSON bundle of selected docs for consumption by the Audiometa frontend.
Reads Markdown from docs/, rewrites internal links to /docs/<slug>, writes publish/docs-bundle.json.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
PUBLISH_DIR = REPO_ROOT / "publish"
OUTPUT_FILE = PUBLISH_DIR / "docs-bundle.json"

DOC_SLUGS = {
    "METADATA_FORMATS.md": "metadata-formats",
    "METADATA_FIELD_GUIDE.md": "field-support",
    "AUDIO_TECHNICAL_INFO_GUIDE.md": "audio-technical-info",
    "WRITING_METADATA.md": "writing-metadata",
}

LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)(#[\w\-]+)?\)")


def slug_to_path(slug: str) -> str:
    return f"/docs/{slug}"


def rewrite_links(content: str, _filename: str) -> str:
    def repl(match: re.Match) -> str:
        label, ref_file, anchor = match.group(1), match.group(2), match.group(3) or ""
        ref_slug = DOC_SLUGS.get(ref_file)
        if ref_slug:
            return f"[{label}]({slug_to_path(ref_slug)}{anchor})"
        return match.group(0)

    return LINK_PATTERN.sub(repl, content)


def first_heading(content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.lstrip("# ").strip()
    return ""


def main() -> None:
    PUBLISH_DIR.mkdir(exist_ok=True)
    bundle = {}

    for filename, slug in DOC_SLUGS.items():
        path = DOCS_DIR / filename
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8")
        content = rewrite_links(raw, filename)
        title = first_heading(raw)
        bundle[slug] = {"title": title or filename, "content": content}

    OUTPUT_FILE.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    sys.stdout.write(f"Wrote {OUTPUT_FILE} with {len(bundle)} docs.\n")


if __name__ == "__main__":
    main()
