# Track and disc numbers

Unified metadata uses different shapes for **track** vs **disc/set** position:

- **`TRACK_NUMBER`**: a single **string** (e.g. `"5"`, `"5/12"`) from ID3v2 `TRCK`, Vorbis `TRACKNUMBER`, RIFF `IPRT`, etc.
- **`DISC_NUMBER`** and **`DISC_TOTAL`**: **integers** (total optional) from ID3v2 `TPOS`, Vorbis `DISCNUMBER` / `DISCTOTAL`, etc.

The sections below document each concept by metadata format.

## Track number

### ID3v1 track number format

ID3v1 does not natively support track numbers. The library supports storing track numbers in the comment field since ID3v1.1 format.

- **Format**: Simple numeric string (e.g., `"5"`, `"12"`)
- **Parsing**: Returns as string
- **Examples**:
  - `"5"` → Track number: `"5"`
  - `"12"` → Track number: `"12"`

### ID3v2 track number format

- **Format**: `"track/total"` (e.g., `"5/12"`, `"99/99"`) or simple `"track"` (e.g., `"5"`, `"1"`)
- **Parsing**: Returns the full track number string as stored
- **Examples**:
  - `"5/12"` → Track number: `"5/12"`
  - `"99/99"` → Track number: `"99/99"`
  - `"1"` → Track number: `"1"` (simple format also supported)

### Vorbis track number format

- **Format**: Simple numeric string (e.g., `"5"`, `"12"`) or **`track/total`** (e.g., `"5/12"`, `"4/11"`), as commonly stored in `TRACKNUMBER` (same idea as ID3v2 `TRCK`). A single separator (`/` or `-`) with optional total segment is accepted; the value is not split into separate unified fields.
- **Parsing**: Returns the **full string** when it matches the library pattern; otherwise `None` (see edge cases below).
- **Examples**:
  - `"5"` → Track number: `"5"`
  - `"5/12"` → Track number: `"5/12"`
  - `"4/11"` → Track number: `"4/11"`

### RIFF track number format

- **Format**: Simple numeric string (e.g., `"5"`, `"12"`)
- **Parsing**: Returns as string
- **Examples**:
  - `"5"` → Track number: `"5"`
  - `"12"` → Track number: `"12"`

### Reading and writing track number

#### Reading track number

The library returns track numbers as strings. The library handles common edge cases:

- `"5/"` → Track number: `"5/"` (trailing slash preserved)
- `"/12"` → Track number: `None` (no track number before slash)
- `"abc/def"` → Track number: `None` (non-numeric values)
- `""` → Track number: `None` (empty string)
- `"5/12/15"` → Track number: `None` (multiple slashes, invalid format)
- `"5-12"` → Track number: `"5-12"` (different separator preserved)
- `"01"` → Track number: `"01"` (leading zeros preserved)

#### Writing track number

The library supports writing track numbers in various formats. For formats that support track totals, the full format is preserved. The following matrix shows what value is written for each input format:

| Input Value | ID3v1  | ID3v2     | Vorbis    | RIFF      |
| ----------- | ------ | --------- | --------- | --------- |
| `5` (int)   | `"5"`  | `"5"`     | `"5"`     | `"5"`     |
| `"5"` (str) | `"5"`  | `"5"`     | `"5"`     | `"5"`     |
| `"5/12"`    | `"5"`  | `"5/12"`  | `"5/12"`  | `"5/12"`  |
| `"99/99"`   | `"99"` | `"99/99"` | `"99/99"` | `"99/99"` |
| `"1"`       | `"1"`  | `"1"`     | `"1"`     | `"1"`     |

**Notes:**

- **ID3v1**: Only supports track numbers (1-255), extracts the track number from formats like "5/12" and ignores the total
- **ID3v2**: Supports full track/total format (e.g., "5/12") as per ID3v2 specification
- **Vorbis**: Supports full track/total format through TRACKNUMBER field
- **RIFF**: Track number writing is not currently supported

## Disc number

