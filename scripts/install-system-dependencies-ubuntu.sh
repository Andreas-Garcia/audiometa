#!/bin/bash
# Install system dependencies for Ubuntu CI
# Pinned versions from system-dependencies-*.toml files (fails if not available, no fallback)
#
# Usage:
#   bash scripts/install-system-dependencies-ubuntu.sh [category]
#
# Categories:
#   - prod: Production dependencies only (ffmpeg, flac, id3v2)
#   - test-only: Test-only dependencies (mediainfo, exiftool, bwfmetaedit, libsndfile)
#   - lint: Lint dependencies only (PowerShell)
#   - all: All dependencies (default)

set -e

# Parse category argument (default to "all")
CATEGORY="${1:-all}"

# Validate category
if [[ ! "$CATEGORY" =~ ^(prod|test-only|lint|all)$ ]]; then
  echo "ERROR: Invalid category: $CATEGORY"
  echo "Valid categories: prod, test-only, lint, all"
  exit 1
fi

# Update package lists first
echo "Updating package lists..."
sudo apt-get update -v || {
  echo "ERROR: Failed to update package lists."
  echo "This may indicate network connectivity issues or repository problems."
  exit 1
}

# Load pinned versions from system-dependencies-*.toml files
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
eval "$(python3 "${SCRIPT_DIR}/load-system-dependency-versions.py" bash "$CATEGORY")"

# Source shared lint dependency utilities
source "${SCRIPT_DIR}/lint-dependencies-common.sh"

echo "Installing pinned package versions..."

# Function to resolve partial version to full version
# If pinned_version is a partial version (e.g., "24.01"), find the first available
# version that starts with it (e.g., "24.01.1-1build2")
resolve_version() {
  local package="$1"
  local pinned_version="$2"

  # If version contains a hyphen, it's already a full version
  if [[ "$pinned_version" == *"-"* ]]; then
    echo "$pinned_version"
    return
  fi

  # For partial versions, find the first available version that starts with it
  # Extract version from apt-cache madison output (format: "package | version | repo")
  local available_version=$(apt-cache madison "$package" 2>/dev/null | \
    awk -v prefix="$pinned_version" '{
      # Extract version from second column (between |)
      gsub(/^[^|]*\|[[:space:]]*/, "")
      gsub(/[[:space:]]*\|.*$/, "")
      version = $0
      # Check if version starts with prefix (handle epoch prefix like "7:")
      if (version ~ "^[0-9]+:" prefix || version ~ "^" prefix) {
        print version
        exit
      }
    }' | head -n1)

  if [ -n "$available_version" ]; then
    echo "$available_version"
  else
    # If no match found, return original (will fail later with better error)
    echo "$pinned_version"
  fi
}

