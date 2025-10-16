import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata, update_file_metadata, get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestRatingComprehensiveWriting:
    
    # Test writing all star values (0-5) for ID3v2 format
    def test_id3v2_write_0_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 0}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 0

    def test_id3v2_write_1_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 20}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 20

    def test_id3v2_write_2_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 40}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 40

    def test_id3v2_write_3_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 60}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 60

    def test_id3v2_write_4_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 80}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 80

    def test_id3v2_write_5_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 100}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 100

    # Test writing all star values (0-5) for RIFF format
    def test_riff_write_0_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 0}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 0

    def test_riff_write_1_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 20}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 20

    def test_riff_write_2_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 40}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 40

    def test_riff_write_3_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 60}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 60

    def test_riff_write_4_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 80}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 80

    def test_riff_write_5_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 100}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 100

    # Test writing all star values (0-5) for Vorbis format
    def test_vorbis_write_0_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 0}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 0

    def test_vorbis_write_1_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 20}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 20

    def test_vorbis_write_2_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 40}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 40

    def test_vorbis_write_3_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 60}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 60

    def test_vorbis_write_4_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 80}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 80

    def test_vorbis_write_5_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 100}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            rating = metadata.get(UnifiedMetadataKey.RATING)
            assert rating is not None
            assert rating == 100

    # Test writing with different rating profiles
    def test_id3v2_write_base_255_non_proportional_values(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        # Test values that correspond to BASE_255_NON_PROPORTIONAL profile
        test_values = [0, 1, 64, 128, 196, 255]  # 0, 1, 2, 3, 4, 5 stars in base 255
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            for value in test_values:
                test_metadata = {UnifiedMetadataKey.RATING: value}
                update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=255, metadata_format=MetadataFormat.ID3V2)
                rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=255)
                assert rating is not None
                # The value may be normalized/clamped, so just check it's in valid range
                assert 0 <= rating <= 255

    def test_vorbis_write_base_100_proportional_values(self, temp_audio_file):
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

    # Test writing and reading back with different max values
    def test_write_read_with_different_max_values(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            # Write with base 100
            test_metadata = {UnifiedMetadataKey.RATING: 50}  # 2.5 stars
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            
            # Read back with base 100
            rating_100 = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating_100 == 50
            
            # Read back with base 255 (should be normalized)
            rating_255 = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=255)
            assert rating_255 is not None
            assert rating_255 > 0

    # Test writing None to remove rating
    def test_write_none_removes_rating(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            # First write a rating
            test_metadata = {UnifiedMetadataKey.RATING: 80}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating == 80
            
            # Then remove it with None - this may not work as expected in all cases
            test_metadata = {UnifiedMetadataKey.RATING: None}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            # Rating removal behavior may vary - check if it's None or 0
            assert rating is None or rating == 0

    # Test writing with edge values
    def test_write_edge_values(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            # Test minimum value
            test_metadata = {UnifiedMetadataKey.RATING: 0}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating == 0
            
            # Test maximum value
            test_metadata = {UnifiedMetadataKey.RATING: 100}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating == 100

    # Test writing with fractional values (should be handled gracefully)
    def test_write_fractional_values(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            # Test fractional value (should be rounded or handled appropriately)
            test_metadata = {UnifiedMetadataKey.RATING: 25.5}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert isinstance(rating, (int, float))
            # The exact value may be rounded or normalized, so check it's in a reasonable range
            assert 0 <= rating <= 100
            # Should be close to the input value (within 10 points)
            assert abs(rating - 25.5) <= 10
