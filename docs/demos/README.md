# Demos (VHS terminal recordings)

This directory contains [VHS](https://github.com/charmbracelet/vhs) (charmbracelet/tap) tape files for producing terminal demo videos/GIFs.

## Prerequisites

- [VHS](https://github.com/charmbracelet/vhs) (requires `ttyd` and `ffmpeg` on `PATH`)
- macOS: `brew install vhs`
- Run tapes from the **project root** of audiometa-python.

## Layout

- **`tapes/`** – VHS tape sources (`.tape` files)
- **`sample.mp3`** – Demo audio asset (Queen track, tracked)
- Generated outputs (`.gif`, `.mp4`) are written to `docs/demos/` per tape `Output` and are gitignored.

## Tapes

| File                           | Description                                                                                           |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- |
| `tapes/get_full_metadata.tape` | Demo of the get-full-metadata feature: `audiometa read` with JSON, YAML, and table output on a track. |

## Usage

From the project root:

```bash
vhs docs/demos/tapes/get_full_metadata.tape
```

The demo uses `docs/demos/sample.mp3` (tracked in repo; Queen track). Output is written to the path in the tape (e.g. `docs/demos/get_full_metadata_demo.gif`). Tapes should set `Output docs/demos/<name>.gif` (or `.mp4`).

**Audio paths in demos**: For **social / marketing** videos, use `docs/demos/sample.mp3` so the path on screen is short and professional. For **dev-only** demos you can reference `audiometa/test/assets/...`; ensure test assets exist and run from repo root.

## Note

`tapes/*.tape` and `sample.mp3` are tracked. Generated outputs (`.gif`, `.mp4`) in `docs/demos/` are gitignored.
