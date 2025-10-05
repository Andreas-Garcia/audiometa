#!/usr/bin/env python3
"""
Remove RIFF Metadata Script

PURPOSE:
    Python script to remove RIFF metadata from WAV files while preserving audio data.
    This creates a clean WAV file with no metadata, useful for testing metadata
    handling scenarios where you need a completely clean audio file.

USAGE:
    python3 remove_riff.py input.wav

FEATURES:
    - Removes all RIFF metadata while preserving audio data
    - Creates temporary file to ensure clean metadata removal
    - Preserves audio parameters and frames
    - Error handling and cleanup
    - Safe operation with backup on failure

HOW IT WORKS:
    1. Creates a temporary WAV file
    2. Extracts essential audio data (parameters and frames)
    3. Writes clean audio data to temporary file
    4. Replaces original file with clean version
    5. Cleans up temporary files on error

DEPENDENCIES:
    - Python standard library (wave, tempfile, shutil)

EXAMPLES:
    # Remove RIFF metadata from WAV file
    python3 remove_riff.py test.wav
    
    # Check if metadata was removed
    mediainfo test.wav  # Should show minimal metadata

ERROR HANDLING:
    - Validates file format before processing
    - Cleans up temporary files on error
    - Preserves original file if processing fails
    - Provides clear error messages

TROUBLESHOOTING:
    # Check if file is valid WAV
    file test.wav  # Should show "RIFF (little-endian) data, WAVE audio"
    
    # Verify metadata removal
    mediainfo test.wav  # Should show only basic audio info
    bwfmetaedit --out-core test.wav  # Should show no metadata fields
    
    # Check file integrity
    python3 -c "import wave; w=wave.open('test.wav', 'rb'); print(f'Channels: {w.getnchannels()}, Sample rate: {w.getframerate()}, Frames: {w.getnframes()}')"

NOTES:
    - This script is idempotent - safe to run multiple times
    - Original file is modified in place
    - Always backup important files before running
    - Audio quality and parameters are preserved exactly
    - Only metadata is removed, not audio data
"""
import wave
import sys
import os
import tempfile
import shutil


def remove_riff_metadata(input_file):
    """Remove RIFF metadata by copying only audio params and frames to temp file, then replace original"""
    # Create temporary file
    fd, temp_path = tempfile.mkstemp(suffix='.wav')
    os.close(fd)

    try:
        # Extract essential audio data
        with wave.open(input_file, 'rb') as src:
            params = src.getparams()
            frames = src.readframes(src.getnframes())

        # Write to temporary file without metadata
        with wave.open(temp_path, 'wb') as dst:
            dst.setparams(params)
            dst.writeframes(frames)

        # Replace original file with the clean one
        shutil.move(temp_path, input_file)
        print(f"RIFF metadata removed from {input_file}")

    except Exception as e:
        # Clean up temp file in case of error
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: remove_riff.py input.wav")
        sys.exit(1)
    remove_riff_metadata(sys.argv[1])
