# Disc Number Handling

For each format, **Spec / convention** is what the standard or usual ecosystem practice implies. **This library** describes how we read and write so typical multi-disc tags map to **`DISC_NUMBER`** / **`DISC_TOTAL`**.

## Format overview

| Format | Native fields             | Read                                                                                                   | Write                                                                                   |
| ------ | ------------------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| ID3v1  | —                         | Not supported                                                                                          | Not supported                                                                           |
| ID3v2  | `TPOS`                    | `n`, `n/m`, `n-m` → integers ([details](#id3v2-disc-number-format))                                    | `n` or `n/m` with **`/`** only; **0–255** per component ([notes](#writing-disc-number)) |
| Vorbis | `DISCNUMBER`, `DISCTOTAL` | First value per tag as integer; **`DISCNUMBER=1/2` not split** ([details](#vorbis-disc-number-format)) | Separate tags ([notes](#writing-disc-number))                                           |
| RIFF   | —                         | Not supported                                                                                          | Not supported                                                                           |

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

- **Spec / convention**: Comment keys are informal; tools use **two tags** or put **`n/m` in `DISCNUMBER`** only (like **`TPOS`**).
- **This library**: **Write** always uses **separate** `DISCNUMBER` and `DISCTOTAL`. **Read** uses the first merged value per key (case-folded names). Each unified field is set only when that comment’s value is a **plain integer**; otherwise **`None`**.

**`DISCNUMBER` with slash (e.g. `1/2`)**: Not split on read, so **`DISC_NUMBER`** is **`None`**. **`DISCTOTAL`** is still read alone—e.g. `DISCNUMBER=1/2` + `DISCTOTAL=2` → **`DISC_NUMBER=None`**, **`DISC_TOTAL=2`**. For both fields today, use **`DISCNUMBER=1`** and **`DISCTOTAL=2`**, or see the table below for intended future behavior.

### Suggested implementation: slash in `DISCNUMBER` and conflicting totals

| Situation                                                                              | Suggested rule                                                                                                                                                                             |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `DISCNUMBER="n"` only                                                                  | `DISC_NUMBER=n`, `DISC_TOTAL=None`                                                                                                                                                         |
| `DISCNUMBER="n/m"` and **no** `DISCTOTAL`                                              | `DISC_NUMBER=n`, `DISC_TOTAL=m`                                                                                                                                                            |
| `DISCNUMBER="n"` and `DISCTOTAL="m"`                                                   | `DISC_NUMBER=n`, `DISC_TOTAL=m`                                                                                                                                                            |
| `DISCNUMBER="n/m"` **and** `DISCTOTAL="m"` **where** `m` ≠ second part of `DISCNUMBER` | **Prefer explicit `DISCTOTAL`** for unified `DISC_TOTAL`, and **the leading integer segment of `DISCNUMBER`** for `DISC_NUMBER`. Optionally **debug log** when the slash suffix disagrees. |
| Invalid `DISCNUMBER` (non-numeric, multiple slashes)                                   | `DISC_NUMBER=None`; derive `DISC_TOTAL` only from `DISCTOTAL` if valid                                                                                                                     |

**Rationale:** `DISCTOTAL` is an explicit correction channel; the numeric prefix of `DISCNUMBER` stays the disc index when the embedded `/total` is stale.

**Vorbis vs ID3v2 on read:** Same unified outcome for a typical **`1/2`** string only when it lives in **ID3v2 `TPOS`** (split) or in **separate** Vorbis tags—not when it is a **single** `DISCNUMBER` value (not split yet).

## Unified Metadata API

- **`DISC_NUMBER`**: Current disc index (**`int`**).
- **`DISC_TOTAL`**: Total discs or **`None`**.

Reading and writing follow the [format overview](#format-overview); ID3v2 regex and Vorbis slash behavior are spelled out in the sections above.

### Writing Disc Number

| Unified Metadata                | ID3v1 | ID3v2          | Vorbis                              | RIFF |
| ------------------------------- | ----- | -------------- | ----------------------------------- | ---- |
| `DISC_NUMBER=1`                 | ✗     | `TPOS="1"`     | `DISCNUMBER="1"`                    | ✗    |
| `DISC_NUMBER=1, DISC_TOTAL=2`   | ✗     | `TPOS="1/2"`   | `DISCNUMBER="1"`, `DISCTOTAL="2"`   | ✗    |
| `DISC_NUMBER=99, DISC_TOTAL=99` | ✗     | `TPOS="99/99"` | `DISCNUMBER="99"`, `DISCTOTAL="99"` | ✗    |
| `DISC_NUMBER=256`               | ✗     | `TPOS="255"`\* | `DISCNUMBER="256"`                  | ✗    |

\* ID3v2 truncates values exceeding 255 to 255.

**Notes:** ID3v1 and RIFF have no disc field. ID3v2 combines number and total into one `TPOS` string with **`/`**. Vorbis writes two comments; omit `DISCTOTAL` when `DISC_TOTAL` is **`None`**. Vorbis has no library-enforced max on write.

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
