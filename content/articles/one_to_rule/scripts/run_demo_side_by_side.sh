#!/usr/bin/env bash
# Generate before_only.gif and after_only.gif with VHS, then combine them
# side-by-side into before_after_side_by_side.gif. Writes final GIF to output/final/.
# Run from repo root or this dir with venv activated. Requires: vhs, ffmpeg.

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../../../demo/scripts/article_output_paths.sh"
resolve_article_context_from_script "$SCRIPT_DIR"
ensure_article_output_dirs
cd "$REPO_ROOT"
LEFT="$REPO_ROOT/$WORK_DIR/before_only.gif"
RIGHT="$REPO_ROOT/$WORK_DIR/after_only.gif"
OUT="$REPO_ROOT/$FINAL_DIR/before_after_side_by_side.gif"

echo "Building left (before_only)..."
bash "$ARTICLE_ABS/scripts/run_vhs_tape.sh" before_only.tape
echo "Building right (after_only)..."
bash "$ARTICLE_ABS/scripts/run_vhs_tape.sh" after_only.tape
echo "Combining side-by-side (palette-encoded for normal size)..."
ffmpeg -y -i "$LEFT" -i "$RIGHT" -filter_complex \
  "[0:v][1:v]hstack=inputs=2[stacked];[stacked]split[s0][s1];[s0]palettegen=max_colors=256[p];[s1][p]paletteuse[v]" \
  -map "[v]" "$OUT"
echo "Done: $OUT"
