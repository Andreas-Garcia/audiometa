# AudioMeta Python

A comprehensive Python library for reading and writing audio metadata across multiple formats including MP3, FLAC and WAV.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Supported Formats](#supported-formats)
- [Core API Reference](#core-api-reference)
  - [Reading Metadata](#reading-metadata)
  - [Writing Metadata](#writing-metadata)
  - [Deleting Metadata](#deleting-metadata)
  - [AudioFile Class](#audiofile-class)
- [Advanced Features](#advanced-features)
  - [Format-Specific Operations](#format-specific-operations)
  - [Writing Strategies](#writing-strategies)
  - [Multiple Artists Handling](#multiple-artists-and-album-artists-handling)
  - [Error Handling](#error-handling)
- [Metadata Field Reference](#metadata-field-reference)
- [Requirements](#requirements)
- [Development](#development)
- [License](#license)
- [Contributing](#contributing)
- [Changelog](#changelog)

## Features

- **Multi-format Support**: ID3v1, ID3v2, Vorbis (FLAC), and RIFF (WAV) metadata formats
- **Comprehensive Metadata Fields**: Support for 50+ metadata fields including title, artist, album, rating, BPM, and more
- **Read/Write Operations**: Full read and write support for most formats
- **Rating Support**: Normalized rating handling across different formats
- **Technical Information**: Access to bitrate, duration, sample rate, channels, and more
- **Complete File Analysis**: Get full metadata including headers and technical details even when no metadata is present
- **Error Handling**: Robust error handling with specific exception types
- **Type Hints**: Full type annotation support for better IDE integration
- **Cross-platform**: Works on Windows, macOS, and Linux (requires ffprobe and flac tools for full functionality)
- **Performance Optimized**: Efficient batch operations and memory management
- **Extensive Testing**: Comprehensive test coverage with 500+ tests

**Note**: OGG file support is planned but not yet implemented.

## Supported Formats

| Format | Read | Write | Rating Support | File Types     | Notes                                                      |
| ------ | ---- | ----- | -------------- | -------------- | ---------------------------------------------------------- |
| ID3v1  | ✅   | ❌    | ❌             | MP3, FLAC, WAV | Read-only, limited to 30 chars per field                   |
| ID3v2  | ✅   | ✅    | ✅             | MP3, WAV, FLAC | Full feature support, most versatile                       |
| Vorbis | ✅   | ✅    | ✅             | FLAC           | Native format for FLAC files                               |
| RIFF   | ✅   | ✅    | ✅\*           | WAV            | Native format for WAV files, \*via non-standard IRTD chunk |

### Format Capabilities

**ID3v1 (Read-only)**

- **Primary Support**: MP3 files (native format)
- **Extended Support**: FLAC and WAV files with ID3v1 tags
- **Limitations**: 30-character field limits, no album artist support
- **Operations**: Read-only (writing not supported due to fixed 128-byte structure)

**ID3v2 (Full Support)**

- **Supported Formats**: MP3, WAV, FLAC
- **Features**: All metadata fields, multiple artists, cover art, extended metadata
- **Versions**: Supports ID3v2.3 (default) and ID3v2.4
- **Note**: Most versatile format, works across multiple file types

**Vorbis (FLAC Native)**

- **Primary Support**: FLAC files (native Vorbis comments)
- **Features**: All metadata fields, multiple artists, cover art
- **Note**: Standard metadata format for FLAC files

**RIFF (WAV Native)**

- **Strict Support**: WAV files only
- **Features**: Most metadata fields, some limitations
- **Limitations**: Some fields not supported (BPM, lyrics, etc.)
- **Note**: Native metadata format for WAV files

## Installation

```bash
pip install audiometa-python
```

### System Requirements

- **Python**: 3.8 or higher
- **Operating Systems**: Windows, macOS, Linux
- **Dependencies**: Automatically installed with the package
- **Required Tools**: ffprobe (for WAV file processing), flac (for FLAC MD5 validation)

### Installing Required Tools

The library requires two external tools for full functionality:

#### ffprobe (for WAV file processing)

**macOS:**

```bash
# Using Homebrew
brew install ffmpeg

# Using MacPorts
sudo port install ffmpeg
```

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install ffmpeg
```

**CentOS/RHEL/Fedora:**

```bash
# CentOS/RHEL
sudo yum install ffmpeg

# Fedora
sudo dnf install ffmpeg
```

**Windows:**

- Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Add to your system PATH

#### flac (for FLAC MD5 validation)

**macOS:**

```bash
# Using Homebrew
brew install flac

# Using MacPorts
sudo port install flac
```

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install flac
```

**CentOS/RHEL/Fedora:**

```bash
# CentOS/RHEL
sudo yum install flac

# Fedora
sudo dnf install flac
```

**Windows:**

- Download from [https://xiph.org/flac/download.html](https://xiph.org/flac/download.html)
- Add to your system PATH

#### Verifying Installation

After installation, verify the tools are available:

```bash
ffprobe -version
flac --version
```

## Getting Started

### What You Need

- Python 3.8+
- Audio files (MP3, FLAC, WAV)
- Basic Python knowledge

### Your First Steps

1. **Install the library** using pip
2. **Try reading metadata** from an existing audio file
3. **Update some metadata** to see how writing works
4. **Explore advanced features** like format-specific operations

### Common Use Cases

- **Music library management**: Organize and clean up metadata
- **Metadata cleanup**: Remove unwanted or duplicate information
- **Format conversion**: Migrate metadata between formats
- **Batch processing**: Update multiple files at once
- **Privacy protection**: Remove personal information from files

## Quick Start

### Reading Metadata

```python
from audiometa import get_merged_unified_metadata

# Read all metadata from a file
metadata = get_merged_unified_metadata("path/to/your/audio.mp3")
print(f"Title: {metadata.get('title', 'Unknown')}")
print(f"Artist: {metadata.get('artists_names', ['Unknown'])}")
print(f"Album: {metadata.get('album_name', 'Unknown')}")
```

### Writing Metadata

```python
from audiometa import update_file_metadata

# Update metadata
new_metadata = {
    'title': 'New Song Title',
    'artists_names': ['Artist Name'],
    'album_name': 'Album Name',
    'rating': 85
}
update_file_metadata("path/to/your/audio.mp3", new_metadata)
```

### Deleting Metadata

There are two ways to remove metadata from audio files:

#### 1. Delete All Metadata (Complete Removal)

```python
from audiometa import delete_all_metadata

# Delete ALL metadata from ALL supported formats (removes metadata headers entirely)
success = delete_all_metadata("path/to/your/audio.mp3")
print(f"All metadata deleted: {success}")

# Delete metadata from specific format only
from audiometa.utils.MetadataFormat import MetadataFormat
success = delete_all_metadata("song.wav", tag_format=MetadataFormat.ID3V2)
# This removes only ID3v2 tags, keeps RIFF metadata
```

**Important**: This function removes the metadata headers/containers entirely from the file, not just the content. This means:

- ID3v2 tag structure is completely removed
- Vorbis comment blocks are completely removed
- RIFF INFO chunks are completely removed
- File size is significantly reduced

#### 2. Remove Specific Fields (Selective Removal)

```python
from audiometa import update_file_metadata, UnifiedMetadataKey

# Remove only specific fields by setting them to None
update_file_metadata("path/to/your/audio.mp3", {
    UnifiedMetadataKey.TITLE: None,        # Remove title field
    UnifiedMetadataKey.ARTISTS_NAMES: None # Remove artist field
    # Other fields remain unchanged
})

# This removes only the specified fields while keeping:
# - Other metadata fields intact
# - Metadata headers/containers in place
# - File size mostly unchanged
```

**When to use each approach:**

- **`delete_all_metadata()`**: When you want to completely strip all metadata from a file
- **Setting fields to `None`**: When you want to clean up specific fields while preserving others

#### Comparison Table

| Aspect               | `delete_all_metadata()`   | Setting fields to `None`      |
| -------------------- | ------------------------- | ----------------------------- |
| **Scope**            | Removes ALL metadata      | Removes only specified fields |
| **Metadata headers** | **Completely removed**    | **Preserved**                 |
| **File size**        | Significantly reduced     | Minimal change                |
| **Other fields**     | All removed               | Unchanged                     |
| **Use case**         | Complete cleanup          | Selective cleanup             |
| **Performance**      | Faster (single operation) | Slower (field-by-field)       |

#### Example Scenarios

**Scenario 1: Complete Privacy Cleanup**

```python
# Remove ALL metadata for privacy
delete_all_metadata("personal_recording.mp3")
# Result: File has no metadata headers at all (ID3v2 tags completely removed)
```

**Scenario 2: Clean Up Specific Information**

```python
# Remove only personal info, keep technical metadata
update_file_metadata("song.mp3", {
    UnifiedMetadataKey.TITLE: None,           # Remove title
    UnifiedMetadataKey.ARTISTS_NAMES: None,   # Remove artist
    # Keep album, genre, year, etc.
})
# Result: File keeps metadata headers but removes specific fields
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
```

## Core API Reference

### Reading Metadata

#### `get_merged_unified_metadata(file_path)`

Reads all metadata from a file and returns a unified dictionary.

```python
from audiometa import get_merged_unified_metadata

metadata = get_merged_unified_metadata("song.mp3")
print(metadata['title'])  # Song title
print(metadata['artists_names'])  # List of artists
```

#### `get_single_format_app_metadata(file_path, format)`

Reads metadata from a specific format only.

```python
from audiometa import get_single_format_app_metadata, MetadataFormat

# Read only ID3v2 metadata
id3v2_metadata = get_single_format_app_metadata("song.mp3", MetadataFormat.ID3V2)

# Read only Vorbis metadata
vorbis_metadata = get_single_format_app_metadata("song.flac", MetadataFormat.VORBIS)
```

#### `get_specific_metadata(file_path, field)`

Reads a specific metadata field.

```python
from audiometa import get_specific_metadata, UnifiedMetadataKey

title = get_specific_metadata("song.mp3", UnifiedMetadataKey.TITLE)
rating = get_specific_metadata("song.mp3", UnifiedMetadataKey.RATING)
```

#### `get_full_metadata(file_path, include_headers=True, include_technical=True)`

Gets comprehensive metadata including all available information from a file, including headers and technical details even when no metadata is present.

This function provides the most complete view of an audio file by combining:

- All metadata from all supported formats (ID3v1, ID3v2, Vorbis, RIFF)
- Technical information (duration, bitrate, sample rate, channels, file size)
- Format-specific headers and structure information
- Raw metadata details from each format

```python
from audiometa import get_full_metadata

# Get complete metadata including headers and technical info
full_metadata = get_full_metadata("song.mp3")

# Access unified metadata (same as get_merged_unified_metadata)
print(f"Title: {full_metadata['unified_metadata']['title']}")
print(f"Artists: {full_metadata['unified_metadata']['artists_names']}")

# Access technical information
print(f"Duration: {full_metadata['technical_info']['duration_seconds']} seconds")
print(f"Bitrate: {full_metadata['technical_info']['bitrate_kbps']} kbps")
print(f"Sample Rate: {full_metadata['technical_info']['sample_rate_hz']} Hz")
print(f"Channels: {full_metadata['technical_info']['channels']}")
print(f"File Size: {full_metadata['technical_info']['file_size_bytes']} bytes")

# Access format-specific metadata
print(f"ID3v2 Title: {full_metadata['format_metadata']['id3v2']['title']}")
print(f"Vorbis Title: {full_metadata['format_metadata']['vorbis']['title']}")

# Access header information
print(f"ID3v2 Version: {full_metadata['headers']['id3v2']['version']}")
print(f"ID3v2 Header Size: {full_metadata['headers']['id3v2']['header_size_bytes']}")
print(f"Has ID3v1 Header: {full_metadata['headers']['id3v1']['present']}")
print(f"RIFF Chunk Info: {full_metadata['headers']['riff']['chunk_info']}")

# Access raw metadata details
print(f"Raw ID3v2 Frames: {full_metadata['raw_metadata']['id3v2']['frames']}")
print(f"Raw Vorbis Comments: {full_metadata['raw_metadata']['vorbis']['comments']}")
```

**Parameters:**

- `file_path`: Path to the audio file or AudioFile object
- `include_headers`: Whether to include format-specific header information (default: True)
- `include_technical`: Whether to include technical audio information (default: True)

**Returns:**
A comprehensive dictionary containing:

```python
{
    'unified_metadata': {
        # Same as get_merged_unified_metadata() result
        'title': 'Song Title',
        'artists_names': ['Artist 1', 'Artist 2'],
        'album_name': 'Album Name',
        # ... all other metadata fields
    },
    'technical_info': {
        'duration_seconds': 180.5,
        'bitrate_kbps': 320,
        'sample_rate_hz': 44100,
        'channels': 2,
        'file_size_bytes': 7234567,
        'file_extension': '.mp3',
        'format_name': 'MP3',
        'is_flac_md5_valid': None,  # Only for FLAC files
    },
    'format_metadata': {
        'id3v1': {
            # ID3v1 specific metadata (if present)
            'title': 'Song Title',
            'artist': 'Artist Name',
            # ... other ID3v1 fields
        },
        'id3v2': {
            # ID3v2 specific metadata (if present)
            'title': 'Song Title',
            'artists_names': ['Artist 1', 'Artist 2'],
            # ... other ID3v2 fields
        },
        'vorbis': {
            # Vorbis specific metadata (if present)
            'title': 'Song Title',
            'artists_names': ['Artist 1', 'Artist 2'],
            # ... other Vorbis fields
        },
        'riff': {
            # RIFF specific metadata (if present)
            'title': 'Song Title',
            'artist': 'Artist Name',
            # ... other RIFF fields
        }
    },
    'headers': {
        'id3v1': {
            'present': True,
            'position': 'end_of_file',
            'size_bytes': 128,
            'version': '1.1',
            'has_track_number': True
        },
        'id3v2': {
            'present': True,
            'version': '2.3.0',
            'header_size_bytes': 2048,
            'flags': {...},
            'extended_header': {...}
        },
        'vorbis': {
            'present': True,
            'vendor_string': 'reference libFLAC 1.3.2',
            'comment_count': 15,
            'block_size': 4096
        },
        'riff': {
            'present': True,
            'chunk_info': {
                'riff_chunk_size': 7234000,
                'info_chunk_size': 1024,
                'audio_format': 'PCM',
                'subchunk_size': 7232000
            }
        }
    },
    'raw_metadata': {
        'id3v1': {
            'raw_data': b'...',  # Raw 128-byte ID3v1 tag
            'parsed_fields': {...}
        },
        'id3v2': {
            'frames': {...},  # Raw ID3v2 frames
            'raw_header': b'...'
        },
        'vorbis': {
            'comments': {...},  # Raw Vorbis comment blocks
            'vendor_string': '...'
        },
        'riff': {
            'info_chunk': {...},  # Raw RIFF INFO chunk data
            'chunk_structure': {...}
        }
    },
    'format_priorities': {
        'file_extension': '.mp3',
        'reading_order': ['id3v2', 'id3v1'],
        'writing_format': 'id3v2'
    }
}
```

**Use Cases:**

- **Complete file analysis**: Get everything about an audio file in one call
- **Debugging metadata issues**: Inspect raw headers and format-specific data
- **Format migration**: Understand what metadata exists in each format before converting
- **File validation**: Check header integrity and format compliance
- **Metadata forensics**: Analyze metadata structure and detect anomalies
- **Batch processing**: Get comprehensive information for multiple files efficiently

**Examples:**

```python
# Basic usage - get everything
full_info = get_full_metadata("song.mp3")

# Get only metadata without technical details
metadata_only = get_full_metadata("song.mp3", include_technical=False)

# Get only technical info without headers
tech_only = get_full_metadata("song.mp3", include_headers=False)

# Check if file has specific format headers
if full_info['headers']['id3v2']['present']:
    print("File has ID3v2 tags")
    print(f"ID3v2 version: {full_info['headers']['id3v2']['version']}")

# Compare metadata across formats
id3v2_title = full_info['format_metadata']['id3v2'].get('title')
vorbis_title = full_info['format_metadata']['vorbis'].get('title')
if id3v2_title != vorbis_title:
    print("Title differs between ID3v2 and Vorbis")

# Analyze file structure
print(f"File size: {full_info['technical_info']['file_size_bytes']} bytes")
print(f"Metadata overhead: {full_info['headers']['id3v2']['header_size_bytes']} bytes")
print(f"Audio data ratio: {(full_info['technical_info']['file_size_bytes'] - full_info['headers']['id3v2']['header_size_bytes']) / full_info['technical_info']['file_size_bytes'] * 100:.1f}%")
```

**Performance Notes:**

- This function is more comprehensive but slightly slower than individual metadata functions
- All metadata is read in a single pass for efficiency
- Technical information is cached to avoid repeated file system calls
- Use `include_headers=False` or `include_technical=False` to improve performance if you don't need all information

### Writing Metadata

#### `update_file_metadata(file_path, metadata, **options)`

Updates metadata in a file.

```python
from audiometa import update_file_metadata

# Basic writing
update_file_metadata("song.mp3", {
    'title': 'New Title',
    'artists_names': ['Artist Name'],
    'rating': 85
})

# Format-specific writing
from audiometa.utils.MetadataFormat import MetadataFormat
update_file_metadata("song.wav", metadata, metadata_format=MetadataFormat.RIFF)

# Strategy-based writing
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy
update_file_metadata("song.mp3", metadata, metadata_strategy=MetadataWritingStrategy.CLEANUP)
```

### Deleting Metadata

#### `delete_all_metadata(file_path, tag_format=None)`

Deletes all metadata or metadata from a specific format.

```python
from audiometa import delete_all_metadata, MetadataFormat

# Delete all metadata
delete_all_metadata("song.mp3")

# Delete only ID3v2 metadata
delete_all_metadata("song.mp3", tag_format=MetadataFormat.ID3V2)

# Delete only Vorbis metadata
delete_all_metadata("song.flac", tag_format=MetadataFormat.VORBIS)
```

**Complete Deletion Behavior:**

- **No `tag_format` specified**: Deletes metadata from ALL supported formats for the file type
- **`tag_format` specified**: Deletes only metadata from that specific format
- **Removes headers entirely**: This is a destructive operation that removes metadata container structures
- **Significantly reduces file size**: Removes all metadata overhead
- **Returns**: `True` if at least one format was successfully deleted, `False` if all deletions fail
- **ID3v1**: Cannot be deleted (read-only format) - skipped silently when deleting all formats

**When to Use `delete_all_metadata` vs Setting to `None`:**

- **Use `delete_all_metadata`**: When you want to remove ALL metadata or ALL metadata of a specific format completely
- **Use `None` values**: When you want to remove only specific fields while keeping others

```python
# Remove everything completely - use delete_all_metadata
# This removes metadata from ALL supported formats (ID3v2, ID3v1, etc.)
delete_all_metadata("song.mp3")

# Remove only specific format - use delete_all_metadata with tag_format
delete_all_metadata("song.wav", tag_format=MetadataFormat.ID3V2)  # Only removes ID3v2, keeps RIFF

# Remove only title and artist - use None values
update_file_metadata("song.mp3", {"title": None, "artists_names": None})
```

### AudioFile Class

#### Object-oriented approach for working with audio files

```python
from audiometa import AudioFile

# Create an AudioFile instance
audio_file = AudioFile("path/to/your/audio.flac")

# Get technical information
print(f"Duration: {audio_file.get_duration_in_sec()} seconds")
print(f"Bitrate: {audio_file.get_bitrate()} kbps")
print(f"Sample Rate: {audio_file.get_sample_rate()} Hz")
print(f"Channels: {audio_file.get_channels()}")
print(f"File extension: {audio_file.file_extension}")

# Check FLAC MD5 validity
if audio_file.file_extension == '.flac':
    is_valid = audio_file.is_flac_file_md5_valid()
    print(f"FLAC MD5 valid: {is_valid}")

# Get metadata using the object
metadata = audio_file.get_merged_unified_metadata()
print(f"Title: {metadata.get('title', 'Unknown')}")
```

## Advanced Features

### Format-Specific Operations

#### Reading from Specific Formats

```python
from audiometa import get_single_format_app_metadata, MetadataFormat

# Read only ID3v2 metadata
id3v2_metadata = get_single_format_app_metadata("song.mp3", MetadataFormat.ID3V2)

# Read only Vorbis metadata
vorbis_metadata = get_single_format_app_metadata("song.flac", MetadataFormat.VORBIS)

# Read only RIFF metadata
riff_metadata = get_single_format_app_metadata("song.wav", MetadataFormat.RIFF)
```

#### Writing to Specific Formats

```python
from audiometa import update_file_metadata
from audiometa.utils.MetadataFormat import MetadataFormat

# Write specifically to ID3v2 format (even for WAV files)
update_file_metadata("song.wav", {"title": "New Title"}, metadata_format=MetadataFormat.ID3V2)

# Write specifically to RIFF format
update_file_metadata("song.wav", {"title": "New Title"}, metadata_format=MetadataFormat.RIFF)
```

### Writing Strategies

The library provides flexible control over how metadata is written to files that may already contain metadata in other formats.

#### Available Strategies

1. **`SYNC` (Default)**: Write to native format and synchronize other metadata formats that are already present
2. **`PRESERVE`**: Write to native format only, preserve existing metadata in other formats
3. **`CLEANUP`**: Write to native format and remove all non-native metadata formats

#### Usage Examples

```python
from audiometa import update_file_metadata
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy

# SYNC strategy (default) - synchronize all existing formats
update_file_metadata("song.wav", {"title": "New Title"},
                    metadata_strategy=MetadataWritingStrategy.SYNC)

# CLEANUP strategy - remove non-native formats
update_file_metadata("song.wav", {"title": "New Title"},
                    metadata_strategy=MetadataWritingStrategy.CLEANUP)

# PRESERVE strategy - keep other formats unchanged
update_file_metadata("song.wav", {"title": "New Title"},
                    metadata_strategy=MetadataWritingStrategy.PRESERVE)
```

### Multiple Artists and Album Artists Handling

The library supports multiple artists and album artists across all audio formats.

```python
from audiometa import update_file_metadata, get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey

# Set multiple artists and album artists
artists = ["Artist One", "Artist Two", "Artist Three"]
album_artists = ["Album Artist One", "Album Artist Two"]
metadata = {
    UnifiedMetadataKey.ARTISTS_NAMES: artists,
    UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: album_artists
}

# Update file (library handles format-specific implementation)
update_file_metadata("song.mp3", metadata)

# Read back (returns lists of artists and album artists)
result = get_merged_unified_metadata("song.mp3")
print(result[UnifiedMetadataKey.ARTISTS_NAMES])
# Output: ['Artist One', 'Artist Two', 'Artist Three']
```

### Error Handling

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

## Metadata Field Reference

The library supports a comprehensive set of metadata fields across different audio formats. The table below shows which fields are supported by each format:

### Metadata Support by Format

| Field             | ID3v1          | ID3v2          | Vorbis       | RIFF          | AudioMeta Support    |
| ----------------- | -------------- | -------------- | ------------ | ------------- | -------------------- |
| Text Encoding     | ASCII          | UTF-8/16/ISO   | UTF-8        | ASCII/UTF-8   | UTF-8                |
| Max Text Length   | 30 chars       | ~8M chars      | ~8M chars    | ~1M chars     | Format limit         |
| Rating Range      | Not supported  | 0-255#         | 0-100#       | 0-100#\*      | 0-10#                |
| Track Number      | 0-255#         | 0-255#         | Unlimited#   | Unlimited#    | Format limit         |
| Disc Number       | Not supported  | 0-255#         | Unlimited#   | Not supported | Format limit         |
| Operations        | R              | R/W            | R/W          | R/W           | ✓                    |
| Multiple Values   | ❌             | ✅ (v2.4)      | ✅           | ❌            | ✅ mp3, flac, ❌ wav |
| per Tag           |                |                |              |               |                      |
| supported         | (W using v2.4) | (W using v2.4) |              |               |                      |
| Technical Info    |                |                |              |               |                      |
| - Duration        | ✓              | ✓              | ✓            | ✓             | ✓                    |
| - Bitrate         | ✓              | ✓              | ✓            | ✓             | ✓                    |
| - Sample Rate     | ✓              | ✓              | ✓            | ✓             | ✓                    |
| - Channels        | ✓ (1-2)        | ✓ (1-255)      | ✓ (1-255)    | ✓ (1-2)       | ✓                    |
| - File Size       | ✓              | ✓              | ✓            | ✓             | ✓                    |
| - Format Info     | ✓              | ✓              | ✓            | ✓             | ✓                    |
| - MD5 Checksum    |                |                | ✓            |               | ✓ (Flac)             |
| Title             | ✓ (30)         | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Artist            | ✓ (30)         | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Album             | ✓ (30)         | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Album Artist      |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| Genre             | ✓ (1#)         | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Release Date      | ✓ (4)          | ✓ (10)         | ✓ (10)       | ✓ (10)        | ✓                    |
| Track Number      | ✓ (1#)         | ✓ (0-255#)     | ✓ (Unlim#)   | ✓ (Unlim#)    | ✓                    |
| Rating            |                | ✓ (0-255#)     | ✓ (0-100#)   | ✓ (0-100#\*)  | ✓                    |
| BPM               |                | ✓ (0-65535#)   | ✓ (0-65535#) |               | ✓                    |
| Language          |                | ✓ (3)          | ✓ (3)        |               | ✓                    |
| Composer          |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Publisher         |                | ✓ (Format)     | ✓ (Format)   |               | ✓                    |
| Copyright         |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Lyrics            |                | ✓ (Format)     | ✓ (Format)   |               | ✓                    |
| Comment           | ✓ (28)         | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Encoder           |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| URL               |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| ISRC              |                | ✓ (12)         | ✓ (12)       |               |                      |
| Mood              |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| Key               |                | ✓ (3)          | ✓ (3)        |               |                      |
| Original Date     |                | ✓ (10)         | ✓ (10)       |               |                      |
| Remixer           |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| Conductor         |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Cover Art         |                | ✓ (10MB#)      | ✓ (10MB#)    |               |                      |
| Compilation       |                | ✓ (1#)         | ✓ (1#)       |               |                      |
| Media Type        |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| File Owner        |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| Recording Date    |                | ✓ (10)         | ✓ (10)       |               |                      |
| File Size         |                | ✓ (16#)        |              |               |                      |
| Encoder Settings  |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| ReplayGain        |                | ✓ (8#)         | ✓ (8#)       |               |                      |
| MusicBrainz ID    |                | ✓ (36)         | ✓ (36)       |               |                      |
| Arranger          |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| Version           |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| Performance       |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| Archival Location |                |                |              | ✓ (Format)    |                      |
| Keywords          |                |                |              | ✓ (Format)    |                      |
| Subject           |                |                |              | ✓ (Format)    |                      |
| Original Artist   |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| Set Subtitle      |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| Initial Key       |                | ✓ (3)          | ✓ (3)        |               |                      |
| Involved People   |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| Musicians         |                | ✓ (Format)     | ✓ (Format)   |               |                      |
| Part of Set       |                | ✓ (Format)     | ✓ (Format)   |               |                      |

### Legend

- ✓: Supported
- (30): Fixed 30-character field (ID3v1 limitation)
- (#): Numeric value or code
- (Format): Limited by the audio format's native capabilities
- (10MB#): Maximum 10 megabytes binary data
- (~8M): Approximately 8 million characters (format limit)
- (~1M): Approximately 1 million characters (format limit)
- (\*): Non-standard implementation (IRTD chunk for RIFF rating)

**AudioMeta Support Column**: Shows the library's unified interface capabilities. The library does not impose artificial limits - it respects each format's native capabilities. Text fields can be as long as the format allows, and numeric ranges follow the format's specifications. The library provides consistent UTF-8 encoding and normalized rating handling (0-10 scale) across all supported formats.

### Reading Priorities (Tag Precedence)

When the same metadata tag exists in multiple formats within the same file, the library follows file-specific precedence orders for reading:

#### FLAC Files

1. **Vorbis** (highest precedence)
2. **ID3v2**
3. **ID3v1** (lowest precedence, read-only)

#### MP3 Files

1. **ID3v2** (highest precedence)
2. **ID3v1** (lowest precedence, read-only)

#### WAV Files

1. **RIFF** (highest precedence)
2. **ID3v2**
3. **ID3v1** (lowest precedence, read-only)

**Examples**:

- For MP3 files: If a title exists in both ID3v1 and ID3v2, the ID3v2 title will be returned.
- For WAV files: If a title exists in both RIFF and ID3v2, the RIFF title will be returned.
- For FLAC files: If a title exists in both Vorbis and ID3v2, the Vorbis title will be returned.

### Writing Defaults by Audio Format

When writing metadata, the library uses these default metadata formats per audio file type:

#### MP3 Files

**Default Writing Format**: ID3v2 (v2.3)

- **Note**: ID3v1 cannot be written to
- **Version Selection**: You can choose between ID3v2.3 (maximum compatibility) and ID3v2.4 (modern features) using the `id3v2_version` parameter

**ID3v2 Version Selection**

The library supports both ID3v2.3 and ID3v2.4 formats for MP3 files. You can choose the version based on your compatibility needs:

**ID3v2.3 (Default - Maximum Compatibility)**

- **Best for**: Maximum compatibility with older players and devices
- **Supported by**: Windows Media Player, older car systems, most DJ software
- **Features**: UTF-16 encoding, basic unsynchronization

**ID3v2.4 (Modern Features)**

- **Best for**: Modern players and applications that support it
- **Supported by**: Modern browsers, recent media players, newer mobile devices
- **Features**: UTF-8 encoding, per-frame unsynchronization, extended metadata

**Usage Examples**

```python
from audiometa import update_file_metadata, get_merged_unified_metadata

# Use default ID3v2.3 (maximum compatibility)
update_file_metadata("song.mp3", {"title": "My Song"})

# Explicitly use ID3v2.3
update_file_metadata("song.mp3", {"title": "My Song"}, id3v2_version=(2, 3, 0))

# Use ID3v2.4 for modern features
update_file_metadata("song.mp3", {"title": "My Song"}, id3v2_version=(2, 4, 0))

# Reading also supports version selection
metadata = get_merged_unified_metadata("song.mp3", id3v2_version=(2, 4, 0))
```

#### FLAC Files

**Default Writing Format**: Vorbis Comments

- **Note**: Vorbis is the native format for FLAC files

#### WAV Files

**Default Writing Format**: RIFF

- **Note**: RIFF is the native format for WAV files

**Note**: ID3v1 is read-only and cannot be written programmatically. The library will read from existing ID3v1 tags but will not attempt to write to them.

### Metadata Writing Strategy

The library provides flexible control over how metadata is written to files that may already contain metadata in other formats. You can choose the strategy that best fits your needs.

#### Default Behavior

By default, the library uses the **SYNC strategy** which writes metadata to the native format and synchronizes other metadata formats that are already present. This provides the best user experience by writing metadata where possible and handling unsupported fields gracefully.

- **MP3 files**: Writes to ID3v2 and syncs other formats
- **FLAC files**: Writes to Vorbis comments and syncs other formats
- **WAV files**: Writes to RIFF and syncs other formats

#### Metadata Strategy Options

You can control metadata writing behavior using the `metadata_strategy` parameter:

**Available Strategies:**

1. **`SYNC` (Default)**: Write to native format and synchronize other metadata formats that are already present. Handles unsupported fields gracefully with warnings.
2. **`PRESERVE`**: Write to native format only, preserve existing metadata in other formats
3. **`CLEANUP`**: Write to native format and remove all non-native metadata formats

#### Forced Format Behavior

When you specify a `metadata_format` parameter, you **cannot** also specify a `metadata_strategy`:

- **Write only to the specified format**: Other formats are left completely untouched
- **Fail fast on unsupported fields**: Raises `MetadataNotSupportedError` for any unsupported metadata
- **Predictable behavior**: No side effects on other metadata formats

```python
# Correct usage - specify only the format
update_file_metadata("song.mp3", metadata,
                    metadata_format=MetadataFormat.RIFF)  # Writes only to RIFF, ignores ID3v2

# This will raise MetadataWritingConflictParametersError - cannot specify both parameters
update_file_metadata("song.mp3", metadata,
                    metadata_format=MetadataFormat.RIFF,
                    metadata_strategy=MetadataWritingStrategy.CLEANUP)  # Raises MetadataWritingConflictParametersError
```

#### ID3v1 Exceptions

**ID3v1 metadata cannot be modified or deleted** due to its read-only nature:

- **Read-only format**: ID3v1 is treated as read-only due to its fixed 128-byte structure
- **Strategy limitations**: All strategies (PRESERVE, CLEANUP, SYNC) cannot preserve ID3v1 metadata
- **Error handling**: Attempting to modify ID3v1 metadata will raise `MetadataNotSupportedError`
- **Overwrite behavior**: When ID3v2 metadata is written, it overwrites the ID3v1 tag

**Important**: ID3v1 metadata cannot be preserved when writing ID3v2 metadata because:

1. ID3v1 is read-only and cannot be written back
2. Writing ID3v2 metadata overwrites the ID3v1 tag at the end of the file
3. The PRESERVE strategy cannot restore ID3v1 metadata after writing ID3v2

This means that if a file contains both ID3v1 and ID3v2 tags, writing new metadata will result in the ID3v1 tag being overwritten with the new values.

#### Usage Examples

**Default Behavior (SYNC strategy)**

```python
from audiometa import update_file_metadata

# WAV file with existing ID3v2 tags
update_file_metadata("song.wav", {"title": "New Title"})

# Result:
# - RIFF tags: Updated with new metadata (native format)
# - ID3v2 tags: Synchronized with new metadata
# - When reading: ID3v2 title is returned (higher precedence)
```

**CLEANUP Strategy - Remove Non-Native Formats**

```python
from audiometa import update_file_metadata
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy

# Clean up WAV file - remove ID3v2, keep only RIFF
update_file_metadata("song.wav", {"title": "New Title"},
                    metadata_strategy=MetadataWritingStrategy.CLEANUP)

# Result:
# - ID3v2 tags: Removed completely
# - RIFF tags: Updated with new metadata
# - When reading: Only RIFF metadata available
```

**SYNC Strategy - Synchronize All Existing Formats**

```python
# Synchronize all existing metadata formats with same values
update_file_metadata("song.wav", {"title": "New Title"},
                    metadata_strategy=MetadataWritingStrategy.SYNC)

# Result:
# - ID3v2 tags: Synchronized with new metadata
# - RIFF tags: Synchronized with new metadata
# - When reading: ID3v2 title is returned (higher precedence)
```

**Format-Specific Writing**

```python
from audiometa.utils.MetadataFormat import MetadataFormat

# Write specifically to ID3v2 format (even for WAV files)
update_file_metadata("song.wav", {"title": "New Title"},
                    metadata_format=MetadataFormat.ID3V2)

# Write specifically to RIFF format
update_file_metadata("song.wav", {"title": "New Title"},
                    metadata_format=MetadataFormat.RIFF)
```

#### Strategy Benefits

**PRESERVE (Default)**

- **Maximum Compatibility**: Older players can still read legacy formats
- **Non-Destructive**: Never loses existing metadata
- **Safe**: Default behavior that won't break existing workflows

**CLEANUP**

- **Best Practice**: Uses only native format for each file type
- **Clean Files**: Removes format confusion and reduces file size
- **Standards Compliant**: Follows established audio metadata standards

**SYNC**

- **Consistency**: Keeps all formats synchronized
- **Compatibility**: Maintains support for different players
- **Convenience**: Single update affects all existing formats

### Unsupported Metadata Handling

The library handles unsupported metadata differently depending on the context:

- **Forced format** (when `metadata_format` is specified): Always fails fast by raising `MetadataNotSupportedError` for any unsupported field
- **SYNC strategy (default)**: Handles unsupported fields gracefully by logging warnings and continuing with supported fields
- **SYNC strategy with `fail_on_unsupported_field=True`**: Fails fast if any field is not supported by NO format
- **Other strategies (PRESERVE, CLEANUP)**: Follow a "fail fast, fail clearly" approach by raising `MetadataNotSupportedError` when any field is not supported

#### Format-Specific Limitations

| Format         | Forced Format     | SYNC Strategy (Default)                                     | Other Strategies (PRESERVE, CLEANUP)                        |
| -------------- | ----------------- | ----------------------------------------------------------- | ----------------------------------------------------------- |
| **RIFF (WAV)** | Always fails fast | Logs warnings for unsupported fields, writes supported ones | Any unsupported metadata raises `MetadataNotSupportedError` |
| **ID3v1**      | Always fails fast | Logs warnings for unsupported fields, writes supported ones | Any unsupported metadata raises `MetadataNotSupportedError` |
| **ID3v2**      | Always fails fast | All fields supported                                        | All fields supported                                        |
| **Vorbis**     | Always fails fast | All fields supported                                        | All fields supported                                        |

#### Example: Handling Unsupported Metadata

```python
from audiometa import update_file_metadata
from audiometa.exceptions import MetadataNotSupportedError
from audiometa.utils.MetadataFormat import MetadataFormat

# SYNC strategy (default) - handles unsupported fields gracefully
update_file_metadata("song.wav", {"title": "Song", "rating": 85, "bpm": 120})
# Result: Writes title and rating to RIFF, logs warning about BPM, continues

# Forced format - always fails fast for unsupported fields
try:
    update_file_metadata("song.wav", {"title": "Song", "rating": 85, "bpm": 120},
                        metadata_format=MetadataFormat.RIFF)
except MetadataNotSupportedError as e:
    print(f"BPM not supported in RIFF format: {e}")
```

### None vs Empty String Handling

The library handles `None` and empty string values differently across audio formats:

| Format            | Setting to `None`        | Setting to `""` (empty string)   | Read Back Result |
| ----------------- | ------------------------ | -------------------------------- | ---------------- |
| **ID3v2 (MP3)**   | Removes field completely | Removes field completely         | `None` / `None`  |
| **Vorbis (FLAC)** | Removes field completely | Creates field with empty content | `None` / `""`    |
| **RIFF (WAV)**    | Removes field completely | Removes field completely         | `None` / `None`  |
| **ID3v1 (MP3)**   | ❌ **Not supported**     | ❌ **Not supported**             | Read-only format |

#### Example

```python
from audiometa import update_file_metadata, get_specific_metadata

# MP3 file - same behavior for None and empty string
update_file_metadata("song.mp3", {"title": None})
title = get_specific_metadata("song.mp3", "title")
print(title)  # Output: None (field removed)

# FLAC file - different behavior for None vs empty string
update_file_metadata("song.flac", {"title": None})
title = get_specific_metadata("song.flac", "title")
print(title)  # Output: None (field removed)

update_file_metadata("song.flac", {"title": ""})
title = get_specific_metadata("song.flac", "title")
print(title)  # Output: "" (field exists but empty)
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

For detailed information about the test suite, including test organization, data files, and testing strategies, see the [Test Documentation](audiometa/test/tests/README.md).

### Code Formatting

```bash
black audio_metadata/
isort audio_metadata/
```

### Commit Message Conventions

This project follows conventional commit message format. Use these prefixes:

- `feat:` - New features
- `fix:` - Bug fixes
- `fix(test):` - Fixing a bug in a test
- `test:` - General test update/fix
- `refactor:` - Code refactoring
- `chore:` - Non-functional maintenance
- `chore(test):` - Maintenance related to tests (rare)
- `docs:` - Documentation changes
- `style:` - Formatting changes
- `perf:` - Performance improvements

**Note**: As of 2025 Oct. 8th, we updated our commit message conventions for test-related changes. Previous commits may use older conventions, but going forward we use the prefixes listed above.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed list of changes.
