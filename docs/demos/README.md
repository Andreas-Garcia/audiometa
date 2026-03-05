# Demos (VHS terminal recordings)

This directory contains [VHS](https://github.com/charmbracelet/vhs) (charmbracelet/tap) tape files for producing terminal demo videos/GIFs.

## Prerequisites

- [VHS](https://github.com/charmbracelet/vhs) (requires `ttyd` and `ffmpeg` on `PATH`)
- macOS: `brew install vhs`
- Run tapes from the **project root** of audiometa-python.

## Tapes

| File                     | Description                                                                                           |
| ------------------------ | ----------------------------------------------------------------------------------------------------- |
| `get_full_metadata.tape` | Demo of the get-full-metadata feature: `audiometa read` with JSON, YAML, and table output on a track. |

## Usage

From the project root:

```bash
vhs docs/demos/get_full_metadata.tape
```

Output is written to the path specified in the tape (e.g. `get_full_metadata_demo.gif` in the current directory, or change `Output` in the tape to `docs/demos/get_full_metadata_demo.gif`).

For a track with **complex metadata**, edit the tape and set the file path to an asset with many tags (e.g. `audiometa/test/assets/metadata=long a_id3v2_big.mp3` if available, or any path to a richly tagged file). Ensure test assets exist: `python3 audiometa/test/assets/create_test_files.py`.

## Note

This directory is gitignored; tape files and generated media are for local use only.
