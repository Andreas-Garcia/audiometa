# Demo audio (this article)

Put the **audio files this article’s tapes and scripts reference** here. That keeps a small, explicit set of paths under `samples/` so `.gitignore` can allow them without opening the whole article root to arbitrary binaries.

Suggested names (only add what this article actually uses):

- `sample.mp3` — MP3 / ID3 demos
- `sample.flac` — FLAC / Vorbis demos
- `sample.wav` — WAV / RIFF demos (e.g. generated with ffmpeg)

One-off or generated copies for a single run (e.g. `demo_read_*.mp3`) should stay in the article root or `output/`; those paths stay gitignored.

Other articles under `content/articles/` can use their own `samples/` the same way. Library-wide demos under `docs/demos/tapes/` keep using `docs/demos/sample.mp3`.
