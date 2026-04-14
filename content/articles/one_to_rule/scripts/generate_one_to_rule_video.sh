#!/usr/bin/env bash
# Hero video: intro + four reading comparisons (other tool left, audiometa right).
# Order: RIFF (WAV), ID3v2 (MP3), ID3v1 (MP3), Vorbis (FLAC).
# Run from repo root; requires venv, ffmpeg, ffprobe, metaflac, mid3v2; vhs only if recording GIFs.
# Intro requires assets/logo.mp4 (tracked) or <article>/logo.mp4.
# Comparison pages use assets/logo-round.png (or assets/logo.png) + "AudioMeta" under the right GIF (replaces plain "unified" text).
# VHS runs with cwd = the article dir (parent of this scripts/) so tapes need no in-GIF cd; Output is output/work/*.gif.
# Final deliverable is written to output/final/; intermediates (GIFs, per-cell MP4, concat list) under output/work/.
#
# Options:
#   --skip-gifs              Do not run VHS; reuse existing output/work/*.gif (fails if any required GIF is missing).
#   --final-name <filename>  Final video filename under output/final/ (default: <article>_them_all.mp4).

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../../../demo/scripts/article_output_paths.sh"
resolve_article_context_from_script "$SCRIPT_DIR"
ensure_article_output_dirs
cd "$REPO_ROOT"
VENV_BIN="$REPO_ROOT/.venv/bin"
if [[ ! -x "$VENV_BIN/audiometa" ]] || [[ ! -x "$VENV_BIN/python3" ]]; then
  echo "Error: project venv required ($VENV_BIN/audiometa and python3). Run: source .venv/bin/activate && pip install -e ." >&2
  exit 1
fi
export PATH="$VENV_BIN:$PATH"

