#!/usr/bin/env bash
# Generate before_only.gif and after_only.gif with VHS, then combine them
# side-by-side into before_after_side_by_side.gif. Writes to article output/.
# Run from repo root or this dir with venv activated. Requires: vhs, ffmpeg.

set -e
cd "$(dirname "$0")/../../.."
OUT_DIR="content/articles/one_to_rule/output"
LEFT="$OUT_DIR/before_only.gif"
RIGHT="$OUT_DIR/after_only.gif"
OUT="$OUT_DIR/before_after_side_by_side.gif"

mkdir -p "$OUT_DIR"
echo "Building left (before_only)..."
vhs content/articles/one_to_rule/tapes/before_only.tape
echo "Building right (after_only)..."
vhs content/articles/one_to_rule/tapes/after_only.tape
echo "Combining side-by-side (palette-encoded for normal size)..."
ffmpeg -y -i "$LEFT" -i "$RIGHT" -filter_complex \
  "[0:v][1:v]hstack=inputs=2[stacked];[stacked]split[s0][s1];[s0]palettegen=max_colors=256[p];[s1][p]paletteuse[v]" \
  -map "[v]" "$OUT"
echo "Done: $OUT"
