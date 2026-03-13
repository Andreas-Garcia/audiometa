# One to rule them all (article)

Hero video + linked post (comparison) assets. All build output (GIFs, video) goes to this article’s `output/`.

## Contents

- **`tapes/`** – VHS tape sources (`.tape` files). **`sample.mp3`**, **`sample.flac`** – Demo audio (tracked). **`sample.wav`** – Created when building (gitignored). Temp copies used by tapes (`demo_vorbis_before.flac`, `demo_vorbis_after.flac`, `demo_write.mp3`) are gitignored.
- **`output/`** – Build output (gitignored): tape GIFs, hero video, side-by-side GIFs, page segments. All scripts write here.
- **Hero video:** `output/one_to_rule_them_all.mp4` (intro + 2×2 pages). Scenario: [VIDEO_SCENARIO_ONE_TO_RULE.md](VIDEO_SCENARIO_ONE_TO_RULE.md).
- **Side-by-side GIFs:** `output/before_after_side_by_side.gif`, `output/before_after_side_by_side_vorbis.gif` (for linked posts).

## Build

From repo root with venv activated:

- **Prerequisites:** [VHS](https://github.com/charmbracelet/vhs), `ttyd`, `ffmpeg`. macOS: `brew install vhs`. Logo: `assets/logo.png` or `one_to_rule/logo.png` when present.
- **Single tape:** `python content/scripts/run_demo_tape.py` (lists 5 most recent tapes; pick one) or `python content/scripts/run_demo_tape.py one_to_rule/<name>` → writes to this article’s `output/`. Or run `vhs content/articles/one_to_rule/tapes/<name>.tape` directly.
- **Hero video:** `./generate_one_to_rule_video.sh` (from this dir) or `./content/scripts/generate_one_to_rule_video.sh` (from repo root) → `output/one_to_rule_them_all.mp4`.
- **Side-by-side GIFs:** `./run_demo_side_by_side.sh` and `./run_demo_side_by_side_vorbis.sh` (from this dir or repo root) → `output/before_after_side_by_side.gif`, `output/before_after_side_by_side_vorbis.gif`.

Regenerate `sample.flac`: `ffmpeg -y -i content/articles/one_to_rule/sample.mp3 -map 0:a -c:a flac content/articles/one_to_rule/sample.flac`.
