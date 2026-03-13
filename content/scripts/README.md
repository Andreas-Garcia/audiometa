# Content scripts

Scripts for building content. Run from repo root with venv activated.

- **`run_demo_tape.py`** – Lists the 5 most recently modified tape files under `content/articles/*/tapes/`; run one and write the GIF to that article’s `output/`. Example: `python content/scripts/run_demo_tape.py` (interactive) or `python content/scripts/run_demo_tape.py one_to_rule/get_full_metadata`.
- **`generate_one_to_rule_video.sh`** – Launcher for the hero video script (implementation in `content/articles/one_to_rule/generate_one_to_rule_video.sh`).

Side-by-side scripts live in the article dir and write to that article’s `output/`: `content/articles/one_to_rule/run_demo_side_by_side.sh` and `run_demo_side_by_side_vorbis.sh`.