SKIP_GIFS=0
FINAL_NAME=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-gifs)
      SKIP_GIFS=1
      shift
      ;;
    --final-name)
      [[ $# -lt 2 ]] && { echo "Error: --final-name requires a value" >&2; exit 1; }
      FINAL_NAME="$2"
      shift 2
      ;;
    -h | --help)
      sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown option: $1 (try --help)" >&2
      exit 1
      ;;
  esac
done
if [[ -z "$FINAL_NAME" ]]; then
  FINAL_NAME="${ARTICLE_NAME}_them_all.mp4"
fi
VIDEO_OUT="$REPO_ROOT/$FINAL_DIR/$FINAL_NAME"
TAPES_DIR="$ARTICLE_ABS/tapes"
CELL_W=600
# Baseline cell height was 420; overall video height is 15% lower (85% scale).
BASE_CELL_H=420
CELL_H=$((BASE_CELL_H * 70 / 100))
# Terminal strips: layout cell + 15%, then +15% again (tall panels); keep within PAGE_H (~714).
GIF_CELL_H=$((CELL_H * 115 * 115 / 10000))
INTRO_W=$((CELL_W * 2))
INTRO_H=$((CELL_H * 2))
PAGE_W=$INTRO_W
PAGE_H=$INTRO_H
INTRO_DURATION=6
SECTION_DURATION=3
# Comparison-page header band (title only; intro uses INTRO_TEXT_Y* below).
TITLE_TOP=52
# GIF hstack vertical offset — lower value = panels sit higher (tighter header).
PANELS_TOP=118
# Intro drawtext Y positions (scaled from 840px reference; higher numerator = lower on frame)
INTRO_TEXT_Y1=$((INTRO_H * 460 / (BASE_CELL_H * 2)))
INTRO_TEXT_Y2=$((INTRO_H * 540 / (BASE_CELL_H * 2)))
# Distance from bottom of GIF row to panel labels (smaller = labels lower on screen)
LABEL_BOTTOM_PAD=-20
FONT_FILE=""
for candidate in \
  "/System/Library/Fonts/Supplemental/Arial.ttf" \
  "/System/Library/Fonts/Helvetica.ttc" \
  "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" \
  "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf" \
  "$(dirname "$0")/../../fonts/Inter-Regular.ttf" \
  "assets/fonts/Inter-Regular.ttf"; do
  [[ -f "$candidate" ]] && FONT_FILE="$candidate" && break
done
FONT_OPT=""
[[ -n "$FONT_FILE" ]] && FONT_OPT=":fontfile=$FONT_FILE"

AUDIO_META_LOGO_STILL=""
for candidate in "$REPO_ROOT/assets/logo-round.png" "$REPO_ROOT/assets/logo.png"; do
  [[ -f "$candidate" ]] && AUDIO_META_LOGO_STILL="$candidate" && break
done
[[ -z "$AUDIO_META_LOGO_STILL" ]] && {
  echo "Error: static logo not found (assets/logo-round.png or assets/logo.png)." >&2
  exit 1
}

# Right column footer: scaled logo + "AudioMeta" (replacing plain "unified" text)
TAG_LOGO_PX=36
TAG_GAP=10
TAG_TEXT_W_EST=130
RIGHT_COL_MID_X=$((CELL_W + CELL_W / 2))
TAG_BRAND_W=$((TAG_LOGO_PX + TAG_GAP + TAG_TEXT_W_EST))
LABEL_ROW_Y=$((PANELS_TOP + GIF_CELL_H - LABEL_BOTTOM_PAD))
TAG_LOGO_X=$((RIGHT_COL_MID_X - TAG_BRAND_W / 2))
TAG_TEXT_X=$((TAG_LOGO_X + TAG_LOGO_PX + TAG_GAP))
TAG_LOGO_Y=$((LABEL_ROW_Y - TAG_LOGO_PX + 4))

if [[ ! -f "$ARTICLE_ABS/samples/sample.wav" ]]; then
  echo "Creating $ARTICLE_REL/samples/sample.wav from samples/sample.mp3..."
  ffmpeg -y -i "$ARTICLE_ABS/samples/sample.mp3" -map 0:a -c:a pcm_s16le "$ARTICLE_ABS/samples/sample.wav" -loglevel warning
fi

echo "Building intro..."
INTRO_MP4="$REPO_ROOT/$WORK_DIR/intro_segment.mp4"
LOGO_PATH=""
for candidate in assets/logo.mp4 "$ARTICLE_ABS/logo.mp4"; do
  [[ -f "$candidate" ]] && LOGO_PATH="$candidate" && break
done
[[ -z "$LOGO_PATH" ]] && { echo "Error: logo not found (assets/logo.mp4 or $ARTICLE_REL/logo.mp4)." >&2; exit 1; }
ffmpeg -y -f lavfi -i "color=c=0xffffff:s=${INTRO_W}x${INTRO_H}:d=${INTRO_DURATION}:r=25" \
  -stream_loop -1 -i "$LOGO_PATH" \
  -filter_complex "
    [1:v]fps=25,scale=560:-1,format=yuv420p,setpts=PTS-STARTPTS[logo];
    [0:v][logo]overlay=x=(main_w-overlay_w)/2:y=-45:eof_action=repeat[v0];
    [v0]drawtext=text='One tool for every format':fontsize=28${FONT_OPT}:fontcolor=black:borderw=1:bordercolor=white:x=(w-text_w)/2:y=${INTRO_TEXT_Y1}:enable='gte(t\,1)'[v1];
    [v1]drawtext=text='RIFF\, ID3v2\, ID3v1\, Vorbis':fontsize=22${FONT_OPT}:fontcolor=black:borderw=1:bordercolor=white:x=(w-text_w)/2:y=${INTRO_TEXT_Y2}:enable='gte(t\,3)'[v]
  " -map "[v]" -an -r 25 -c:v libx264 -pix_fmt yuv420p -t "$INTRO_DURATION" "$INTRO_MP4" -loglevel warning

echo "Building section page..."
SECTION_MP4="$REPO_ROOT/$WORK_DIR/section_unified_metadata_reading.mp4"
ffmpeg -y -f lavfi -i "color=c=0xffffff:s=${PAGE_W}x${PAGE_H}:d=${SECTION_DURATION}:r=25" \
  -vf "drawtext=text='Unified Metadata Reading':fontsize=64${FONT_OPT}:fontcolor=black:borderw=1:bordercolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
  -r 25 -c:v libx264 -pix_fmt yuv420p -t "$SECTION_DURATION" "$SECTION_MP4" -loglevel warning

if [[ "$SKIP_GIFS" -eq 0 ]]; then
  command -v vhs >/dev/null || { echo "Error: vhs not found in PATH (use --skip-gifs to reuse existing GIFs)" >&2; exit 1; }
fi
run_tape() {
  local name="$1"
  local tape_path="$TAPES_DIR/$2"
  local out="$REPO_ROOT/$WORK_DIR/$3"
  [[ -f "$tape_path" ]] || { echo "Error: tape not found: $tape_path" >&2; exit 1; }
  if [[ "$SKIP_GIFS" -eq 1 ]]; then
    [[ -f "$out" ]] || {
      echo "Error: missing $out — record GIFs first or run without --skip-gifs" >&2
      exit 1
    }
    return 0
  fi
  if [[ ! -f "$out" ]]; then
    echo "Running $name..."
    bash "$ARTICLE_ABS/scripts/run_vhs_tape.sh" "$2"
  fi
  [[ -f "$out" ]] || { echo "Error: tape did not produce: $out" >&2; exit 1; }
}

echo "Preparing demo files for ID3v1 and Vorbis..."
"$VENV_BIN/python3" "$ARTICLE_ABS/scripts/ensure_demo_read_id3v1.py"
cp "$ARTICLE_ABS/samples/sample.flac" "$REPO_ROOT/$WORK_DIR/demo_read_vorbis.flac"

if [[ "$SKIP_GIFS" -eq 1 ]]; then
  echo "Skipping VHS (--skip-gifs); using existing cell GIFs..."
else
  echo "Recording cell GIFs..."
fi
run_tape "RIFF ffprobe" "before_only_riff.tape" "before_only_riff.gif"
run_tape "RIFF audiometa" "after_only_riff.tape" "after_only_riff.gif"
run_tape "ID3v2 mid3v2" "before_only.tape" "before_only.gif"
run_tape "ID3v2 audiometa" "after_only.tape" "after_only.gif"
run_tape "ID3v1 other" "read_id3v1_other.tape" "read_id3v1_other.gif"
run_tape "ID3v1 audiometa" "read_id3v1_audiometa.tape" "read_id3v1_audiometa.gif"
run_tape "Vorbis metaflac" "read_vorbis_metaflac.tape" "read_vorbis_metaflac.gif"
run_tape "Vorbis audiometa" "read_vorbis_audiometa.tape" "read_vorbis_audiometa.gif"

PAGE_DURATION=16
echo "Converting GIFs to MP4..."
# x=0, y=0: after scale-to-cover, take the top-left CELL_W×GIF_CELL_H. VHS terminal frames are top-heavy (title + output);
# the lower part is often empty padding—bottom- or center-crop can show mostly blank (black) or misaligned hstack pairs.
for stem in before_only_riff after_only_riff before_only after_only read_id3v1_other read_id3v1_audiometa read_vorbis_metaflac read_vorbis_audiometa; do
  ffmpeg -y -i "$REPO_ROOT/$WORK_DIR/${stem}.gif" -t "$PAGE_DURATION" \
    -vf "format=rgb24,scale=${CELL_W}:${GIF_CELL_H}:force_original_aspect_ratio=increase,crop=${CELL_W}:${GIF_CELL_H}:0:0,format=yuv420p" \
    -r 25 -c:v libx264 -pix_fmt yuv420p "$REPO_ROOT/$WORK_DIR/${stem}.mp4" -loglevel warning
done

build_page_2() {
  local name="$1"
  local title_line_1="$2"
  local left_label="$3"
  local a="$4" b="$5"
  local out="$REPO_ROOT/$WORK_DIR/page_${name}.mp4"
  local title_line_1_escaped
  local left_label_escaped
  title_line_1_escaped=$(printf '%s' "$title_line_1" | sed 's/:/\\:/g; s/,/\\,/g')
  left_label_escaped=$(printf '%s' "$left_label" | sed 's/:/\\:/g; s/,/\\,/g')
  ffmpeg -y -i "$a" -i "$b" \
    -f lavfi -i "color=c=0xffffff:s=${PAGE_W}x${PAGE_H}:d=${PAGE_DURATION}:r=25" \
    -i "$AUDIO_META_LOGO_STILL" \
    -filter_complex "
      [0:v][1:v]hstack=inputs=2,format=yuv420p[row];
      [2:v][row]overlay=0:${PANELS_TOP}[withrow];
      [withrow]drawtext=text='$title_line_1_escaped':fontsize=35${FONT_OPT}:fontcolor=black:borderw=1:bordercolor=white:x=(w-text_w)/2:y=${TITLE_TOP}[v1];
      [v1]drawtext=text='$left_label_escaped':fontsize=24${FONT_OPT}:fontcolor=black:borderw=1:bordercolor=white:x=((${CELL_W}-text_w)/2):y=${LABEL_ROW_Y}[v2];
      [3:v]scale=-1:${TAG_LOGO_PX},format=yuv420p[lg];
      [v2][lg]overlay=x=${TAG_LOGO_X}:y=${TAG_LOGO_Y}[v3];
      [v3]drawtext=text='AudioMeta':fontsize=24${FONT_OPT}:fontcolor=black:borderw=1:bordercolor=white:x=${TAG_TEXT_X}:y=${LABEL_ROW_Y}[v]
    " -map "[v]" -r 25 -c:v libx264 -pix_fmt yuv420p -t "$PAGE_DURATION" "$out" -loglevel warning
}

build_page_2 "read_riff" "Reading RIFF (WAV)" "ffprobe" \
  "$REPO_ROOT/$WORK_DIR/before_only_riff.mp4" "$REPO_ROOT/$WORK_DIR/after_only_riff.mp4"
build_page_2 "read_id3v2" "Reading ID3v2 (MP3)" "mid3v2" \
  "$REPO_ROOT/$WORK_DIR/before_only.mp4" "$REPO_ROOT/$WORK_DIR/after_only.mp4"
build_page_2 "read_id3v1" "Reading ID3v1 (MP3)" "raw TAG" \
  "$REPO_ROOT/$WORK_DIR/read_id3v1_other.mp4" "$REPO_ROOT/$WORK_DIR/read_id3v1_audiometa.mp4"
build_page_2 "read_vorbis" "Reading Vorbis (FLAC)" "metaflac" \
  "$REPO_ROOT/$WORK_DIR/read_vorbis_metaflac.mp4" "$REPO_ROOT/$WORK_DIR/read_vorbis_audiometa.mp4"

echo "Concatenating final video..."
CONCAT_LIST="$REPO_ROOT/$WORK_DIR/concat_list.txt"
ABS_WORK="$(cd "$REPO_ROOT/$WORK_DIR" && pwd)"
printf "file '%s/intro_segment.mp4'\nfile '%s/section_unified_metadata_reading.mp4'\nfile '%s/page_read_riff.mp4'\nfile '%s/page_read_id3v2.mp4'\nfile '%s/page_read_id3v1.mp4'\nfile '%s/page_read_vorbis.mp4'\n" \
  "$ABS_WORK" "$ABS_WORK" "$ABS_WORK" "$ABS_WORK" "$ABS_WORK" "$ABS_WORK" \
  > "$CONCAT_LIST"
ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" -c copy "$VIDEO_OUT" -loglevel warning

if [[ -d "$REPO_ROOT/$ARTICLE_REL/linkedin/output" ]]; then
  cp "$VIDEO_OUT" "$REPO_ROOT/$ARTICLE_REL/linkedin/output/" || true
fi

echo "Done: $VIDEO_OUT"
