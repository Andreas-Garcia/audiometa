# Mixed Format Deletion Tests

This directory contains comprehensive tests for deletion of metadata from audio files that contain multiple metadata formats simultaneously.

## Test Structure

### Format-Specific Tests

- **`test_wav_mixed_formats_deletion.py`** - Tests for WAV files with both ID3v2 and RIFF metadata
- **`test_mp3_mixed_formats_deletion.py`** - Tests for MP3 files with both ID3v1 and ID3v2 metadata  
- **`test_flac_mixed_formats_deletion.py`** - Tests for FLAC files with both Vorbis and ID3v2 metadata

### Comprehensive Tests

- **`test_comprehensive_mixed_formats_deletion.py`** - Cross-format tests covering all scenarios
- **`test_wav_sample_file_deletion.py`** - Tests using real sample files with mixed formats

## Test Scenarios

### WAV Files (ID3v2 + RIFF)
- ✅ Both formats can coexist in the same file
- ✅ `delete_all_metadata` removes both ID3v2 and RIFF metadata
- ✅ Works regardless of which format is added first
- ✅ Uses real sample files for validation

### MP3 Files (ID3v1 + ID3v2)
- ✅ ID3v2 metadata is fully removable
- ⚠️ ID3v1 metadata is read-only and cannot be removed (by design)
- ✅ `delete_all_metadata` removes ID3v2 while preserving ID3v1
- ✅ Tests handle the read-only nature of ID3v1 appropriately

### FLAC Files (Vorbis + ID3v2)
- ✅ Both formats can coexist in the same file
- ✅ `delete_all_metadata` removes both Vorbis and ID3v2 metadata
- ✅ Works regardless of which format is added first
- ✅ Uses proper field names (e.g., `artists_names` instead of `artist`)

## Key Features Tested

1. **Coexistence**: Multiple metadata formats can exist in the same file
2. **Deletion Order**: Tests both possible orders of metadata addition
3. **Format Limitations**: Respects read-only formats (ID3v1)
4. **Real Files**: Uses actual sample files with mixed formats
5. **Comprehensive Coverage**: Tests all supported audio formats and metadata combinations

## Important Notes

- **ID3v1 is read-only**: Cannot be written or deleted programmatically
- **Field Mapping**: Different formats use different field names (e.g., `artist` vs `artists_names`)
- **Format Priority**: Each file type has a native format that takes precedence
- **Deletion Behavior**: `delete_all_metadata` removes all writable formats, skips read-only ones

## Running Tests

```bash
# Run all mixed format tests
pytest audiometa/test/tests/integration/delete_all_metadata/header_deletion/mixed_format/ -v

# Run specific format tests
pytest audiometa/test/tests/integration/delete_all_metadata/header_deletion/mixed_format/test_wav_mixed_formats_deletion.py -v
pytest audiometa/test/tests/integration/delete_all_metadata/header_deletion/mixed_format/test_mp3_mixed_formats_deletion.py -v
pytest audiometa/test/tests/integration/delete_all_metadata/header_deletion/mixed_format/test_flac_mixed_formats_deletion.py -v
```
