#!/bin/bash
# Install demo dependencies for macOS
# These are OPTIONAL tools for creating demo videos and marketing materials
# Required for: Creating terminal demo videos with VHS
#
# Usage:
#   bash scripts/install-demo-dependencies-macos.sh

set -e

echo "Installing demo dependencies for macOS..."
echo "Note: These are OPTIONAL tools for creating demo videos."
echo ""

# Check if Homebrew is installed
if ! command -v brew &>/dev/null; then
  echo "ERROR: Homebrew is not installed."
  echo "Install Homebrew first: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
  exit 1
fi

# Install ttyd (required by VHS)
echo "Installing ttyd (required by VHS)..."
if command -v ttyd &>/dev/null; then
  echo "  ttyd already installed: $(ttyd --version 2>&1 | head -1)"
else
  if ! brew install ttyd; then
    echo "ERROR: Failed to install ttyd."
    echo "Install manually: brew install ttyd"
    exit 1
  fi
  echo "  ttyd installed: $(ttyd --version 2>&1 | head -1)"
fi

# Install/reinstall ffmpeg to fix potential libvpx issues
echo ""
echo "Checking ffmpeg installation..."
if command -v ffmpeg &>/dev/null; then
  FFMPEG_VERSION=$(ffmpeg -version 2>/dev/null | head -n1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -n1 || echo "unknown")
  echo "  ffmpeg already installed: $FFMPEG_VERSION"

  # Check for libvpx issues (common with VHS)
  echo "  Checking for libvpx dependency issues..."
  if ffmpeg -version &>/dev/null; then
    echo "  ffmpeg is working correctly"
  else
    echo "  WARNING: ffmpeg may have dependency issues"
    echo "  Attempting to fix by reinstalling libvpx and ffmpeg..."
    brew reinstall libvpx
    brew reinstall ffmpeg
  fi
else
  echo "  ffmpeg not found, installing..."
  brew install ffmpeg
fi

# Install VHS
echo ""
echo "Installing VHS..."
if command -v vhs &>/dev/null; then
  echo "  VHS already installed: $(vhs --version 2>&1 | head -1)"
else
  # Add Charm tap and install VHS
  echo "  Adding charmbracelet/tap..."
  brew tap charmbracelet/tap 2>/dev/null || true

  echo "  Installing VHS..."
  if ! brew install charmbracelet/tap/vhs; then
    echo "ERROR: Failed to install VHS."
    echo "Install manually: brew install charmbracelet/tap/vhs"
    exit 1
  fi
  echo "  VHS installed: $(vhs --version 2>&1 | head -1)"
fi

# Verify installation
echo ""
echo "Verifying installation..."

MISSING_TOOLS=()
for tool in ttyd ffmpeg vhs; do
  if ! command -v "$tool" &>/dev/null; then
    MISSING_TOOLS+=("$tool")
  else
    echo "  ✓ $tool is available"
  fi
done

if [ ${#MISSING_TOOLS[@]} -ne 0 ]; then
  echo ""
  echo "ERROR: The following tools are not available:"
  printf '  - %s\n' "${MISSING_TOOLS[@]}"
  exit 1
fi

# Test VHS can run
echo ""
echo "Testing VHS..."
if vhs --version &>/dev/null; then
  echo "  ✓ VHS is working correctly"
else
  echo "  WARNING: VHS installed but may have issues"
  echo "  Try running: vhs --version"
fi

echo ""
echo "✓ Demo dependencies installed successfully!"
echo ""
echo "You can now create demo videos using:"
echo "  vhs docs/demos/get_full_metadata.tape"
echo ""
echo "Or run any .tape file:"
echo "  vhs your-demo.tape"
