#!/usr/bin/env bash
# Generate before_only_vorbis.gif and after_only_vorbis.gif with VHS, then combine
# side-by-side into before_after_side_by_side_vorbis.gif. Writes to article output/.
# Run from repo root or this dir with venv activated. Requires: vhs, ffmpeg, metaflac.

set -e
cd "$(dirname "$0")/../../.."
OUT_DIR="content/articles/one_to_rule/output"
LEFT="$OUT_DIR/before_only_vorbis.gif"
RIGHT="$OUT_DIR/after_only_vorbis.gif"
OUT="$OUT_DIR/before_after_side_by_side_vorbis.gif"

mkdir -p "$OUT_DIR"
echo "Building left (before_only_vorbis, metaflac)..."
cp content/articles/one_to_rule/sample.flac content/articles/one_to_rule/demo_vorbis_before.flac
vhs content/articles/one_to_rule/tapes/before_only_vorbis.tape
echo "Building right (after_only_vorbis, audiometa write)..."
cp content/articles/one_to_rule/sample.flac content/articles/one_to_rule/demo_vorbis_after.flac
vhs content/articles/one_to_rule/tapes/after_only_vorbis.tape
echo "Combining side-by-side (palette-encoded for normal size)..."
ffmpeg -y -i "$LEFT" -i "$RIGHT" -filter_complex \
  "[0:v][1:v]hstack=inputs=2[stacked];[stacked]split[s0][s1];[s0]palettegen=max_colors=256[p];[s1][p]paletteuse[v]" \
  -map "[v]" "$OUT"
echo "Done: $OUT"
