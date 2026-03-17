#!/bin/bash
# Runs a Python script with the project's venv Python (3.12+), so hooks use pinned interpreter.
# Usage: run-with-venv-python.sh <script> [script-args...]

set -e

SCRIPT="$1"
shift

if [ -z "$SCRIPT" ] || [ ! -f "$SCRIPT" ]; then
    echo "ERROR: Script path required and must exist: $SCRIPT" >&2
    exit 1
fi

# In CI, use default python3 (CI sets up the correct version)
if [ -n "$CI" ] || [ -n "$GITHUB_ACTIONS" ]; then
    exec python3 "$SCRIPT" "$@"
fi

# Use venv Python so we run with project's pinned version (3.12+)
if [ -f ".venv/bin/python3" ]; then
    exec ".venv/bin/python3" "$SCRIPT" "$@"
fi

echo "ERROR: .venv not found. Create it and install deps: python3 -m venv .venv && source .venv/bin/activate && pip install -e \".[dev]\"" >&2
exit 1
