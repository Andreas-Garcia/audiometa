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

## Test Data Strategy

The test suite uses a **hybrid approach** for test data management, combining pre-created files with on-the-fly generation to optimize for both performance and flexibility.

### Pre-created Test Files (`../data/audio_files/`)

**176 pre-created audio files** covering specific scenarios and edge cases:

- **Edge cases**: Corrupted files, bad extensions, unusual filenames
- **Metadata combinations**: Files with specific metadata formats and values
- **Performance scenarios**: Different bitrates, durations, and file sizes
- **Regression tests**: Known problematic files that previously caused issues
- **Format validation**: Files with multiple metadata formats in the same file

**Benefits:**

- ⚡ **Fast**: Instant access, no script execution overhead
- 🎯 **Reliable**: Pre-tested and known to work correctly
- 📊 **Comprehensive**: Covers complex scenarios that would be difficult to generate
- 🔄 **Stable**: Consistent across test runs

### On-the-fly Generation (Script Helpers)

**Dynamic test file creation** using external command-line tools:

- **Writing tests**: When testing the application's metadata writing functionality
- **Dynamic scenarios**: Specific metadata combinations not available in pre-created files
- **Clean state**: Fresh files for each test run
- **Isolation**: Prevents test setup from depending on the code being tested

**How Script Helpers Work:**

The script helper strategy uses external command-line tools to set up test metadata:

1. **External Scripts**: Located in `../data/scripts/`, these are shell scripts that use standard audio metadata tools:

   - `set-id3v2-max-metadata.sh` - Uses `mid3v2` to set ID3v2 metadata
   - `set-vorbis-max-metadata.sh` - Uses `metaflac` to set Vorbis metadata
   - `set-riff-max-metadata.sh` - Uses `bwfmetaedit` to set RIFF metadata
   - `set-id3v1-max-metadata.sh` - Uses `id3v2 --id3v1-only` to set ID3v1 metadata
   - `remove-id3.py` - Removes ID3 metadata
   - `remove-riff.py` - Removes RIFF metadata

**⚠️ Important: ID3v1 Metadata Creation Limitations**

**`mid3v2` cannot write ID3v1 metadata** - it can only delete it. For ID3v1 metadata creation, you must use:

- `id3v2 --id3v1-only` (external tool)
- Our library's `update_file_metadata()` with `MetadataFormat.ID3V1`

**For tests requiring ID3v1 metadata:**

- Use `TempFileWithMetadata(metadata, "id3v1")` (recommended - clean and simple)
- Use `ScriptHelper.set_id3v1_max_metadata()` (alternative - uses external script)
- Use `update_file_metadata()` with `MetadataFormat.ID3V1` (alternative)
- **Do NOT use `TempFileWithMetadata` with "mp3" for ID3v1** - it uses `mid3v2` which cannot write ID3v1

**Example - Correct way to create ID3v1 metadata in tests:**

```python
# ✅ CORRECT: Use TempFileWithMetadata with "id3v1" format type
with TempFileWithMetadata({
    "title": "Test Title",
    "artist": "Test Artist",
    "album": "Test Album",
    "year": "2023",
    "genre": "Rock"
}, "id3v1") as test_file:
    # Now test your functionality...

# ✅ ALTERNATIVE: Use ScriptHelper with external script
from audiometa.test.tests.test_script_helpers import ScriptHelper

with TempFileWithMetadata({}, "mp3") as test_file:
    script_helper = ScriptHelper()
    script_helper.set_id3v1_max_metadata(test_file.path)

# ✅ ALTERNATIVE: Use library's update_file_metadata
with TempFileWithMetadata({}, "mp3") as test_file:
    id3v1_metadata = {
        UnifiedMetadataKey.TITLE: "Test Title",
        UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
        UnifiedMetadataKey.ALBUM_NAME: "Test Album"
    }
    update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)

# ❌ WRONG: This won't create ID3v1 metadata
with TempFileWithMetadata({"title": "Test"}, "mp3") as test_file:
    # This creates ID3v2 metadata, not ID3v1!
```

2. **ScriptHelper Class**: Provides a Python interface to these external scripts:

   ```python
   from audiometa.test.tests.test_script_helpers import ScriptHelper

   helper = ScriptHelper()
   helper.set_id3v2_max_metadata(test_file)
   helper.set_vorbis_max_metadata(test_file)
   ```

3. **Test File Management**: Safe ways to create temporary test files:
   - `TempFileWithMetadata` - **RECOMMENDED**: Context manager for automatic cleanup
   - **Supported format types**: `'mp3'`, `'id3v1'`, `'flac'`, `'wav'`
   - **For ID3v1 metadata**: Use `TempFileWithMetadata(metadata, "id3v1")`

**Benefits:**

- 🔧 **Flexible**: Can create any metadata scenario on demand
- 🧪 **Isolated**: Test setup doesn't depend on the code being tested
- 🆕 **Fresh**: Clean state for each test
- 🎛️ **Configurable**: Easy to modify test scenarios
- **Reliability**: Uses proven external tools for metadata setup
- **Maintainability**: Clear separation between test setup and test logic

**⚠️ Important: Test File Management**

