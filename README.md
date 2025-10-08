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

| Field             | ID3v1          | ID3v2          | Vorbis       | RIFF          | AudioMeta Support    |
| ----------------- | -------------- | -------------- | ------------ | ------------- | -------------------- |
| Text Encoding     | ASCII          | UTF-8/16/ISO   | UTF-8        | ASCII/UTF-8   | UTF-8                |
| Max Text Length   | 30 chars       | ~8M chars      | ~8M chars    | ~1M chars     | Format limit         |
| Rating Range      | Not supported  | 0-255#         | 0-100#       | Not supported | 0-10#                |
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
| Rating            |                | ✓ (0-255#)     | ✓ (0-100#)   |               | ✓                    |
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

By default, the library writes metadata **only to the native format** for each file type and **does not modify** existing metadata in other formats:

- **MP3 files**: Writes to ID3v2 only
- **FLAC files**: Writes to Vorbis comments only
- **WAV files**: Writes to RIFF only

#### Metadata Strategy Options

You can control metadata writing behavior using the `metadata_strategy` parameter:

**Available Strategies:**

1. **`PRESERVE` (Default)**: Write to native format only, preserve existing metadata in other formats
2. **`CLEANUP`**: Write to native format and remove all non-native metadata formats
3. **`SYNC`**: Write to native format and synchronize other metadata formats that are already present
4. **`IGNORE`**: Write to native format only, ignore other formats completely (same as PRESERVE)

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

**Default Behavior (PRESERVE strategy)**

```python
from audiometa import update_file_metadata

# WAV file with existing ID3v2 tags
update_file_metadata("song.wav", {"title": "New Title"})

# Result:
# - ID3v2 tags: Preserved (unchanged)
# - RIFF tags: Updated with new metadata
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

**IGNORE**

- **Performance**: Fastest option, minimal processing
- **Simple**: Just writes to native format, ignores everything else

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

## None vs Empty String Handling

The library handles `None` and empty string values differently across audio formats. Here's a summary of the behavior:

| Format            | Setting to `None`        | Setting to `""` (empty string)   | Read Back Result |
| ----------------- | ------------------------ | -------------------------------- | ---------------- |
| **ID3v2 (MP3)**   | Removes field completely | Removes field completely         | `None` / `None`  |
| **Vorbis (FLAC)** | Removes field completely | Creates field with empty content | `None` / `""`    |
| **RIFF (WAV)**    | Removes field completely | Removes field completely         | `None` / `None`  |
| **ID3v1 (MP3)**   | ❌ **Not supported**     | ❌ **Not supported**             | Read-only format |

### Key Differences

- **ID3v2**: Both `None` and `""` remove the field completely (mutagen removes empty frames automatically)
- **Vorbis**: `None` removes the field, `""` creates an empty field
- **RIFF**: Both `None` and `""` remove the field completely
- **ID3v1**: Not supported

### Example

```python
from audiometa import update_file_metadata, get_specific_metadata

# MP3 file - same behavior for None and empty string (mutagen removes empty frames)
update_file_metadata("song.mp3", {"title": None})
title = get_specific_metadata("song.mp3", "title")
print(title)  # Output: None (field removed)

update_file_metadata("song.mp3", {"title": ""})
title = get_specific_metadata("song.mp3", "title")
print(title)  # Output: None (field removed, mutagen removes empty frames)

# FLAC file - different behavior for None vs empty string (like MP3)
update_file_metadata("song.flac", {"title": None})
title = get_specific_metadata("song.flac", "title")
print(title)  # Output: None (field removed)

update_file_metadata("song.flac", {"title": ""})
title = get_specific_metadata("song.flac", "title")
print(title)  # Output: "" (field exists but empty)

# WAV file - same behavior for None and empty string
update_file_metadata("song.wav", {"title": None})
title = get_specific_metadata("song.wav", "title")
print(title)  # Output: None (field removed)

update_file_metadata("song.wav", {"title": ""})
title = get_specific_metadata("song.wav", "title")
print(title)  # Output: None (field removed)
```

## Multiple Artists and Album Artists Handling

The library supports multiple artists and album artists across all audio formats, following industry standards and technical specifications for each metadata format.

### Format-Specific Standards

#### **ID3v2 (MP3 Files)**

**ID3v2.4 (Recommended)**

- **Multiple TPE1 frames**: Each artist gets their own `TPE1` (Lead Performer/Soloist) frame
- **Multiple TPE2 frames**: Each album artist gets their own `TPE2` (Band/Orchestra/Accompaniment) frame
- **Null separator**: Use null character (`\0`) as separator within a single frame
- **Examples**:

  ```
  TPE1=Artist One
  TPE1=Artist Two
  TPE1=Artist Three

  TPE2=Album Artist One
  TPE2=Album Artist Two
  ```

**ID3v2.3 (Legacy)**

- **Single TPE1 frame with separator**: Use consistent delimiter in one frame for track artists
- **Single TPE2 frame with separator**: Use consistent delimiter in one frame for album artists
- **Common separators**: Semicolon (`;`), slash (`/`), or double slash (`//`)
- **Examples**:
  - `TPE1=Artist One; Artist Two; Artist Three`
  - `TPE2=Album Artist One; Album Artist Two`

#### **Vorbis Comments (FLAC, Ogg Vorbis)**

**Multiple ARTIST and ALBUMARTIST fields (Recommended)**

- **Separate fields**: Each artist gets their own `ARTIST` field
- **Separate album artist fields**: Each album artist gets their own `ALBUMARTIST` field
- **No delimiters needed**: This is the cleanest approach
- **Examples**:

  ```
  ARTIST=Artist One
  ARTIST=Artist Two
  ARTIST=Artist Three

  ALBUMARTIST=Album Artist One
  ALBUMARTIST=Album Artist Two
  ```

#### **RIFF/WAV Files**

**Multiple IART and IPRD fields**

- **Separate IART fields**: Each artist gets their own `IART` (Artist) field
- **Separate IPRD fields**: Each album artist gets their own `IPRD` (Product) field
- **Examples**:

  ```
  IART=Artist One
  IART=Artist Two
  IART=Artist Three

  IPRD=Album Artist One
  IPRD=Album Artist Two
  ```

#### **ID3v1 (MP3 Legacy)**

**Single field with separator**

- **30-character limit**: Must fit in single `ARTIST` field
- **No album artist support**: ID3v1 does not support album artist field
- **Common separators**: Slash (`/`), semicolon (`;`), or comma (`,`)
- **Example**: `ARTIST=Artist One / Artist Two`

### Library Implementation

The library automatically handles multiple artists and album artists using these approaches:

1. **Reading**: Automatically detects and parses multiple artists and album artists using format-appropriate methods
2. **Writing**: Uses the best method available for each format (multiple fields when supported, separators when required)
3. **Separator Priority**: When separators are needed, uses this priority order:
   - `//` (double slash)
   - `\\` (double backslash)
   - `;` (semicolon)
   - `\` (backslash)
   - `/` (forward slash)
   - `,` (comma)

### Example Usage

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
print(result[UnifiedMetadataKey.ALBUM_ARTISTS_NAMES])
# Output: ['Album Artist One', 'Album Artist Two']
```

### Multiple Artists/Album Artists Support Summary

| Format      | Track Artists                 | Album Artists               | Reading Method                    | Writing Method             |
| ----------- | ----------------------------- | --------------------------- | --------------------------------- | -------------------------- |
| **ID3v2.4** | ✅ Multiple TPE1 frames       | ✅ Multiple TPE2 frames     | Multiple frames or null-separated | Multiple frames            |
| **ID3v2.3** | ✅ Single TPE1 + separators   | ✅ Single TPE2 + separators | Splits on separators              | Separators in single frame |
| **ID3v2.2** | ✅ Single TPE1 + separators   | ✅ Single TPE2 + separators | Splits on separators              | Separators in single frame |
| **Vorbis**  | ✅ Multiple ARTIST fields     | ✅ Multiple ALBUMARTIST     | Multiple fields directly          | Multiple fields            |
| **RIFF**    | ✅ Multiple IART fields       | ✅ Multiple IPRD fields     | Multiple fields directly          | Multiple fields            |
| **ID3v1**   | ⚠️ Single ARTIST + separators | ❌ Not supported            | Splits on separators              | Separators in single field |

### Key Implementation Details

| Aspect                 | Implementation                                                    |
| ---------------------- | ----------------------------------------------------------------- |
| **Separator Priority** | `//` → `\\` → `;` → `\` → `/` → `,`                               |
| **Reading Logic**      | Tries multiple separators in order, strips whitespace             |
| **Writing Strategy**   | Uses multiple fields when supported, separators when required     |
| **Unified Interface**  | Both `ARTISTS_NAMES` and `ALBUM_ARTISTS_NAMES` return `list[str]` |
| **Error Handling**     | Gracefully handles mixed formats and malformed data               |

### Best Practices

1. **Prefer multiple fields over delimiters** when the format supports it
2. **Use consistent separators** when multiple fields aren't supported
3. **Avoid separators that might appear in artist names** (e.g., avoid comma if artist name contains comma)
4. **Distinguish between track artists and album artists** - track artists are the performers of individual songs, while album artists represent the primary artist(s) responsible for the entire album
5. **Test compatibility** across different media players and devices
6. **Maintain consistency** across your entire music library
7. **Use album artists for compilations** - set album artist to "Various Artists" or the compilation name while keeping individual track artists

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
