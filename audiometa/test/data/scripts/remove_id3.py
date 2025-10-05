#!/usr/bin/env python3
"""
Remove ID3 Tags Script

PURPOSE:
    Python script to remove ID3 tags while preserving native format metadata.
    This is useful for testing metadata handling when you want to remove ID3
    tags but keep the native format metadata intact.

USAGE:
    python3 remove_id3.py <audio_file> [audio_file2 ...]

FEATURES:
    - Removes ID3 tags from audio files
    - Preserves native format metadata (Vorbis comments in FLAC, RIFF metadata in WAV)
    - Supports multiple file formats: MP3, FLAC, WAV
    - Error handling for files without ID3 tags
    - Batch processing of multiple files

SUPPORTED FORMATS:
    - MP3: Removes ID3 tags completely (no native metadata to preserve)
    - FLAC: Removes ID3 tags, preserves Vorbis comments
    - WAV: Removes ID3 tags, preserves RIFF metadata

DEPENDENCIES:
    - mutagen library for audio file manipulation

INSTALLATION:
    pip install mutagen

EXAMPLES:
    # Remove ID3 from single file
    python3 remove_id3.py test.mp3
    
    # Remove ID3 from multiple files
    python3 remove_id3.py test.mp3 test.flac test.wav
    
    # Remove ID3 from all files in directory
    python3 remove_id3.py *.mp3 *.flac *.wav

ERROR HANDLING:
    - Gracefully handles files without ID3 tags
    - Preserves audio data integrity
    - Provides clear error messages for processing failures
    - Continues processing other files if one fails

TROUBLESHOOTING:
    # Check if mutagen is installed
    python3 -c "import mutagen; print('mutagen installed')"
    
    # Check file format support
    python3 -c "from mutagen.flac import FLAC; from mutagen.mp3 import MP3; from mutagen.wave import WAVE; print('All formats supported')"
    
    # Verify ID3 removal
    id3v2 -l test.mp3  # Should show "No ID3v1 tag found" and "No ID3v2 tag found"

NOTES:
    - This script is idempotent - safe to run multiple times
    - Original files are modified in place
    - Always backup important files before running
    - For FLAC files, Vorbis comments are preserved and saved
    - For WAV files, RIFF metadata is preserved and saved
"""
import sys
import os
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.wave import WAVE
from mutagen.mp3 import MP3


def remove_id3_tags(filename):
    """Remove ID3 tags while preserving native format metadata"""
    file_ext = os.path.splitext(filename)[1].lower()

    try:
        # Always try to remove ID3 tags first
        try:
            ID3(filename).delete()
            print(f"ID3 tags removed from {filename}")
        except:
            print(f"No ID3 tags found or could not remove from {filename}")

        # Format-specific preservation of native metadata
        if file_ext == '.flac':
            audio = FLAC(filename)
            audio.save()
            print(f"FLAC Vorbis comments preserved in {filename}")
        elif file_ext == '.wav':
            audio = WAVE(filename)
            audio.save()
            print(f"WAV RIFF metadata preserved in {filename}")
        elif file_ext == '.mp3':
            # For MP3, we've already removed ID3 so nothing more to do
            print(f"MP3 processed {filename}")
        else:
            print(f"Unknown file type: {filename}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: remove_id3.py <audio_file> [audio_file2 ...]")
        sys.exit(1)

    for filename in sys.argv[1:]:
        remove_id3_tags(filename)
