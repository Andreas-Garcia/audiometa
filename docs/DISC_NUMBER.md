# Disc Number Handling

For each format, **Spec / convention** is what the standard or usual ecosystem practice implies. **This library** describes how broadly we read and write so typical multi-disc tags (and a few edge cases) map cleanly to **`DISC_NUMBER`** / **`DISC_TOTAL`**. We aim for **wide read** compatibility where the format allows; where the spec has no disc field, we do not invent one.

## ID3v1 Disc Number Format

- **Spec / convention**: **ID3v1** is a fixed **128-byte** trailer with title, artist, album, year, comment, genre—**no** disc or “part of set” field. Extending it would break the layout.
- **This library**: **Not supported**; unified disc fields raise “not supported” for ID3v1.

- **Support**: ✗ Not supported
- **Reason**: ID3v1 has a fixed 128-byte structure with no field for disc number
- **Workaround**: None available (format limitation)

## ID3v2 Disc Number Format

- **Spec / convention**: **ID3v2** defines **`TPOS`** (“part of a set”) as a numeric string, by the same pattern as **`TRCK`**: **part** or **`part/total`** with **`/`**. Stored values are effectively limited by the **8-bit** character model in common use (**0–255** per component).
- **This library**: We parse **`part`**, **`part/total`**, and—on read only—**`part-total`** with **`-`** as an alias separator (wider than the letter of the spec, matching how we treat `TRCK`). Invalid multi-part strings yield **`None`**. **Write** uses **`/`** only so other ID3v2 software sees the canonical shape.

- **Frame**: TPOS (Part of a set)
- **Stored form**: ID3v2 convention is **`/`** between part and total (same family as `TRCK`). On **read**, this library also accepts **`-`** between the two numbers (lenient alias, parity with `TRCK` / `TRACK_NUMBER`); **writes** still use **`/`** only.
- **Read parsing** (current implementation):
  - `DISC_NUMBER` ← first integer if the value matches `^(\d+)(?:[-/](\d+))?$`; otherwise **`None`**
  - `DISC_TOTAL` ← second integer only if the value matches `^(\d+)[-/](\d+)$` (both parts required); otherwise **`None`**
- **Range**: 0-255 for both disc number and total discs (ID3v2 constraints)
- **Examples**:
  - `"1/2"` → `DISC_NUMBER=1`, `DISC_TOTAL=2`
  - `"1-2"` → `DISC_NUMBER=1`, `DISC_TOTAL=2` (non-standard separator, accepted on read)
  - `"1"` → `DISC_NUMBER=1`, `DISC_TOTAL=None`
  - `"1/2/3"` → `DISC_NUMBER=None`, `DISC_TOTAL=None` (invalid for this parser)
  - `"99/99"` → `DISC_NUMBER=99`, `DISC_TOTAL=99`

**Limitations:**

- Maximum disc number: 255
- Maximum total discs: 255
- Values exceeding 255 are typically truncated or may cause errors depending on the implementation

## Vorbis Disc Number Format

- **Spec / convention**: **Vorbis comment** keys are **ASCII** names with **UTF-8** values; **`DISCNUMBER`** and **`DISCTOTAL`** are **informal** but widely used. There is **no** normative grammar—tools either use **two separate fields** or cram **`n/m` into `DISCNUMBER`**, copying ID3 habits.
- **This library**: **Write** always uses **separate** `DISCNUMBER` and `DISCTOTAL` (widest compatibility with metaflac-style workflows). **Read** today accepts **plain integers** in each tag; **combined `DISCNUMBER=n/m`** is **not** yet split (see below)—so we do **not** yet cover the full width of field data in the wild; the table under *Suggested implementation* is the intended direction.

Vorbis comments use `DISCNUMBER` and optionally `DISCTOTAL`. Many taggers also store **`disc/total` inside `DISCNUMBER` alone** (same idea as ID3v2 `TPOS`).

### Current read behavior (library)

- Each mapped tag value is read with **plain integer conversion** on the first entry (`int(...)`).
- **`DISCNUMBER="1/2"`** does **not** parse as an integer → unified **`DISC_NUMBER`** is **`None`** (and **`DISC_TOTAL`** is only filled from **`DISCTOTAL`** when that tag is a valid integer).
- So today, only **separate** numeric `DISCNUMBER` / `DISCTOTAL` (or `DISCTOTAL` alone with a numeric `DISCNUMBER`) behaves as users expect from the unified API.

### Suggested implementation: slash in `DISCNUMBER` and conflicting totals

When adding TPOS-like parsing for Vorbis, these cases should be decided explicitly:

