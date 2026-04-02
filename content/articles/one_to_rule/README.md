# One to rule them all (article)

Hero video + linked-post assets. Build output goes to `output/` (gitignored).

## Contents

- **`samples/`** – Tracked demo audio: **`samples/sample.mp3`**, **`samples/sample.flac`**, **`samples/sample.wav`** (same underlying track; see `samples/README.md`). Tapes use paths like `samples/sample.mp3` with cwd = this article dir.
- **`tapes/`** – VHS sources. **`Output`** in each tape is `output/<name>.gif`; run **`vhs` with cwd = this article dir** (see `generate_one_to_rule_video.sh`, `run_demo_side_by_side*.sh`, `run_demo_tape.py`) so the shell starts here—**do not type `cd` in the tape** (VHS only allows `Set Shell "bash"` etc.). **`demo_read_id3v1.mp3`**, **`demo_read_vorbis.flac`** – generated for ID3v1/Vorbis cells (gitignored).
- **`ensure_demo_read_id3v1.py`** – builds `demo_read_id3v1.mp3` from `samples/sample.mp3` (ID3v1-only tag, same song). **`sync_article_sample_metadata.py`** – aligns ID3/Vorbis tags on `samples/sample.{mp3,flac}`. **`print_id3v1_tags.py`** – prints TAG fields for the left panel.
- **Hero video:** `output/one_to_rule_them_all.mp4` — intro + **four reading comparisons** (RIFF, ID3v2, ID3v1, Vorbis): other tool left, **audiometa** right. See [VIDEO_SCENARIO_ONE_TO_RULE.md](VIDEO_SCENARIO_ONE_TO_RULE.md).
- **Side-by-side GIFs:** `run_demo_side_by_side.sh` (ID3v2 mid3v2 vs audiometa), `run_demo_side_by_side_vorbis.sh` (metaflac vs audiometa read).

## Build

From repo root with venv: **ffmpeg**, **ffprobe**, **metaflac**, **mid3v2**, **vhs**, intro logo video under `assets/logo.mp4` or `one_to_rule/logo.mp4`, plus **`assets/logo-round.png`** (or `assets/logo.png`) for the right-column **AudioMeta** mark in the hero layout.

- **Hero video:** `bash content/articles/one_to_rule/generate_one_to_rule_video.sh` — add `--skip-gifs` to reuse existing `output/*.gif` and skip VHS (faster when only ffmpeg/layout changed).
- **Single tape:** `python content/scripts/run_demo_tape.py` or `(cd content/articles/one_to_rule && vhs tapes/<name>.tape)`

Regenerate `samples/sample.flac` from MP3: `ffmpeg -y -i content/articles/one_to_rule/samples/sample.mp3 -map 0:a -c:a flac content/articles/one_to_rule/samples/sample.flac`, then run `python content/articles/one_to_rule/sync_article_sample_metadata.py` so Vorbis comments match the canonical track.
