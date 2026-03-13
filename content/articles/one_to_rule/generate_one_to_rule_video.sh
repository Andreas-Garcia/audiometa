#!/usr/bin/env bash
# Generate the "One to rule them all" video from content/articles/one_to_rule/VIDEO_SCENARIO_ONE_TO_RULE.md.
# Parts: intro (title + subtitles), Before Read 2x2, Now Read 2x2, Before Write 2x2, Now Write 2x2.
# Lives in content/articles/one_to_rule/. Run from anywhere; requires venv, vhs, ffmpeg. Optional: metaflac, mid3v2 (for before cells).
# Writes to content/articles/one_to_rule/output/.

set -e
cd "$(dirname "$0")/../../.."
OUT_DIR="content/articles/one_to_rule/output"
SHARED_OUT="content/articles/one_to_rule/output"
VIDEO_OUT="$OUT_DIR/one_to_rule_them_all.mp4"
CELL_W=600
CELL_H=350
PAGE_W=$((CELL_W * 2))
PAGE_H=$((CELL_H * 2))
# Intro duration (seconds)
INTRO_DURATION=14

mkdir -p "$OUT_DIR"

# 1. Ensure sample.wav exists
if [[ ! -f content/articles/one_to_rule/sample.wav ]]; then
  echo "Creating content/articles/one_to_rule/sample.wav from sample.mp3..."
  ffmpeg -y -i content/articles/one_to_rule/sample.mp3 -map 0:a -c:a pcm_s16le content/articles/one_to_rule/sample.wav -loglevel warning
fi

# 2. Intro segment: logo (if present), then title, then subtitle 1, then subtitle 2 (staggered)
echo "Building intro..."
INTRO_MP4="$OUT_DIR/intro_segment.mp4"
LOGO_PATH=""
for candidate in assets/logo.png content/articles/one_to_rule/logo.png; do
  if [[ -f "$candidate" ]]; then
    LOGO_PATH="$candidate"
    break
  fi
done
# White background (same as logo). Logo at top; title and subtitles in lower half, text in black.
# Escape commas in drawtext: use '\,' so they are not parsed as filter separators
if [[ -n "$LOGO_PATH" ]]; then
  # With logo: [0]=color [1]=logo → scale logo, overlay, then drawtext (black text, lower half)
  ffmpeg -y -f lavfi -i "color=c=0xffffff:s=${PAGE_W}x${PAGE_H}:d=${INTRO_DURATION}:r=25" -i "$LOGO_PATH" \
    -filter_complex "
      [1:v]scale=560:-1[logo];
      [0:v][logo]overlay=x=(main_w-overlay_w)/2:y=30[v0];
      [v0]drawtext=text='AudioMeta - One audio metadata manager to rule them all':fontsize=28:fontcolor=black:borderw=1:bordercolor=white:x=(w-text_w)/2:y=420:enable='gte(t,2)'[v1];
      [v1]drawtext=text='Main formats\: MP3\, WAV\, FLAC':fontsize=22:fontcolor=black:borderw=1:bordercolor=white:x=(w-text_w)/2:y=500:enable='gte(t,6)'[v2];
      [v2]drawtext=text='Main metadata formats\: ID3v1\, ID3v2\, Vorbis\, RIFF':fontsize=22:fontcolor=black:borderw=1:bordercolor=white:x=(w-text_w)/2:y=560:enable='gte(t,10)'[v]
    " -map "[v]" -r 25 -c:v libx264 -pix_fmt yuv420p -t "$INTRO_DURATION" "$INTRO_MP4" -loglevel warning
else
  ffmpeg -y -f lavfi -i "color=c=0xffffff:s=${PAGE_W}x${PAGE_H}:d=${INTRO_DURATION}:r=25" \
    -vf "
      drawtext=text='AudioMeta - One audio metadata manager to rule them all':fontsize=28:fontcolor=black:borderw=1:bordercolor=white:x=(w-text_w)/2:y=320:enable='gte(t,2)',
      drawtext=text='Main formats\: MP3\, WAV\, FLAC':fontsize=22:fontcolor=black:borderw=1:bordercolor=white:x=(w-text_w)/2:y=400:enable='gte(t,6)',
      drawtext=text='Main metadata formats\: ID3v1\, ID3v2\, Vorbis\, RIFF':fontsize=22:fontcolor=black:borderw=1:bordercolor=white:x=(w-text_w)/2:y=460:enable='gte(t,10)'
    " \
    -r 25 -c:v libx264 -pix_fmt yuv420p -t "$INTRO_DURATION" "$INTRO_MP4" -loglevel warning
fi

# 3. Build cell GIFs for Before Read (reuse shared tape GIFs)
echo "Building Before Read cells..."
if [[ ! -f "$SHARED_OUT/before_only.gif" ]]; then
  vhs content/articles/one_to_rule/tapes/before_only.tape
