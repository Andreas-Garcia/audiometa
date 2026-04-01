#!/usr/bin/env bash
# Run a VHS tape for this article: injects @@ONE_TO_RULE_ABS@@ then records.
# Usage (from repo root or anywhere): bash content/articles/one_to_rule/run_vhs_tape.sh <name>.tape
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TAPE_ARG="${1:?usage: $0 <tape>.tape}"
TAPE_BASENAME="${TAPE_ARG##*/}"
[[ "$TAPE_BASENAME" == *.tape ]] || TAPE_BASENAME="${TAPE_BASENAME}.tape"
TAPE_PATH="$HERE/tapes/$TAPE_BASENAME"
[[ -f "$TAPE_PATH" ]] || {
  echo "Tape not found: $TAPE_PATH" >&2
  exit 1
}
tmp="$(mktemp -t vhs_one_to_rule.XXXXXX.tape)"
cleanup() {
  rm -f "$tmp"
}
trap cleanup EXIT
python3 -c "
from pathlib import Path
import sys

root = Path('$HERE').resolve()
tape = Path('$TAPE_PATH')
text = tape.read_text()
needle = '@@ONE_TO_RULE_ABS@@'
if needle not in text:
    sys.stderr.write(f'Error: {needle!r} missing in {tape}\n')
    sys.exit(1)
Path('$tmp').write_text(text.replace(needle, str(root)))
"
(cd "$HERE" && command vhs "$tmp")
