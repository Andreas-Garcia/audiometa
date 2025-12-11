#!/bin/bash
# Wrapper for ShellCheck
# Requires shellcheck to be installed

# Check if shellcheck is available
if ! command -v shellcheck &>/dev/null; then
  echo "ERROR: shellcheck is required but not found."
  echo ""
  echo "Install shellcheck:"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "  macOS: brew install shellcheck"
    echo "  Or download from: https://github.com/koalaman/shellcheck#installing"
  elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "  Ubuntu/Debian: sudo apt-get install shellcheck"
    echo "  Or download from: https://github.com/koalaman/shellcheck#installing"
  else
    echo "  Visit: https://github.com/koalaman/shellcheck#installing"
  fi
  exit 1
fi

# Run shellcheck for each file
# This replicates the behavior of the shellcheck hook
for file in "$@"; do
  shellcheck --severity=error "$file" || exit 1
done
