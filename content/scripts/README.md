# Content scripts

Scripts for building content that are not demo-specific. Run from repo root with venv activated.

Demo utility scripts moved to `content/demo/scripts/`:

- **`run_demo_tape.py`** – Lists the 5 most recently modified tape files under `content/articles/*/tapes/`; run one and write the GIF to that article’s `output/`. Example: `python content/demo/scripts/run_demo_tape.py` (interactive) or `python content/demo/scripts/run_demo_tape.py one_to_rule/get_full_metadata`.

Hero video: `content/articles/one_to_rule/scripts/generate_one_to_rule_video.sh` (intro + four read comparisons: RIFF, ID3v2, ID3v1, Vorbis). It lives under that article’s `scripts/`, not in this `content/scripts/` folder.

Side-by-side: `content/articles/one_to_rule/scripts/run_demo_side_by_side.sh` and `run_demo_side_by_side_vorbis.sh` (write to that article’s `output/`).
