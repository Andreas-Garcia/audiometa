# Track Number Handling

For each container/metadata format below, **Spec / convention** summarizes what the standard or usual practice defines. **This library** states how far we go beyond the minimum so real files from many tools still round-trip sensibly through the unified API. Where the spec is silent or tools disagree, we prefer **lenient read** (accept common variants) and **conservative write** (emit shapes other software expects).

## Shared read rule (`TRACK_NUMBER`)

For formats that map `TRACK_NUMBER` through the default read path (ID3v2 `TRCK`, Vorbis `TRACKNUMBER`, RIFF `IPRT`, …), the first stored value is accepted only if it matches:

`^\d+([-/]\d*)?$`

- **One** optional separator: **`/`** or **`-`**, with an optional total segment (digits may be empty after the separator, e.g. `"5/"`).
- Anything else (multiple slashes, non-digits, leading slash only) → unified `TRACK_NUMBER` is **`None`** (not an error).

ID3v2 describes `number` and `number/total` with **`/`**; **`-`** is not in the spec but is accepted on read like the other formats above.

## ID3v1 Track Number Format

- **Spec / convention**: Original ID3v1 has no track field. **ID3v1.1** encodes an optional **8-bit track number** in the last byte of the 30-byte comment area (tag still 128 bytes total). Values are effectively **1–255**; there is no standard `track/total` in the tag itself.
- **This library**: Exposes the track as a **decimal string** (e.g. `"5"`). When writing from values like `"5/12"`, we keep **ID3v1 limits** (single-byte track, total from slash form ignored for storage).

- **Format**: Simple numeric string (e.g., `"5"`, `"12"`)
- **Parsing**: Returns as string
- **Examples**:
  - `"5"` → Track number: `"5"`
  - `"12"` → Track number: `"12"`

## ID3v2 Track Number Format

- **Spec / convention**: **ID3v2** defines **`TRCK`** as a numeric string; the informal description is **track number** and optionally **track number / count** separated by **`/`** (same pattern family as `TPOS`). The frame is UTF-16 or ISO-8859-1 depending on version; content is still “text that looks like `n` or `n/m`”.
- **This library**: We accept the **widest common text shapes** on read: **`/`** or **`-`** as separator, optional total (including empty after slash), leading zeros, and we reject only clearly invalid strings (see [edge cases](#reading-track-number)). **Write** uses the string you set so `n/m` is preserved for other ID3v2 readers.

- **Frame**: `TRCK`
- **Parsing**: Same [shared read rule](#shared-read-rule-track_number) as Vorbis/RIFF (full string returned when valid).
- **Examples**:
  - `"5/12"` → Track number: `"5/12"`
  - `"99/99"` → Track number: `"99/99"`
  - `"1"` → Track number: `"1"`
  - `"5-12"` → Track number: `"5-12"`

## Vorbis Track Number Format

- **Spec / convention**: **Vorbis comments** are **UTF-8 key/value** pairs; the spec does **not** mandate a grammar for `TRACKNUMBER`. De facto usage mirrors **ID3v2 `TRCK`**: plain **`n`** or **`n/m`**, often copied from MP3 taggers.
- **This library**: We apply the same [shared read rule](#shared-read-rule-track_number) as for `TRCK`, so **`n`**, **`n/m`**, **`n-m`**, trailing slash, etc. match one consistent rule across FLAC/Vorbis-tagged files and MP3.

- **Field**: `TRACKNUMBER`
- **Parsing**: Same [shared read rule](#shared-read-rule-track_number) as ID3v2/RIFF.
- **Examples**:
  - `"5"` → Track number: `"5"`
  - `"5/12"` → Track number: `"5/12"`
  - `"4/11"` → Track number: `"4/11"`
  - `"5-12"` → Track number: `"5-12"`

## RIFF Track Number Format

- **Spec / convention**: **RIFF INFO** (`LIST` + `INFO`) stores **length-prefixed** subchunks with **FourCC** keys. The **Microsoft / multimedia registry** associates **`IPRT`** with a **“part of set” / track** style label; **other tools** (e.g. some BWF workflows) use **`ITRK`** for “track number”. There is no single mandatory FourCC for “track” in all WAV software.
- **This library**: We read/write **`IPRT`** as **UTF-8 text** and apply the same [shared read rule](#shared-read-rule-track_number) as for `TRCK`/`TRACKNUMBER`, so **`n`**, **`n/m`**, **`n-m`** behave consistently. That covers a **wide** set of strings tools stuff into INFO. We do **not** map **`ITRK`** to `TRACK_NUMBER` today—files only tagged with `ITRK` need a different tool or a future mapping if we add it.

- **Native tag**: INFO subchunk **`IPRT`** (UTF-8 text), same [shared read rule](#shared-read-rule-track_number) as above.
- **Writing**: Supported via the unified API (`MetadataFormat.RIFF`); values are written to **`IPRT`**.
- **Interoperability**: Some tools use **`ITRK`** for track number. This library maps unified `TRACK_NUMBER` to **`IPRT`** only; files with `ITRK` but no `IPRT` will not expose `TRACK_NUMBER` through that mapping.

## Reading and Writing Track Number

### Reading Track Number

Edge cases for the shared pattern (all formats that use it):

- `"5/"` → Track number: `"5/"` (trailing slash allowed; empty total segment)
- `"/12"` → Track number: `None` (no leading track digits)
- `"abc/def"` → Track number: `None` (non-numeric)
- `""` → Track number: **`None`** when the field is absent or dropped; some **Vorbis** paths may surface an **explicit empty** stored value as **`""`** (see tests)
- `"5/12/15"` → Track number: `None` (more than one separator group)
- `"5-12"` → Track number: `"5-12"`
- `"01"` → Track number: `"01"` (leading zeros preserved)

### Writing Track Number

The library supports writing track numbers in various formats. For formats that support track totals, the full format is preserved. The following matrix shows what value is written for each input format:

| Input Value | ID3v1  | ID3v2     | Vorbis    | RIFF      |
| ----------- | ------ | --------- | --------- | --------- |
| `5` (int)   | `"5"`  | `"5"`     | `"5"`     | `"5"`     |
| `"5"` (str) | `"5"`  | `"5"`     | `"5"`     | `"5"`     |
| `"5/12"`    | `"5"`  | `"5/12"`  | `"5/12"`  | `"5/12"`  |
| `"99/99"`   | `"99"` | `"99/99"` | `"99/99"` | `"99/99"` |
| `"1"`       | `"1"`  | `"1"`     | `"1"`     | `"1"`     |

**Notes:**

- **ID3v1**: Only supports track numbers (1-255), extracts the track number from formats like `"5/12"` and ignores the total
- **ID3v2**: Full `track/total` in `TRCK` per convention
- **Vorbis**: Full string stored in `TRACKNUMBER`
- **RIFF**: Full string stored in `IPRT` (see interoperability note above)
