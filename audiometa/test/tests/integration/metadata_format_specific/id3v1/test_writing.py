

import pytest
from pathlib import Path

from audiometa import (
    get_unified_metadata,
    update_file_metadata
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestId3v1Writing:

    def test_multiple_metadata_reading(self):
        with TempFileWithMetadata({}, "id3v1") as test_file:
            test_metadata = {
                # Basic metadata commonly supported across formats
                UnifiedMetadataKey.TITLE: "Test Song Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album",
                UnifiedMetadataKey.GENRES_NAMES: "Test Genre",
                UnifiedMetadataKey.RATING: 8
            }
            
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100)
            
            # Verify all fields
            metadata = get_unified_metadata(test_file.path, normalized_rating_max_value=10)
            
            # Basic metadata assertions
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Test Genre"]
            assert metadata.get(UnifiedMetadataKey.RATING) == 0

    def test_multiple_metadata_writing(self):
        with TempFileWithMetadata({}, "id3v1") as test_file:
            test_metadata = {
                # Basic metadata commonly supported across formats
                UnifiedMetadataKey.TITLE: "Written Song Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Written Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Written Album",
                UnifiedMetadataKey.GENRES_NAMES: ["Written Genre"],
                UnifiedMetadataKey.RATING: 9
            }
            
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100)
            
            # Verify all fields were written
            metadata = get_unified_metadata(test_file.path, normalized_rating_max_value=10)
            
            # Basic metadata assertions
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Written Song Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Written Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Written Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Written Genre"]
            assert metadata.get(UnifiedMetadataKey.RATING) == 0