fi
if [[ ! -f "$SHARED_OUT/before_only_vorbis.gif" ]]; then
  cp content/articles/one_to_rule/sample.flac content/articles/one_to_rule/demo_vorbis_before.flac 2>/dev/null || true
  vhs content/articles/one_to_rule/tapes/before_only_vorbis.tape
fi
cp "$SHARED_OUT/before_only.gif" "$OUT_DIR/cell_before_read_id3v1.gif" 2>/dev/null || true
cp "$SHARED_OUT/before_only.gif" "$OUT_DIR/cell_before_read_id3v2.gif" 2>/dev/null || true
cp "$SHARED_OUT/before_only_vorbis.gif" "$OUT_DIR/cell_before_read_vorbis.gif" 2>/dev/null || true
# RIFF placeholder (no tape yet)
if [[ ! -f "$OUT_DIR/cell_before_read_riff.gif" ]]; then
  ffmpeg -y -f lavfi -i "color=c=0x282a36:s=${CELL_W}x${CELL_H}:d=5:r=25" \
    -vf "drawtext=text='RIFF (ffprobe)':fontsize=20:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
    -r 25 "$OUT_DIR/cell_before_read_riff.gif" -loglevel warning
fi
for cell in id3v1 id3v2 riff vorbis; do
  if [[ ! -f "$OUT_DIR/cell_before_read_$cell.gif" ]]; then
    ffmpeg -y -f lavfi -i "color=c=0x282a36:s=${CELL_W}x${CELL_H}:d=5:r=25" \
      -vf "drawtext=text='Before read - $cell':fontsize=18:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
      -r 25 "$OUT_DIR/cell_before_read_$cell.gif" -loglevel warning
  fi
done

# 4. Build Now Read cells (reuse shared after_only, after_only_vorbis + placeholder for RIFF)
echo "Building Now Read cells..."
if [[ ! -f "$SHARED_OUT/after_only.gif" ]]; then
  vhs content/articles/one_to_rule/tapes/after_only.tape
fi
if [[ ! -f "$SHARED_OUT/after_only_vorbis.gif" ]]; then
  cp content/articles/one_to_rule/sample.flac content/articles/one_to_rule/demo_vorbis_after.flac 2>/dev/null || true
  vhs content/articles/one_to_rule/tapes/after_only_vorbis.tape
fi
cp "$SHARED_OUT/after_only.gif" "$OUT_DIR/cell_now_read_id3v1.gif" 2>/dev/null || true
cp "$SHARED_OUT/after_only.gif" "$OUT_DIR/cell_now_read_id3v2.gif" 2>/dev/null || true
cp "$SHARED_OUT/after_only_vorbis.gif" "$OUT_DIR/cell_now_read_vorbis.gif" 2>/dev/null || true
if [[ ! -f "$OUT_DIR/cell_now_read_riff.gif" ]]; then
  ffmpeg -y -f lavfi -i "color=c=0x282a36:s=${CELL_W}x${CELL_H}:d=5:r=25" \
    -vf "drawtext=text='audiometa read (RIFF)':fontsize=18:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
    -r 25 "$OUT_DIR/cell_now_read_riff.gif" -loglevel warning
fi
for cell in id3v1 id3v2 riff vorbis; do
  if [[ ! -f "$OUT_DIR/cell_now_read_$cell.gif" ]]; then
    ffmpeg -y -f lavfi -i "color=c=0x282a36:s=${CELL_W}x${CELL_H}:d=5:r=25" \
      -vf "drawtext=text='Now read - $cell':fontsize=18:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
      -r 25 "$OUT_DIR/cell_now_read_$cell.gif" -loglevel warning
  fi
done

# 5. Build Before Write and Now Write cells (reuse vorbis GIFs from shared, placeholders for rest)
echo "Building Before Write and Now Write cells..."
cp "$SHARED_OUT/before_only_vorbis.gif" "$OUT_DIR/cell_before_write_vorbis.gif" 2>/dev/null || true
cp "$SHARED_OUT/after_only_vorbis.gif" "$OUT_DIR/cell_now_write_vorbis.gif" 2>/dev/null || true
for cell in id3v1 id3v2 riff; do
  for when in before now; do
    out="$OUT_DIR/cell_${when}_write_$cell.gif"
    if [[ ! -f "$out" ]]; then
      label="${when^} write - $cell"
      ffmpeg -y -f lavfi -i "color=c=0x282a36:s=${CELL_W}x${CELL_H}:d=5:r=25" \
        -vf "drawtext=text='$label':fontsize=18:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
        -r 25 "$out" -loglevel warning
    fi
  done
done
for cell in vorbis; do
  if [[ ! -f "$OUT_DIR/cell_before_write_$cell.gif" ]]; then
    cp "$SHARED_OUT/before_only_vorbis.gif" "$OUT_DIR/cell_before_write_$cell.gif"
  fi
  if [[ ! -f "$OUT_DIR/cell_now_write_$cell.gif" ]]; then
    cp "$SHARED_OUT/after_only_vorbis.gif" "$OUT_DIR/cell_now_write_$cell.gif"
  fi
