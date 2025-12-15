# MusicBrainz Artist IDs

## Table of Contents

- [What it is](#what-it-is)
- [Format support and mapping](#format-support-and-mapping)
- [Reading](#reading)
- [Writing](#writing)

## What it is

MusicBrainz Artist IDs are unique UUIDs (36 characters with hyphens) that identify artists in the MusicBrainz database. Each artist has one MBID, but tracks can have multiple artists, so this field supports multiple IDs. It is typically written as UUID strings, for example: `9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6`.

## Format support and mapping

## Reading

AudioMeta reads all relevant metadata locations that may contain a MusicBrainz Artist ID to preserve source data and provide interoperability. When multiple candidate values are present, AudioMeta chooses a canonical value according to a format-specific priority while preserving other values where possible.

| Format     | Support | Field / Key                                                   | Multiple |
| ---------- | ------- | ------------------------------------------------------------- | -------- |
| **ID3v2**  | ✅      | `TXXX` (description: `MusicBrainz Artist Id`)                 | ✅       |
| **Vorbis** | ✅      | `MUSICBRAINZ_ARTISTID` or `musicbrainz_artistid` (Vorbis key) | ✅       |
| **RIFF**   | ✅      | `MBAR` FourCC (native INFO)                                   | ✅       |
| **ID3v1**  | ❌      | —                                                             | ❌       |

- **ID3v2**: AudioMeta reads `TXXX` frames with description/name `MusicBrainz Artist Id`. AudioMeta accepts descriptions in any case (e.g., `musicbrainz artist id`, `MUSICBRAINZ ARTIST ID`, `MusicBrainz artist id`) for compatibility with various tagging tools. Multiple values are stored in a single TXXX frame using separators (ID3v2.3) or null-separated values (ID3v2.4), following the standard ID3v2 multiple values handling.

- **Vorbis**: AudioMeta reads the `MUSICBRAINZ_ARTISTID` key in Vorbis comments. AudioMeta accepts any case and preserves source-case values, but it prefers the canonical uppercase form when returning unified metadata. Multiple comments with the same key are collected and returned as a list.

- **RIFF**: AudioMeta reads `MBAR` FourCC entries in the INFO chunk when present. Multiple MBAR entries are collected and returned as a list.

**Examples:**

```python
from audiometa import get_unified_metadata, get_unified_metadata_field
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.metadata_format import MetadataFormat

# Read all metadata (including MusicBrainz Artist IDs)
metadata = get_unified_metadata("song.mp3")
mb_artist_ids = metadata.get(UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
print(mb_artist_ids)  # ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"] for single, ["id1", "id2"] for multiple

# Read only the MusicBrainz Artist IDs field
mb_artist_ids = get_unified_metadata_field("song.flac", UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
print(mb_artist_ids)  # e.g., ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]

# Read from specific format
metadata = get_unified_metadata("song.wav", metadata_format=MetadataFormat.RIFF)
mb_artist_ids = metadata.get(UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)

# Note: AudioMeta accepts TXXX descriptions in any case (e.g., "MusicBrainz Artist Id",
# "musicbrainz artist id", "MUSICBRAINZ ARTIST ID"). If multiple exist, it prioritizes
# the canonical "MusicBrainz Artist Id" form.

# Priority example: File with TXXX frames:
# - "MusicBrainz Artist Id" = "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"
# - "musicbrainz artist id" = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
# - "MUSICBRAINZ ARTIST ID" = "11111111-2222-3333-4444-555555555555"
# Returns the canonical value
metadata = get_unified_metadata("priority_example.mp3")
mb_artist_ids = metadata.get(UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
print(mb_artist_ids)  # ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]
```

## Writing

| Format     | Support | Field / Key                                   | Multiple |
| ---------- | ------- | --------------------------------------------- | -------- |
| **ID3v2**  | ✅      | `TXXX` (description: `MusicBrainz Artist Id`) | ✅       |
| **Vorbis** | ✅      | `MUSICBRAINZ_ARTISTID` (Vorbis key)           | ✅       |
| **RIFF**   | ✅      | `MBAR` FourCC (native INFO)                   | ✅       |
| **ID3v1**  | ❌      | —                                             | ❌       |

- **UUID format**: Each MusicBrainz Artist ID should be a valid UUID string. Accept either the canonical 36-character hyphenated UUID (preferred) or, in non-standard flows, a 32-character hex string (without hyphens).
- **Multiple values**: Multiple Artist IDs can be stored. When writing, provide a list of UUID strings. For ID3v2, values are stored in a single TXXX frame using separators (ID3v2.3) or null-separated values (ID3v2.4), following the standard ID3v2 multiple values handling.
- **Clearing**: To remove all MusicBrainz Artist IDs from a file, set the value to `None`, an empty list, or an empty string when writing.

**Examples:**

```python
from audiometa import update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.metadata_format import MetadataFormat

# Write single MusicBrainz Artist ID
update_metadata(
    "song.mp3",
    {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]}
)

# Write multiple MusicBrainz Artist IDs
update_metadata(
    "song.mp3",
    {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6", "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"]}
)

# Write MusicBrainz Artist ID (32-character hex string without hyphens)
update_metadata(
    "song.flac",
    {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["9d6f6f7c9d524c768f9e01d18d8f8ec6"]}
)

# Write to specific format
update_metadata(
    "song.wav",
    {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]},
    metadata_format=MetadataFormat.RIFF
)

# Delete MusicBrainz Artist IDs by setting to None
update_metadata(
    "song.mp3",
    {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: None}
)
```

# Delete MusicBrainz Artist IDs by setting to empty list or None

```python
from audiometa import update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey

update_metadata(
    "song.flac",
    {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: []}
)
```

**Validation Examples:**

```python
from audiometa import validate_metadata_for_update
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import InvalidMetadataFieldFormatError, InvalidMetadataFieldTypeError

# Valid: Single 36-character hyphenated UUID in list
validate_metadata_for_update(
    {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]}
)

# Valid: Multiple UUIDs
validate_metadata_for_update(
    {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6", "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"]}
)

# Valid: 32-character hex string without hyphens
validate_metadata_for_update(
    {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["9d6f6f7c9d524c768f9e01d18d8f8ec6"]}
)

# Valid: None (clearing the field)
validate_metadata_for_update(
    {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: None}
)

# Valid: Empty list (clearing the field)
validate_metadata_for_update(
    {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: []}
)

# Invalid: Not a valid UUID format
try:
    validate_metadata_for_update(
        {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["not-a-uuid"]}
    )
except InvalidMetadataFieldFormatError:
    print("Invalid UUID format")

# Invalid: Too short
try:
    validate_metadata_for_update(
        {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["9d6f6f7c-9d52-4c76"]}
    )
except InvalidMetadataFieldFormatError:
    print("UUID too short")

# Invalid: Wrong type
try:
    validate_metadata_for_update(
        {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: 12345}
    )
except InvalidMetadataFieldTypeError:
    print("Must be a list")
```
