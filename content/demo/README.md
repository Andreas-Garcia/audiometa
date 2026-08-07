# Demo Content Hub

Central location for demo docs, scripts, and shared library tapes.

## Layout

- **`docs/`** - Demo guides and references:
  - `VHS_DEMO_README.md`
  - `DEMO_INSTALLATION.md`
  - `DEMO_VIDEOS_README.md`
- **`scripts/`** - Demo-only helper scripts:
  - `install-demo-dependencies-macos.sh`
  - `demo_repl.py`
  - `run_demo_tape.py`
  - `article_output_paths.sh` (shared article output path helpers for demo scripts)
- **`demos/`** - Shared library tapes (`tapes/`) and generated output (`output/`, gitignored).

## Article-specific demos

Article demo assets stay under `content/articles/<article>/` with local `tapes/`, `samples/`, `scripts/`, and `output/` (`work/` for intermediates, `final/` for deliverables).
