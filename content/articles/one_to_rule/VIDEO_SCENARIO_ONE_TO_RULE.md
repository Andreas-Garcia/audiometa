# Video scenario: AudioMeta — One audio metadata manager to rule them all

Narrative only. Implementation later.

---

## Structure

Five parts: **intro** (title + staggered subtitles), then **Before / Now** for **reading** (2 panels: ID3v2, RIFF), then **Before / Now** for **writing** (2 panels: ID3v1, Vorbis).

---

## Part 1: Intro

- **Title (appears first):**
  **AudioMeta - One audio metadata manager to rule them all**

- **Subtitle 1 (appears a bit later than title):**
  **Main formats: MP3, WAV, FLAC**

- **Subtitle 2 (appears a bit later than subtitle 1):**
  **Main metadata formats: ID3v1, ID3v2, Vorbis, RIFF**

---

## Part 2: Before — Reading (ID3v2, RIFF)

- **Page title:**
  **Before: Reading (mid3v2, ffprobe)**

- **Content:** 2 panels side by side: **ID3v2** (mid3v2) | **RIFF** (ffprobe). Each cell is a short GIF showing metadata being read with the format-specific tool.

---

## Part 3: Now — Reading with AudioMeta (ID3v2, RIFF)

- **Page title:**
  **Now: Reading with AudioMeta (ID3v2, RIFF)**

- **Content:** 2 panels side by side: **ID3v2** | **RIFF**. Each cell shows `audiometa read` (one tool for all).

---

## Part 4: Before — Writing (ID3v1, Vorbis)

- **Page title:**
  **Before: Writing (ID3v1, Vorbis)**

- **Content:** 2 panels side by side: **ID3v1** | **Vorbis**. Each cell is a short GIF showing metadata being written with the format-specific tool (e.g. mid3v2, metaflac).

---

## Part 5: Now — Writing with AudioMeta (ID3v1, Vorbis)

- **Page title:**
  **Now: Writing with AudioMeta (ID3v1, Vorbis)**

- **Content:** 2 panels side by side: **ID3v1** | **Vorbis**. Each cell shows `audiometa write` (one tool for all).

---

## Constraint

All four metadata formats (**ID3v1**, **ID3v2**, **Vorbis**, **RIFF**) and the three main audio formats (MP3, WAV, FLAC) are named in the intro. Reading pages use 2 panels (ID3v2, RIFF); writing pages use 2 panels (ID3v1, Vorbis) for direct before/now comparison.