**NEVER use `create_test_file_with_metadata()` directly in tests!** This function has been moved to `_internal_test_helpers.py` to prevent direct usage. It causes test pollution because files persist after tests complete.

**✅ Correct usage:**

```python
def test_something():
    with TempFileWithMetadata(metadata, "mp3") as test_file:
        # ... test code ...
    # File automatically cleaned up!
```

**❌ Wrong usage:**

```python
def test_something():
    test_file = create_test_file_with_metadata(metadata, "mp3")
    # ... test code ...
    # File persists and causes test pollution!
```

### Script Helper Approach

The test suite uses a **streamlined script helper approach**:

```python
with TempFileWithMetadata(
    basic_metadata,     # Metadata to set
    "mp3"               # Format type
) as test_file:
    # Use test_file for testing
    # File is automatically cleaned up
```

**Benefits of the streamlined approach:**

- **Cleaner API**: No need for source file parameters
- **Simpler tests**: Fewer fixture dependencies
- **Better encapsulation**: Helper handles file creation internally
- **Consistent starting state**: Always starts with clean files
- **Easier maintenance**: Less complex test setup

### Temporary Files (Fixtures)

**Empty audio files** created during test execution:

- **Basic functionality**: Simple read/write operations
- **Error handling**: Testing with empty or invalid files
- **Clean slate**: Starting point for dynamic test scenarios

### When to Use Each Approach

| Scenario                      | Approach          | Reason                                                                        |
| ----------------------------- | ----------------- | ----------------------------------------------------------------------------- |
| Reading existing metadata     | Pre-created files | Fast, reliable, comprehensive coverage                                        |
| Testing writing functionality | Script helpers    | Set up test data with external tools, then test app's writing by reading back |
| Edge case testing             | Pre-created files | Complex scenarios already prepared                                            |
| Dynamic test scenarios        | Script helpers    | Flexible, on-demand creation                                                  |
| Basic functionality           | Temporary files   | Simple, clean, fast                                                           |
| Regression testing            | Pre-created files | Known problematic files                                                       |

### Examples for Each Scenario

#### Reading existing metadata (Pre-created files)

```python
def test_read_metadata_from_pre_created_file(sample_mp3_file):
    """Test reading metadata from a pre-created file with known metadata."""
    audio_file = AudioFile(sample_mp3_file)
    metadata = audio_file.read_metadata()
    assert metadata.title == "Sample Title"
    assert metadata.artist == "Sample Artist"
```

#### Testing writing functionality (Script helpers)

```python
def test_write_metadata_using_script_helper():
    """Test writing metadata by setting up with external tools, then testing our app."""
    # Use script helper to set up test data
    with TempFileWithMetadata(
        {"title": "Original Title", "artist": "Original Artist"},
        "mp3"
    ) as test_file:
        # Now test our application's writing functionality
        audio_file = AudioFile(test_file)
        audio_file.write_metadata({"title": "New Title"})

        # Verify by reading back
        metadata = audio_file.read_metadata()
        assert metadata.title == "New Title"
```

#### Edge case testing (Pre-created files)

```python
def test_corrupted_metadata_handling(corrupted_mp3_file):
    """Test handling of corrupted metadata using pre-created problematic file."""
    audio_file = AudioFile(corrupted_mp3_file)
    # Test that our app gracefully handles corrupted metadata
    with pytest.raises(CorruptedMetadataError):
        audio_file.read_metadata()
```

#### Dynamic test scenarios (Script helpers)

```python
def test_specific_metadata_combination():
    """Test a specific metadata scenario not available in pre-created files."""
    # Create specific metadata combination on demand
    with TempFileWithMetadata(
        {
            "title": "Custom Title",
            "artist": "Custom Artist",
            "genre": "Custom Genre"
        },
        "mp3"
    ) as test_file:
        audio_file = AudioFile(test_file)
        metadata = audio_file.read_metadata()
        assert metadata.genre == "Custom Genre"
```

#### Basic functionality (Temporary files)

```python
def test_basic_read_write_operations(empty_mp3_file):
    """Test basic functionality with a simple temporary file."""
    audio_file = AudioFile(empty_mp3_file)

    # Test writing
    audio_file.write_metadata({"title": "Test Title"})

    # Test reading
    metadata = audio_file.read_metadata()
    assert metadata.title == "Test Title"
```

#### Regression testing (Pre-created files)

```python
def test_regression_issue_123(problematic_wav_file):
    """Test a specific regression that was fixed in issue #123."""
    # This file previously caused a crash
    audio_file = AudioFile(problematic_wav_file)
    metadata = audio_file.read_metadata()
    # Verify the fix works
    assert metadata is not None
```

### File Organization

```
../data/audio_files/           # Pre-created test files
├── sample.mp3                 # Basic sample files
├── metadata=*.mp3            # Metadata scenarios
├── rating_*.wav              # Rating test cases
├── artists=*.mp3             # Artist metadata tests
└── duration=*.flac           # Duration test cases

../data/scripts/               # External scripts for generation
├── set-id3v2-max-metadata.sh
├── set-vorbis-max-metadata.sh
└── remove-*.py
```

All test files are shared across test categories through fixtures defined in `conftest.py`.

## Fixtures

All test fixtures are defined in `conftest.py` and are available to all test files regardless of their location in the subfolder structure.
