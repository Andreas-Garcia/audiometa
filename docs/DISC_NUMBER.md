# Disc Number Handling

For each format, **Spec / convention** is what the standard or usual ecosystem practice implies. **This library** describes how we read and write so typical multi-disc tags map to **`DISC_NUMBER`** / **`DISC_TOTAL`**.

## Format overview

| Format | Native fields             | Read                                                                                                                                                                               | Write                                                                                   |
| ------ | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| ID3v1  | —                         | Not supported                                                                                                                                                                      | Not supported                                                                           |
| ID3v2  | `TPOS`                    | `n`, `n/m`, `n-m` → integers ([details](#id3v2-disc-number-format))                                                                                                                | `n` or `n/m` with **`/`** only; **0–255** per component ([notes](#writing-disc-number)) |
| Vorbis | `DISCNUMBER`, `DISCTOTAL` | Same **`n` / `n/m` / `n-m`** rules as ID3v2 **`TPOS`** on first **`DISCNUMBER`**; **`DISCTOTAL` overrides** embedded total when both apply ([details](#vorbis-disc-number-format)) | Separate tags ([notes](#writing-disc-number))                                           |
| RIFF   | —                         | Not supported                                                                                                                                                                      | Not supported                                                                           |

## ID3v1 and RIFF

**ID3v1**: Fixed **128-byte** trailer—**no** disc field; extending it would break the layout.

**RIFF INFO**: No standard disc / part-of-set FourCC comparable to **`TPOS`**; disc index is out of band for typical WAV metadata.

**This library**: Unified disc fields are **not supported** for ID3v1 or RIFF (no stable mapping).

## ID3v2 Disc Number Format

- **Spec / convention**: **`TPOS`** (“part of a set”) follows the same **`part`** / **`part/total`** pattern as **`TRCK`**, with **`/`**. Common practice limits components to **0–255** (8-bit model).
- **This library**: **Read** parses **`n`**, **`n/m`**, and **`n-m`** (hyphen alias on read only, same idea as `TRCK`). **Write** uses **`/`** only. Invalid strings (e.g. multiple slashes) → **`None`** for the affected unified fields.

**Read parsing** (current implementation):

- `DISC_NUMBER` ← first capture if `^(\d+)(?:[-/](\d+))?$`; else **`None`**
- `DISC_TOTAL` ← second capture only if `^(\d+)[-/](\d+)$` (both parts required); else **`None`**

**Range**: **Read** does not clamp—values **> 255** in the file still parse. **Write** clamps toward **255** where the writer enforces the 8-bit model.

**Examples**: `"1/2"` / `"1-2"` → `1` and `2`; `"1"` → `1`, total **`None`**; `"1/2/3"` → both **`None`**; `"99/99"` → `99` and `99`.

## Vorbis Disc Number Format

- **Spec / convention**: Comment keys are informal; tools often use **two tags** or a **single `DISCNUMBER=n/m`** string, mirroring ID3 **`TPOS`**.
- **This library**: **Write** always uses **separate** `DISCNUMBER` and `DISCTOTAL` ([Writing Disc Number](#writing-disc-number)). **Read** uses the first merged value per key (case-folded names), with **`DISCNUMBER` parsed like ID3v2 `TPOS`** and **`DISCTOTAL` as an explicit override** for the unified total when present.

### Read parsing (aligned with ID3v2 `TPOS`)

Take **`d`** = first value of **`DISCNUMBER`** (after merge), **`t`** = first value of **`DISCTOTAL`** if that tag exists.

1. **Unified `DISC_NUMBER`**
   Parse **`d`** with the **same rules** as ID3v2 **`TPOS`** for the number: first capture of `^(\d+)(?:[-/](\d+))?$`. If it matches → **`DISC_NUMBER`** is that integer; else **`None`**.
   (So **`"1/2"`** and **`"1-2"`** → **`1`**; **`"1"`** → **`1`**; invalid / multi-slash → **`None`**.)

2. **Unified `DISC_TOTAL`**

   - If **`t`** is present and parses as a **non-negative integer** → **`DISC_TOTAL`** = **`t`** (**explicit tag wins**).
   - Else derive total from **`d`** only: second capture of `^(\d+)[-/](\d+)$` (both parts required), same as ID3v2. If that does not apply → **`None`**.

3. **Rationale (conflict strategy)**
   Embedded **`n/m`** in **`DISCNUMBER`** is often copied from other formats and can be **stale**; a separate **`DISCTOTAL`** is usually a deliberate correction. So **`DISCTOTAL` always overrides** the **`m`** from **`DISCNUMBER=n/m`** when both are usable. **`DISC_NUMBER`** still comes **only** from **`d`** (leading segment), never from **`DISCTOTAL`**.

### Examples

| `DISCNUMBER` | `DISCTOTAL` | `DISC_NUMBER` | `DISC_TOTAL` | Note                                    |
| ------------ | ----------- | ------------- | ------------ | --------------------------------------- |
| `1/2`        | —           | 1             | 2            | Same outcome as `TPOS="1/2"`            |
| `1-2`        | —           | 1             | 2            | Hyphen accepted on read, like ID3v2     |
| `1`          | `2`         | 1             | 2            | Two-tag style                           |
| `1/3`        | `2`         | 1             | 2            | Explicit total overrides `/3`           |
| `1/2`        | `bogus`     | 1             | 2            | Invalid `DISCTOTAL` → fall back to `/2` |
| `1/2/3`      | —           | `None`        | `None`       | Invalid combined string (same as ID3v2) |
| —            | `2`         | `None`        | 2            | Total only; no disc index from tags     |

## Unified Metadata API

- **`DISC_NUMBER`**: Current disc index (**`int`**).
- **`DISC_TOTAL`**: Total discs or **`None`**.

Reading and writing follow the [format overview](#format-overview); ID3v2 **`TPOS`** and Vorbis **`DISCNUMBER`** share the same read rules, with Vorbis **`DISCTOTAL`** overriding the embedded total as above.

### Writing Disc Number

| Unified Metadata                | ID3v1 | ID3v2          | Vorbis                              | RIFF |
| ------------------------------- | ----- | -------------- | ----------------------------------- | ---- |
| `DISC_NUMBER=1`                 | ✗     | `TPOS="1"`     | `DISCNUMBER="1"`                    | ✗    |
| `DISC_NUMBER=1, DISC_TOTAL=2`   | ✗     | `TPOS="1/2"`   | `DISCNUMBER="1"`, `DISCTOTAL="2"`   | ✗    |
| `DISC_NUMBER=99, DISC_TOTAL=99` | ✗     | `TPOS="99/99"` | `DISCNUMBER="99"`, `DISCTOTAL="99"` | ✗    |
| `DISC_NUMBER=256`               | ✗     | `TPOS="255"`\* | `DISCNUMBER="256"`                  | ✗    |

\* ID3v2 truncates values exceeding 255 to 255.

**Notes:** ID3v1 and RIFF have no disc field. ID3v2 combines number and total into one `TPOS` string with **`/`**. Vorbis writes two comments and omits `DISCTOTAL` when `DISC_TOTAL` is **`None`** in normal writes. For partial updates, when updating only `DISC_NUMBER` and the existing Vorbis metadata stores combined `DISCNUMBER=n/m` or `DISCNUMBER=n-m` with no `DISCTOTAL`, the library preserves the total by materializing `DISCTOTAL` from the combined value. Vorbis has no library-enforced max on write.

## Common Use Cases

1. **Single disc**: `DISC_NUMBER=1`, `DISC_TOTAL=1` or `DISC_TOTAL=None`
2. **Multi-disc**: `DISC_NUMBER=1`, `DISC_TOTAL=2` for disc 1 of 2
3. **Large sets**: e.g. `DISC_TOTAL=10`
4. **Unknown total**: `DISC_NUMBER=1`, `DISC_TOTAL=None`

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