done

# 6. Build 4 pages (2x2 grid each). Loop each GIF so we have enough length, then scale/pad/trim to PAGE_DURATION.
PAGE_DURATION=8
build_page() {
  local name="$1"
  local title="$2"
  shift 2
  local a="$1" b="$2" c="$3" d="$4"
  local out="$OUT_DIR/page_${name}.mp4"
  # Escape colons and commas in title for ffmpeg drawtext
  local title_escaped
  title_escaped=$(printf '%s' "$title" | sed 's/:/\\:/g; s/,/\\,/g')
  # Loop each GIF input (-stream_loop -1), scale and pad to CELL_WxCELL_H, trim to PAGE_DURATION
  ffmpeg -y -stream_loop -1 -i "$a" -stream_loop -1 -i "$b" -stream_loop -1 -i "$c" -stream_loop -1 -i "$d" \
    -filter_complex "
      [0:v]scale=${CELL_W}:${CELL_H}:force_original_aspect_ratio=decrease,pad=${CELL_W}:${CELL_H}:(ow-iw)/2:(oh-ih)/2,trim=duration=${PAGE_DURATION},setpts=PTS-STARTPTS[v0];
      [1:v]scale=${CELL_W}:${CELL_H}:force_original_aspect_ratio=decrease,pad=${CELL_W}:${CELL_H}:(ow-iw)/2:(oh-ih)/2,trim=duration=${PAGE_DURATION},setpts=PTS-STARTPTS[v1];
      [2:v]scale=${CELL_W}:${CELL_H}:force_original_aspect_ratio=decrease,pad=${CELL_W}:${CELL_H}:(ow-iw)/2:(oh-ih)/2,trim=duration=${PAGE_DURATION},setpts=PTS-STARTPTS[v2];
      [3:v]scale=${CELL_W}:${CELL_H}:force_original_aspect_ratio=decrease,pad=${CELL_W}:${CELL_H}:(ow-iw)/2:(oh-ih)/2,trim=duration=${PAGE_DURATION},setpts=PTS-STARTPTS[v3];
      [v0][v1]hstack=inputs=2[top];
      [v2][v3]hstack=inputs=2[bot];
      [top][bot]vstack=inputs=2[grid];
      [grid]drawtext=text='$title_escaped':fontsize=24:fontcolor=white:borderw=2:bordercolor=black:x=(w-text_w)/2:y=20[v]
    " -map "[v]" -r 25 -c:v libx264 -pix_fmt yuv420p -t "$PAGE_DURATION" "$out" -loglevel warning
}

build_page "before_read" "Before: Reading with (mid3v2, metaflac, ffprobe)" \
  "$OUT_DIR/cell_before_read_id3v1.gif" \
  "$OUT_DIR/cell_before_read_id3v2.gif" \
  "$OUT_DIR/cell_before_read_riff.gif" \
  "$OUT_DIR/cell_before_read_vorbis.gif"

build_page "now_read" "Now: Reading with AudioMeta" \
  "$OUT_DIR/cell_now_read_id3v1.gif" \
  "$OUT_DIR/cell_now_read_id3v2.gif" \
  "$OUT_DIR/cell_now_read_riff.gif" \
  "$OUT_DIR/cell_now_read_vorbis.gif"

build_page "before_write" "Before: Writing with (mid3v2, metaflac)" \
  "$OUT_DIR/cell_before_write_id3v1.gif" \
  "$OUT_DIR/cell_before_write_id3v2.gif" \
  "$OUT_DIR/cell_before_write_riff.gif" \
  "$OUT_DIR/cell_before_write_vorbis.gif"

build_page "now_write" "Now: Writing with AudioMeta" \
  "$OUT_DIR/cell_now_write_id3v1.gif" \
  "$OUT_DIR/cell_now_write_id3v2.gif" \
  "$OUT_DIR/cell_now_write_riff.gif" \
  "$OUT_DIR/cell_now_write_vorbis.gif"

# 7. Concat intro + 4 pages (use absolute paths for concat)
echo "Concatenating final video..."
CONCAT_LIST="$OUT_DIR/concat_list.txt"
ABS_OUT="$(cd "$OUT_DIR" && pwd)"
printf "file '%s/intro_segment.mp4'\nfile '%s/page_before_read.mp4'\nfile '%s/page_now_read.mp4'\nfile '%s/page_before_write.mp4'\nfile '%s/page_now_write.mp4'\n" \
  "$ABS_OUT" "$ABS_OUT" "$ABS_OUT" "$ABS_OUT" "$ABS_OUT" \
  > "$CONCAT_LIST"
ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" -c copy "$VIDEO_OUT" -loglevel warning

echo "Done: $VIDEO_OUT"
