#!/usr/bin/env bash
# Run a VHS tape for this article: injects @@ONE_TO_RULE_ABS@@ then records.
# Usage (from repo root or anywhere): bash content/articles/one_to_rule/scripts/run_vhs_tape.sh <name>.tape
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ARTICLE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
VENV_BIN="$REPO_ROOT/.venv/bin"
if [[ ! -x "$VENV_BIN/audiometa" ]] || [[ ! -x "$VENV_BIN/python3" ]]; then
  echo "Error: use the project venv (no global audiometa): $VENV_BIN/audiometa and python3 missing." >&2
  echo "  python3 -m venv .venv && source .venv/bin/activate && pip install -e ." >&2
  exit 1
fi
export PATH="$VENV_BIN:$PATH"
TAPE_ARG="${1:?usage: $0 <tape>.tape}"
TAPE_BASENAME="${TAPE_ARG##*/}"
[[ "$TAPE_BASENAME" == *.tape ]] || TAPE_BASENAME="${TAPE_BASENAME}.tape"
TAPE_PATH="$ARTICLE_ROOT/tapes/$TAPE_BASENAME"
[[ -f "$TAPE_PATH" ]] || {
  echo "Tape not found: $TAPE_PATH" >&2
  exit 1
}
tmp="$(mktemp -t vhs_one_to_rule.XXXXXX.tape)"
cleanup() {
  rm -f "$tmp"
}
trap cleanup EXIT
"$VENV_BIN/python3" -c "
from pathlib import Path
import sys

article_root = Path('$ARTICLE_ROOT').resolve()
tape = Path('$TAPE_PATH')
text = tape.read_text()
needle = '@@ONE_TO_RULE_ABS@@'
if needle not in text:
    sys.stderr.write(f'Error: {needle!r} missing in {tape}\n')
    sys.exit(1)
Path('$tmp').write_text(text.replace(needle, str(article_root)))
"
(cd "$ARTICLE_ROOT" && command vhs "$tmp")
