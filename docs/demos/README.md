# Demos (VHS terminal recordings)

This directory contains [VHS](https://github.com/charmbracelet/vhs) (charmbracelet/tap) tape files for producing terminal demo videos/GIFs.

## Prerequisites

- [VHS](https://github.com/charmbracelet/vhs) (requires `ttyd` and `ffmpeg` on `PATH`)
- macOS: `brew install vhs`
- Run tapes from the **project root** of audiometa-python.

## Layout

- **`tapes/`** – VHS tape sources (`.tape` files)
- **`sample.mp3`** – Demo audio asset (Queen track, tracked)
- **`output/`** – Generated GIFs/MP4s (gitignored). Tapes and the wrapper write here.

## Tapes

| File                           | Description                                                                                           |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- |
| `tapes/get_full_metadata.tape` | Demo of the get-full-metadata feature: `audiometa read` with JSON, YAML, and table output on a track. |

## Usage

From the project root (with venv activated):

**Wrapper (recommended)** – tape name and optional sample; writes GIF to `docs/demos/output/<name>.gif`:

```bash
python scripts/run_demo_tape.py get_full_metadata
python scripts/run_demo_tape.py get_full_metadata --sample other.mp3
```

**Direct VHS:**

```bash
vhs docs/demos/tapes/get_full_metadata.tape
```

The demo uses `docs/demos/sample.mp3` by default (tracked in repo; Queen track). The wrapper overrides the tape’s `Output` to `docs/demos/output/<name>.gif` and can use a different `--sample` file under `docs/demos/`.

**Audio paths in demos**: For **social / marketing** videos, use `docs/demos/sample.mp3` so the path on screen is short and professional. For **dev-only** demos you can reference `audiometa/test/assets/...`; ensure test assets exist and run from repo root.

## Note

`tapes/*.tape` and `sample.mp3` are tracked. `output/` is gitignored (generated `.gif`/`.mp4` only).
