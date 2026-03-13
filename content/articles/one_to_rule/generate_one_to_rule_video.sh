#!/usr/bin/env bash
# Generate the "One to rule them all" video from content/articles/one_to_rule/VIDEO_SCENARIO_ONE_TO_RULE.md.
# Parts: intro (title + subtitles), then 4 pages with 2 panels each: Read (id3v2, riff) and Write (id3v1, vorbis).
# All cell GIFs come from VHS tapes; no placeholders. Fails early if logo or any required tape output is missing.
# Run from repo root; requires venv, vhs, ffmpeg, ffprobe, metaflac, mid3v2.

set -e
cd "$(dirname "$0")/../../.."
OUT_DIR="content/articles/one_to_rule/output"
SHARED_OUT="content/articles/one_to_rule/output"
VIDEO_OUT="$OUT_DIR/one_to_rule_them_all.mp4"
TAPES_DIR="content/articles/one_to_rule/tapes"
CELL_W=600
CELL_H=350
# All segments same size (intro and content pages)
INTRO_W=$((CELL_W * 2))
INTRO_H=$((CELL_H * 2))
PAGE_W=$INTRO_W
PAGE_H=$INTRO_H
# Intro duration (seconds)
INTRO_DURATION=5
# Content page: title band height (space above panels)
TITLE_TOP=30
PANELS_TOP=80
# Font: use same style as logo (clean sans-serif). Auto-detect from common paths, or set FONT_FILE to override.
FONT_FILE=""
for candidate in \
  "/System/Library/Fonts/Supplemental/Arial.ttf" \
  "/System/Library/Fonts/Helvetica.ttc" \
  "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" \
  "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf" \
  "$(dirname "$0")/../fonts/Inter-Regular.ttf" \
  "assets/fonts/Inter-Regular.ttf"; do
  [[ -f "$candidate" ]] && FONT_FILE="$candidate" && break
done
FONT_OPT=""
[[ -n "$FONT_FILE" ]] && FONT_OPT=":fontfile=$FONT_FILE"

mkdir -p "$OUT_DIR"

# 1. Ensure sample.wav exists
if [[ ! -f content/articles/one_to_rule/sample.wav ]]; then
  echo "Creating content/articles/one_to_rule/sample.wav from sample.mp3..."
  ffmpeg -y -i content/articles/one_to_rule/sample.mp3 -map 0:a -c:a pcm_s16le content/articles/one_to_rule/sample.wav -loglevel warning
fi

# 2. Intro segment: logo required, then title and subtitle (staggered). Fails if logo missing.
echo "Building intro..."
INTRO_MP4="$OUT_DIR/intro_segment.mp4"
LOGO_PATH=""
for candidate in assets/logo.png content/articles/one_to_rule/logo.png; do
  if [[ -f "$candidate" ]]; then
    LOGO_PATH="$candidate"
    break
  fi
done
[[ -z "$LOGO_PATH" ]] && { echo "Error: logo not found (expected assets/logo.png or content/articles/one_to_rule/logo.png)." >&2; exit 1; }
# White background (same as logo). Logo at top; title and subtitles in lower half, text in black.
# Escape commas in drawtext: use '\,' so they are not parsed as filter separators
ffmpeg -y -f lavfi -i "color=c=0xffffff:s=${INTRO_W}x${INTRO_H}:d=${INTRO_DURATION}:r=25" -i "$LOGO_PATH" \
  -filter_complex "
    [1:v]scale=560:-1[logo];
    [0:v][logo]overlay=x=(main_w-overlay_w)/2:y=-45[v0];
    [v0]drawtext=text='One audio metadata manager to rule them all':fontsize=28${FONT_OPT}:fontcolor=black:borderw=1:bordercolor=white:x=(w-text_w)/2:y=420:enable='gte(t,1)'[v1];
    [v1]drawtext=text='MP3\, WAV\, FLAC | ID3v1\, ID3v2\, Vorbis\, RIFF':fontsize=22${FONT_OPT}:fontcolor=black:borderw=1:bordercolor=white:x=(w-text_w)/2:y=500:enable='gte(t,3)'[v]
  " -map "[v]" -r 25 -c:v libx264 -pix_fmt yuv420p -t "$INTRO_DURATION" "$INTRO_MP4" -loglevel warning

# 3. Build cell GIFs from tapes only (no placeholders). Run VHS when needed; fail if output missing.
run_tape() {
  local name="$1"
  local tape="$TAPES_DIR/$2"
  local out="$SHARED_OUT/$3"
  [[ -f "$tape" ]] || { echo "Error: tape not found: $tape" >&2; exit 1; }
  if [[ ! -f "$out" ]]; then
    if [[ "$2" == before_only_vorbis.tape ]]; then
      cp content/articles/one_to_rule/sample.flac content/articles/one_to_rule/demo_vorbis_before.flac || true
    elif [[ "$2" == after_only_vorbis.tape ]]; then
      cp content/articles/one_to_rule/sample.flac content/articles/one_to_rule/demo_vorbis_after.flac || true
    fi
    echo "Running $name..."
    vhs "$tape"
  fi
  [[ -f "$out" ]] || { echo "Error: tape did not produce: $out" >&2; exit 1; }
}

