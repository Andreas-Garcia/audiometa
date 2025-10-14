# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **ID3v1 writing support**: ID3v1 metadata can now be written and modified (previously read-only)
- Direct file manipulation for ID3v1 tags using 128-byte structure
- ID3v1 field truncation and validation (30-character limits for text fields)
- ID3v1 genre name to code conversion
- ID3v1.1 track number support (1-255 range)
- ID3v1 metadata deletion support
- ID3v2 version selection for MP3 files
- Support for choosing between ID3v2.3 (maximum compatibility) and ID3v2.4 (modern features)
- `id3v2_version` parameter in all metadata functions
- Automatic version upgrade when reading existing files

### Changed

- **ID3v1 is no longer read-only**: Full read/write support with direct file manipulation
- ID3v1 now supports all metadata writing strategies (SYNC, PRESERVE, CLEANUP)
- ID3v1 field mapping updated to use RELEASE_DATE instead of YEAR
- Default ID3v2 version changed from v2.4 to v2.3 for maximum compatibility
- ID3v2Manager now accepts `id3v2_version` parameter
- All public API functions now support `id3v2_version` parameter

### Technical Details

- **ID3v1 Implementation**: Uses direct file manipulation instead of mutagen for writing
- **Field Constraints**: Automatic truncation to 30 characters for text fields, 4 characters for year
- **Encoding**: Latin-1 encoding with error handling for non-ASCII characters
- **Genre Handling**: Automatic conversion from genre names to ID3v1 genre codes (0-255)
- **Track Numbers**: ID3v1.1 format with null byte indicator and 1-255 range validation
- **File Structure**: Maintains 128-byte fixed structure at end of file
- **Compatibility**: Works with MP3, FLAC, and WAV files containing ID3v1 tags

## [0.1.0] - 2024-10-03

### Added

- Initial migration release (UNSTABLE) by [Andreas Garcia](https://github.com/Andreas-Garcia)
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

- **ID3v1**: Read/Write with direct file manipulation (limited to 30 chars per field, Latin-1 encoding)
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
