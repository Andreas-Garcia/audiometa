# AudioMeta Python

A comprehensive Python library for reading and writing audio metadata across multiple formats including MP3, FLAC, WAV, and more.

## Features

- **Multi-format Support**: ID3v1, ID3v2, Vorbis (OGG/FLAC), and RIFF (WAV) metadata formats
- **Comprehensive Metadata Fields**: Support for 50+ metadata fields including title, artist, album, rating, BPM, and more
- **Read/Write Operations**: Full read and write support for most formats
- **Rating Support**: Normalized rating handling across different formats
- **Technical Information**: Access to bitrate, duration, sample rate, channels, and more
- **Error Handling**: Robust error handling with specific exception types
- **Type Hints**: Full type annotation support for better IDE integration

## Supported Formats

| Format | Read | Write | Rating Support | Notes                         |
| ------ | ---- | ----- | -------------- | ----------------------------- |
| ID3v1  | ✅   | ✅    | ❌             | Limited to 30 chars per field |
| ID3v2  | ✅   | ✅    | ✅             | Full feature support          |
| Vorbis | ✅   | ✅    | ✅             | OGG/FLAC files                |
| RIFF   | ✅   | ✅    | ❌             | WAV files                     |

## File Format Support by Metadata Manager

Each metadata manager has specific file format requirements and support:

### ID3v1 Manager

- **Primary Support**: MP3 files (native ID3v1 format, optimal)
- **Extended Support**: FLAC and WAV files that may contain ID3v1 tags (not optimal but supported)
- **Note**: While ID3v1 is natively designed for MP3 files, some FLAC and WAV files may contain ID3v1 tags, which this manager can read

### ID3v2 Manager

- **Supported Formats**: MP3, WAV, FLAC
- **Note**: ID3v2 is the most versatile format and works across multiple file types

### Vorbis Manager

- **Primary Support**: FLAC files (native Vorbis comments)
- **Extended Support**: OGG files
- **Note**: Vorbis comments are the standard metadata format for FLAC and OGG files

### RIFF Manager

- **Strict Support**: WAV files only
- **Note**: RIFF is the native metadata format for WAV files and is not supported in other formats

## Installation

```bash
pip install audiometa-python
```

## Quick Start

### Basic Usage

```python
from audiometa import get_merged_app_metadata, update_file_metadata, AudioFile

# Read metadata from a file
metadata = get_merged_app_metadata("path/to/your/audio.mp3")
print(f"Title: {metadata.get('title', 'Unknown')}")
print(f"Artist: {metadata.get('artists_names', ['Unknown'])}")
print(f"Album: {metadata.get('album_name', 'Unknown')}")

# Update metadata
new_metadata = {
    'title': 'New Song Title',
    'artists_names': ['Artist Name'],
    'album_name': 'Album Name',
    'rating': 85
}
update_file_metadata("path/to/your/audio.mp3", new_metadata)
```

### Working with AudioFile

```python
from audiometa import AudioFile

# Create an AudioFile instance
audio_file = AudioFile("path/to/your/audio.flac")

# Get technical information
print(f"Duration: {audio_file.get_duration_in_sec()} seconds")
print(f"Bitrate: {audio_file.get_bitrate()} kbps")
print(f"File extension: {audio_file.file_extension}")

# Check FLAC MD5 validity
if audio_file.file_extension == '.flac':
    is_valid = audio_file.is_flac_file_md5_valid()
    print(f"FLAC MD5 valid: {is_valid}")
```

### Format-Specific Operations

```python
from audiometa import get_single_format_app_metadata, MetadataFormat

# Read only ID3v2 metadata
id3v2_metadata = get_single_format_app_metadata(
    "path/to/your/audio.mp3",
    MetadataFormat.ID3V2
)

# Read only Vorbis metadata
vorbis_metadata = get_single_format_app_metadata(
    "path/to/your/audio.ogg",
    MetadataFormat.VORBIS
)
```

