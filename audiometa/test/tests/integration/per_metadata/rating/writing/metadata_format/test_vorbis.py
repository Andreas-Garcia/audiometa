import pytest

from audiometa import get_merged_unified_metadata, update_file_metadata, get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestVorbisRatingWriting:
    
    def test_write_0_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 0}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 0

    def test_write_1_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 20}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 20

    def test_write_2_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 40}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 40

    def test_write_3_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 60}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 60

    def test_write_4_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 80}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 80

    def test_write_5_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 100}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 100

    def test_write_base_100_proportional_values(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        # Test values that correspond to BASE_100_PROPORTIONAL profile
        test_values = [0, 20, 40, 60, 80, 100]  # 0, 1, 2, 3, 4, 5 stars in base 100
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            for value in test_values:
                test_metadata = {UnifiedMetadataKey.RATING: value}
                update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
                rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
                assert rating is not None
                assert rating == value
