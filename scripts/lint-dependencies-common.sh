#!/bin/bash
# Shared utilities for lint dependency installation (shellcheck, PowerShell)
# Can be sourced by both macOS and Ubuntu installation scripts

# Function to get shellcheck version from --version output
# Works on both macOS and Ubuntu (handles different grep syntax)
get_shellcheck_version() {
  local version_output
  if command -v shellcheck &>/dev/null; then
    # Try macOS-compatible grep first (works on both)
    version_output=$(shellcheck --version 2>&1 | grep -oE 'version: [0-9.]+' | sed 's/version: //' || echo "")
    if [ -z "$version_output" ]; then
      # Fallback: try Ubuntu-style grep (requires -P which macOS grep doesn't support)
      version_output=$(shellcheck --version 2>&1 | grep -oP 'version: \K[0-9.]+' 2>/dev/null || echo "")
    fi
  fi
  echo "$version_output"
}

# Function to check if installed version matches pinned version (prefix matching)
# Returns 0 if versions match, 1 otherwise
check_shellcheck_version_match() {
  local installed_version="$1"
  local pinned_version="$2"

  if [ -z "$installed_version" ] || [ -z "$pinned_version" ]; then
    return 1
  fi

  # Check if one version is a prefix of the other (allows 0.9.0 to match 0.9.0.1)
  if [[ "$installed_version" == "$pinned_version"* ]] || [[ "$pinned_version" == "$installed_version"* ]]; then
    return 0
  fi

  return 1
}

# Function to load lint dependency versions
# Sets PINNED_SHELLCHECK variable
load_lint_dependency_versions() {
  local script_dir="$1"
  local version_output

  version_output=$(python3 "${script_dir}/load-system-dependency-versions.py" bash lint 2>/dev/null || echo "")
  if [ -n "$version_output" ]; then
    eval "$version_output"
  fi
}

# Function to verify shellcheck installation
# Prints success message and returns 0 if installed, 1 otherwise
verify_shellcheck_installation() {
  local pinned_version="$1"
  local platform="$2"  # "macos" or "ubuntu"

  if ! command -v shellcheck &>/dev/null; then
    echo "WARNING: shellcheck installed but not found in PATH."
    if [ "$platform" = "macos" ]; then
      echo "You may need to restart your terminal or run: export PATH=\"/opt/homebrew/bin:\$PATH\""
      echo "For Intel Macs: export PATH=\"/usr/local/bin:\$PATH\""
    else
      echo "You may need to restart your terminal or check installation."
    fi
    return 1
  fi

  local installed_version
  installed_version=$(get_shellcheck_version)
  if [ -n "$installed_version" ]; then
    echo "  shellcheck ${installed_version} installed successfully"
    if [ -n "$pinned_version" ]; then
      if ! check_shellcheck_version_match "$installed_version" "$pinned_version"; then
        echo "  WARNING: Installed version ${installed_version} does not match pinned version ${pinned_version}"
        if [ "$platform" = "macos" ]; then
          echo "  Homebrew installs latest version - this is expected if Homebrew has updated shellcheck"
        fi
        echo "  Consider updating system-dependencies-lint.toml with version ${installed_version}"
      fi
    fi
    return 0
  fi

  return 1
}