### Specific Metadata Fields

```python
from audiometa import get_specific_metadata, AppMetadataKey

# Get specific metadata fields
title = get_specific_metadata("path/to/your/audio.mp3", AppMetadataKey.TITLE)
rating = get_specific_metadata("path/to/your/audio.mp3", AppMetadataKey.RATING)
bpm = get_specific_metadata("path/to/your/audio.mp3", AppMetadataKey.BPM)
```

## Supported Metadata Fields

The library supports a comprehensive set of metadata fields across different audio formats. The table below shows which fields are supported by each format:

### Metadata Support by Format

| Field             | ID3v1          | ID3v2          | Vorbis       | RIFF          | App Support |
| ----------------- | -------------- | -------------- | ------------ | ------------- | ----------- |
| Text Encoding     | ASCII          | UTF-8/16/ISO   | UTF-8        | ASCII/UTF-8   | UTF-8       |
| Max Text Length   | 30 chars       | ~8M chars      | ~8M chars    | ~1M chars     | 255 chars   |
| Rating Range      | Not supported  | 0-255#         | 0-100#       | Not supported | 0-100#      |
| Track Number      | 0-255#         | 0-255#         | Unlimited#   | Unlimited#    | 0-999#      |
| Disc Number       | Not supported  | 0-255#         | Unlimited#   | Not supported | 0-999#      |
| Operations        | R              | R/W            | R/W          | R/W           | ✓           |
| supported         | (W using v2.4) | (W using v2.4) |              |               |             |
| Technical Info    |                |                |              |               |             |
| - Duration        | ✓              | ✓              | ✓            | ✓             |             |
| - Bitrate         | ✓              | ✓              | ✓            | ✓             | ✓           |
| - Sample Rate     | ✓              | ✓              | ✓            | ✓             |             |
| - Channels        | ✓ (1-2)        | ✓ (1-255)      | ✓ (1-255)    | ✓ (1-2)       |             |
| - File Size       | ✓              | ✓              | ✓            | ✓             | ✓           |
| - Format Info     | ✓              | ✓              | ✓            | ✓             |             |
| - MD5 Checksum    |                |                | ✓            |               | ✓ (Flac)    |
| Title             | ✓ (30)         | ✓ (256)        | ✓ (256)      | ✓ (256)       | ✓ (256)     |
| Artist            | ✓ (30)         | ✓ (256)        | ✓ (256)      | ✓ (256)       | ✓ (256)     |
| Album             | ✓ (30)         | ✓ (256)        | ✓ (256)      | ✓ (256)       | ✓ (256)     |
| Album Artist      |                | ✓ (256)        | ✓ (256)      |               | ✓ (256)     |
| Genre             | ✓ (1#)         | ✓ (256)        | ✓ (256)      | ✓ (256)       | ✓ (256)     |
| Release Date      | ✓ (4)          | ✓ (10)         | ✓ (10)       | ✓ (10)        | (10)        |
| Track Number      | ✓ (1#)         | ✓ (0-255#)     | ✓ (Unlim#)   | ✓ (Unlim#)    | (0-999#)    |
| Rating            |                | ✓ (0-255#)     | ✓ (0-100#)   |               | ✓ (0-10#)   |
| BPM               |                | ✓ (0-65535#)   | ✓ (0-65535#) |               | (0-999#)    |
| Language          |                | ✓ (3)          | ✓ (3)        |               | ✓ (3)       |
| Composer          |                | ✓ (256)        | ✓ (256)      | ✓ (256)       | (256)       |
| Publisher         |                | ✓ (256)        | ✓ (256)      |               | (256)       |
| Copyright         |                | ✓ (256)        | ✓ (256)      | ✓ (256)       | (256)       |
| Lyrics            |                | ✓ (2000)       | ✓ (2000)     |               | (2000)      |
| Comment           | ✓ (28)         | ✓ (1000)       | ✓ (1000)     | ✓ (1000)      | (1000)      |
| Encoder           |                | ✓ (256)        | ✓ (256)      | ✓ (256)       | (256)       |
| URL               |                | ✓ (2048)       | ✓ (2048)     |               | (2048)      |
| ISRC              |                | ✓ (12)         | ✓ (12)       |               | (12)        |
| Mood              |                | ✓ (256)        | ✓ (256)      |               | (256)       |
| Key               |                | ✓ (3)          | ✓ (3)        |               | (3)         |
| Original Date     |                | ✓ (10)         | ✓ (10)       |               | (10)        |
| Remixer           |                | ✓ (256)        | ✓ (256)      |               | (256)       |
| Conductor         |                | ✓ (256)        | ✓ (256)      | ✓ (256)       | (256)       |
| Cover Art         |                | ✓ (10MB#)      | ✓ (10MB#)    |               | (10MB#)     |
| Compilation       |                | ✓ (1#)         | ✓ (1#)       |               | (1#)        |
| Media Type        |                | ✓ (256)        | ✓ (256)      | ✓ (256)       | (256)       |
| File Owner        |                | ✓ (256)        | ✓ (256)      |               | (256)       |
| Recording Date    |                | ✓ (10)         | ✓ (10)       |               | (10)        |
| File Size         |                | ✓ (16#)        |              |               | (16#)       |
| Encoder Settings  |                | ✓ (1000)       | ✓ (1000)     |               | (1000)      |
| ReplayGain        |                | ✓ (8#)         | ✓ (8#)       |               | (8#)        |
| MusicBrainz ID    |                | ✓ (36)         | ✓ (36)       |               | (36)        |
| Arranger          |                | ✓ (256)        | ✓ (256)      |               | (256)       |
| Version           |                | ✓ (256)        | ✓ (256)      |               | (256)       |
| Performance       |                | ✓ (256)        | ✓ (256)      |               | (256)       |
| Archival Location |                |                |              | ✓ (256)       | (256)       |
| Keywords          |                |                |              | ✓ (256)       | (256)       |
| Subject           |                |                |              | ✓ (256)       | (256)       |
| Original Artist   |                | ✓ (256)        | ✓ (256)      |               | (256)       |
| Set Subtitle      |                | ✓ (256)        | ✓ (256)      |               | (256)       |
| Initial Key       |                | ✓ (3)          | ✓ (3)        |               | (3)         |
| Involved People   |                | ✓ (1000)       | ✓ (1000)     |               | (1000)      |
| Musicians         |                | ✓ (1000)       | ✓ (1000)     |               | (1000)      |
| Part of Set       |                | ✓ (256)        | ✓ (256)      |               | (256)       |

### Legend

- ✓: Supported
- (30): Fixed 30-character field
- (#): Numeric value or code
- (255): Maximum 255 characters
- (1000): Maximum 1000 characters
- (2000): Maximum 2000 characters
- (10MB#): Maximum 10 megabytes binary data
- (~8M): Approximately 8 million characters (format limit)
- (~1M): Approximately 1 million characters (format limit)

## Error Handling

The library provides specific exception types for different error conditions:

```python
from audiometa.exceptions import (
    FileCorruptedError,
    FileTypeNotSupportedError,
    MetadataNotSupportedError
)

try:
    metadata = get_merged_app_metadata("invalid_file.txt")
except FileTypeNotSupportedError:
    print("File format not supported")
except FileCorruptedError:
    print("File is corrupted")
except MetadataNotSupportedError:
    print("Metadata field not supported for this format")
```

## Requirements

- Python 3.8+
- mutagen >= 1.45.0
- ffprobe (for WAV file processing)
- flac (for FLAC MD5 validation)

## Development

### Setup Development Environment

```bash
git clone https://github.com/your-username/audiometa-python.git
cd audiometa-python
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black audio_metadata/
isort audio_metadata/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed list of changes.
