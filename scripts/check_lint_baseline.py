#!/usr/bin/env python3
"""Verify vendored Ruff baseline digest and strict pyproject overlay + mypy baseline."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path

REQUIRED_RUFF_EXTEND = "baselines/ruff.toml"
ALLOWED_RUFF_TOP = {"extend", "exclude", "extend-exclude", "lint"}
ALLOWED_RUFF_LINT_OVERLAY = {"per-file-ignores", "extend-per-file-ignores"}
MYPY_OPTIONAL_KEYS = {"overrides"}


def _repo_root(argv: list[str]) -> Path:
    if len(argv) > 1:
        return Path(argv[1]).resolve()
    return Path.cwd().resolve()


def _parse_digests(content: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([a-fA-F0-9]{64})\s+(\S+)\s*$", line)
        if not m:
            print(f"Invalid DIGESTS line (expected '<64-hex>  <path>'): {line!r}", file=sys.stderr)
            sys.exit(1)
        out[m.group(2)] = m.group(1).lower()
    return out


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _verify_digests(repo: Path) -> None:
    digests_path = repo / "baselines" / "DIGESTS"
    if not digests_path.is_file():
        print(f"Missing {digests_path.relative_to(repo)}", file=sys.stderr)
        sys.exit(1)
    expected = _parse_digests(digests_path.read_text(encoding="utf-8"))
    if not expected:
        print("baselines/DIGESTS has no digest entries.", file=sys.stderr)
        sys.exit(1)
    for rel, want in expected.items():
        target = repo / rel
        if not target.is_file():
            print(f"Missing file for digest entry {rel!r}", file=sys.stderr)
            sys.exit(1)
        got = _sha256_file(target)
        if got != want:
            print(
                f"SHA-256 mismatch for {rel}:\n  expected {want}\n  actual   {got}",
                file=sys.stderr,
            )
            sys.exit(1)


def _verify_ruff_overlay(pyproject: dict) -> None:
    tool = pyproject.get("tool") or {}
    ruff = tool.get("ruff") or {}
    if ruff.get("extend") != REQUIRED_RUFF_EXTEND:
        print(
            f'[tool.ruff] must set extend = "{REQUIRED_RUFF_EXTEND}" '
            f'(got {ruff.get("extend")!r}).',
            file=sys.stderr,
        )
        sys.exit(1)
    for key in ruff:
        if key not in ALLOWED_RUFF_TOP:
            print(
                f"Disallowed [tool.ruff] key {key!r}: move settings into baselines/ruff.toml "
                "or use only extend, exclude, extend-exclude, lint (per-file ignores).",
                file=sys.stderr,
            )
            sys.exit(1)
    lint = ruff.get("lint")
    if lint is None:
        return
    if not isinstance(lint, dict):
        print("[tool.ruff.lint] must be a table.", file=sys.stderr)
        sys.exit(1)
    for key in lint:
        if key not in ALLOWED_RUFF_LINT_OVERLAY:
            print(
                f"Disallowed [tool.ruff.lint] key {key!r}: only "
                f"{sorted(ALLOWED_RUFF_LINT_OVERLAY)} are allowed in pyproject.toml "
                "(rule selection belongs in baselines/ruff.toml).",
                file=sys.stderr,
            )
            sys.exit(1)


def _verify_mypy(repo: Path, pyproject: dict) -> None:
    expected_path = repo / "baselines" / "expected-mypy.json"
    if not expected_path.is_file():
        print(f"Missing {expected_path.relative_to(repo)}", file=sys.stderr)
        sys.exit(1)
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    tool = pyproject.get("tool") or {}
    mypy = tool.get("mypy")
    if not isinstance(mypy, dict):
        print("Missing or invalid [tool.mypy] table.", file=sys.stderr)
        sys.exit(1)
    for key, want in expected.items():
        if key not in mypy:
            print(f"Missing required [tool.mypy] key {key!r}.", file=sys.stderr)
            sys.exit(1)
        if mypy[key] != want:
            print(
                f"[tool.mypy] key {key!r} must equal baseline {want!r} (got {mypy[key]!r}).",
                file=sys.stderr,
            )
            sys.exit(1)
    for key in mypy:
        if key in expected:
            continue
        if key not in MYPY_OPTIONAL_KEYS:
            print(
                f"Disallowed extra [tool.mypy] key {key!r}: only {sorted(MYPY_OPTIONAL_KEYS)} "
                "may be added beyond the baseline.",
                file=sys.stderr,
            )
            sys.exit(1)
    overrides = mypy.get("overrides")
    if overrides is None:
        return
    if not isinstance(overrides, list):
        print("[tool.mypy.overrides] must be an array of tables.", file=sys.stderr)
        sys.exit(1)
    for i, block in enumerate(overrides):
        if not isinstance(block, dict):
            print(f"[tool.mypy.overrides][{i}] must be a table.", file=sys.stderr)
            sys.exit(1)


def main() -> None:
    repo = _repo_root(sys.argv)
    pyproject_path = repo / "pyproject.toml"
    if not pyproject_path.is_file():
        print("Missing pyproject.toml", file=sys.stderr)
        sys.exit(1)
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    _verify_digests(repo)
    _verify_ruff_overlay(data)
    _verify_mypy(repo, data)
    print("Lint baseline checks passed.")


if __name__ == "__main__":
    main()
