# AudioMeta Python

A comprehensive Python library for reading and writing audio metadata across multiple formats including MP3, FLAC and WAV.

**Author**: [Andreas Garcia](https://github.com/Andreas-Garcia)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Line Interface](#command-line-interface)
- [Supported Formats](#supported-formats)
- [Core API Reference](#core-api-reference)
  - [Reading Metadata](#reading-metadata)
  - [Writing Metadata](#writing-metadata)
  - [Deleting Metadata](#deleting-metadata)
  - [AudioFile Class](#audiofile-class)
- [Advanced Features](#advanced-features)
  - [Format-Specific Operations](#format-specific-operations)
  - [Writing Strategies](#writing-strategies)
  - [Multi-Value Fields Support](#multi-value-fields-support)
  - [Genre Handling](#genre-handling)
  - [Rating Profiles](#rating-profiles)
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
| ID3v1  | ✅   | ✅    | ✅             | MP3, FLAC, WAV | Limited to 30 chars per field, Latin-1 encoding            |
| ID3v2  | ✅   | ✅    | ✅             | MP3, WAV, FLAC | Full feature support, most versatile                       |
| Vorbis | ✅   | ✅    | ✅             | FLAC           | Native format for FLAC files                               |
| RIFF   | ✅   | ✅    | ✅\*           | WAV            | Native format for WAV files, \*via non-standard IRTD chunk |

### Format Capabilities

**ID3v1 (Legacy Format)**

- **Primary Support**: MP3 files (native format)
- **Extended Support**: FLAC and WAV files with ID3v1 tags
- **Limitations**: 30-character field limits, no album artist support
- **Operations**: Full read/write support with direct file manipulation

**ID3v2 (Full Support)**

- **Supported Formats**: MP3, WAV, FLAC
- **Features**: All metadata fields, multiple artists, cover art, extended metadata
- **Versions**: Supports ID3v2.3 (default) and ID3v2.4
- **Note**: Most versatile format, works across multiple file types

**Vorbis (FLAC Native)**

- **Primary Support**: FLAC files (native Vorbis comments)
- **Features**: Most metadata fields, multiple artists, cover art
- **Limitations**: Some fields not supported (lyrics, etc.)
- **Note**: Standard metadata format for FLAC files

**RIFF (WAV Native)**

- **Strict Support**: WAV files only
- **Features**: Most metadata fields including album artist, language, comments
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

## Command Line Interface

AudioMeta provides a powerful command-line interface for quick metadata operations without writing Python code.

### Installation

After installing the package, the `audiometa` command will be available:

```bash
pip install audiometa-python
audiometa --help
```

### Basic Usage

#### Reading Metadata

```bash
# Read full metadata from a file
audiometa read song.mp3

# Read unified metadata only (simplified output)
audiometa unified song.mp3

# Read multiple files
audiometa read *.mp3

# Process directory recursively
audiometa read music/ --recursive

# Output in different formats
audiometa read song.mp3 --format table
audiometa read song.mp3 --format yaml
audiometa read song.mp3 --output metadata.json
```

#### Writing Metadata

```bash
# Write basic metadata
audiometa write song.mp3 --title "New Title" --artist "Artist Name"

# Write multiple fields
audiometa write song.mp3 --title "Song Title" --artist "Artist" --album "Album" --year "2024" --rating 85

# Update multiple files
audiometa write *.mp3 --artist "New Artist"
```

#### Deleting Metadata

```bash
# Delete all metadata from a file
audiometa delete song.mp3

# Delete metadata from multiple files
audiometa delete *.mp3
```

### Advanced Options

#### Output Control

```bash
# Exclude technical information
audiometa read song.mp3 --no-technical

# Exclude header information
audiometa read song.mp3 --no-headers

# Save to file
audiometa read song.mp3 --output metadata.json
```

#### Error Handling

```bash
# Continue processing other files on error
audiometa read *.mp3 --continue-on-error
```

#### Batch Processing

```bash
# Process all audio files in a directory
audiometa read music/ --recursive

# Process specific file patterns
audiometa read "**/*.mp3" --recursive
```

### Output Formats

- **JSON** (default): Structured data for programmatic use
- **YAML**: Human-readable structured format (requires PyYAML)
- **Table**: Simple text table format

### Examples

```bash
# Quick metadata check
audiometa unified song.mp3 --format table

# Batch metadata update
audiometa write music/ --recursive --artist "Various Artists"

# Export metadata for analysis
audiometa read music/ --recursive --format json --output all_metadata.json

# Clean up metadata
audiometa delete music/ --recursive
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
- **ID3v1**: Can be deleted and written using direct file manipulation

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

### Multiple Values

The library intelligently handles multiple values across different metadata formats, automatically choosing the best approach for each situation.

#### Supported Multi-Value Fields

The following fields support semantic multiple values:

| Field                     | ID3v2.3 (MP3) | ID3v2.4 (MP3) | Vorbis (FLAC) | RIFF (WAV) | ID3v1 |
| ------------------------- | ------------- | ------------- | ------------- | ---------- | ----- |
| **`ARTISTS_NAMES`**       | ✅\*          | ✅            | ✅            | ✅\*       | ✅\*  |
| **`ALBUM_ARTISTS_NAMES`** | ✅\*          | ✅            | ✅            | ✅\*       | ✅\*  |
| **`GENRES_NAMES`**        | ✅\*          | ✅            | ✅            | ✅\*       | ✅\*  |
| **`COMPOSER`**            | ✅\*          | ✅            | ✅            | ✅\*       | ✅\*  |
| **`MUSICIANS`**           | ✅\*          | ✅            | ✅            | ✅\*       | ✅\*  |
| **`CONDUCTOR`**           | ✅\*          | ✅            | ✅            | ✅\*       | ✅\*  |
| **`ARRANGER`**            | ✅\*          | ✅            | ✅            | ✅\*       | ✅\*  |

**Legend:**

- ✅ = Multiple entries supported (best practice)
- ✅\* = Separator-based parsing only (legacy limitation)

**ID3v2 Version Differences:**

- **ID3v2.3**: Uses concatenation with separators (✅\*) - specification limitation
- **ID3v2.4**: Uses multiple separate frames (✅) - specification feature

#### Reading Multiple Values

The library uses **smart separator parsing** that adapts to the format and data structure:

**Logic:**

- **Modern formats (ID3v2, Vorbis) + Multiple entries**: No separator parsing (trusts separate entries)
- **Modern formats (ID3v2, Vorbis) + Single entry**: Applies separator parsing (legacy data)
- **Legacy formats (RIFF, ID3v1)**: Always applies separator parsing (only option)

```python
from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey

# Read multiple values
result = get_merged_unified_metadata("song.mp3")
print(result[UnifiedMetadataKey.ARTISTS_NAMES])
# Output: ['Artist One', 'Artist Two', 'Artist Three']

print(result[UnifiedMetadataKey.GENRES_NAMES])
# Output: ['Rock', 'Alternative', 'Indie']
```

**Separator Priority (when parsing is applied):**

1. `//` (double slash)
2. `\\` (double backslash)
3. `;` (semicolon)
4. `\` (backslash)
5. `/` (forward slash)
6. `,` (comma)

**Examples of Smart Parsing:**

```python
# Scenario 1: Vorbis (FLAC) with separate entries
# Raw data: ["Artist One", "Artist; with; semicolons", "Artist Three"]
# Result: ["Artist One", "Artist; with; semicolons", "Artist Three"]
# ✅ Separators preserved in individual entries (Vorbis supports multiple frames)

# Scenario 2: ID3v2/RIFF/ID3v1 with single entry containing separators
# Raw data: ["Artist One;Artist Two;Artist Three"]
# Result: ["Artist One", "Artist Two", "Artist Three"]
# ✅ Single entry gets parsed (these formats use single frame with separators)

# Scenario 3: Legacy format (RIFF/ID3v1) - always parses
# Raw data: ["Artist One;Artist Two"]
# Result: ["Artist One", "Artist Two"]
# ✅ Always applies separator parsing
```

#### Writing Multiple Values

**Strategy Overview:**

The library uses a **smart writing strategy** that adapts to format capabilities and data characteristics:

1. **Modern formats (ID3v2, Vorbis)**: Uses multiple separate entries (best practice)
2. **Legacy formats (RIFF, ID3v1)**: Uses smart separator-based concatenation
3. **Smart separator selection**: Chooses the best separator that won't conflict with actual values

**Basic Usage:**

```python
from audiometa import update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey

# Write multiple values - library automatically uses best approach
metadata = {
    UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Artist Three"],
    UnifiedMetadataKey.COMPOSER: ["Composer A", "Composer B"],
    UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Alternative", "Indie"]
}

# For FLAC: Creates separate entries (Vorbis supports multiple frames)
# For MP3/WAV/ID3v1: Uses smart separator-based (single frame with separators)
update_file_metadata("song.mp3", metadata)
```

**Format-Specific Writing:**

```python
from audiometa.utils.MetadataFormat import MetadataFormat

# Force specific format for optimal results
update_file_metadata("song.mp3", metadata, metadata_format=MetadataFormat.ID3V2)
update_file_metadata("song.flac", metadata, metadata_format=MetadataFormat.VORBIS)
update_file_metadata("song.wav", metadata, metadata_format=MetadataFormat.RIFF)
```

**Format Limitations:**

- **Vorbis (FLAC)**: Supports true multiple entries (separate frames) ✅
- **ID3v2.4 (MP3)**: Supports true multiple entries (separate frames) ✅
- **ID3v2.3 (MP3)**: Uses single frame with separators (e.g., "Artist One;Artist Two") ⚠️
- **RIFF (WAV)**: Uses single frame with separators ⚠️
- **ID3v1**: Uses single frame with separators ⚠️

> **Note**: ID3v2.3, RIFF, and ID3v1 formats do not support multiple separate frames for the same metadata field. Multiple values are stored as a single frame with separator characters. ID3v2.4 supports multiple separate frames, but the library uses ID3v2.3 by default for maximum compatibility.

**Smart Separator Selection (Legacy Formats):**

When writing to legacy formats that require concatenated values, the library uses **intelligent separator selection**:

**Separator Priority (when concatenation is needed):**

1. `//` (double slash) - highest priority
2. `\\` (double backslash)
3. `;` (semicolon)
4. `\` (backslash)
5. `/` (forward slash)
6. `,` (comma) - lowest priority

**Selection Logic:**

- Scans values for each separator in priority order
- Uses the first separator that doesn't appear in any of the values
- Ensures no false splitting when reading back the data

**Examples of Smart Separator Selection:**

```python
# Example 1: Clean values - uses highest priority separator
values = ["Artist One", "Artist Two", "Artist Three"]
# Result: "Artist One//Artist Two//Artist Three" (uses //)

# Example 2: Values contain // - uses next priority separator
values = ["Artist//One", "Artist Two", "Artist Three"]
# Result: "Artist//One\\Artist Two\\Artist Three" (uses \\)

# Example 3: Values contain // and \\ - uses semicolon
values = ["Artist//One", "Artist\\Two", "Artist Three"]
# Result: "Artist//One;Artist\\Two;Artist Three" (uses ;)

# Example 4: All common separators present - uses comma
values = ["Artist//One", "Artist\\Two", "Artist;Three", "Artist/Four"]
# Result: "Artist//One,Artist\\Two,Artist;Three,Artist/Four" (uses ,)
```

**Handling Separator Characters in Modern Formats:**

```python
# Values with separators are preserved correctly as separate entries
metadata = {
    UnifiedMetadataKey.ARTISTS_NAMES: [
        "Artist; with; semicolons",      # Preserved as single value
        "Another, Artist, with, commas", # Preserved as single value
        "Artist | with | pipes"          # Preserved as single value
    ]
}

update_file_metadata("song.mp3", metadata)
# Result: Each value remains intact as separate entries
# No incorrect splitting when reading back
```

**Mixed Format Scenarios:**

```python
# Writing to a file that already has concatenated values
# Library detects existing format and handles appropriately

# If file has: "Artist One;Artist Two" (concatenated)
# And you write: ["Artist Three", "Artist Four"]
# Result depends on format:
# - Vorbis (FLAC): ["Artist One", "Artist Two", "Artist Three", "Artist Four"] (separate entries)
# - ID3v2/RIFF/ID3v1: "Artist One;Artist Two;Artist Three;Artist Four" (concatenated)
```

**Removing Multiple Values:**

```python
# Remove field entirely
update_file_metadata("song.mp3", {
    UnifiedMetadataKey.ARTISTS_NAMES: None
})

# Remove field with empty list
update_file_metadata("song.mp3", {
    UnifiedMetadataKey.ARTISTS_NAMES: []
})
```

#### Why This Approach Works

**Reading Strategy:**

1. **Respects format capabilities**: Uses separate entries when possible
2. **Handles mixed scenarios**: Processes both modern and legacy data correctly
3. **Preserves intentional separators**: Values containing separators stay intact
4. **Backward compatible**: Works with legacy single-entry data
5. **No false positives**: Won't incorrectly split values that contain separators intentionally

**Writing Strategy:**

1. **Format-appropriate approach**: Uses multiple entries for modern formats, smart concatenation for legacy
2. **Intelligent separator selection**: Chooses separators that won't conflict with actual values
3. **Consistent with reading**: Uses the same separator priority order for round-trip compatibility
4. **Handles edge cases**: Gracefully manages values containing all common separators
5. **Preserves data integrity**: Ensures values can be accurately read back without corruption
6. **Automatic**: No configuration needed - the library chooses the best approach

### Single-Value Fields Behavior

For fields that semantically cannot have multiple values (like `TITLE`, `ALBUM_NAME`, `COMMENT`, etc.), the library ensures consistent single-value behavior:

#### How Single-Value Fields Handle Multiple Values

When the underlying audio format contains multiple values for a single-value field, **the library always returns the first value only**.

**Examples:**

- If a file has multiple titles: `["Main Title", "Alternative Title"]` → Returns: `"Main Title"`
- If a file has multiple album names: `["Album Name", "Extended Album Name"]` → Returns: `"Album Name"`

#### Field Classification

The library automatically classifies fields as single-value or multi-value:

**Single-Value Fields** (return strings):

- `TITLE`
- `ALBUM_NAME`
- `COMMENT`
- `YEAR`
- `TRACK_NUMBER`
- And most other metadata fields

**Multi-Value Fields** (return lists):

- `ARTISTS_NAMES`
- `ALBUM_ARTISTS_NAMES`
- `GENRES_NAMES`
- `COMPOSER`
- `MUSICIANS`
- `CONDUCTOR`
- `ARRANGER`

#### Why This Behavior?

1. **Semantic Consistency**: Fields like "title" conceptually represent a single value
2. **User Expectations**: Applications expect single values for these fields
3. **Format Compatibility**: Some formats (like ID3v1) only support single values
4. **Predictable API**: Ensures consistent return types regardless of underlying format

#### Example Usage

```python
from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey

# Even if the file has multiple titles, you get only the first one
metadata = get_merged_unified_metadata("song.mp3")
title = metadata.get(UnifiedMetadataKey.TITLE)  # Returns: "Main Title" (string)

# Multi-value fields return lists
artists = metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)  # Returns: ["Artist 1", "Artist 2"] (list)
```

### Genre Handling

AudioMeta provides comprehensive genre support across all audio formats, with intelligent handling of genre codes, multiple genres, and format-specific limitations.

#### Genre Support by Format

| Format            | Multiple Genres | Genre Codes | Custom Genres | Notes                                                                      |
| ----------------- | --------------- | ----------- | ------------- | -------------------------------------------------------------------------- |
| **ID3v2 (MP3)**   | ✅              | ✅          | ✅            | Full support for multiple genres and custom names                          |
| **Vorbis (FLAC)** | ✅              | ❌          | ✅            | Text-based genres with separator support                                   |
| **RIFF (WAV)**    | ✅\*            | ✅          | ✅\*          | Text mode: multiple genres via separators; Code mode: single genre (0-147) |
| **ID3v1**         | ❌              | ✅          | ❌            | Single genre with code conversion                                          |

#### ID3v1 Genre Code System

ID3v1 uses a standardized genre code system with 192 predefined genres:

- **Genres 0-79**: Original ID3v1 specification
- **Genres 80-125**: Winamp extensions
- **Genres 126-147**: Other players' extensions
- **Genres 148-191**: Winamp 5.6 extensions (November 2010)
- **Code 255**: Unknown/unspecified genre

**Popular Genres:**

```python
# Common genre codes
0: "Blues"
17: "Rock"
18: "Techno"
25: "Euro-Techno"
32: "Classical"
80: "Folk"
131: "Indie"
189: "Dubstep"
```

#### Automatic Genre Conversion

The library automatically converts genre names to appropriate codes when writing to ID3v1 and RIFF formats:

```python
# Writing genres - automatic conversion
update_file_metadata("song.mp3", {
    UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Alternative"]
})

# For ID3v1: Converts "Rock" to code 17 (takes first genre only)
# For RIFF: Uses genre codes (0-147) or falls back to text mode
# For ID3v2/Vorbis: Stores as text values
```

**Conversion Logic:**

1. **Exact Match**: Case-insensitive exact name match
2. **Partial Match**: Genre name contained in standard name
3. **Fallback**: Code 255 (unknown) if no match found

#### Multiple Genre Handling

**Reading Multiple Genres:**

```python
metadata = get_merged_unified_metadata("song.mp3")
genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
# Returns: ['Rock', 'Alternative', 'Indie'] (list)
```

**Writing Multiple Genres:**

```python
# All formats accept lists
update_file_metadata("song.mp3", {
    UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Alternative", "Indie"]
})

# Format-specific behavior:
# - ID3v2: Stores all genres as separate frames
# - Vorbis: Stores as semicolon-separated values
# - RIFF: Uses first genre only (code-based)
# - ID3v1: Uses first genre only (code-based)
```

#### Format-Specific Limitations

**RIFF/WAV Format:**

- **Genre Code Mode (Preferred)**: Uses predefined codes (0-147)
- **Text Mode (Less Common)**: Direct text storage (limited compatibility)
- **Single Genre Only**: No multiple genre support
- **No Custom Genres**: Limited to standard genre list

#### RIFF Genre Support

RIFF supports two distinct genre modes, each with different capabilities and compatibility characteristics.

**Genre Code Mode:**

- **Format**: Single numeric value (0-147) stored in IGNR tag
- **Compatibility**: High - works with older software and players
- **Limitations**:
  - Only predefined genres from ID3v1/RIFF standard list
  - Single genre only
  - No custom genres
- **Example**: Code `17` = "Rock", Code `20` = "Alternative"

**Text Mode (Less Common):**

- **Format**: Text string stored in IGNR tag
- **Compatibility**: Lower - not all software recognizes this mode
- **Capabilities**:
  - Multiple genres via separators (real-world usage)
  - Custom genre names
  - Mixed genre codes and names
  - More flexible than code mode

**Common Multi-Genre Text Patterns:**

- `"Rock; Alternative; Indie"` (semicolon-separated names)
- `"Jazz, Fusion, Experimental"` (comma-separated names)
- `"Electronic/Dance/Ambient"` (slash-separated names)
- `"17; 20; 131"` (semicolon-separated codes)
- `"8, 30, 26"` (comma-separated codes)
- `"Rock; 20; Indie"` (mixed names and codes)

**Why This Matters:**
Many audio editing software and tagging tools write multiple genres to RIFF files using separators, even though it's not standardized. This creates a gap between what users write and what AudioMeta currently reads.

**Examples:**

```python
# Example 1: Genre names only
# File contains: "Rock; Alternative; Indie" in IGNR tag
metadata = get_merged_unified_metadata("song.wav")
genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
# Currently returns: ["Rock"] (first genre only)
# Future: Will return: ["Rock", "Alternative", "Indie"]

# Example 2: Genre codes only
# File contains: "17; 20; 131" in IGNR tag
metadata = get_merged_unified_metadata("song.wav")
genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
# Currently returns: ["Rock"] (first code converted to name)
# Future: Will return: ["Rock", "Alternative", "Indie"]

# Example 3: Mixed codes and names
# File contains: "Rock; 20; Indie" in IGNR tag
metadata = get_merged_unified_metadata("song.wav")
genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
# Currently returns: ["Rock"] (first genre only)
# Future: Will return: ["Rock", "Alternative", "Indie"]
```

**ID3v1 Format:**

- **Single Genre Only**: Takes first genre from list
- **Code-Based**: Converts names to numeric codes
- **No Custom Genres**: Limited to predefined list
- **30-Character Limit**: Genre names truncated if too long

**ID3v2/Vorbis Formats:**

- **Full Flexibility**: Multiple genres, custom names
- **Text-Based**: No code conversion needed
- **Separator Support**: Handles semicolon-separated values
- **Unlimited**: No practical limits on genre count

#### Working with Genre Codes

```python
from audiometa.utils.id3v1_genre_code_map import ID3V1_GENRE_CODE_MAP

# Look up genre code
genre_code = 17  # Rock
genre_name = ID3V1_GENRE_CODE_MAP[genre_code]  # "Rock"

# Find code by name
def find_genre_code(name):
    for code, genre in ID3V1_GENRE_CODE_MAP.items():
        if genre and genre.lower() == name.lower():
            return code
    return None

rock_code = find_genre_code("Rock")  # Returns 17
```

#### Best Practices

1. **Use Descriptive Names**: Write genres as readable text, let the library handle conversion
2. **Order Matters**: For single-genre formats, the first genre in the list is used
3. **Format Awareness**: Check format capabilities before writing multiple genres
4. **Fallback Handling**: Unknown genres gracefully fall back to "Unknown" (code 255)

```python
# Recommended approach
genres = ["Rock", "Alternative", "Indie"]
update_file_metadata("song.mp3", {
    UnifiedMetadataKey.GENRES_NAMES: genres
})

# The library automatically:
# - Converts to codes for ID3v1/RIFF
# - Stores as text for ID3v2/Vorbis
# - Handles format limitations gracefully
```

### Rating Profiles

AudioMeta implements a sophisticated rating profile system to handle the complex compatibility requirements across different audio players and formats. This system ensures that ratings work consistently regardless of which software was used to create them.

#### The Rating Profile Problem

**The Problem**: Different audio players use completely different numeric values for the same star ratings. For example, a 3-star rating can be stored as:

- `128` (Windows Media Player, MusicBee, Winamp)
- `60` (FLAC players, Vorbis)
- `153` (Traktor)

**The Solution**: AudioMeta automatically detects and converts between these different rating systems, so you always get consistent 0-10 scale values regardless of which software created the file.

> 📋 **Complete Compatibility Table**: See [`rating_profiles.py`](audiometa/utils/rating_profiles.py) for the detailed reference table showing all player compatibility and exact numeric values.

**Key Points:**

- **0/None ratings**: `0` can mean either "no rating" (Traktor) or "0 stars" (MusicBee) - AudioMeta distinguishes between them and handles "no rating" cases
- **Half-star support**: Limited support - mainly MusicBee and some ID3v2 implementations
- **Traktor limitation**: Only supports whole stars (1, 2, 3, 4, 5)
- **Format compatibility**: Different formats use different rating systems
- **Automatic handling**: AudioMeta manages all the complexity for you

#### Rating Profile Types

AudioMeta recognizes three main rating profiles:

**Profile A: 255 Non-Proportional (Most Common)**

- Used by: ID3v2 (MP3), RIFF (WAV), most standard players
- Examples: Windows Media Player, MusicBee, Winamp, kid3
- **Half-star support**: ✅ Full support (0.5, 1.5, 2.5, 3.5, 4.5 stars)

**Profile B: 100 Proportional (FLAC Standard)**

- Used by: Vorbis (FLAC), some WAV ID3v2 implementations
- Examples: FLAC files, some modern players
- **Half-star support**: ✅ Full support (0.5, 1.5, 2.5, 3.5, 4.5 stars)

**Profile C: 255 Proportional (Traktor)**

- Used by: Traktor software (Native Instruments)
- Examples: Traktor Pro, Traktor DJ
- **Half-star support**: ❌ No support (only whole stars: 1, 2, 3, 4, 5)

#### How AudioMeta Handles Rating Profiles

**Automatic Profile Detection**

```python
from audiometa import get_merged_unified_metadata

# AudioMeta automatically detects the rating profile and normalizes the value
metadata = get_merged_unified_metadata("song.mp3")
rating = metadata.get('rating')  # Always returns 0-10 scale regardless of source profile

# Examples of what you get:
# - File rated 3 stars in Windows Media Player (128) → rating = 6.0
# - File rated 3 stars in FLAC player (60) → rating = 6.0
# - File rated 3 stars in Traktor (153) → rating = 6.0
# - File rated 3.5 stars in MusicBee (186) → rating = 7.0
# - File rated 2.5 stars in FLAC (50) → rating = 5.0
```

**Writing with Profile Compatibility**

```python
from audiometa import update_file_metadata

# AudioMeta automatically uses the most compatible profile for each format
update_file_metadata("song.mp3", {"rating": 6})   # Uses Profile A (128)
update_file_metadata("song.flac", {"rating": 6})  # Uses Profile B (60)
update_file_metadata("song.wav", {"rating": 6})   # Uses Profile A (128)

# Half-star ratings are also supported:
update_file_metadata("song.mp3", {"rating": 7})   # 3.5 stars → Profile A (186)
update_file_metadata("song.flac", {"rating": 5})  # 2.5 stars → Profile B (50)
```

#### Half-Star Rating Support

AudioMeta fully supports half-star ratings (0.5, 1.5, 2.5, 3.5, 4.5 stars) across most formats:

```python
# Reading half-star ratings
metadata = get_merged_unified_metadata("half_star_rated.mp3")
rating = metadata.get('rating')  # Could be 1.0, 3.0, 5.0, 7.0, 9.0 for half-stars

# Writing half-star ratings
update_file_metadata("song.mp3", {"rating": 7})   # 3.5 stars
update_file_metadata("song.flac", {"rating": 5})  # 2.5 stars
update_file_metadata("song.wav", {"rating": 9})   # 4.5 stars
```

**Format Support for Half-Stars:**

- ✅ **ID3v2 (MP3)**: Full half-star support
- ✅ **Vorbis (FLAC)**: Full half-star support
- ✅ **RIFF (WAV)**: Full half-star support
- ❌ **Traktor**: Only whole stars (1, 2, 3, 4, 5)

#### Cross-Player Compatibility

AudioMeta ensures that ratings work across different players:

```python
# Read a file rated in Windows Media Player
metadata = get_merged_unified_metadata("windows_rated.mp3")
print(f"Rating: {metadata['rating']}")  # 6.0 (3 stars)

# Write the same rating to a FLAC file
update_file_metadata("new_song.flac", {"rating": 6})

# The FLAC file will now show 3 stars in any FLAC-compatible player
# The MP3 file will continue to show 3 stars in Windows Media Player
```

#### Traktor Special Handling

Traktor uses special email tags to identify its ratings:

```python
# AudioMeta automatically detects Traktor ratings
metadata = get_merged_unified_metadata("traktor_rated.mp3")
# If the file was rated in Traktor, AudioMeta handles it correctly
# even though Traktor uses different numeric values
```

#### Rating Profile Examples

**Reading from Different Sources**

```python
# All these files show 3 stars, but use different internal values
files = [
    "windows_rated.mp3",    # Internal value: 128
    "flac_rated.flac",      # Internal value: 60
    "traktor_rated.mp3"    # Internal value: 153
]

for file_path in files:
    metadata = get_merged_unified_metadata(file_path)
    print(f"{file_path}: {metadata['rating']}")  # All show 6.0
```

**Writing for Maximum Compatibility**

```python
# Write a 4-star rating (8.0) to different formats
update_file_metadata("song.mp3", {"rating": 8})   # Writes 196 (Profile A)
update_file_metadata("song.flac", {"rating": 8})   # Writes 80 (Profile B)
update_file_metadata("song.wav", {"rating": 8})    # Writes 196 (Profile A)

# All files will show 4 stars in their respective players
```

#### Advanced Rating Operations

**Normalized Rating Scale**

```python
# AudioMeta uses a 0-10 scale internally
# 0 = No rating
# 2 = 1 star
# 4 = 2 stars
# 6 = 3 stars
# 8 = 4 stars
# 10 = 5 stars

update_file_metadata("song.mp3", {"rating": 8})  # 4 stars
```

**Format-Specific Rating Writing**

```python
from audiometa.utils.MetadataFormat import MetadataFormat

# Force a specific format (useful for compatibility testing)
update_file_metadata("song.wav", {"rating": 6},
                    metadata_format=MetadataFormat.ID3V2)  # Uses Profile A
update_file_metadata("song.wav", {"rating": 6},
                    metadata_format=MetadataFormat.RIFF)   # Uses Profile A
```

#### Why Rating Profiles Matter

Without AudioMeta's rating profile system:

- **Incompatible ratings**: A file rated 3 stars in Windows Media Player might show as 1 star in a FLAC player
- **Lost ratings**: Converting between formats could lose rating information
- **Player lock-in**: Ratings created in one player wouldn't work in others

With AudioMeta's system:

- **Universal compatibility**: Ratings work the same regardless of source or destination
- **Seamless conversion**: Converting between formats preserves rating meaning
- **Player independence**: Use any player to rate, any player to read

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
| Multiple Entries  | ❌             | ✅ (v2.4)      | ✅           | ❌            | ✅ mp3, flac, ❌ wav |
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
| Album Artist      |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Genre             | ✓ (1#)         | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Release Date      | ✓ (4)          | ✓ (10)         | ✓ (10)       | ✓ (10)        | ✓                    |
| Track Number      | ✓ (1#)         | ✓ (0-255#)     | ✓ (Unlim#)   | ✓ (Unlim#)    | ✓                    |
| Rating            |                | ✓ (0-255#)     | ✓ (0-100#)   | ✓ (0-100#\*)  | ✓                    |
| BPM               |                | ✓ (0-65535#)   | ✓ (0-65535#) | ✓ (0-65535#)  | ✓                    |
| Language          |                | ✓ (3)          | ✓ (3)        | ✓ (3)         | ✓                    |
| Composer          |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Publisher         |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Copyright         |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Lyrics            |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Comment           | ✓ (28)         | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    | ✓                    |
| Encoder           |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| URL               |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| ISRC              |                | ✓ (12)         | ✓ (12)       | ✓ (12)        |                      |
| Mood              |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Key               |                | ✓ (3)          | ✓ (3)        | ✓ (3)         |                      |
| Original Date     |                | ✓ (10)         | ✓ (10)       | ✓ (10)        |                      |
| Remixer           |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Conductor         |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Cover Art         |                | ✓ (10MB#)      | ✓ (10MB#)    | ✓ (10MB#)     |                      |
| Compilation       |                | ✓ (1#)         | ✓ (1#)       | ✓ (1#)        |                      |
| Media Type        |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| File Owner        |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Recording Date    |                | ✓ (10)         | ✓ (10)       | ✓ (10)        |                      |
| File Size         |                | ✓ (16#)        | ✓ (Format)   | ✓ (16#)       |                      |
| Encoder Settings  |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| ReplayGain        |                | ✓ (8#)         | ✓ (8#)       | ✓ (8#)        |                      |
| MusicBrainz ID    |                | ✓ (36)         | ✓ (36)       | ✓ (36)        |                      |
| Arranger          |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Version           |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Performance       |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Archival Location |                |                |              | ✓ (Format)    |                      |
| Keywords          |                |                |              | ✓ (Format)    |                      |
| Subject           |                |                |              | ✓ (Format)    |                      |
| Original Artist   |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Set Subtitle      |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Initial Key       |                | ✓ (3)          | ✓ (3)        | ✓ (3)         |                      |
| Involved People   |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Musicians         |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |
| Part of Set       |                | ✓ (Format)     | ✓ (Format)   | ✓ (Format)    |                      |

### Track Number Formats

The library handles different track number formats across audio metadata standards:

#### ID3v2 Format (MP3, WAV, FLAC)

- **Format**: `"track/total"` (e.g., `"5/12"`, `"99/99"`)
- **Parsing**: Library extracts only the track number (first part before `/`)
- **Why extract only the track number?**
  - **Industry Standard**: This is the standard practice used by Mutagen, eyed3, and most audio players
  - **ID3v2 Specification**: The specification allows both simple (`"5"`) and complex (`"5/12"`) formats
  - **User Experience**: Users typically care about "track 5" rather than "track 5 of 12"
  - **Compatibility**: Works consistently across different tagging software and players
  - **Consistency**: Provides uniform behavior regardless of how the file was originally tagged
- **Examples**:
  - `"5/12"` → Track number: `5`
  - `"99/99"` → Track number: `99`
  - `"1"` → Track number: `1` (simple format also supported)

#### ID3v1 Format (MP3, FLAC, WAV)

- **Format**: Simple numeric string (e.g., `"5"`, `"12"`)
- **Parsing**: Direct conversion to integer
- **Examples**:
  - `"5"` → Track number: `5`
  - `"12"` → Track number: `12`

#### Vorbis Format (FLAC)

- **Format**: Simple numeric string (e.g., `"5"`, `"12"`)
- **Parsing**: Direct conversion to integer
- **Examples**:
  - `"5"` → Track number: `5`
  - `"12"` → Track number: `12`

#### RIFF Format (WAV)

- **Format**: Simple numeric string (e.g., `"5"`, `"12"`)
- **Parsing**: Direct conversion to integer
- **Examples**:
  - `"5"` → Track number: `5`
  - `"12"` → Track number: `12`

#### Edge Case Handling

The library gracefully handles common edge cases:

- `"5/"` → Track number: `5` (trailing slash ignored)
- `"/12"` → Track number: `None` (no track number before slash)
- `"abc/def"` → Track number: `None` (non-numeric values)
- `""` → Track number: `None` (empty string)
- `"5/12/15"` → Track number: `5` (takes first part before first slash)
- `"5-12"` → `ValueError` (different separator, no slash)

### ID3v2 Multiple Entries Specification

The ID3v2 specification has different rules for handling multiple values depending on the version:

#### ID3v2.3 (Default - Maximum Compatibility)

- **Multiple Frames**: ❌ **NOT supported** - Only one frame per type allowed
- **Multiple Values**: Uses concatenation within a single frame with separators
- **Example**: `"Artist One;Artist Two;Artist Three"` in a single `TPE1` frame
- **Why**: ID3v2.3 specification limits each frame type to one instance per tag
- **Compatibility**: Maximum compatibility with older players and devices

#### ID3v2.4 (Modern Features)

- **Multiple Frames**: ✅ **Supported** - Multiple frames of the same type allowed
- **Multiple Values**: Uses separate frames for each value
- **Example**: Three separate `TPE1` frames: `"Artist One"`, `"Artist Two"`, `"Artist Three"`
- **Why**: ID3v2.4 specification explicitly allows multiple instances of the same frame type
- **Compatibility**: Modern players and applications that support ID3v2.4

#### Library Behavior

The library automatically adapts based on the ID3v2 version:

- **ID3v2.3 (default)**: Uses concatenation with smart separator selection
- **ID3v2.4**: Uses multiple separate frames when `id3v2_version=(2, 4, 0)` is specified

```python
from audiometa import update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey

# ID3v2.3 (default) - uses concatenation
update_file_metadata("song.mp3", {
    UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
})
# Result: Single TPE1 frame with "Artist One;Artist Two"

# ID3v2.4 - uses multiple frames
update_file_metadata("song.mp3", {
    UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
}, id3v2_version=(2, 4, 0))
# Result: Two separate TPE1 frames: "Artist One" and "Artist Two"
```

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
3. **ID3v1** (lowest precedence, legacy format)

#### MP3 Files

1. **ID3v2** (highest precedence)
2. **ID3v1** (lowest precedence, legacy format)

#### WAV Files

1. **RIFF** (highest precedence)
2. **ID3v2**
3. **ID3v1** (lowest precedence, legacy format)

**Examples**:

- For MP3 files: If a title exists in both ID3v1 and ID3v2, the ID3v2 title will be returned.
- For WAV files: If a title exists in both RIFF and ID3v2, the RIFF title will be returned.
- For FLAC files: If a title exists in both Vorbis and ID3v2, the Vorbis title will be returned.

### Writing Defaults by Audio Format

When writing metadata, the library uses these default metadata formats per audio file type:

#### MP3 Files

**Default Writing Format**: ID3v2 (v2.3)

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

**Note**: ID3v1 is a legacy format with limitations (30-character field limits, Latin-1 encoding). The library supports both reading and writing ID3v1 tags using direct file manipulation.

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
2. **`PRESERVE`**: Write to native format only, preserve existing metadata in other formats. Handles unsupported fields gracefully with warnings.
3. **`CLEANUP`**: Write to native format and remove all non-native metadata formats. Handles unsupported fields gracefully with warnings.

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

#### Usage Examples

**Default Behavior (SYNC strategy)**

```python
from audiometa import update_file_metadata

# WAV file with existing ID3v1 tags (30-char limit)
update_file_metadata("song.wav", {"title": "This is a Very Long Title That Exceeds ID3v1 Limits"})

# Result:
# - RIFF tags: Updated with full title (native format)
# - ID3v1 tags: Synchronized with truncated title (30 chars max)
# - When reading: RIFF title is returned (higher precedence)
# Note: ID3v1 title becomes "This is a Very Long Title Th" (truncated)
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
# - RIFF tags: Synchronized with new metadata (native format)
# - ID3v2 tags: Synchronized with new metadata (if present)
# - ID3v1 tags: Synchronized with new metadata (if present)
# - When reading: RIFF title is returned (highest precedence)
# Note: SYNC preserves and updates ALL existing metadata formats
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

The library handles unsupported metadata consistently across all strategies:

- **Forced format** (when `metadata_format` is specified): Always fails fast by raising `MetadataNotSupportedError` for any unsupported field. **No writing is performed** - the file remains completely unchanged.
- **All strategies (SYNC, PRESERVE, CLEANUP) with `fail_on_unsupported_field=False` (default)**: Handle unsupported fields gracefully by logging warnings and continuing with supported fields
- **All strategies (SYNC, PRESERVE, CLEANUP) with `fail_on_unsupported_field=True`**: Fails fast if any field is not supported by the target format. **No writing is performed** - the file remains completely unchanged (atomic operation).

#### Format-Specific Limitations

| Format         | Forced Format                     | All Strategies (SYNC, PRESERVE, CLEANUP) with `fail_on_unsupported_field=False` | All Strategies with `fail_on_unsupported_field=True` |
| -------------- | --------------------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **RIFF (WAV)** | Always fails fast, **no writing** | Logs warnings for unsupported fields, writes supported ones                     | Fails fast for unsupported fields, **no writing**    |
| **ID3v1**      | Always fails fast, **no writing** | Logs warnings for unsupported fields, writes supported ones                     | Fails fast for unsupported fields, **no writing**    |
| **ID3v2**      | Always fails fast, **no writing** | All fields supported                                                            | All fields supported                                 |
| **Vorbis**     | Always fails fast, **no writing** | All fields supported                                                            | All fields supported                                 |

#### Atomic Write Operations

When `fail_on_unsupported_field=True` is used, the library ensures **atomic write operations**:

- **All-or-nothing behavior**: Either all metadata is written successfully, or nothing is written at all
- **File integrity**: If any field is unsupported, the file remains completely unchanged
- **No partial updates**: Prevents inconsistent metadata states where only some fields are updated
- **Error safety**: Ensures that failed operations don't leave files in a partially modified state

This atomic behavior is crucial for:

- **Data integrity**: Prevents corruption from partial writes
- **Consistency**: Ensures metadata is always in a valid state
- **Reliability**: Makes operations predictable and safe to retry
- **Debugging**: Clear failure modes make issues easier to diagnose

#### Example: Handling Unsupported Metadata

```python
from audiometa import update_file_metadata
from audiometa.exceptions import MetadataNotSupportedError
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy

# All strategies - handle unsupported fields gracefully with warnings
update_file_metadata("song.wav", {"title": "Song", "rating": 85, "bpm": 120})
# Result: Writes title and rating to RIFF, logs warning about BPM, continues

update_file_metadata("song.wav", {"title": "Song", "rating": 85, "bpm": 120},
                    metadata_strategy=MetadataWritingStrategy.PRESERVE)
# Result: Writes title and rating to RIFF, logs warning about BPM, preserves other formats

update_file_metadata("song.wav", {"title": "Song", "rating": 85, "bpm": 120},
                    metadata_strategy=MetadataWritingStrategy.CLEANUP)
# Result: Writes title and rating to RIFF, logs warning about BPM, removes other formats

# Forced format - always fails fast for unsupported fields, no writing performed
try:
    update_file_metadata("song.wav", {"title": "Song", "rating": 85, "bpm": 120},
                        metadata_format=MetadataFormat.RIFF)
except MetadataNotSupportedError as e:
    print(f"BPM not supported in RIFF format: {e}")
    # File remains completely unchanged - no metadata was written

# Strategies with fail_on_unsupported_field=True - atomic operation, no writing on failure
try:
    update_file_metadata("song.wav", {"title": "Song", "rating": 85, "bpm": 120},
                        metadata_strategy=MetadataWritingStrategy.SYNC,
                        fail_on_unsupported_field=True)
except MetadataNotSupportedError as e:
    print(f"BPM not supported: {e}")
    # File remains completely unchanged - no metadata was written (atomic operation)

# Practical example: Demonstrating atomic behavior
from audiometa import get_merged_unified_metadata

# File with existing metadata
original_metadata = get_merged_unified_metadata("song.wav")
print(f"Original title: {original_metadata.get('title')}")  # e.g., "Original Title"

# Attempt to write metadata with unsupported field
try:
    update_file_metadata("song.wav", {
        "title": "New Title",      # This would be supported
        "rating": 85,              # This would be supported
        "bpm": 120                 # This is NOT supported by RIFF format
    }, fail_on_unsupported_field=True)
except MetadataNotSupportedError:
    pass

# Verify file is unchanged (atomic behavior)
final_metadata = get_merged_unified_metadata("song.wav")
print(f"Final title: {final_metadata.get('title')}")  # Still "Original Title" - no changes made
```

### None vs Empty String Handling

The library handles `None` and empty string values differently across audio formats:

| Format            | Setting to `None`        | Setting to `""` (empty string)   | Read Back Result               |
| ----------------- | ------------------------ | -------------------------------- | ------------------------------ |
| **ID3v2 (MP3)**   | Removes field completely | Removes field completely         | `None` / `None`                |
| **Vorbis (FLAC)** | Removes field completely | Creates field with empty content | `None` / `""`                  |
| **RIFF (WAV)**    | Removes field completely | Removes field completely         | `None` / `None`                |
| **ID3v1 (MP3)**   | ✅ **Supported**         | ✅ **Supported**                 | Legacy format with limitations |

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
