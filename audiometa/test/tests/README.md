# Test Organization

This directory contains the test suite for audiometa-python, organized using the standard unit/integration/e2e testing pattern.

## Test Structure

### Unit Tests (`unit/`)

Tests for individual components and classes in isolation. These are fast, focused tests that verify individual functions and methods work correctly.

- **Marker**: `@pytest.mark.unit`
- **Speed**: Very fast (milliseconds)
- **Dependencies**: Mocked/stubbed
- **Files**:
  - `test_exceptions.py` - Exception class tests
  - `managers/` - Individual metadata manager tests
    - `test_id3v1_manager.py` - ID3v1 metadata manager tests
    - `test_id3v2_manager.py` - ID3v2 metadata manager tests
    - `test_vorbis_manager.py` - Vorbis metadata manager tests
    - `test_riff_manager.py` - RIFF metadata manager tests
  - `main_functions/` - Individual function tests
    - `test_bitrate_functions.py`
    - `test_duration_functions.py`
    - `test_error_handling.py`
    - `test_flac_md5_functions.py`
    - `test_id3_metadata_functions.py`

### Integration Tests (`integration/`)

Tests that verify how multiple components work together with real dependencies. These test component interactions and data flow.

- **Marker**: `@pytest.mark.integration`
- **Speed**: Medium (seconds)
- **Dependencies**: Real but limited scope
- **Files**:
  - `test_integration.py` - Component interaction tests
  - `test_comprehensive_reading.py` - Metadata reading from real files
  - `test_comprehensive_writing.py` - Metadata writing to real files
  - `test_format_specific.py` - Format-specific scenarios
  - `test_metadata_reading.py` - Metadata reading workflows
  - `test_metadata_writing.py` - Metadata writing workflows
  - `test_metadata_types.py` - Metadata type handling
  - `test_audio_file.py` - AudioFile class integration
  - `basic_tags/` - Basic metadata field tests
    - `test_album.py`, `test_artists.py`, `test_basic_metadata.py`
    - `test_genre.py`, `test_rating.py`, `test_title.py`
  - `additional_tags/` - Additional metadata field tests
    - `test_additional_metadata.py`, `test_composer.py`, `test_copyright.py`
    - `test_lyrics.py`, `test_publisher.py`
  - `technical_tags/` - Technical metadata field tests
    - `test_bpm.py`, `test_language.py`, `test_release_date.py`
    - `test_technical_metadata.py`, `test_track_number.py`
  - `test_advanced_metadata.py` - Advanced metadata fields (cover art, etc.)

### End-to-End Tests (`e2e/`)

Tests that verify complete user workflows from start to finish. These simulate real user scenarios and test the entire system.

- **Marker**: `@pytest.mark.e2e`
- **Speed**: Slow (minutes)
- **Dependencies**: Full system with all real dependencies
- **Files**:
  - `test_complete_workflows.py` - Complete metadata editing workflows
  - `test_user_scenarios.py` - Real-world user scenarios

## Running Tests

### Run all tests

```bash
pytest
```

### Run tests by category

```bash
# Unit tests only (fast)
pytest -m unit

# Integration tests only (medium speed)
pytest -m integration

# End-to-end tests only (slow)
pytest -m e2e
```

### Run tests by folder

```bash
# Unit tests
pytest audiometa/test/tests/unit/

# Integration tests
pytest audiometa/test/tests/integration/

# End-to-end tests
pytest audiometa/test/tests/e2e/
```

### Combine markers

```bash
# Run unit and integration tests (skip slow e2e)
pytest -m "unit or integration"

# Run everything except e2e tests
pytest -m "not e2e"

# Run only fast tests
pytest -m unit
```

## Test Data

Test audio files are located in `../data/audio_files/` (separate from the test directory) and are shared across all test categories through fixtures defined in `conftest.py`.

## Fixtures

All test fixtures are defined in `conftest.py` and are available to all test files regardless of their location in the subfolder structure.
