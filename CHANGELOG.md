# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2024-10-03

### Added

- Initial migration release (UNSTABLE)
- First step in migration from legacy audio metadata project
- Support for ID3v1, ID3v2, Vorbis, and RIFF formats
- Comprehensive metadata field support (50+ fields)
- Full read/write operations for most formats
- Rating support across different formats
- Type hints and comprehensive error handling
- Technical information access (bitrate, duration, sample rate, channels)
- FLAC MD5 validation support
- Support for cover art and lyrics
- MusicBrainz ID support
- ReplayGain information
- Multiple metadata field categories:
  - Basic information (title, artist, album, genre, rating)
  - Technical information (release date, track number, BPM, language)
  - Additional metadata (composer, publisher, copyright, lyrics, etc.)

### Supported Formats

- **ID3v1**: Read/Write (limited to 30 chars per field, no rating support)
- **ID3v2**: Read/Write with full feature support including ratings (v2.2, v2.3, v2.4)
- **Vorbis**: Read/Write for FLAC files with rating support (OGG file support is planned but not yet implemented)
- **RIFF**: Read/Write for WAV files (no rating support)

### Requirements

- Python 3.8+
- mutagen >= 1.45.0
- ffprobe (for WAV file processing)
- flac (for FLAC MD5 validation)

### Migration Notes

- This is an unstable pre-release version
- API may change significantly in future releases
- Not recommended for production use until stable release
- Migrated from legacy audio metadata project with improved architecture
