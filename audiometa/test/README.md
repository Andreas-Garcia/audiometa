# Audiometa-Python Tests

This directory contains comprehensive tests for the audiometa-python library, focusing on audio metadata reading, writing, and processing functionality.

## Test Structure

```
test/
├── conftest.py              # Test configuration and fixtures
├── test_audio_file.py       # Tests for AudioFile class
├── test_metadata_reading.py # Tests for metadata reading functions
├── test_metadata_writing.py # Tests for metadata writing functions
├── test_metadata_managers.py # Tests for metadata manager classes
├── test_exceptions.py       # Tests for exception classes
├── test_main_functions.py   # Tests for main module functions
├── test_integration.py      # Integration tests
├── test_basic_metadata.py   # Tests for basic metadata fields
├── test_technical_metadata.py # Tests for technical metadata fields
├── test_additional_metadata.py # Tests for additional metadata fields
├── test_advanced_metadata.py # Tests for advanced metadata fields
├── test_rating_scenarios.py # Tests for rating scenarios
└── data/
    └── audio_files/         # Test audio files
        ├── sample.mp3       # Sample MP3 file
        ├── sample.flac      # Sample FLAC file
        ├── sample.wav       # Sample WAV file
        ├── sample.ogg       # Sample OGG file
        └── create_test_files.py # Script to create test files
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
pytest test_audio_file.py
pytest test_metadata_reading.py
pytest test_metadata_writing.py
pytest test_basic_metadata.py
pytest test_technical_metadata.py
pytest test_additional_metadata.py
pytest test_advanced_metadata.py
pytest test_rating_scenarios.py
```

### Run Metadata Category Tests

```bash
# Run all basic metadata tests
pytest test_basic_metadata.py

# Run all technical metadata tests
pytest test_technical_metadata.py

# Run all additional metadata tests
pytest test_additional_metadata.py

# Run all advanced metadata tests
pytest test_advanced_metadata.py

# Run all rating scenario tests
pytest test_rating_scenarios.py
```

### Run Tests with Coverage

```bash
pytest --cov=audiometa
```

### Run Only Unit Tests

```bash
pytest -m "not integration"
```

### Run Only Integration Tests

```bash
pytest -m integration
```

## Test Categories

### Unit Tests

- **AudioFile Tests**: Test the AudioFile class functionality
- **Metadata Reading Tests**: Test reading metadata from various formats
- **Metadata Writing Tests**: Test writing metadata to various formats
- **Manager Tests**: Test individual metadata manager classes
- **Exception Tests**: Test exception handling and error conditions
- **Main Function Tests**: Test utility functions

### Comprehensive Metadata Tests

- **Basic Metadata Tests**: Test core metadata fields (title, artist, album, genre, rating)
- **Technical Metadata Tests**: Test technical fields (release date, track number, BPM, language)
- **Additional Metadata Tests**: Test extended fields (composer, publisher, copyright, lyrics, etc.)
- **Advanced Metadata Tests**: Test advanced fields (cover art, MusicBrainz, ReplayGain, etc.)
- **Rating Scenario Tests**: Test rating handling across formats and normalizations

### Integration Tests

- **Complete Workflow Tests**: Test end-to-end metadata operations
- **Cross-Format Tests**: Test metadata operations across different formats
- **Error Handling Tests**: Test error handling in complete workflows

## Test Files

The test suite includes sample audio files in multiple formats:

- **MP3**: ID3v1 and ID3v2 metadata support
- **FLAC**: Vorbis metadata support with MD5 validation
- **WAV**: RIFF metadata support
- **OGG**: Vorbis metadata support

## Dependencies

The tests require:

- `pytest` for test framework
- `pytest-cov` for coverage reporting (optional)
- `ffmpeg` for creating test audio files
- `mutagen` for audio metadata handling

## Test Data

Test audio files are automatically created using ffmpeg when running the test suite. The files contain silent audio content suitable for metadata testing without requiring large file downloads.

## Comprehensive Metadata Coverage

The test suite provides extensive coverage of all 50+ metadata fields supported by audiometa-python:

### Basic Metadata Fields

- **Title**: Song title across all formats
- **Artists Names**: Single and multiple artist support
- **Album Name**: Album information
- **Album Artists Names**: Album artist information
- **Genre Name**: Genre classification
- **Rating**: Rating support with different normalizations (0-100, 0-255)

### Technical Metadata Fields

- **Release Date**: Date information in various formats
- **Track Number**: Track numbering (1-999)
- **BPM**: Beats per minute (1-999)
- **Language**: Language codes (3-character)

### Additional Metadata Fields

- **Composer**: Composer information
- **Publisher**: Publisher information
- **Copyright**: Copyright notices
- **Lyrics**: Song lyrics with multiline support
- **Comment**: Comments and notes
- **Encoder**: Encoder information
- **URL**: Web links
- **ISRC**: International Standard Recording Code
- **Mood**: Mood classification
- **Key**: Musical key information

### Advanced Metadata Fields

- **Cover Art**: Binary image data
- **Compilation**: Compilation flag
- **Media Type**: Media classification
- **File Owner**: File ownership
- **Recording Date**: Recording date information
- **Encoder Settings**: Detailed encoder settings
- **ReplayGain**: ReplayGain information
- **MusicBrainz ID**: MusicBrainz identifiers
- **Original Date**: Original release date
- **Remixer**: Remixer information
- **Conductor**: Conductor information

### Format-Specific Support

- **MP3**: Full ID3v1 and ID3v2 support
- **FLAC**: Full Vorbis metadata support
- **WAV**: RIFF metadata support (limited fields)
- **OGG**: Vorbis metadata support

## Coverage

The test suite aims for comprehensive coverage of:

- All supported audio formats (MP3, FLAC, WAV, OGG)
- All 50+ metadata fields and operations
- Format-specific field support and limitations
- Rating normalization scenarios (0-100, 0-255)
- Error conditions and exception handling
- Edge cases and boundary conditions
- Integration scenarios
- Cross-format compatibility
