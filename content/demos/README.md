# Library VHS demos

REPL- and script-style terminal demos for the project (not tied to a single article).

## Layout

- **`tapes/`** — `audiometa_demo.tape`, `audiometa_demo_script.tape` (tracked).
- **`output/`** — Generated GIF/MP4 (gitignored via `content/**/output/`).

Tapes assume the shell starts in **`content/demos`** and run a hidden `cd ../..` so commands in the recording use short repo-root paths (`audiometa/test/assets/...`, `scripts/demo_repl.py`).

## Run

```bash
source .venv/bin/activate
mkdir -p content/demos/output
(cd content/demos && vhs tapes/audiometa_demo.tape)
```

See [VHS_DEMO_README.md](../../VHS_DEMO_README.md) and [DEMO_INSTALLATION.md](../../DEMO_INSTALLATION.md).