| Situation | Suggested rule |
| --------- | -------------- |
| `DISCNUMBER="n"` only | `DISC_NUMBER=n`, `DISC_TOTAL=None` |
| `DISCNUMBER="n/m"` and **no** `DISCTOTAL` | `DISC_NUMBER=n`, `DISC_TOTAL=m` |
| `DISCNUMBER="n"` and `DISCTOTAL="m"` | `DISC_NUMBER=n`, `DISC_TOTAL=m` |
| `DISCNUMBER="n/m"` **and** `DISCTOTAL="m"` **where** `m` ≠ second part of `DISCNUMBER` | **Prefer explicit `DISCTOTAL`** for unified `DISC_TOTAL`, and **the leading integer segment of `DISCNUMBER`** for `DISC_NUMBER` (so retaggers can correct total without rewriting the combined string). Optionally emit a **debug log** when the slash suffix disagrees. |
| Invalid `DISCNUMBER` (non-numeric, multiple slashes) | `DISC_NUMBER=None`; derive `DISC_TOTAL` only from `DISCTOTAL` if valid |

**Rationale:** `DISCTOTAL` is an explicit correction channel; the numeric prefix of `DISCNUMBER` remains the disc index even when the embedded `/total` is stale.

**Fields (native-on-write):**

- **Writing** (current): separate `DISCNUMBER` and `DISCTOTAL` tags, matching the unified API.

**Advantages over ID3v2:**

- No 255 limit on disc numbers
- Separate fields allow for more flexible storage
- Can represent multi-disc sets with more than 255 discs (theoretical)
- Native support for separate fields matches the unified API design

## RIFF Disc Number Format

- **Spec / convention**: Standard **RIFF INFO** lists do **not** define a **disc** or **part-of-set** FourCC comparable to **`TPOS`**. BWF/INFO extensions focus on title, artist, dates, ISRC, etc.—disc index is **out of band** for typical WAV metadata.
- **This library**: **Not supported** for unified disc fields (no stable field to map).

- **Support**: ✗ Not supported
- **Reason**: RIFF INFO chunk has no standard field for disc number
- **Workaround**: None available (format limitation)

## Unified Metadata API

The library provides two separate unified metadata fields for disc number handling:

- **`DISC_NUMBER`**: Integer representing the current disc number (required)
- **`DISC_TOTAL`**: Integer representing the total number of discs, or `None` if unknown (optional)

This two-field approach provides:

- **Type safety**: Both fields are integers, not strings requiring parsing
- **Flexibility**: Can set disc number without knowing total, or update total independently
- **Semantic clarity**: Disc number and total are conceptually separate pieces of information
- **Native Vorbis support**: Matches Vorbis' separate `DISCNUMBER` and `DISCTOTAL` fields

### Reading Disc Number

The library returns disc numbers as separate fields:

- `DISC_NUMBER`: Integer (e.g., `1`, `2`, `99`)
- `DISC_TOTAL`: Integer or `None` (e.g., `2`, `3`, `None`)

**Format Mapping:**

- **ID3v2**: `TPOS` parsed with `^(\d+)(?:[-/](\d+))?$` for `DISC_NUMBER`; `DISC_TOTAL` only if `^(\d+)[-/](\d+)$` matches (see [ID3v2 disc number format](#id3v2-disc-number-format)).
- **Vorbis**: Today, integer parse per tag; combined `DISCNUMBER=disc/total` is **not** split until the behavior in [Vorbis disc number format](#vorbis-disc-number-format) is implemented.
- **ID3v1**: Not supported
- **RIFF**: Not supported

### Writing Disc Number

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
  - No hard limit on disc numbers (unlimited in theory)
- **RIFF**: Disc number writing is not supported - no standard field in INFO chunk

## Format Comparison

| Format | Frame/Field           | Format Support | Range Limit | Unified API Mapping                           |
| ------ | --------------------- | -------------- | ----------- | --------------------------------------------- |
| ID3v1  | ✗                     | ✗              | N/A         | ✗                                             |
| ID3v2  | TPOS                  | ✓              | 0-255       | `"disc/total"` → `DISC_NUMBER`, `DISC_TOTAL`  |
| Vorbis | DISCNUMBER, DISCTOTAL | ✓              | Unlimited   | Separate tags; combined `DISCNUMBER` not split on read (yet) |
| RIFF   | ✗                     | ✗              | N/A         | ✗                                             |

## Common Use Cases

1. **Single Disc Albums**: `DISC_NUMBER=1`, `DISC_TOTAL=1` or `DISC_NUMBER=1`, `DISC_TOTAL=None`
2. **Multi-Disc Albums**: `DISC_NUMBER=1`, `DISC_TOTAL=2` for disc 1 of 2-disc set
3. **Large Box Sets**: `DISC_NUMBER=1`, `DISC_TOTAL=10` for disc 1 of 10-disc set
4. **Unknown Total**: `DISC_NUMBER=1`, `DISC_TOTAL=None` when total number of discs is unknown

## API Usage Examples

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

## Limitations Summary

- **ID3v1**: Cannot store disc numbers (format limitation)
- **ID3v2**: Limited to 255 discs maximum (both disc number and total); invalid `TPOS` strings yield `None` for disc fields
- **Vorbis**: No hard limit on numeric values; **combined `DISCNUMBER=disc/total` is not split on read** in the current implementation (see suggested rules above)
- **RIFF**: Cannot store disc numbers (format limitation)
