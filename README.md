# AudioMeta Python

A comprehensive Python library for reading and writing audio metadata across multiple formats including MP3, FLAC, WAV, and more.

## Features

- **Multi-format Support**: ID3v1, ID3v2, Vorbis (FLAC), and RIFF (WAV) metadata formats
- **Comprehensive Metadata Fields**: Support for 50+ metadata fields including title, artist, album, rating, BPM, and more
- **Read/Write Operations**: Full read and write support for most formats
- **Rating Support**: Normalized rating handling across different formats
- **Technical Information**: Access to bitrate, duration, sample rate, channels, and more
- **Error Handling**: Robust error handling with specific exception types

**Note**: OGG file support is planned but not yet implemented.

- **Type Hints**: Full type annotation support for better IDE integration

## Supported Formats

| Format | Read | Write | Rating Support | Notes                                    |
| ------ | ---- | ----- | -------------- | ---------------------------------------- |
| ID3v1  | ✅   | ❌    | ❌             | Read-only, limited to 30 chars per field |
| ID3v2  | ✅   | ✅    | ✅             | Full feature support                     |
| Vorbis | ✅   | ✅    | ✅             | FLAC files                               |
| RIFF   | ✅   | ✅    | ❌             | WAV files                                |

## File Format Support by Metadata Manager

Each metadata manager has specific file format requirements and support:

### ID3v1 Manager

- **Primary Support**: MP3 files (native ID3v1 format, optimal)
- **Extended Support**: FLAC and WAV files that may contain ID3v1 tags (not optimal but supported)
- **Operations**: Read-only (writing not supported due to fixed 128-byte structure)
- **Note**: While ID3v1 is natively designed for MP3 files, some FLAC and WAV files may contain ID3v1 tags, which this manager can read

### ID3v2 Manager

- **Supported Formats**: MP3, WAV, FLAC
- **Note**: ID3v2 is the most versatile format and works across multiple file types

### Vorbis Manager

- **Primary Support**: FLAC files (native Vorbis comments)
- **Note**: Vorbis comments are the standard metadata format for FLAC files

### RIFF Manager

- **Strict Support**: WAV files only
- **Limitations**: Some metadata fields not supported (raises `MetadataNotSupportedError`)
- **Note**: RIFF is the native metadata format for WAV files and is not supported in other formats

## Installation

```bash
pip install audiometa-python
```

## Quick Start

### Basic Usage

