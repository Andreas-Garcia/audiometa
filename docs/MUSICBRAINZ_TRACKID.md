# MusicBrainz Track ID

## Table of Contents

- [What it is](#what-it-is)
- [Format support and mapping](#format-support-and-mapping)
- [Reading](#reading)
- [Writing](#writing)

## What it is

The MusicBrainz Track ID (also called the Recording ID in MusicBrainz terminology) is a unique UUID (36 characters with hyphens) that identifies the recording in the MusicBrainz database. It is typically written as a UUID string, for example: `9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6`.

## Format support and mapping

## Reading

AudioMeta reads all relevant metadata locations that may contain a MusicBrainz Track ID to preserve source data and provide interoperability. When multiple candidate values are present, AudioMeta chooses a canonical value according to a format-specific priority while preserving other values where possible.

| Format     | Support | Field / Key                                                                               | Multiple |
| ---------- | ------- | ----------------------------------------------------------------------------------------- | -------- |
| **ID3v2**  | ✅      | `UFID` (owner: `http://musicbrainz.org`) and `TXXX` (description: `MusicBrainz Track Id`) | ❌       |
| **Vorbis** | ✅      | `MUSICBRAINZ_TRACKID` or `musicbrainz_trackid` (Vorbis key)                               | ❌       |
| **RIFF**   | ✅      | `MBID` FourCC (native INFO)                                                               | ❌       |
| **ID3v1**  | ❌      | —                                                                                         | ❌       |

- **ID3v2**: AudioMeta reads all relevant ID3v2 frames that can carry a MusicBrainz Track ID (including `UFID` frames and `TXXX` frames). Canonical priority:

  1. `UFID` with owner `http://musicbrainz.org` (preferred)
  2. `TXXX` frame with description/name `MusicBrainz Track Id` (fallback)

- **Vorbis**: AudioMeta reads the `MUSICBRAINZ_TRACKID` key in Vorbis comments. AudioMeta accepts any case and preserves source-case values, but it prefers the canonical uppercase form when returning unified metadata.

- **RIFF**: AudioMeta reads `MBID` FourCC entries in the INFO chunk when present.

**Examples:**

```python
from audiometa import get_unified_metadata, get_unified_metadata_field
from audiometa import UnifiedMetadataKey
from audiometa.utils.metadata_format import MetadataFormat

# Read all metadata (including MusicBrainz Track ID)
metadata = get_unified_metadata("song.mp3")
track_id = metadata.get(UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
print(track_id)  # e.g., "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"

# Read only the MusicBrainz Track ID field
track_id = get_unified_metadata_field("song.flac", UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
print(track_id)  # e.g., "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"

# Read from specific format
metadata = get_unified_metadata("song.wav", metadata_format=MetadataFormat.RIFF)
track_id = metadata.get(UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
```

## Writing

| Format     | Support | Field / Key                              | Multiple |
| ---------- | ------- | ---------------------------------------- | -------- |
| **ID3v2**  | ✅      | `UFID` (owner: `http://musicbrainz.org`) | ❌       |
| **Vorbis** | ✅      | `MUSICBRAINZ_TRACKID` (Vorbis key)       | ❌       |
| **RIFF**   | ✅      | `MBID` FourCC (native INFO)              | ❌       |
| **ID3v1**  | ❌      | —                                        | ❌       |

- **UUID format**: The MusicBrainz Track ID should be a valid UUID string. Accept either the canonical 36-character hyphenated UUID (preferred) or, in non-standard flows, a 32-character hex string (without hyphens).
- **One value per file**: Only a single MusicBrainz Track ID should be present in the relevant metadata container for a given file (e.g., a single UFID or a single `MUSICBRAINZ_TRACKID` Vorbis key or a single `MBID` RIFF FourCC).
- **Clearing**: To remove the MusicBrainz Track ID from a file, set the value to `None` or an empty string when writing.

**Examples:**

```python
from audiometa import update_metadata
from audiometa import UnifiedMetadataKey
from audiometa.utils.metadata_format import MetadataFormat

# Write MusicBrainz Track ID (canonical 36-character hyphenated UUID)
update_metadata(
    "song.mp3",
    {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"}
)

# Write MusicBrainz Track ID (32-character hex string without hyphens)
update_metadata(
    "song.flac",
    {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "9d6f6f7c9d524c768f9e01d18d8f8ec6"}
)

# Write to specific format
update_metadata(
    "song.wav",
    {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"},
    metadata_format=MetadataFormat.RIFF
)

# Delete MusicBrainz Track ID by setting to None
update_metadata(
    "song.mp3",
    {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: None}
)

# Delete MusicBrainz Track ID by setting to empty string
update_metadata(
    "song.flac",
    {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: ""}
)
```

**Validation Examples:**

```python
from audiometa import validate_metadata_for_update
from audiometa import UnifiedMetadataKey
from audiometa.exceptions import InvalidMetadataFieldFormatError, InvalidMetadataFieldTypeError

# Valid: 36-character hyphenated UUID (preferred format)
validate_metadata_for_update(
    {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"}
)

# Valid: 32-character hex string without hyphens
validate_metadata_for_update(
    {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "9d6f6f7c9d524c768f9e01d18d8f8ec6"}
)

# Valid: None (clearing the field)
validate_metadata_for_update(
    {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: None}
)

# Valid: Empty string (clearing the field)
validate_metadata_for_update(
    {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: ""}
)

# Invalid: Not a valid UUID format
try:
    validate_metadata_for_update(
        {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "not-a-uuid"}
    )
except InvalidMetadataFieldFormatError:
    print("Invalid UUID format")

# Invalid: Too short
try:
    validate_metadata_for_update(
        {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "9d6f6f7c-9d52-4c76"}
    )
except InvalidMetadataFieldFormatError:
    print("UUID too short")

# Invalid: Wrong type
try:
    validate_metadata_for_update(
        {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: 12345}
    )
except InvalidMetadataFieldTypeError:
    print("Must be a string")
```