# Check available versions before attempting installation (skip for lint-only)
if [[ "$CATEGORY" != "lint" ]]; then
  echo "Checking available package versions..."
  HAS_ERRORS=0
  # Determine which packages to check based on category
  PACKAGES_TO_CHECK=()
  if [[ "$CATEGORY" =~ ^(prod|all)$ ]]; then
    PACKAGES_TO_CHECK+=(ffmpeg flac id3v2)
  fi
  if [[ "$CATEGORY" =~ ^(test-only|all)$ ]]; then
    PACKAGES_TO_CHECK+=(mediainfo libimage-exiftool-perl libsndfile1)
  fi

  for package in "${PACKAGES_TO_CHECK[@]}"; do
  var_name="PINNED_${package^^}"
  var_name="${var_name//-/_}"
  pinned_version="${!var_name}"
  echo "Checking $package=$pinned_version..."

  # Check if package exists at all
  if ! apt-cache madison "$package" &>/dev/null || [ -z "$(apt-cache madison "$package" 2>/dev/null)" ]; then
    echo "ERROR: Package $package is not available in any repository."
    echo "You may need to enable universe/multiverse repositories or the package name has changed."
    HAS_ERRORS=1
    continue
  fi

  # Skip version check for "latest"
  if [ "$pinned_version" != "latest" ]; then
    # Resolve partial version to full version for checking
    resolved_version=$(resolve_version "$package" "$pinned_version")

    # Check if resolved version exists (or if partial version matches any available version)
    if [ "$resolved_version" = "$pinned_version" ] && [[ "$pinned_version" != *"-"* ]]; then
      # Partial version that couldn't be resolved - check if any version starts with it
      if ! apt-cache madison "$package" 2>/dev/null | grep -qE "(^|[[:space:]]\|[[:space:]]*)([0-9]+:)?${pinned_version}"; then
        echo "ERROR: Pinned version $pinned_version for $package is not available."
        echo "Available versions for $package:"
        apt-cache madison "$package" 2>/dev/null | head -5 || echo "  (could not list versions)"
        echo ""
        HAS_ERRORS=1
      fi
    elif [ "$resolved_version" != "$pinned_version" ]; then
      # Partial version was resolved - verify resolved version exists
      if ! apt-cache madison "$package" 2>/dev/null | grep -qF "$resolved_version"; then
        echo "ERROR: Resolved version $resolved_version for $package (from pinned $pinned_version) is not available."
        echo "Available versions for $package:"
        apt-cache madison "$package" 2>/dev/null | head -5 || echo "  (could not list versions)"
        echo ""
        HAS_ERRORS=1
      fi
    else
      # Full version - check if it exists
      if ! apt-cache madison "$package" 2>/dev/null | grep -q "$pinned_version"; then
        echo "ERROR: Pinned version $pinned_version for $package is not available."
        echo "Available versions for $package:"
        apt-cache madison "$package" 2>/dev/null | head -5 || echo "  (could not list versions)"
        echo ""
        HAS_ERRORS=1
      fi
    fi
  fi
  done

  if [ $HAS_ERRORS -eq 1 ]; then
    echo ""
    echo "Update system-dependencies-prod.toml or system-dependencies-test-only.toml with versions from the lists above."
    echo "Use the format from the first column (e.g., '7:8.0.2-1ubuntu1' for ffmpeg)."
    exit 1
  fi
fi

# Check installed versions and remove if different (skip for lint-only)
if [[ "$CATEGORY" != "lint" ]]; then
  PACKAGES_TO_INSTALL=()
  # Determine which packages to install based on category
  PACKAGES_TO_PROCESS=()
  if [[ "$CATEGORY" =~ ^(prod|all)$ ]]; then
    PACKAGES_TO_PROCESS+=(ffmpeg flac)
  fi
  if [[ "$CATEGORY" =~ ^(test-only|all)$ ]]; then
    PACKAGES_TO_PROCESS+=(mediainfo libsndfile1)
  fi

  for package in "${PACKAGES_TO_PROCESS[@]}"; do
  var_name="PINNED_${package^^}"
  pinned_version="${!var_name}"

  # Resolve partial version to full version for installation
  resolved_version=$(resolve_version "$package" "$pinned_version")

  # Check if package is actually installed via apt (more reliable than command -v)
  INSTALLED_APT_VERSION=$(dpkg -l | grep "^ii.*${package}" | awk '{print $3}' || echo "")

  # Only check versions if package is actually installed via apt
  if [ -n "$INSTALLED_APT_VERSION" ]; then
    if [ "$pinned_version" = "latest" ]; then
      # For "latest", just check if package is installed
      echo "${package} ${INSTALLED_APT_VERSION} already installed (using latest)"
      continue
    else
      # Check if installed version matches pinned version (using flexible matching)
      # Extract upstream version (before first '-') for comparison
      installed_upstream="${INSTALLED_APT_VERSION%%-*}"
      resolved_upstream="${resolved_version%%-*}"

      # Normalize versions (remove +dfsg, +ds suffixes and revision suffixes)
      installed_normalized="${installed_upstream%%+*}"
      installed_normalized="${installed_normalized%%_*}"
      resolved_normalized="${resolved_upstream%%+*}"
      resolved_normalized="${resolved_normalized%%_*}"

      # Check if versions match (exact or prefix match)
      if [ "$installed_normalized" = "$resolved_normalized" ] || \
         [[ "$installed_normalized" == "$resolved_normalized".* ]] || \
         [[ "$resolved_normalized" == "$installed_normalized".* ]]; then
        echo "${package} ${INSTALLED_APT_VERSION} already installed (matches pinned version ${pinned_version})"
        continue
      else
        echo "Removing existing ${package} version ${INSTALLED_APT_VERSION} (installing pinned version ${pinned_version} -> ${resolved_version})..."
        sudo apt-get remove -y "$package" 2>/dev/null || true
        INSTALLED_APT_VERSION=""  # Clear after removal
      fi
    fi
  else
    # Package not installed via apt, will be added to installation list
    echo "${package} not installed via apt, will install version ${pinned_version}"
  fi

  # Add to installation list if not already installed with correct version
  if [ -z "$INSTALLED_APT_VERSION" ]; then
    if [ "$pinned_version" = "latest" ]; then
      PACKAGES_TO_INSTALL+=("${package}")
    else
      PACKAGES_TO_INSTALL+=("${package}=${resolved_version}")
    fi
  fi