```python
from audiometa import get_merged_unified_metadata, update_file_metadata, AudioFile

# Read metadata from a file
metadata = get_merged_unified_metadata("path/to/your/audio.mp3")
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
    "path/to/your/audio.flac",
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

| Field             | ID3v1          | ID3v2          | Vorbis       | RIFF          | AudioMeta Support |
| ----------------- | -------------- | -------------- | ------------ | ------------- | ----------------- |
| Text Encoding     | ASCII          | UTF-8/16/ISO   | UTF-8        | ASCII/UTF-8   | UTF-8             |
| Max Text Length   | 30 chars       | ~8M chars      | ~8M chars    | ~1M chars     | Format limit      |
| Rating Range      | Not supported  | 0-255#         | 0-100#       | Not supported | 0-10#             |
| Track Number      | 0-255#         | 0-255#         | Unlimited#   | Unlimited#    | Format limit      |
| Disc Number       | Not supported  | 0-255#         | Unlimited#   | Not supported | Format limit      |
| Operations        | R              | R/W            | R/W          | R/W           | ✓                 |
| supported         | (W using v2.4) | (W using v2.4) |              |               |                   |
| Technical Info    |                |                |              |               |                   |
| - Duration        | ✓              | ✓              | ✓            | ✓             | ✓                 |
| - Bitrate         | ✓              | ✓              | ✓            | ✓             | ✓                 |
| - Sample Rate     | ✓              | ✓              | ✓            | ✓             | ✓                 |
| - Channels        | ✓ (1-2)        | ✓ (1-255)      | ✓ (1-255)    | ✓ (1-2)       | ✓                 |
| - File Size       | ✓              | ✓              | ✓            | ✓             | ✓                 |
| - Format Info     | ✓              | ✓              | ✓            | ✓             | ✓                 |
| - MD5 Checksum    |                |                | ✓            |               | ✓ (Flac)          |
| Title             | ✓ (30)         | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                 |
| Artist            | ✓ (30)         | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                 |
| Album             | ✓ (30)         | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                 |
| Album Artist      |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Genre             | ✓ (1#)         | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                 |
| Release Date      | ✓ (4)          | ✓ (10)         | ✓ (10)       | ✓ (10)        | ✓                 |
| Track Number      | ✓ (1#)         | ✓ (0-255#)     | ✓ (Unlim#)   | ✓ (Unlim#)    | ✓                 |
| Rating            |                | ✓ (0-255#)     | ✓ (0-100#)   |               | ✓                 |
| BPM               |                | ✓ (0-65535#)   | ✓ (0-65535#) |               | ✓                 |
| Language          |                | ✓ (3)          | ✓ (3)        |               | ✓                 |
| Composer          |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                 |
| Publisher         |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Copyright         |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                 |
| Lyrics            |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Comment           | ✓ (28)         | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                 |
| Encoder           |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                 |
| URL               |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| ISRC              |                | ✓ (12)         | ✓ (12)       |               | ✓                 |
| Mood              |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Key               |                | ✓ (3)          | ✓ (3)        |               | ✓                 |
| Original Date     |                | ✓ (10)         | ✓ (10)       |               | ✓                 |
| Remixer           |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Conductor         |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                 |
| Cover Art         |                | ✓ (10MB#)      | ✓ (10MB#)    |               | ✓                 |
| Compilation       |                | ✓ (1#)         | ✓ (1#)       |               | ✓                 |
| Media Type        |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                 |
| File Owner        |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Recording Date    |                | ✓ (10)         | ✓ (10)       |               | ✓                 |
| File Size         |                | ✓ (16#)        |              |               | ✓                 |
| Encoder Settings  |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| ReplayGain        |                | ✓ (8#)         | ✓ (8#)       |               | ✓                 |
| MusicBrainz ID    |                | ✓ (36)         | ✓ (36)       |               | ✓                 |
| Arranger          |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Version           |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Performance       |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Archival Location |                |                |              | ✓ (Format)    | ✓                 |
| Keywords          |                |                |              | ✓ (Format)    | ✓                 |
| Subject           |                |                |              | ✓ (Format)    | ✓                 |
| Original Artist   |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Set Subtitle      |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Initial Key       |                | ✓ (3)          | ✓ (3)        |               | ✓                 |
| Involved People   |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Musicians         |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |
| Part of Set       |                | ✓ (Format)     | ✓ (Format)   |               | ✓                 |

### Legend

- ✓: Supported
- (30): Fixed 30-character field (ID3v1 limitation)
- (#): Numeric value or code
- (Format): Limited by the audio format's native capabilities
- (10MB#): Maximum 10 megabytes binary data
- (~8M): Approximately 8 million characters (format limit)
- (~1M): Approximately 1 million characters (format limit)

**AudioMeta Support Column**: Shows the library's unified interface capabilities. The library does not impose artificial limits - it respects each format's native capabilities. Text fields can be as long as the format allows, and numeric ranges follow the format's specifications. The library provides consistent UTF-8 encoding and normalized rating handling (0-10 scale) across all supported formats.

### Reading Priorities (Tag Precedence)

When the same metadata tag exists in multiple formats within the same file, the library follows this precedence order for reading:

1. **Vorbis** (highest precedence)
2. **ID3v2**
3. **RIFF**
4. **ID3v1** (lowest precedence, read-only)

**Example**: If a title exists in both ID3v1 and ID3v2, the ID3v2 title will be returned.

### Writing Defaults by Audio Format

When writing metadata, the library uses these default metadata formats per audio file type:

#### MP3 Files

**Default Writing Format**: ID3v2 (v2.4)

- **Note**: ID3v1 cannot be written to

#### FLAC Files

**Default Writing Format**: Vorbis Comments

- **Note**: Vorbis is the native format for FLAC files

#### WAV Files

**Default Writing Format**: RIFF

- **Note**: RIFF is the native format for WAV files

**Note**: ID3v1 is read-only and cannot be written programmatically. The library will read from existing ID3v1 tags but will not attempt to write to them.

## Error Handling

The library provides specific exception types for different error conditions:

```python
from audiometa.exceptions import (
    FileCorruptedError,
    FileTypeNotSupportedError,
    MetadataNotSupportedError
)

