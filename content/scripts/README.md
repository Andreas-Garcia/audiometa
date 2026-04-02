# Content scripts

Scripts for building content. Run from repo root with venv activated.

- **`run_demo_tape.py`** – Lists the 5 most recently modified tape files under `content/articles/*/tapes/`; run one and write the GIF to that article’s `output/`. Example: `python content/scripts/run_demo_tape.py` (interactive) or `python content/scripts/run_demo_tape.py one_to_rule/get_full_metadata`.

Hero video is built from the article directory: `content/articles/one_to_rule/generate_one_to_rule_video.sh` (intro + four read comparisons: RIFF, ID3v2, ID3v1, Vorbis). That script is tracked next to the article’s tapes, not in this `scripts/` folder.

Side-by-side scripts live in the article dir and write to that article’s `output/`: `content/articles/one_to_rule/run_demo_side_by_side.sh` and `run_demo_side_by_side_vorbis.sh`.
