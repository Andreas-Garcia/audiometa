# Article demo audio (tracked)

Place **canonical** demo files here so paths are obvious and `.gitignore` can whitelist this directory without allowing random binaries at the article root.

Expected filenames (add as needed for your tapes/scripts):

- `sample.mp3` — ID3 / MP3 demos
- `sample.flac` — Vorbis / FLAC demos
- `sample.wav` — RIFF / WAV demos (e.g. created with ffmpeg from another sample)

Ephemeral copies used only during a run (e.g. `demo_read_*.mp3`) stay in the article root or `output/`; those remain gitignored.

`docs/demos/` keeps a single shared `sample.mp3` for library-wide tapes; article-specific demos can mirror all three formats here.
