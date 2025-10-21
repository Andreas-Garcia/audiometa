from pathlib import Path

import pytest

from audiometa import update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import InvalidMetadataTypeError


class TestMultipleValuesErrorHandling:
    def test_write_invalid_data_types_in_list(self, temp_audio_file: Path):
        # Test with invalid data types in multiple value lists
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [1, 2, 3]  # Numbers instead of strings
        }
        with pytest.raises(InvalidMetadataTypeError):
            update_file_metadata(temp_audio_file, metadata)

    def test_write_mixed_data_types_in_list(self, temp_audio_file: Path):
        # Test with mixed data types in multiple value lists
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", 123, None, "Artist Two"]
        }
        with pytest.raises(InvalidMetadataTypeError):
            update_file_metadata(temp_audio_file, metadata)