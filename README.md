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

The library supports a comprehensive set of metadata fields:

### Basic Information

- `title` - Song title
- `artists_names` - List of artist names
- `album_name` - Album name
- `album_artists_names` - List of album artist names
- `genre_name` - Genre name
- `rating` - Rating (0-100 or 0-255 depending on format)

### Technical Information

- `release_date` - Release date
- `track_number` - Track number
- `bpm` - Beats per minute
- `language` - Language code

### Additional Metadata

- `composer` - Composer name
- `publisher` - Publisher name
- `copyright` - Copyright information
- `lyrics` - Song lyrics
- `comment` - Comments
- `encoder` - Encoder information
- `url` - URL
- `isrc` - ISRC code
- `mood` - Mood
- `key` - Musical key
- `original_date` - Original release date
- `remixer` - Remixer name
- `conductor` - Conductor name
- `cover_art` - Cover art (bytes)
- `compilation` - Compilation flag
- `media_type` - Media type
- `file_owner` - File owner
- `recording_date` - Recording date
- `file_size` - File size
- `encoder_settings` - Encoder settings
- `replaygain` - ReplayGain information
- `musicbrainz_id` - MusicBrainz ID
- `arranger` - Arranger name
- `version` - Version information
- `performance` - Performance information
- `archival_location` - Archival location
- `keywords` - Keywords
- `subject` - Subject
- `original_artist` - Original artist
- `set_subtitle` - Set subtitle
- `initial_key` - Initial key
- `involved_people` - Involved people
- `musicians` - Musicians
- `part_of_set` - Part of set

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
