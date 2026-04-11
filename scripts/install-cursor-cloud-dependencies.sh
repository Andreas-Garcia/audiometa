#!/bin/bash
set -euo pipefail

if [ "${CURSOR_CLOUD_DRY_RUN:-0}" = "1" ]; then
  echo "DRY RUN: would install Cursor Cloud lint dependencies for Ubuntu 24.04"
  exit 0
fi

if [ "$(uname -s)" != "Linux" ]; then
  echo "Skipping Cursor Cloud dependency install: non-Linux platform"
  exit 0
fi

DISTRO_ID=""
DISTRO_VERSION=""

if [ -r /etc/os-release ]; then
  # shellcheck disable=SC1091
  . /etc/os-release
  DISTRO_ID="${ID:-}"
  DISTRO_VERSION="${VERSION_ID:-}"
fi

if [ -z "$DISTRO_ID" ] || [ -z "$DISTRO_VERSION" ]; then
  if command -v lsb_release >/dev/null 2>&1; then
    DISTRO_ID="$(lsb_release -is)"
    DISTRO_VERSION="$(lsb_release -rs)"
  fi
fi

if [ -z "$DISTRO_ID" ] || [ -z "$DISTRO_VERSION" ]; then
  echo "Skipping Cursor Cloud dependency install: unable to detect Linux distribution"
  exit 0
fi

if [ "$DISTRO_ID" != "ubuntu" ] || [ "$DISTRO_VERSION" != "24.04" ]; then
  echo "Skipping Cursor Cloud dependency install: expected Ubuntu 24.04, got ${DISTRO_ID} ${DISTRO_VERSION}"
  exit 0
fi

bash scripts/install-system-dependencies-ubuntu.sh lint