done

# Install packages if any need installation
if [ ${#PACKAGES_TO_INSTALL[@]} -gt 0 ]; then
  echo "Installing packages: ${PACKAGES_TO_INSTALL[*]}"
  echo "Note: This may take several minutes. Large packages like ffmpeg can take time to download..."

  # Check if any packages are held
  echo "Checking for held packages..."
  for package in "${PACKAGES_TO_INSTALL[@]}"; do
    pkg_name="${package%%=*}"
    if dpkg --get-selections | grep -q "^${pkg_name}[[:space:]]*hold"; then
      echo "  WARNING: ${pkg_name} is on hold, will attempt to install anyway"
    fi
  done
  echo ""

  # First, verify the exact package versions are available
  echo "Verifying package versions are available in repositories..."
  for package in "${PACKAGES_TO_INSTALL[@]}"; do
    pkg_name="${package%%=*}"
    pkg_version="${package#*=}"
    if [ "$pkg_version" = "latest" ]; then
      echo "  Checking ${pkg_name} (latest)..."
      if ! apt-cache madison "$pkg_name" 2>/dev/null | head -1; then
        echo "    ERROR: ${pkg_name} not found in repositories"
      fi
    else
      echo "  Checking ${pkg_name}=${pkg_version}..."
      if ! apt-cache madison "$pkg_name" 2>/dev/null | grep -q "$pkg_version"; then
        echo "    ERROR: ${pkg_name} version ${pkg_version} not found in repositories"
        echo "    Available versions:"
        apt-cache madison "$pkg_name" 2>/dev/null | head -3 || echo "      (could not list versions)"
      fi
    fi
  done
  echo ""

  # Check what apt-get would do (dry-run to see if packages are available)
  echo "Checking what apt-get would install (dry-run)..."
  sudo apt-get install -y --dry-run --allow-downgrades --allow-change-held-packages "${PACKAGES_TO_INSTALL[@]}" 2>&1 | head -100 || true
  echo ""

  # Use --show-progress for better output visibility (instead of -v which might cause issues)
  # Add --allow-downgrades and --allow-change-held-packages to ensure installation proceeds
  # Run apt-get install with output both to stdout/stderr and to log file for debugging
  # Use set -o pipefail to ensure we catch the exit status of apt-get, not tee
  set -o pipefail
  if ! sudo apt-get install -y --show-progress --allow-downgrades --allow-change-held-packages "${PACKAGES_TO_INSTALL[@]}" 2>&1 | tee /tmp/apt-install.log; then
    set +o pipefail
    echo ""
    echo "ERROR: Failed to install pinned versions."
    echo "This may indicate:"
    echo "  - Network connectivity issues"
    echo "  - Package repository problems"
    echo "  - Versions are no longer available"
    echo "  - Package conflicts or dependency issues"
    echo ""
    echo "Full installation log saved to /tmp/apt-install.log"
    echo "Last 50 lines of log:"
    tail -50 /tmp/apt-install.log
    exit 1
  fi
  set +o pipefail

  # Check if apt-get actually installed anything
  if grep -q "0 newly installed" /tmp/apt-install.log; then
    echo ""
    echo "WARNING: apt-get reported '0 newly installed' - packages may not have been installed"
    echo "This could indicate:"
    echo "  - Packages are already installed (but verification will check)"
    echo "  - Version specifications don't match available packages"
    echo "  - Dependency conflicts prevented installation"
  fi

  echo ""
  echo "Package installation completed successfully."

  # Verify packages were actually installed
  echo "Verifying installed packages..."
  VERIFICATION_FAILED=0
  for package in "${PACKAGES_TO_INSTALL[@]}"; do
    # Extract package name (remove version suffix if present)
    pkg_name="${package%%=*}"
    INSTALLED_CHECK=$(dpkg -l | grep "^ii.*${pkg_name}" | awk '{print $2 " " $3}' || echo "")
    if [ -n "$INSTALLED_CHECK" ]; then
      echo "  ✓ ${INSTALLED_CHECK} installed"
    else
      echo "  ✗ ${pkg_name} NOT found in dpkg -l after installation"
      echo "    This may indicate installation failed silently"
      VERIFICATION_FAILED=1
    fi
  done

  if [ $VERIFICATION_FAILED -eq 1 ]; then
    echo ""
    echo "ERROR: Some packages were not installed successfully."
    echo ""
    echo "apt-get install command that was run:"
    echo "  sudo apt-get install -y --show-progress --allow-downgrades --allow-change-held-packages ${PACKAGES_TO_INSTALL[*]}"
    echo ""
    echo "Full installation output from /tmp/apt-install.log:"
    echo "----------------------------------------"
    cat /tmp/apt-install.log
    echo "----------------------------------------"
    echo ""
    echo "Checking what apt-get actually did:"
    echo "  dpkg -l | grep -E '($(IFS='|'; echo "${PACKAGES_TO_INSTALL[*]%%=*}"))':"
    dpkg -l | grep -E "($(IFS='|'; echo "${PACKAGES_TO_INSTALL[*]%%=*}"))" || echo "  No matching packages found in dpkg -l"
    exit 1
  fi
else
  echo "No packages to install (all required packages are already installed or installation was skipped)"
  echo "Packages that were checked: ${PACKAGES_TO_PROCESS[*]}"
fi

# Install libimage-exiftool-perl with pinned version (skip for lint-only)
if [[ "$CATEGORY" != "lint" ]] && [ -n "$PINNED_LIBIMAGE_EXIFTOOL_PERL" ]; then
  echo "Installing libimage-exiftool-perl=${PINNED_LIBIMAGE_EXIFTOOL_PERL}..."

  # Check if already installed with correct version
  INSTALLED_APT_VERSION=$(dpkg -l | grep "^ii.*libimage-exiftool-perl" | awk '{print $3}' || echo "")
  if [ -n "$INSTALLED_APT_VERSION" ] && [ "$INSTALLED_APT_VERSION" = "$PINNED_LIBIMAGE_EXIFTOOL_PERL" ]; then
    echo "libimage-exiftool-perl ${INSTALLED_APT_VERSION} already installed (matches pinned version)"
  else
    if [ -n "$INSTALLED_APT_VERSION" ]; then
      echo "Removing existing libimage-exiftool-perl version ${INSTALLED_APT_VERSION} (installing pinned version ${PINNED_LIBIMAGE_EXIFTOOL_PERL})..."
      sudo apt-get remove -y libimage-exiftool-perl 2>/dev/null || true
    fi

    # Verify version is available before installing
    echo "Verifying libimage-exiftool-perl version ${PINNED_LIBIMAGE_EXIFTOOL_PERL} is available..."
    if ! apt-cache madison libimage-exiftool-perl 2>/dev/null | grep -q "$PINNED_LIBIMAGE_EXIFTOOL_PERL"; then
      echo "ERROR: libimage-exiftool-perl version ${PINNED_LIBIMAGE_EXIFTOOL_PERL} is not available."
      echo "Available versions:"
      apt-cache madison libimage-exiftool-perl 2>/dev/null | head -5 || echo "  (could not list versions)"
      exit 1
    fi

    # Install with --show-progress instead of -v
    if ! sudo apt-get install -y --show-progress --allow-downgrades --allow-change-held-packages "libimage-exiftool-perl=${PINNED_LIBIMAGE_EXIFTOOL_PERL}"; then
      echo "ERROR: Failed to install pinned version of libimage-exiftool-perl."
      echo "This may indicate network issues or the version is no longer available."
      exit 1
    fi

    # Verify it was actually installed
    INSTALLED_CHECK=$(dpkg -l | grep "^ii.*libimage-exiftool-perl" | awk '{print $2 " " $3}' || echo "")
    if [ -z "$INSTALLED_CHECK" ]; then
      echo "ERROR: libimage-exiftool-perl was not installed successfully."
      exit 1
    else
      echo "✓ ${INSTALLED_CHECK} installed"
    fi
  fi
fi

# Install id3v2 using shared script (skip for lint-only and test-only)
if [[ "$CATEGORY" =~ ^(prod|all)$ ]] && [ -n "$PINNED_ID3V2" ]; then
  echo "Installing id3v2..."
  "${SCRIPT_DIR}/install-id3v2-linux.sh" "${PINNED_ID3V2}"
fi

# Install bwfmetaedit using shared script (skip for lint-only and prod-only)
if [[ "$CATEGORY" =~ ^(test-only|all)$ ]]; then
  echo "Installing bwfmetaedit..."
  "${SCRIPT_DIR}/install-bwfmetaedit-ubuntu.sh"
fi
fi

# Install lint dependencies (PowerShell and shellcheck)
# Install for lint category or all category
if [[ "$CATEGORY" =~ ^(lint|all)$ ]]; then
  # Install PowerShell Core (required for PowerShell script linting in pre-commit hooks)
  echo "Installing PowerShell Core..."
  if command -v pwsh &>/dev/null; then
    echo "  PowerShell Core already installed"
  else
    echo "  Installing PowerShell Core via Microsoft repository..."
    # Add Microsoft repository for PowerShell
    sudo apt-get update
    sudo apt-get install -y wget apt-transport-https software-properties-common || {
      echo "ERROR: Failed to install prerequisites for PowerShell installation."
      exit 1
    }

    # Download and install Microsoft repository key
    wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb || {
      echo "ERROR: Failed to download Microsoft repository configuration."
      exit 1
    }
    sudo dpkg -i packages-microsoft-prod.deb || {
      echo "ERROR: Failed to install Microsoft repository configuration."
      rm -f packages-microsoft-prod.deb
      exit 1
    }
    rm -f packages-microsoft-prod.deb

    # Update package lists and install PowerShell
    sudo apt-get update
    sudo apt-get install -y powershell || {
      echo "ERROR: Failed to install PowerShell Core."
      echo "Install manually: https://github.com/PowerShell/PowerShell#get-powershell"
      exit 1
    }
  fi

  # Verify PowerShell installation
  if ! command -v pwsh &>/dev/null; then
    echo "WARNING: PowerShell Core installed but not found in PATH."
    echo "You may need to restart your terminal or check installation."
  fi

  # Install shellcheck (required for shell script linting in pre-commit hooks)
  load_lint_dependency_versions "$SCRIPT_DIR"

  if [ -n "$PINNED_SHELLCHECK" ]; then
    echo "Installing shellcheck=${PINNED_SHELLCHECK}..."

    # Check if shellcheck is already installed
    if command -v shellcheck &>/dev/null; then
      INSTALLED_VERSION=$(get_shellcheck_version)
      if [ -n "$INSTALLED_VERSION" ]; then
        # Check if installed version matches pinned version
        if check_shellcheck_version_match "$INSTALLED_VERSION" "$PINNED_SHELLCHECK"; then
          echo "  shellcheck ${INSTALLED_VERSION} already installed (matches pinned version ${PINNED_SHELLCHECK})"
        else
          echo "  Removing existing shellcheck version ${INSTALLED_VERSION} (installing pinned version ${PINNED_SHELLCHECK})..."
          sudo apt-get remove -y shellcheck 2>/dev/null || true
          sudo apt-get install -y "shellcheck=${PINNED_SHELLCHECK}" || {
            echo "ERROR: Failed to install shellcheck=${PINNED_SHELLCHECK}."
            echo "Install manually: sudo apt-get install shellcheck=${PINNED_SHELLCHECK}"
            exit 1
          }
        fi
      else
        echo "  shellcheck installed but version could not be determined, reinstalling..."
        sudo apt-get install -y "shellcheck=${PINNED_SHELLCHECK}" || {
          echo "ERROR: Failed to install shellcheck=${PINNED_SHELLCHECK}."
          echo "Install manually: sudo apt-get install shellcheck=${PINNED_SHELLCHECK}"
          exit 1
        }
      fi
    else
      echo "  Installing shellcheck=${PINNED_SHELLCHECK} via apt..."
      sudo apt-get install -y "shellcheck=${PINNED_SHELLCHECK}" || {
        echo "ERROR: Failed to install shellcheck=${PINNED_SHELLCHECK}."
        echo "Install manually: sudo apt-get install shellcheck=${PINNED_SHELLCHECK}"
        exit 1
      }
    fi

    # Verify shellcheck installation
    verify_shellcheck_installation "$PINNED_SHELLCHECK" "ubuntu" || true
  else
    echo "WARNING: PINNED_SHELLCHECK not set, skipping shellcheck installation"
  fi
fi

# Ensure standard binary paths are in PATH
# In some CI environments, PATH might not include standard locations
STANDARD_PATHS=("/usr/bin" "/usr/local/bin" "/bin")
for path in "${STANDARD_PATHS[@]}"; do
  if [ -d "$path" ] && [[ ":$PATH:" != *":${path}:"* ]]; then
    export PATH="${path}:$PATH"
    if [ -n "$GITHUB_PATH" ]; then
      echo "$path" >> "$GITHUB_PATH"
    fi
  fi
done

# Refresh command cache (helps in some shells after package installation)
hash -r 2>/dev/null || true

# Verify installed tools are available in PATH (skip for lint-only)
if [[ "$CATEGORY" != "lint" ]]; then
  echo "Verifying installed tools are available in PATH..."
  MISSING_TOOLS=()
  # Determine which tools to check based on category
  TOOLS_TO_CHECK=()
  if [[ "$CATEGORY" =~ ^(prod|all)$ ]]; then
    TOOLS_TO_CHECK+=(ffprobe flac metaflac id3v2)
  fi
  if [[ "$CATEGORY" =~ ^(test-only|all)$ ]]; then
    TOOLS_TO_CHECK+=(mediainfo exiftool)
  fi

  for tool in "${TOOLS_TO_CHECK[@]}"; do
    if ! command -v "$tool" &>/dev/null; then
      MISSING_TOOLS+=("$tool")
      # First, check standard locations directly
      FOUND_TOOL=""
      for std_path in /usr/bin /usr/local/bin /bin; do
        if [ -f "${std_path}/${tool}" ]; then
          FOUND_TOOL="${std_path}/${tool}"
          break
        fi
      done

      # If not found in standard paths, try to find via package manager
      if [ -z "$FOUND_TOOL" ]; then
        # Try common package names for the tool
        case "$tool" in
          ffprobe)
            FFMPEG_PKG=$(dpkg -l | grep -i "^ii.*ffmpeg" | head -1 | awk '{print $2}' || echo "")
            if [ -n "$FFMPEG_PKG" ]; then
              FOUND_TOOL=$(dpkg -L "$FFMPEG_PKG" 2>/dev/null | grep -E "/bin/ffprobe$" | head -1 || echo "")
            fi
            ;;
          exiftool)
            FOUND_TOOL=$(dpkg -L libimage-exiftool-perl 2>/dev/null | grep -E "/bin/exiftool$" | head -1 || echo "")
            ;;
          flac)
            FLAC_PKG=$(dpkg -l | grep -i "^ii.*flac" | head -1 | awk '{print $2}' || echo "")
            if [ -n "$FLAC_PKG" ]; then
              FOUND_TOOL=$(dpkg -L "$FLAC_PKG" 2>/dev/null | grep -E "/bin/flac$" | head -1 || echo "")
            fi
            ;;
          metaflac)
            FLAC_PKG=$(dpkg -l | grep -i "^ii.*flac" | head -1 | awk '{print $2}' || echo "")
            if [ -n "$FLAC_PKG" ]; then
              FOUND_TOOL=$(dpkg -L "$FLAC_PKG" 2>/dev/null | grep -E "/bin/metaflac$" | head -1 || echo "")
            fi
            ;;
        esac
      fi

      # If we found the tool, add its directory to PATH
      if [ -n "$FOUND_TOOL" ] && [ -f "$FOUND_TOOL" ]; then
        TOOL_DIR=$(dirname "$FOUND_TOOL")
        if [[ ":$PATH:" != *":${TOOL_DIR}:"* ]]; then
          export PATH="${TOOL_DIR}:$PATH"
          if [ -n "$GITHUB_PATH" ]; then
            echo "$TOOL_DIR" >> "$GITHUB_PATH"
          fi
          echo "  Found $tool at $FOUND_TOOL, added $TOOL_DIR to PATH"
        fi
      fi
    fi
  done

  # Refresh command cache after PATH updates
  hash -r 2>/dev/null || true

  # Re-check after PATH updates
  STILL_MISSING=()
  for tool in "${TOOLS_TO_CHECK[@]}"; do
    if ! command -v "$tool" &>/dev/null; then
      STILL_MISSING+=("$tool")
    fi
  done

  if [ ${#STILL_MISSING[@]} -ne 0 ]; then
    echo "ERROR: The following tools are not available in PATH after installation:"
    printf '  - %s\n' "${STILL_MISSING[@]}"
    echo ""
    echo "Current PATH: $PATH"
    echo ""
    echo "Attempting to locate installed packages..."
    for tool in "${STILL_MISSING[@]}"; do
      echo "  Searching for $tool:"
      # Try to find the package
      case "$tool" in
        ffprobe)
          echo "    Checking for ffmpeg packages:"
          dpkg -l | grep -i ffmpeg || echo "      No ffmpeg package found"
          FFMPEG_PKG=$(dpkg -l | grep -i "^ii.*ffmpeg" | head -1 | awk '{print $2}' || echo "")
          if [ -n "$FFMPEG_PKG" ]; then
            echo "    Found package: $FFMPEG_PKG"
            echo "    Listing binaries in package:"
            dpkg -L "$FFMPEG_PKG" 2>/dev/null | grep -E "/bin/ffprobe$" || echo "      ffprobe binary not found in package"
            echo "    Checking if ffprobe exists in filesystem:"
            find /usr -name "ffprobe" 2>/dev/null | head -3 || echo "      ffprobe not found in /usr"
          fi
          ;;
        flac)
          echo "    Checking for flac packages:"
          dpkg -l | grep -i "^ii.*flac" || echo "      No flac package found"
          FLAC_PKG=$(dpkg -l | grep -i "^ii.*flac" | head -1 | awk '{print $2}' || echo "")
          if [ -n "$FLAC_PKG" ]; then
            echo "    Found package: $FLAC_PKG"
            echo "    Listing binaries in package:"
            dpkg -L "$FLAC_PKG" 2>/dev/null | grep -E "/bin/flac$" || echo "      flac binary not found in package"
            echo "    Checking if flac exists in filesystem:"
            find /usr -name "flac" 2>/dev/null | head -3 || echo "      flac not found in /usr"
          fi
          ;;
        metaflac)
          echo "    Checking for flac packages (metaflac is part of flac):"
          dpkg -l | grep -i "^ii.*flac" || echo "      No flac package found"
          FLAC_PKG=$(dpkg -l | grep -i "^ii.*flac" | head -1 | awk '{print $2}' || echo "")
          if [ -n "$FLAC_PKG" ]; then
            echo "    Found package: $FLAC_PKG"
            echo "    Listing binaries in package:"
            dpkg -L "$FLAC_PKG" 2>/dev/null | grep -E "/bin/metaflac$" || echo "      metaflac binary not found in package"
            echo "    Checking if metaflac exists in filesystem:"
            find /usr -name "metaflac" 2>/dev/null | head -3 || echo "      metaflac not found in /usr"
          fi
          ;;
        exiftool)
          echo "    Checking for exiftool packages:"
          dpkg -l | grep -i exiftool || echo "      No exiftool package found"
          echo "    Checking libimage-exiftool-perl package:"
          if dpkg -l | grep -q "^ii.*libimage-exiftool-perl"; then
            echo "    Found package: libimage-exiftool-perl"
            echo "    Listing binaries in package:"
            dpkg -L libimage-exiftool-perl 2>/dev/null | grep -E "/bin/exiftool$" || echo "      exiftool binary not found in package"
            echo "    Checking if exiftool exists in filesystem:"
            find /usr -name "exiftool" 2>/dev/null | head -3 || echo "      exiftool not found in /usr"
          else
            echo "      libimage-exiftool-perl package not installed"
          fi
          ;;
        mediainfo)
          echo "    Checking for mediainfo packages:"
          dpkg -l | grep -i "^ii.*mediainfo" || echo "      No mediainfo package found"
          MEDIAINFO_PKG=$(dpkg -l | grep -i "^ii.*mediainfo" | head -1 | awk '{print $2}' || echo "")
          if [ -n "$MEDIAINFO_PKG" ]; then
            echo "    Found package: $MEDIAINFO_PKG"
            echo "    Listing binaries in package:"
            dpkg -L "$MEDIAINFO_PKG" 2>/dev/null | grep -E "/bin/mediainfo$" || echo "      mediainfo binary not found in package"
            echo "    Checking if mediainfo exists in filesystem:"
            find /usr -name "mediainfo" 2>/dev/null | head -3 || echo "      mediainfo not found in /usr"
          fi
          ;;
        id3v2)
          echo "    Checking for id3v2:"
          which id3v2 2>/dev/null || find /usr -name "id3v2" 2>/dev/null | head -3 || echo "      id3v2 not found"
          ;;
      esac
      echo ""
    done
    echo ""
    echo "Installation may have failed. Check the output above for errors."
    exit 1
  fi

  # Verify installed versions match pinned versions using shared Python script
  echo ""
  echo "Verifying installed versions match pinned versions..."
  if ! python3 "${SCRIPT_DIR}/verify-system-dependency-versions.py"; then
    echo ""
    echo "ERROR: Version verification failed. Installed versions don't match pinned versions."
    exit 1
  fi
fi

# Check/install npm/node (required for git-worktree-scripts dev dependency)
echo ""
echo "Checking npm/node installation (required for git-worktree-scripts)..."
if ! command -v npm &>/dev/null; then
  if ! command -v node &>/dev/null; then
    echo "Installing Node.js and npm..."
    if ! curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -; then
      echo "ERROR: Failed to add NodeSource repository."
      exit 1
    fi
    if ! sudo apt-get install -y nodejs; then
      echo "ERROR: Failed to install Node.js."
      exit 1
    fi
  else
    echo "Node.js is installed but npm is not available."
    echo "Installing npm..."
    if ! sudo apt-get install -y npm; then
      echo "ERROR: Failed to install npm."
      exit 1
    fi
  fi
fi

# Verify npm is available in PATH after installation
if ! command -v npm &>/dev/null; then
  echo "ERROR: npm is not available in PATH after installation."
  exit 1
fi

echo "  npm is installed: $(npm --version)"

echo "All system dependencies installed successfully!"
