# AudioMeta VHS Demo

Library demo tapes live under **`content/demos/tapes/`** and write GIF/MP4 to **`content/demos/output/`** (gitignored). Run VHS with cwd `content/demos` so outputs and paths resolve correctly (see `content/demos/README.md`).

## What is VHS?

[VHS](https://github.com/charmbracelet/vhs) is a tool for generating terminal recordings in a reproducible way using declarative `.tape` files.

## Installation

### Quick Installation (Recommended)

Use our installation script which handles all dependencies:

```bash
# macOS
bash scripts/install-demo-dependencies-macos.sh

# The script will install:
#   - VHS (terminal recorder)
#   - ttyd (required by VHS)
#   - ffmpeg (if not already installed)
#   - Fixes common libvpx/ffmpeg dependency issues
```

### Manual Installation

#### macOS

```bash
# Install VHS
brew tap charmbracelet/tap
brew install charmbracelet/tap/vhs

# Install dependencies
brew install ttyd ffmpeg
```

#### Linux

```bash
# Download from releases
# https://github.com/charmbracelet/vhs/releases

# Install dependencies
sudo apt-get install ttyd ffmpeg
```

## Usage

### Generate the demo video

```bash
# Project root, venv activated
source .venv/bin/activate
mkdir -p content/demos/output

# Run VHS with cwd = content/demos (required for Output paths)
(cd content/demos && vhs tapes/audiometa_demo.tape)
```

This will generate:

- `content/demos/output/audiometa_demo.mp4` - Video file (for Twitter)
- `content/demos/output/audiometa_demo.gif` - Animated GIF (for README/documentation)

### Preview before recording

```bash
(cd content/demos && vhs tapes/audiometa_demo.tape --preview)
```

## Customization

Edit `content/demos/tapes/audiometa_demo.tape` to customize:

- **Output format**: Change `Output` lines
- **Terminal size**: Adjust `Set Width` and `Set Height`
- **Font size**: Modify `Set FontSize`
- **Theme**: Change `Set Theme` (options: Dracula, Nord, Monokai, etc.)
- **Typing speed**: Adjust `Set TypingSpeed`
- **Pause times**: Modify `Sleep` durations

## Demo Content

The VHS demo shows:

1. Starting Python REPL
2. Importing `get_full_metadata`
3. Calling the function on a sample file
4. Accessing `unified_metadata`
5. Accessing `technical_info`
6. Accessing `raw_metadata` keys
7. Accessing `format_priorities`
8. Final comment about the feature

## Benefits of VHS

- ✅ **Reproducible** - Same video every time
- ✅ **Version controlled** - `.tape` file in git
- ✅ **Easy to update** - Just edit the tape file
- ✅ **Multiple formats** - MP4, GIF, WebM
- ✅ **High quality** - Professional terminal recordings
- ✅ **Customizable** - Themes, fonts, timing

## Example VHS Commands

```bash
# Generate video only (from repo root; cwd still content/demos for the recording shell)
(cd content/demos && vhs tapes/audiometa_demo.tape --output output/audiometa_demo.mp4)

# Generate GIF only
(cd content/demos && vhs tapes/audiometa_demo.tape --output output/audiometa_demo.gif)

# Use different theme
# Edit the tape file: Set Theme "Nord"
(cd content/demos && vhs tapes/audiometa_demo.tape)

# Faster playback
# Edit the tape file: Set PlaybackSpeed 1.5
(cd content/demos && vhs tapes/audiometa_demo.tape)
```

## Troubleshooting

### VHS not found

```bash
# Make sure VHS is installed
which vhs

# If not installed, follow installation instructions above
```

### ffmpeg not found

```bash
# Install ffmpeg
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

### Python not in PATH

```bash
# Activate virtual environment first
source .venv/bin/activate

# Then run VHS
(cd content/demos && vhs tapes/audiometa_demo.tape)
```

## Links

- [VHS GitHub](https://github.com/charmbracelet/vhs)
- [VHS Documentation](https://github.com/charmbracelet/vhs#vhs)
- [VHS Examples](https://github.com/charmbracelet/vhs/tree/main/examples)