For each format, **spec / convention** is what the standard or common ecosystem practice implies. **This library** describes how values are read/written so multi-disc tags map predictably to **`DISC_NUMBER`** / **`DISC_TOTAL`**.

### Format overview

| Format | Native fields             | Read                                                                                                                                                                               | Write                                                                                   |
| ------ | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| ID3v1  | —                         | Not supported                                                                                                                                                                      | Not supported                                                                           |
| ID3v2  | `TPOS`                    | `n`, `n/m`, `n-m` → integers ([details](#id3v2-disc-number-format))                                                                                                                | `n` or `n/m` with **`/`** only; **0–255** per component ([notes](#writing-disc-number)) |
| Vorbis | `DISCNUMBER`, `DISCTOTAL` | Same **`n` / `n/m` / `n-m`** rules as ID3v2 **`TPOS`** on first **`DISCNUMBER`**; **`DISCTOTAL` overrides** embedded total when both apply ([details](#vorbis-disc-number-format)) | Separate tags ([notes](#writing-disc-number))                                           |
| RIFF   | —                         | Not supported                                                                                                                                                                      | Not supported                                                                           |

### ID3v1 and RIFF

**ID3v1**: fixed **128-byte** trailer with no disc field.
**RIFF INFO**: no standard disc / part-of-set FourCC comparable to `TPOS`.
**This library**: unified disc fields are not supported for ID3v1 or RIFF.

### ID3v1 disc number format

ID3v1 does not support disc numbers due to its limited fixed structure.

- **Support**: ✗ Not supported
- **Reason**: ID3v1 has a fixed 128-byte structure with no field for disc number
- **Workaround**: None available (format limitation)

### ID3v2 disc number format

ID3v2 supports disc numbers through the `TPOS` (Part of a set) frame.

- **Frame**: TPOS (Part of a set)
- **Format**: `"disc/total"` (e.g., `"1/2"`, `"2/3"`, `"99/99"`) or simple `"disc"` (e.g., `"1"`, `"2"`). Hyphen (`"1-2"`) is accepted on **read** as an alias.
- **Range**: 0-255 for both disc number and total discs
- **Unified API Mapping**:
  - `TPOS="1/2"` → `DISC_NUMBER=1`, `DISC_TOTAL=2`
  - `TPOS="1"` → `DISC_NUMBER=1`, `DISC_TOTAL=None`
- **Examples**:
  - `"1/2"` → `DISC_NUMBER=1`, `DISC_TOTAL=2` (disc 1 of 2)
  - `"2/3"` → `DISC_NUMBER=2`, `DISC_TOTAL=3` (disc 2 of 3)
  - `"1"` → `DISC_NUMBER=1`, `DISC_TOTAL=None` (simple format, disc 1, total unknown)
  - `"99/99"` → `DISC_NUMBER=99`, `DISC_TOTAL=99` (maximum supported value)

**Limitations:**

- Maximum disc number: 255
- Maximum total discs: 255
- Values exceeding 255 are typically truncated or may cause errors depending on the implementation
- Read-side parsing does not clamp values >255 when such values already exist in tags

### Vorbis disc number format

Vorbis comments support disc numbers through `DISCNUMBER` and optionally `DISCTOTAL`. Many encoders and taggers also store a **combined** `disc/total` string in `DISCNUMBER` alone (same idea as ID3v2 `TPOS`), e.g. `DISCNUMBER=1/2`. AudioMeta **reads** all of these shapes; when **writing**, it uses separate `DISCNUMBER` and `DISCTOTAL` tags (native for the unified API).

- **Fields**:
  - `DISCNUMBER` - Current disc number as a simple numeric string (e.g. `"1"`, `"2"`) **or** combined `"disc/total"` (e.g. `"1/2"`, `"1/1"`)
  - `DISCTOTAL` - Total number of discs when stored separately (optional simple numeric string, e.g. `"2"`, `"3"`)
- **Range**: Unlimited (no hard limit, but practical limits apply)
- **Unified API Mapping (reading)**:
  - `DISCNUMBER="1"`, `DISCTOTAL="2"` → `DISC_NUMBER=1`, `DISC_TOTAL=2`
  - `DISCNUMBER="1/2"` → `DISC_NUMBER=1`, `DISC_TOTAL=2` (same idea as ID3v2 `TPOS`; hyphen `1-2` is accepted on read)
  - `DISCNUMBER="1/3"`, `DISCTOTAL="2"` → `DISC_NUMBER=1`, `DISC_TOTAL=2` (explicit `DISCTOTAL` overrides the total embedded in `DISCNUMBER` when it is a valid non-negative integer)
  - `DISCNUMBER="2"` → `DISC_NUMBER=2`, `DISC_TOTAL=None`
  - `DISCNUMBER="99"`, `DISCTOTAL="99"` → `DISC_NUMBER=99`, `DISC_TOTAL=99`
  - `DISCTOTAL="2"` with no usable `DISCNUMBER` → `DISC_NUMBER=None`, `DISC_TOTAL=2`
- **Examples**:
  - `DISCNUMBER="1"`, `DISCTOTAL="2"` → `DISC_NUMBER=1`, `DISC_TOTAL=2` (disc 1 of 2)
  - `DISCNUMBER="1/2"` → `DISC_NUMBER=1`, `DISC_TOTAL=2` (combined form, common in the wild)
  - `DISCNUMBER="2"` → `DISC_NUMBER=2`, `DISC_TOTAL=None` (disc 2, total unknown)
  - `DISCNUMBER="99"`, `DISCTOTAL="99"` → `DISC_NUMBER=99`, `DISC_TOTAL=99` (disc 99 of 99)

**Advantages over ID3v2:**

- No 255 limit on disc numbers
- Separate fields allow for more flexible storage
- Can represent multi-disc sets with more than 255 discs (theoretical)
- Native support for separate fields matches the unified API design

### RIFF disc number format

RIFF (WAV) format does not natively support disc numbers in its INFO chunk structure.

- **Support**: ✗ Not supported
- **Reason**: RIFF INFO chunk has no standard field for disc number
- **Workaround**: None available (format limitation)

### Unified metadata API (disc)

The library provides two separate unified metadata fields for disc number handling:

- **`DISC_NUMBER`**: Integer representing the current disc number (required)
- **`DISC_TOTAL`**: Integer representing the total number of discs, or `None` if unknown (optional)

This two-field approach provides:

- **Type safety**: Both fields are integers, not strings requiring parsing
- **Flexibility**: Can set disc number without knowing total, or update total independently
- **Semantic clarity**: Disc number and total are conceptually separate pieces of information
- **Native Vorbis support**: Matches Vorbis' separate `DISCNUMBER` and `DISCTOTAL` fields

#### Reading disc number

The library returns disc numbers as separate fields:

- `DISC_NUMBER`: Integer (e.g., `1`, `2`, `99`)
- `DISC_TOTAL`: Integer or `None` (e.g., `2`, `3`, `None`)

**Format Mapping:**

- **ID3v2**: Reads `TPOS` frame with `"disc/total"` format (e.g., `"1/2"`) → `DISC_NUMBER=1`, `DISC_TOTAL=2`
- **ID3v2**: Reads `TPOS` frame with `"disc"` format (e.g., `"1"`) → `DISC_NUMBER=1`, `DISC_TOTAL=None`
- **Vorbis**: Reads `DISCNUMBER` like ID3v2 `TPOS` (`n`, `n/m`, `n-m`); explicit `DISCTOTAL` overrides the embedded total when valid
- **ID3v1**: Not supported
- **RIFF**: Not supported

#### Writing disc number

The library writes disc numbers based on the unified metadata fields:

| Unified Metadata                | ID3v1 | ID3v2          | Vorbis                              | RIFF |
| ------------------------------- | ----- | -------------- | ----------------------------------- | ---- |
| `DISC_NUMBER=1`                 | ✗     | `TPOS="1"`     | `DISCNUMBER="1"`                    | ✗    |
| `DISC_NUMBER=1, DISC_TOTAL=2`   | ✗     | `TPOS="1/2"`   | `DISCNUMBER="1"`, `DISCTOTAL="2"`   | ✗    |
| `DISC_NUMBER=99, DISC_TOTAL=99` | ✗     | `TPOS="99/99"` | `DISCNUMBER="99"`, `DISCTOTAL="99"` | ✗    |
| `DISC_NUMBER=256`               | ✗     | `TPOS="255"`\* | `DISCNUMBER="256"`                  | ✗    |

\* ID3v2 truncates values exceeding 255 to 255

**Notes:**

- **ID3v1**: Disc number is not supported - no field available in the format
- **ID3v2**:
  - Combines `DISC_NUMBER` and `DISC_TOTAL` into `"disc/total"` format when writing (e.g., `"1/2"`)
  - If `DISC_TOTAL` is `None`, writes only disc number (e.g., `"1"`)
  - Values are limited to 0-255 range
  - Values exceeding 255 are typically truncated to 255
- **Vorbis**:
  - Writes `DISCNUMBER` and `DISCTOTAL` as separate fields (native format)
  - If `DISC_TOTAL` is `None`, only `DISCNUMBER` is written
  - Partial update behavior: when a file already has combined `DISCNUMBER` (`n/m` or `n-m`) and no usable explicit `DISCTOTAL`,
    updating only `DISC_NUMBER` preserves the embedded total by writing/updating `DISCTOTAL` (a valid explicit `DISCTOTAL` stays authoritative)
  - No hard limit on disc numbers (unlimited in theory)
- **RIFF**: Disc number writing is not supported - no standard field in INFO chunk

### Format comparison (disc)

| Format | Frame/Field           | Format Support | Range Limit | Unified API Mapping                                                              |
| ------ | --------------------- | -------------- | ----------- | -------------------------------------------------------------------------------- |
| ID3v1  | ✗                     | ✗              | N/A         | ✗                                                                                |
| ID3v2  | TPOS                  | ✓              | 0-255       | `"disc/total"` → `DISC_NUMBER`, `DISC_TOTAL`                                     |
| Vorbis | DISCNUMBER, DISCTOTAL | ✓              | Unlimited   | Separate tags and combined `DISCNUMBER=disc/total` → `DISC_NUMBER`, `DISC_TOTAL` |
| RIFF   | ✗                     | ✗              | N/A         | ✗                                                                                |

### Common use cases (disc)

1. **Single Disc Albums**: `DISC_NUMBER=1`, `DISC_TOTAL=1` or `DISC_NUMBER=1`, `DISC_TOTAL=None`
2. **Multi-Disc Albums**: `DISC_NUMBER=1`, `DISC_TOTAL=2` for disc 1 of 2-disc set
3. **Large Box Sets**: `DISC_NUMBER=1`, `DISC_TOTAL=10` for disc 1 of 10-disc set
4. **Unknown Total**: `DISC_NUMBER=1`, `DISC_TOTAL=None` when total number of discs is unknown

### API usage examples (disc)

```python
from audiometa import update_metadata, get_unified_metadata
from audiometa import UnifiedMetadataKey

# Set disc number with total
update_metadata("album.mp3", {
    UnifiedMetadataKey.DISC_NUMBER: 1,
    UnifiedMetadataKey.DISC_TOTAL: 2
})

# Set disc number without total
update_metadata("album.mp3", {
    UnifiedMetadataKey.DISC_NUMBER: 1
})

# Read disc number
metadata = get_unified_metadata("album.mp3")
disc_number = metadata.get(UnifiedMetadataKey.DISC_NUMBER)  # 1
disc_total = metadata.get(UnifiedMetadataKey.DISC_TOTAL)    # 2 or None
```

### Limitations summary (disc)

- **ID3v1**: Cannot store disc numbers (format limitation)
- **ID3v2**: Limited to 255 discs maximum (both disc number and total)
- **Vorbis**: No hard limit, but practical limits apply based on implementation
- **RIFF**: Cannot store disc numbers (format limitation)
