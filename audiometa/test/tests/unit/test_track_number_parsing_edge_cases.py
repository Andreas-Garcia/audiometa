"""Unit tests for track number parsing edge cases."""

import pytest
from pathlib import Path
from unittest.mock import Mock

from audiometa.manager.MetadataManager import MetadataManager
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.unit
class TestTrackNumberParsingEdgeCases:
    """Test cases for track number parsing edge cases in MetadataManager."""

    def test_track_number_parsing_standard_id3v2_format(self):
        """Test standard ID3v2 track/total format parsing."""
        # Mock the MetadataManager to test the parsing logic
        manager = self._create_mock_manager()
        
        # Test standard ID3v2 format
        result = self._test_track_parsing(manager, "5/12")
        assert result == 5
        
        result = self._test_track_parsing(manager, "99/99")
        assert result == 99
        
        result = self._test_track_parsing(manager, "1/10")
        assert result == 1

    def test_track_number_parsing_simple_format(self):
        """Test simple track number format parsing."""
        manager = self._create_mock_manager()
        
        # Test simple format
        result = self._test_track_parsing(manager, "5")
        assert result == 5
        
        result = self._test_track_parsing(manager, "99")
        assert result == 99
        
        result = self._test_track_parsing(manager, "1")
        assert result == 1

    def test_track_number_parsing_edge_cases(self):
        """Test various edge cases for track number parsing."""
        manager = self._create_mock_manager()
        
        # Test edge cases
        test_cases = [
            ("5/", 5),           # Trailing slash
            ("/12", None),       # Leading slash, no track number
            ("abc/def", None),   # Non-numeric values
            ("", None),          # Empty string
            (None, None),        # None value
            ("5/", 5),           # Trailing slash
            ("/10", None),       # Leading slash
            ("abc", None),       # Non-numeric simple
            ("", None),          # Empty string
        ]
        
        for input_value, expected in test_cases:
            result = self._test_track_parsing(manager, input_value)
            assert result == expected, f"Failed for input '{input_value}': expected {expected}, got {result}"

    def test_track_number_parsing_whitespace_handling(self):
        """Test whitespace handling in track number parsing."""
        manager = self._create_mock_manager()
        
        # Test whitespace handling
        test_cases = [
            (" 5/12 ", 5),       # Whitespace around track/total
            ("5 /12", 5),        # Space before slash
            ("5/ 12", 5),        # Space after slash
            (" 5 ", 5),          # Whitespace around simple number
            (" 5/ ", 5),         # Whitespace around track with trailing slash
        ]
        
        for input_value, expected in test_cases:
            result = self._test_track_parsing(manager, input_value)
            assert result == expected, f"Failed for input '{input_value}': expected {expected}, got {result}"

    def test_track_number_parsing_numeric_edge_cases(self):
        """Test numeric edge cases for track number parsing."""
        manager = self._create_mock_manager()
        
        # Test numeric edge cases
        test_cases = [
            ("0/10", 0),         # Zero track number
            ("10/0", 10),        # Zero total tracks
            ("0", 0),            # Zero simple
            ("00/10", 0),        # Leading zeros
            ("05/12", 5),        # Leading zeros in track
            ("5/012", 5),        # Leading zeros in total
        ]
        
        for input_value, expected in test_cases:
            result = self._test_track_parsing(manager, input_value)
            assert result == expected, f"Failed for input '{input_value}': expected {expected}, got {result}"

    def test_track_number_parsing_invalid_formats(self):
        """Test invalid format handling."""
        manager = self._create_mock_manager()
        
        # Test invalid formats - these should raise exceptions or return None
        test_cases = [
            ("5-12", None),      # Different separator (no slash)
            ("5.12", None),      # Decimal separator (no slash)
            ("5,12", None),      # Comma separator (no slash)
            ("5:12", None),      # Colon separator (no slash)
            ("5 12", None),      # Space separator (no slash)
        ]
        
        for input_value, expected in test_cases:
            result = self._test_track_parsing(manager, input_value)
            assert result == expected, f"Failed for input '{input_value}': expected {expected}, got {result}"

    def test_track_number_parsing_multiple_slashes(self):
        """Test handling of multiple slashes (takes first part)."""
        manager = self._create_mock_manager()
        
        # Test multiple slashes - should take first part
        test_cases = [
            ("5/12/15", 5),      # Multiple slashes - takes first part
            ("1/2/3/4", 1),      # Multiple slashes - takes first part
            ("10/20/30/40", 10), # Multiple slashes - takes first part
        ]
        
        for input_value, expected in test_cases:
            result = self._test_track_parsing(manager, input_value)
            assert result == expected, f"Failed for input '{input_value}': expected {expected}, got {result}"

    def test_track_number_parsing_large_numbers(self):
        """Test large number handling."""
        manager = self._create_mock_manager()
        
        # Test large numbers
        test_cases = [
            ("999/999", 999),    # Large numbers
            ("1000/1000", 1000), # Very large numbers
            ("999", 999),        # Large simple number
        ]
        
        for input_value, expected in test_cases:
            result = self._test_track_parsing(manager, input_value)
            assert result == expected, f"Failed for input '{input_value}': expected {expected}, got {result}"

    def test_track_number_parsing_unicode_and_special_chars(self):
        """Test unicode and special character handling."""
        manager = self._create_mock_manager()
        
        # Test unicode and special characters
        test_cases = [
            ("５/１２", 5),       # Full-width numbers (Python considers them valid digits)
            ("5/12🎵", 5),        # Emoji after slash - takes first part
            ("5/12★", 5),        # Special characters after slash - takes first part
            ("5/12\n", 5),       # Newline after slash - takes first part
            ("5/12\t", 5),       # Tab after slash - takes first part
            ("🎵/12", None),     # Emoji before slash - not numeric
            ("★/12", None),      # Special chars before slash - not numeric
        ]
        
        for input_value, expected in test_cases:
            result = self._test_track_parsing(manager, input_value)
            assert result == expected, f"Failed for input '{input_value}': expected {expected}, got {result}"

    def _create_mock_manager(self):
        """Create a mock MetadataManager for testing."""
        # Create a mock AudioFile
        mock_audio_file = Mock()
        mock_audio_file.get_file_path_or_object.return_value = "test.mp3"
        
        # Create MetadataManager with minimal setup
        manager = MetadataManager(
            audio_file=mock_audio_file,
            metadata_keys_direct_map_read={UnifiedMetadataKey.TRACK_NUMBER: "TRCK"},
            metadata_keys_direct_map_write={UnifiedMetadataKey.TRACK_NUMBER: "TRCK"}
        )
        
        return manager

    def _test_track_parsing(self, manager, value):
        """Test track number parsing with a given value."""
        # Mock the raw_clean_metadata to simulate different track number values
        manager.raw_clean_metadata = {"TRCK": [value] if value is not None else []}
        
        try:
            return manager.get_app_specific_metadata(UnifiedMetadataKey.TRACK_NUMBER)
        except Exception:
            return None

    def test_track_number_parsing_integration_with_real_files(self, sample_mp3_file: Path):
        """Test track number parsing with real files to ensure integration works."""
        from audiometa import get_merged_unified_metadata
        
        # Test with a real file
        metadata = get_merged_unified_metadata(sample_mp3_file)
        track_number = metadata.get(UnifiedMetadataKey.TRACK_NUMBER)
        
        # Should be either None or a valid integer
        assert track_number is None or isinstance(track_number, int)
        if track_number is not None:
            assert track_number >= 0  # Track numbers should be non-negative
