#!/usr/bin/env bash
# Side-by-side GIF: metaflac (read) vs audiometa read on the same FLAC.
# Writes final GIF to output/final/.
# Run from repo root or this dir with venv. Requires: vhs, ffmpeg, metaflac.

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../../../demo/scripts/article_output_paths.sh"
resolve_article_context_from_script "$SCRIPT_DIR"
ensure_article_output_dirs
cd "$REPO_ROOT"
LEFT="$REPO_ROOT/$WORK_DIR/read_vorbis_metaflac.gif"
RIGHT="$REPO_ROOT/$WORK_DIR/read_vorbis_audiometa.gif"
OUT="$REPO_ROOT/$FINAL_DIR/before_after_side_by_side_vorbis.gif"

cp "$ARTICLE_ABS/samples/sample.flac" "$REPO_ROOT/$WORK_DIR/demo_read_vorbis.flac"
echo "Building left (metaflac read)..."
bash "$ARTICLE_ABS/scripts/run_vhs_tape.sh" read_vorbis_metaflac.tape
echo "Building right (audiometa read)..."
bash "$ARTICLE_ABS/scripts/run_vhs_tape.sh" read_vorbis_audiometa.tape
echo "Combining side-by-side..."
ffmpeg -y -i "$LEFT" -i "$RIGHT" -filter_complex \
  "[0:v][1:v]hstack=inputs=2[stacked];[stacked]split[s0][s1];[s0]palettegen=max_colors=256[p];[s1][p]paletteuse[v]" \
  -map "[v]" "$OUT"
echo "Done: $OUT"