echo "Building Read cells (id3v2, riff)..."
run_tape "before_only (ID3v2)" "before_only.tape" "before_only.gif"
run_tape "after_only (ID3v2)" "after_only.tape" "after_only.gif"
run_tape "before_only_riff" "before_only_riff.tape" "before_only_riff.gif"
run_tape "after_only_riff" "after_only_riff.tape" "after_only_riff.gif"

echo "Building Write cells (id3v1, vorbis)..."
run_tape "before_only_id3v1" "before_only_id3v1.tape" "before_only_id3v1.gif"
run_tape "after_only_id3v1" "after_only_id3v1.tape" "after_only_id3v1.gif"
run_tape "before_only_vorbis" "before_only_vorbis.tape" "before_only_vorbis.gif"
run_tape "after_only_vorbis" "after_only_vorbis.tape" "after_only_vorbis.gif"

cp "$SHARED_OUT/before_only.gif" "$OUT_DIR/cell_before_read_id3v2.gif"
cp "$SHARED_OUT/after_only.gif" "$OUT_DIR/cell_now_read_id3v2.gif"
cp "$SHARED_OUT/before_only_riff.gif" "$OUT_DIR/cell_before_read_riff.gif"
cp "$SHARED_OUT/after_only_riff.gif" "$OUT_DIR/cell_now_read_riff.gif"
cp "$SHARED_OUT/before_only_id3v1.gif" "$OUT_DIR/cell_before_write_id3v1.gif"
cp "$SHARED_OUT/after_only_id3v1.gif" "$OUT_DIR/cell_now_write_id3v1.gif"
cp "$SHARED_OUT/before_only_vorbis.gif" "$OUT_DIR/cell_before_write_vorbis.gif"
cp "$SHARED_OUT/after_only_vorbis.gif" "$OUT_DIR/cell_now_write_vorbis.gif"

# 4. Build 4 pages (2 panels each): same size as intro (PAGE_W x PAGE_H), title in reserved band, panels below.
PAGE_DURATION=8
build_page_2() {
  local name="$1"
  local title="$2"
  local a="$3" b="$4"
  local out="$OUT_DIR/page_${name}.mp4"
  local title_escaped
  title_escaped=$(printf '%s' "$title" | sed 's/:/\\:/g; s/,/\\,/g')
  ffmpeg -y -stream_loop -1 -i "$a" -stream_loop -1 -i "$b" \
    -f lavfi -i "color=c=0x282a36:s=${PAGE_W}x${PAGE_H}:d=${PAGE_DURATION}:r=25" \
    -filter_complex "
      [0:v]scale=${CELL_W}:${CELL_H}:force_original_aspect_ratio=increase,crop=${CELL_W}:${CELL_H}:(iw-${CELL_W})/2:(ih-${CELL_H})/2,trim=duration=${PAGE_DURATION},setpts=PTS-STARTPTS[v0];
      [1:v]scale=${CELL_W}:${CELL_H}:force_original_aspect_ratio=increase,crop=${CELL_W}:${CELL_H}:(iw-${CELL_W})/2:(ih-${CELL_H})/2,trim=duration=${PAGE_DURATION},setpts=PTS-STARTPTS[v1];
      [v0][v1]hstack=inputs=2[row];
      [2:v][row]overlay=0:${PANELS_TOP}[withrow];
      [withrow]drawtext=text='$title_escaped':fontsize=24${FONT_OPT}:fontcolor=white:borderw=2:bordercolor=black:x=(w-text_w)/2:y=${TITLE_TOP}[v]
    " -map "[v]" -r 25 -c:v libx264 -pix_fmt yuv420p -t "$PAGE_DURATION" "$out" -loglevel warning
}

build_page_2 "before_read" "Before: Reading (mid3v2, ffprobe)" \
  "$OUT_DIR/cell_before_read_id3v2.gif" \
  "$OUT_DIR/cell_before_read_riff.gif"

build_page_2 "now_read" "Now: Reading with AudioMeta (ID3v2, RIFF)" \
  "$OUT_DIR/cell_now_read_id3v2.gif" \
  "$OUT_DIR/cell_now_read_riff.gif"

build_page_2 "before_write" "Before: Writing (ID3v1, Vorbis)" \
  "$OUT_DIR/cell_before_write_id3v1.gif" \
  "$OUT_DIR/cell_before_write_vorbis.gif"

build_page_2 "now_write" "Now: Writing with AudioMeta (ID3v1, Vorbis)" \
  "$OUT_DIR/cell_now_write_id3v1.gif" \
  "$OUT_DIR/cell_now_write_vorbis.gif"

# 5. Concat intro + 4 pages (use absolute paths for concat)
echo "Concatenating final video..."
CONCAT_LIST="$OUT_DIR/concat_list.txt"
ABS_OUT="$(cd "$OUT_DIR" && pwd)"
printf "file '%s/intro_segment.mp4'\nfile '%s/page_before_read.mp4'\nfile '%s/page_now_read.mp4'\nfile '%s/page_before_write.mp4'\nfile '%s/page_now_write.mp4'\n" \
  "$ABS_OUT" "$ABS_OUT" "$ABS_OUT" "$ABS_OUT" "$ABS_OUT" \
  > "$CONCAT_LIST"
ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" -c copy "$VIDEO_OUT" -loglevel warning

echo "Done: $VIDEO_OUT"