try:
    metadata = get_merged_unified_metadata("invalid_file.txt")
except FileTypeNotSupportedError:
    print("File format not supported")
except FileCorruptedError:
    print("File is corrupted")
except MetadataNotSupportedError:
    print("Metadata field not supported for this format")
```

## Unsupported Metadata Handling

The library follows a **"fail fast, fail clearly"** approach for unsupported metadata. When attempting to update metadata that is not supported by a specific format, the library will raise `MetadataNotSupportedError` with a clear message.

### Format-Specific Limitations

| Format         | Behavior                                                    |
| -------------- | ----------------------------------------------------------- |
| **RIFF (WAV)** | Any unsupported metadata raises `MetadataNotSupportedError` |
| **ID3v1**      | Any unsupported metadata raises `MetadataNotSupportedError` |
| **ID3v2**      | All fields supported                                        |
| **Vorbis**     | All fields supported                                        |

### Example: Handling Unsupported Metadata

```python
from audiometa import update_file_metadata
from audiometa.exceptions import MetadataNotSupportedError

# This will work - all fields are supported in MP3 files
try:
    update_file_metadata("song.mp3", {"title": "Song", "rating": 85, "bpm": 120})
    print("Metadata updated successfully")
except MetadataNotSupportedError as e:
    print(f"Some metadata fields not supported: {e}")

# This will raise an exception - some fields not supported in WAV files
try:
    update_file_metadata("song.wav", {"title": "Song", "rating": 85, "bpm": 120})
except MetadataNotSupportedError as e:
    print(f"Some metadata fields not supported in WAV files: {e}")
```

### Best Practices

1. **Check format support** before updating metadata
2. **Handle exceptions** gracefully in your application
3. **Use format-specific managers** for advanced control
4. **Filter unsupported fields** before bulk updates

```python
# Example: Safe metadata update
def safe_update_metadata(file_path, metadata):
    """Update metadata with proper error handling."""
    try:
        update_file_metadata(file_path, metadata)
        return True
    except MetadataNotSupportedError as e:
        print(f"Some metadata fields not supported: {e}")
        return False
    except Exception as e:
        print(f"Error updating metadata: {e}")
        return False
```

## None Field Handling

When updating metadata fields with `None` values, the library **removes the field entirely** from the file's metadata rather than setting it to a null value. This behavior is consistent across all supported formats and ensures clean, efficient metadata storage.

### Behavior by Format

| Format            | None Handling Behavior                                             |
| ----------------- | ------------------------------------------------------------------ |
| **ID3v2 (MP3)**   | Deletes all existing frames for the field, does not add new frames |
| **Vorbis (FLAC)** | Deletes the field from the metadata dictionary if it exists        |
| **RIFF (WAV)**    | Skips writing the field entirely (effectively removes it)          |

### Example

```python
from audiometa import update_file_metadata, get_specific_metadata

# Set a field to None - this will REMOVE the field from the file
update_file_metadata("song.mp3", {"title": None})

# Reading the field back will return None (because it no longer exists)
title = get_specific_metadata("song.mp3", "title")
print(title)  # Output: None

# The field is completely absent from the file's metadata structure
# This is different from setting it to an empty string:
update_file_metadata("song.mp3", {"title": ""})
title = get_specific_metadata("song.mp3", "title")
print(title)  # Output: "" (empty string, field still exists)
```

### Why This Design?

- **Clean Metadata**: Prevents accumulation of empty/null fields over time
- **Efficient Storage**: Reduces file size by not storing unnecessary metadata
- **Clear Semantics**: `None` means "not set" rather than "set to null"
- **Format Consistency**: Works the same way across all supported audio formats

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
