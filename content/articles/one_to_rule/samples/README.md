# Demo audio (this article)

Put the **audio files this article’s tapes and scripts reference** here. That keeps a small, explicit set of paths under `samples/` so `.gitignore` can allow them without opening the whole article root to arbitrary binaries.

**Canonical track (keep in sync across all three files):** _We Are the Champions_ — **Queen**, album _News of the World_, release date 1977-10-28, track 4/11. Run `python content/articles/one_to_rule/scripts/sync_article_sample_metadata.py` from repo root (venv activated) after replacing binaries so ID3v2/Vorbis tags stay aligned.

Suggested names (only add what this article actually uses):

- `sample.mp3` — MP3 / ID3 demos
- `sample.flac` — FLAC / Vorbis demos
- `sample.wav` — WAV / RIFF demos (e.g. `ffmpeg -y -i samples/sample.mp3 -map 0:a -c:a pcm_s16le samples/sample.wav`)

Generated demo copies used by tapes (e.g. `output/demo_read_id3v1.mp3`, `output/demo_read_vorbis.flac`) stay under **`output/`** with GIFs/MP4; those paths are gitignored.

Other articles under `content/articles/` can use their own `samples/` the same way. Library REPL-style VHS demos live under `content/demos/tapes/` and use repo test assets / `scripts/demo_repl.py` (see `content/demos/README.md`).
