#!/usr/bin/env bash
# Side-by-side GIF: metaflac (read) vs audiometa read on the same FLAC.
# Writes final GIF to output/final/.
# Run from repo root or this dir with venv. Requires: vhs, ffmpeg, metaflac.

set -e
cd "$(dirname "$0")/../../../.."
ARTICLE="content/articles/one_to_rule"
OUT_DIR="$ARTICLE/output"
FINAL_DIR="$OUT_DIR/final"
LEFT="$OUT_DIR/read_vorbis_metaflac.gif"
RIGHT="$OUT_DIR/read_vorbis_audiometa.gif"
OUT="$FINAL_DIR/before_after_side_by_side_vorbis.gif"

mkdir -p "$OUT_DIR" "$FINAL_DIR"
cp "$ARTICLE/samples/sample.flac" "$OUT_DIR/demo_read_vorbis.flac"
echo "Building left (metaflac read)..."
bash "$ARTICLE/scripts/run_vhs_tape.sh" read_vorbis_metaflac.tape
echo "Building right (audiometa read)..."
bash "$ARTICLE/scripts/run_vhs_tape.sh" read_vorbis_audiometa.tape
echo "Combining side-by-side..."
ffmpeg -y -i "$LEFT" -i "$RIGHT" -filter_complex \
  "[0:v][1:v]hstack=inputs=2[stacked];[stacked]split[s0][s1];[s0]palettegen=max_colors=256[p];[s1][p]paletteuse[v]" \
  -map "[v]" "$OUT"
echo "Done: $OUT"
