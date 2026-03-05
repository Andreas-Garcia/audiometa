# AudioMeta VHS Demo

This directory contains a VHS tape file for generating the AudioMeta demo video.

## What is VHS?

[VHS](https://github.com/charmbracelet/vhs) is a tool for generating terminal recordings in a reproducible way using declarative `.tape` files.

## Installation

### macOS

```bash
brew install vhs
```

### Linux

```bash
# Download from releases
# https://github.com/charmbracelet/vhs/releases
```

### Dependencies

VHS requires `ffmpeg` and `ttyd`:

```bash
# macOS
brew install ffmpeg ttyd

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

## Usage

### Generate the demo video

```bash
# Make sure you're in the project root with venv activated
source .venv/bin/activate

# Run VHS with the tape file
vhs audiometa_demo.tape
```

This will generate:

- `audiometa_demo.mp4` - Video file (for Twitter)
- `audiometa_demo.gif` - Animated GIF (for README/documentation)

### Preview before recording

```bash
# Preview the tape file
vhs audiometa_demo.tape --preview
```

## Customization

Edit `audiometa_demo.tape` to customize:

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
# Generate video only
vhs audiometa_demo.tape --output audiometa_demo.mp4

# Generate GIF only
vhs audiometa_demo.tape --output audiometa_demo.gif

# Use different theme
# Edit the tape file: Set Theme "Nord"
vhs audiometa_demo.tape

# Faster playback
# Edit the tape file: Set PlaybackSpeed 1.5
vhs audiometa_demo.tape
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
vhs audiometa_demo.tape
```

## Links

- [VHS GitHub](https://github.com/charmbracelet/vhs)
- [VHS Documentation](https://github.com/charmbracelet/vhs#vhs)
- [VHS Examples](https://github.com/charmbracelet/vhs/tree/main/examples)
