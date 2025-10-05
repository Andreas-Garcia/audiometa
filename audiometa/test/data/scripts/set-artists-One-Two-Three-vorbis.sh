#!/bin/bash
#
# Multi-Artist Test Script
#
# PURPOSE:
#     Sets multiple artist values for testing multi-artist support in Vorbis comments.
#     This script is specifically designed to test how the audiometa library handles
#     multiple artist values in Vorbis comments, which is a common scenario in music metadata.
#
# USAGE:
#     ./set-artists-One-Two-Three-vorbis.sh <flac_file>
#
# FEATURES:
#     - Sets three separate ARTIST tags: "One", "Two", "Three"
#     - Tests multi-artist metadata handling
#     - Removes existing ARTIST tags to avoid duplicates
#     - Verifies the changes using metaflac
#     - Tests Vorbis comment array support
#     - Error handling and validation
#
# DEPENDENCIES:
#     - metaflac tool for FLAC metadata manipulation
#
# INSTALLATION:
#     brew install flac  # provides metaflac
#
# PROCESS:
#     1. Validation: Checks if file exists and metaflac is available
#     2. Cleanup: Removes any existing ARTIST tags to avoid duplicates
#     3. Setting: Sets three separate ARTIST tags:
#        - ARTIST=One
#        - ARTIST=Two
#        - ARTIST=Three
#     4. Verification: Lists all ARTIST tags to confirm success
#
# EXAMPLES:
#     # Set multiple artists
#     ./set-artists-One-Two-Three-vorbis.sh test.flac
#     
#     # Verify the results
#     metaflac --list --tag=ARTIST test.flac
#     metaflac --list test.flac | grep ARTIST
#
# VERIFICATION:
#     The script automatically verifies the changes by listing all ARTIST tags:
#     metaflac --list --tag=ARTIST test.flac
#     You should see three separate ARTIST entries.
#
# USE CASES:
#     - Testing multi-artist metadata handling
#     - Verifying artist array processing
#     - Testing edge cases with multiple values
#     - Validating Vorbis comment array support
#     - Testing artist list handling in audiometa library
#
# TROUBLESHOOTING:
#     # Check if metaflac is installed
#     which metaflac
#     
#     # Install if missing (macOS)
#     brew install flac  # provides metaflac
#     
#     # Check file format
#     file test.flac  # Should show "FLAC audio"
#     
#     # Verify multiple artists were set
#     metaflac --list --tag=ARTIST test.flac  # Should show 3 entries
#     metaflac --list test.flac | grep -c ARTIST  # Should show 3
#
# NOTES:
#     - This script is idempotent - safe to run multiple times
#     - Original file is modified in place
#     - Always backup important files before running
#     - Vorbis comments support multiple values for the same tag
#     - This tests the audiometa library's handling of artist arrays
#     - Useful for testing collaborative tracks and compilation albums
#

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <flac_file>"
    exit 1
fi

# Resolve the file path and check if file exists
FLAC_FILE=$(readlink -f "$1")
if [ ! -f "$FLAC_FILE" ]; then
    echo "Error: File not found: $1"
    exit 1
fi

# Check if metaflac is available
if ! command -v metaflac &> /dev/null; then
    echo "Error: metaflac is required but not installed."
    exit 1
fi

echo "Setting artists metadata for: $FLAC_FILE"

# First remove any existing ARTIST tags to avoid duplicates
metaflac --remove-tag=ARTIST "$FLAC_FILE"

# Set three specific artists using separate ARTIST tags
metaflac \
    --set-tag="ARTIST=One" \
    --set-tag="ARTIST=Two" \
    --set-tag="ARTIST=Three" \
    "$FLAC_FILE"

RESULT=$?
if [ $RESULT -eq 0 ]; then
    echo "Artists metadata set successfully!"
    # Verify the changes
    echo "Current artists metadata:"
    metaflac --list --tag=ARTIST "$FLAC_FILE"
else
    echo "Error: Failed to write artists metadata (exit code: $RESULT)"
    exit 1
fi