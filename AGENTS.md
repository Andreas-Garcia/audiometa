# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

AudioMeta Python is a library and CLI (`audiometa`) for reading, writing, and deleting audio file metadata (MP3, FLAC, WAV) across formats (ID3v1, ID3v2, Vorbis, RIFF). No web services or databases—just Python + system CLI tools.

### Virtual environment

Always activate before running any command:

```bash
source .venv/bin/activate
```

### System dependencies

The `flac` apt package (CLI tools) is separate from `libflac12t64` (library). The install script (`scripts/install-system-dependencies-ubuntu.sh`) may install only the library; verify `flac` and `metaflac` are on PATH after running it. If missing, install explicitly: `sudo apt-get install -y flac`.

Pre-commit hooks require `shellcheck` and `pwsh` (PowerShell). These are installed via the `lint` category: `bash scripts/install-system-dependencies-ubuntu.sh lint`. If you only need Python linting, run `ruff`, `mypy`, and `isort` directly instead of `pre-commit run --all-files`.

### Key commands

See `CONTRIBUTING.md` for full details. Quick reference:

- **Lint**: `ruff check audiometa/` / `mypy --follow-imports=normal audiometa/ --exclude audiometa/test/` / `isort --check-only --profile black --line-length=120 audiometa/`
- **Test**: `pytest` (all 1553 tests) / `pytest -m unit` / `pytest -m integration` / `pytest -m e2e`
- **CLI**: `audiometa read <file>` / `audiometa write <file> --title "..." --artist "..."` / `audiometa delete <file>`

### Demo videos

Demos are generated with [VHS](https://github.com/charmbracelet/vhs) from `.tape` files. See `VHS_DEMO_README.md` and `DEMO_INSTALLATION.md` for full instructions. **Demos** live under `content/articles/` (one dir per article, each with `tapes/` and a single `output/` for GIFs and video). Example article: `content/articles/one_to_rule/`. Quick path: install deps (macOS) with `bash scripts/install-demo-dependencies-macos.sh`, activate venv, then run `(cd content/articles/one_to_rule && vhs tapes/<name>.tape)` or `python content/scripts/run_demo_tape.py` or `./content/articles/one_to_rule/generate_one_to_rule_video.sh` (hero video; all cells from tapes, no placeholders, fails early if required asset missing). Side-by-side scripts live in the article dir (e.g. `one_to_rule/run_demo_side_by_side.sh`). When editing tapes or demo workflow, follow `.cursor/rules/demo-videos.mdc`; for authoring .tape content, follow `.cursor/rules/demo-tape-authoring.mdc`.

### Gotchas

- `python3.12-venv` must be installed (`sudo apt-get install -y python3.12-venv`) before creating `.venv`.
- `core.hooksPath` git config may block `pre-commit install`; unset it first: `git config --unset-all core.hooksPath`.
- Test audio files in `audiometa/test/assets/` are generated via `create_test_files.py`, not checked in as binaries.
- `numpy==2.3.4` is a dev dependency (for `soundfile` test file generation); it is not a production dependency.
