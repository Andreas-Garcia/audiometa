# One-to-rule hero video (reading only)

1. **Intro**: logo + tagline — read metadata across formats with one CLI.
2. **RIFF (WAV)** — left: `ffprobe` tags; right: `audiometa unified` (table).
3. **ID3v2 (MP3)** — left: `mid3v2 -l`; right: `audiometa unified` (table).
4. **ID3v1 (MP3)** — left: raw 128-byte TAG fields; right: `audiometa unified` (table) on the same demo file.
5. **Vorbis (FLAC)** — left: `metaflac --list`; right: `audiometa unified` (table).

Build: `bash content/articles/one_to_rule/scripts/generate_one_to_rule_video.sh` from repo root (venv on). Output: `content/articles/one_to_rule/output/final/one_to_rule_them_all.mp4`.

To drop stale segments after layout changes, remove old GIFs/MP4s under `output/work/` (and the hero file under `output/final/` if needed) and re-run.
