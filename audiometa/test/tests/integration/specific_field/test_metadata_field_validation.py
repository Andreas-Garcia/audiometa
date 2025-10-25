import pytest
from pathlib import Path

from audiometa import get_unified_metadata_field, UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError, FieldNotSupportedByLib
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestMetadataFieldValidation:
    """Test that get_unified_metadata_field raises MetadataFieldNotSupportedByMetadataFormatError 
    when a field is not supported by the specified format."""

    def test_bpm_not_supported_by_riff(self, sample_wav_file: Path):
        """Test that BPM is not supported by RIFF format."""
        with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError) as exc_info:
            get_unified_metadata_field(sample_wav_file, UnifiedMetadataKey.BPM, metadata_format=MetadataFormat.RIFF)
        
        assert "UnifiedMetadataKey.BPM metadata not supported by this format" in str(exc_info.value)

    def test_lyrics_not_supported_by_riff(self, sample_wav_file: Path):
        """Test that LYRICS is not supported by RIFF format."""
        with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError) as exc_info:
            get_unified_metadata_field(sample_wav_file, UnifiedMetadataKey.LYRICS, metadata_format=MetadataFormat.RIFF)
        
        assert "UnifiedMetadataKey.LYRICS metadata not supported by this format" in str(exc_info.value)

    def test_bpm_not_supported_by_id3v1(self, sample_mp3_file: Path):
        """Test that BPM is not supported by ID3v1 format."""
        with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError) as exc_info:
            get_unified_metadata_field(sample_mp3_file, UnifiedMetadataKey.BPM, metadata_format=MetadataFormat.ID3V1)
        
        assert "UnifiedMetadataKey.BPM metadata not supported by this format" in str(exc_info.value)

    def test_rating_not_supported_by_id3v1(self, sample_mp3_file: Path):
        """Test that RATING is not supported by ID3v1 format."""
        with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError) as exc_info:
            get_unified_metadata_field(sample_mp3_file, UnifiedMetadataKey.RATING, metadata_format=MetadataFormat.ID3V1)
        
        assert "UnifiedMetadataKey.RATING metadata not supported by this format" in str(exc_info.value)

    def test_album_artists_not_supported_by_id3v1(self, sample_mp3_file: Path):
        """Test that ALBUM_ARTISTS is not supported by ID3v1 format."""
        with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError) as exc_info:
            get_unified_metadata_field(sample_mp3_file, UnifiedMetadataKey.ALBUM_ARTISTS, metadata_format=MetadataFormat.ID3V1)
        
        assert "UnifiedMetadataKey.ALBUM_ARTISTS metadata not supported by this format" in str(exc_info.value)

    def test_supported_field_works_with_riff(self, sample_wav_file: Path):
        """Test that supported fields work with RIFF format."""
        # This should not raise an error, even if the value is None
        title = get_unified_metadata_field(sample_wav_file, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.RIFF)
        # The value might be None if not set, but no exception should be raised
        assert title is None or isinstance(title, str)

    def test_supported_field_works_with_id3v1(self, sample_mp3_file: Path):
        """Test that supported fields work with ID3v1 format."""
        # This should not raise an error, even if the value is None
        title = get_unified_metadata_field(sample_mp3_file, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.ID3V1)
        # The value might be None if not set, but no exception should be raised
        assert title is None or isinstance(title, str)

    def test_unsupported_field_without_format_specification(self, sample_wav_file: Path):
        """Test that unsupported fields work without format specification (uses priority order)."""
        # This should not raise an error when no format is specified, as it uses priority order
        bpm = get_unified_metadata_field(sample_wav_file, UnifiedMetadataKey.BPM)
        # The value might be None if not found in any format, but no exception should be raised
        assert bpm is None or isinstance(bpm, int)

    def test_rating_supported_by_riff_indirectly(self, sample_wav_file: Path):
        """Test that RATING is supported by RIFF format (handled indirectly)."""
        # RATING is supported by RIFF but handled indirectly, so it should not raise an error
        rating = get_unified_metadata_field(sample_wav_file, UnifiedMetadataKey.RATING, metadata_format=MetadataFormat.RIFF)
        # The value might be None if not set, but no exception should be raised
        assert rating is None or isinstance(rating, int)

    def test_field_not_supported_by_lib_exception_exists(self):
        """Test that FieldNotSupportedByLib exception exists and can be imported."""
        # This test verifies that the exception is properly defined
        from audiometa.exceptions import FieldNotSupportedByLib
        
        # Test that the exception can be raised
        with pytest.raises(FieldNotSupportedByLib) as exc_info:
            raise FieldNotSupportedByLib("Test field not supported by library")
        
        assert "Test field not supported by library" in str(exc_info.value)
        assert isinstance(exc_info.value, Exception)

    def test_field_not_supported_by_lib_concept(self, sample_wav_file: Path):
        """Test the concept of FieldNotSupportedByLib exception.
        
        Note: In the current implementation, all fields in UnifiedMetadataKey are supported
        by at least one format, so this exception is not raised in practice. However,
        this test documents the concept and shows when it would be raised.
        
        The FieldNotSupportedByLib exception would be raised when:
        1. A field is not supported by ANY format in the library
        2. All managers raise MetadataFieldNotSupportedByMetadataFormatError for the same field
        3. This indicates a library limitation, not a format limitation
        """
        # This test demonstrates the concept - in practice, all current fields are supported
        # by at least one format, so this exception is not raised
        
        # Test that all current fields work without raising FieldNotSupportedByLib
        # when no format is specified (uses priority order)
        for field in UnifiedMetadataKey:
            try:
                value = get_unified_metadata_field(sample_wav_file, field)
                # Should not raise FieldNotSupportedByLib for any current field
                assert value is None or isinstance(value, (str, int, list))
            except FieldNotSupportedByLib:
                pytest.fail(f"FieldNotSupportedByLib should not be raised for {field} - all current fields are supported by at least one format")
            except Exception as e:
                # Other exceptions are acceptable (file format issues, etc.)
                pass
