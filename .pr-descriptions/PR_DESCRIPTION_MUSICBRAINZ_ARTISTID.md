# PR Description: MusicBrainz Artist ID Support

## Description

This PR adds comprehensive support for MusicBrainz Artist ID metadata field across all supported audio formats (ID3v2, Vorbis, RIFF). MusicBrainz Artist IDs are unique UUIDs that identify artists in the MusicBrainz database, and this field supports multiple artist IDs per track.

**Key Changes/Improvements:**

- Added full read/write support for MusicBrainz Artist IDs in ID3v2 (MP3), Vorbis (FLAC), and RIFF (WAV) formats
- Added CLI integration with `--musicbrainz-artist-ids` option (can be specified multiple times)
- Implemented UUID format validation and normalization (supports both 36-char hyphenated and 32-char hex formats)
- Added comprehensive test coverage (27 integration tests, 14 unit tests)
- Fixed CLI bug where `--artist` argument wasn't processed when `--musicbrainz-artist-ids` was not provided
- Fixed ID3v2 reader to properly handle null-separated values in TXXX frames
- Added test helper support for MusicBrainz Artist IDs to ensure proper test isolation

## Related Issues

None

## Type of Change

- [x] New feature (non-breaking change which adds functionality)
- [x] Bug fix (non-breaking change which fixes an issue)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [x] Documentation update
- [ ] Code refactoring (no functional changes)
- [ ] Performance improvement
- [x] Test addition/update
- [ ] CI/CD or infrastructure change

## Pre-PR Checklist

### Code Quality

- [x] Removed commented-out code
- [x] No hardcoded credentials, API keys, or secrets
- [x] Ran pre-commit hooks: `pre-commit run --all-files`

### Tests

- [x] All tests pass: `pytest`
- [x] Coverage meets threshold (≥85%): `pytest --cov=audiometa --cov-report=term-missing --cov-fail-under=85`
- [x] New features have corresponding tests
- [x] Bug fixes include regression tests

### Documentation

- [x] Updated docstrings for new functions/classes (only when needed)
- [ ] Updated README if adding new features or changing behavior
- [ ] Updated CONTRIBUTING.md if changing development workflow
- [x] Added/updated type hints where appropriate
- [x] Updated CHANGELOG.md with changes

### Git Hygiene

- [x] Commit messages follow the [commit message convention](docs/COMMITTING.md)
- [x] No merge conflicts with target branch
- [x] Branch is up to date with target branch
- [x] No accidental commits (large files, secrets, personal configs)

## Breaking Changes

- [ ] This PR includes breaking changes
- [ ] Breaking changes are clearly documented below
- [ ] Migration path is provided (if applicable)

### Breaking Changes Description

N/A

## Testing Instructions

### How to Test

1. **Test API Usage:**

   ```python
   from audiometa import update_metadata, get_unified_metadata_field
   from audiometa.utils.unified_metadata_key import UnifiedMetadataKey

   # Write single MusicBrainz Artist ID
   update_metadata(
       "song.mp3",
       {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]}
   )

   # Write multiple MusicBrainz Artist IDs
   update_metadata(
       "song.mp3",
       {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: [
           "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",
           "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
       ]}
   )

   # Read MusicBrainz Artist IDs
   artist_ids = get_unified_metadata_field("song.mp3", UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
   print(artist_ids)  # ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6", "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"]
   ```

2. **Test CLI Usage:**

   ```bash
   # Write single MusicBrainz Artist ID
   python -m audiometa write song.mp3 --musicbrainz-artist-ids "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"

   # Write multiple MusicBrainz Artist IDs
   python -m audiometa write song.mp3 \
     --musicbrainz-artist-ids "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6" \
     --musicbrainz-artist-ids "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

   # Read MusicBrainz Artist IDs
   python -m audiometa read song.mp3 --format json
   ```

3. **Test Different Formats:**

   - Test with MP3 files (ID3v2 format)
   - Test with FLAC files (Vorbis format)
   - Test with WAV files (RIFF format)

4. **Test UUID Format Normalization:**

   - Test with 36-character hyphenated UUIDs (preferred format)
   - Test with 32-character hex UUIDs (should be normalized to hyphenated format)

5. **Test Multiple Values:**

   - Test writing multiple artist IDs
   - Test reading multiple artist IDs
   - Verify proper handling of separators (ID3v2.3) and null-separated values (ID3v2.4)

6. **Test CLI Bug Fix:**
   - Verify that `--artist` argument works independently of `--musicbrainz-artist-ids`
   - Test writing artists without MusicBrainz Artist IDs
   - Test writing both artists and MusicBrainz Artist IDs together

### Test Results

- All 27 integration tests pass
- All 14 unit tests pass
- All E2E tests pass (including comprehensive CLI read/write tests)
- Test coverage meets threshold (≥85%)

## Additional Context

**Format Support Matrix:**

| Format     | Support | Field / Key                                                   | Multiple |
| ---------- | ------- | ------------------------------------------------------------- | -------- |
| **ID3v2**  | ✅      | `TXXX` (description: `MusicBrainz Artist Id`)                 | ✅       |
| **Vorbis** | ✅      | `MUSICBRAINZ_ARTISTID` or `musicbrainz_artistid` (Vorbis key) | ✅       |
| **RIFF**   | ✅      | `MBAR` FourCC (native INFO)                                   | ✅       |
| **ID3v1**  | ❌      | —                                                             | ❌       |

**Implementation Details:**

- ID3v2: Uses TXXX frames with description "MusicBrainz Artist Id". Multiple values stored using separators (ID3v2.3) or null-separated values (ID3v2.4)
- Vorbis: Uses `MUSICBRAINZ_ARTISTID` key in Vorbis comments. Multiple comments with the same key are collected
- RIFF: Uses `MBAR` FourCC entries in INFO chunk. Multiple MBAR entries are collected

**Bug Fixes:**

1. **CLI Artists Handling**: Fixed bug where `--artist` argument was nested inside `if args.musicbrainz_artist_ids:` block, causing artists not to be set when MusicBrainz Artist IDs weren't provided
2. **ID3v2 Reader**: Fixed reading of null-separated values in TXXX frames for ID3v2.4 format by properly splitting null-separated values

**Test Helper Improvements:**

- Added `set_musicbrainz_artistids()` to `ID3v2MetadataSetter` for MP3 files
- Added `set_musicbrainz_artistids()` to `VorbisMetadataSetter` for FLAC files
- Added `create_multiple_mbar_fields()` to `ManualRIFFMetadataCreator` for WAV files

**Benefits:**

- Complete MusicBrainz Artist ID support across all major audio formats
- Consistent API and CLI interface for MusicBrainz metadata
- Proper UUID validation and normalization
- Comprehensive test coverage ensures reliability
- Full documentation with examples and format support matrix

## Checklist for Reviewers

- [ ] Code follows project conventions and style
- [ ] Logic is sound and well-structured
- [ ] Error handling is appropriate
- [ ] CI tests pass on all platforms and Python versions
- [ ] Test coverage is adequate for the changes
- [ ] Public API changes are documented
- [ ] Breaking changes are clearly marked and documented
- [ ] All review comments are addressed
- [ ] No unresolved discussions
