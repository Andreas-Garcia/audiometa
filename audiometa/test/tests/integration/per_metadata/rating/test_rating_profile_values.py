import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata, update_file_metadata, get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.rating_profiles import RatingReadProfile, RatingWriteProfile
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestRatingProfileValues:
    
    def test_base_255_non_proportional_profile_values(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        # Test that the profile values are correctly defined
        profile_values = RatingReadProfile.BASE_255_NON_PROPORTIONAL.value
        expected_values = [0, 13, 1, 54, 64, 118, 128, 186, 196, 242, 255]
        
        # Verify the profile values are correct
        assert profile_values == expected_values
        
        # Test that we can write and read back profile values
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            for i, raw_value in enumerate(profile_values):
                if raw_value is None:
                    continue  # Skip None values
                    
                # Write the raw value
                test_metadata = {UnifiedMetadataKey.RATING: raw_value}
                update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=255, metadata_format=MetadataFormat.ID3V2)
                
                # Read back and verify - the value may be normalized/clamped
                rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=255)
                assert rating is not None
                assert isinstance(rating, (int, float))
                # The rating should be in the valid range
                assert 0 <= rating <= 255
                
                # Also test reading with base 100 normalization
                rating_normalized = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
                assert rating_normalized is not None
                assert isinstance(rating_normalized, (int, float))
                assert 0 <= rating_normalized <= 100

    def test_base_100_proportional_profile_values(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        # Test that the profile values are correctly defined
        profile_values = RatingReadProfile.BASE_100_PROPORTIONAL.value
        expected_values = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        
        # Verify the profile values are correct
        assert profile_values == expected_values
        
        # Test that we can write and read back profile values
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            for i, raw_value in enumerate(profile_values):
                if raw_value is None:
                    continue  # Skip None values
                    
                # Write the raw value
                test_metadata = {UnifiedMetadataKey.RATING: raw_value}
                update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
                
                # Read back and verify
                rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
                assert rating is not None
                assert rating == raw_value

    def test_base_255_proportional_profile_values(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        # Test that the profile values are correctly defined
        profile_values = RatingReadProfile.BASE_255_PROPORTIONAL.value
        expected_values = [None, None, 51, None, 102, None, 153, None, 204, None, 255]
        
        # Verify the profile values are correct
        assert profile_values == expected_values
        
        # Test that we can write and read back profile values
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            for i, raw_value in enumerate(profile_values):
                if raw_value is None:
                    continue  # Skip None values
                    
                # Write the raw value
                test_metadata = {UnifiedMetadataKey.RATING: raw_value}
                update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=255, metadata_format=MetadataFormat.ID3V2)
                
                # Read back and verify - the value may be normalized/clamped
                rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=255)
                assert rating is not None
                assert isinstance(rating, (int, float))
                # The rating should be in the valid range
                assert 0 <= rating <= 255
                
                # Also test reading with base 100 normalization
                rating_normalized = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
                assert rating_normalized is not None
                assert isinstance(rating_normalized, (int, float))
                assert 0 <= rating_normalized <= 100

    def test_write_profile_consistency(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        # Test that write profiles match read profiles
        write_profile = RatingWriteProfile.BASE_255_NON_PROPORTIONAL.value
        read_profile = RatingReadProfile.BASE_255_NON_PROPORTIONAL.value
        
        assert write_profile == read_profile
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            for raw_value in write_profile:
                if raw_value is None:
                    continue
                    
                # Write using the profile value
                test_metadata = {UnifiedMetadataKey.RATING: raw_value}
                update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=255, metadata_format=MetadataFormat.ID3V2)
                
                # Read back and verify - the value may be normalized/clamped
                rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=255)
                assert rating is not None
                assert isinstance(rating, (int, float))
                # The rating should be in the valid range
                assert 0 <= rating <= 255

    def test_profile_value_mapping_consistency(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        # Test that the same star rating maps to the same normalized value
        # regardless of which profile was used to write it
        
        star_ratings = [0, 1, 2, 3, 4, 5]
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            for stars in star_ratings:
                # Write using normalized value (base 100)
                normalized_value = stars * 20  # 0, 20, 40, 60, 80, 100
                test_metadata = {UnifiedMetadataKey.RATING: normalized_value}
                update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
                
                # Read back with base 100
                rating_100 = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
                assert rating_100 == normalized_value
                
                # Read back with base 255 (should be normalized)
                rating_255 = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=255)
                assert rating_255 is not None
                assert isinstance(rating_255, (int, float))
                # The normalized value should be proportional
                assert abs(rating_255 - (normalized_value * 255 / 100)) <= 1

    def test_profile_edge_cases(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            # Test minimum value (0)
            test_metadata = {UnifiedMetadataKey.RATING: 0}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=255, metadata_format=MetadataFormat.ID3V2)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=255)
            assert rating == 0
            
            # Test maximum value (255)
            test_metadata = {UnifiedMetadataKey.RATING: 255}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=255, metadata_format=MetadataFormat.ID3V2)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=255)
            assert rating == 255

    def test_profile_cross_format_compatibility(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        # Test that the same normalized value works across different formats
        test_value = 60  # 3 stars in base 100
        
        # Test ID3v2
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: test_value}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating == test_value
        
        # Test RIFF
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: test_value}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating == test_value
        
        # Test Vorbis
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: test_value}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating == test_value

    def test_profile_value_roundtrip_accuracy(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        # Test that values can be written and read back accurately
        test_values = [0, 1, 13, 20, 40, 60, 80, 100, 128, 196, 255]
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
            for value in test_values:
                # Write value
                test_metadata = {UnifiedMetadataKey.RATING: value}
                update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=255, metadata_format=MetadataFormat.ID3V2)
                
                # Read back with same max value
                rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=255)
                assert rating == value
                
                # Read back with different max value (should normalize)
                rating_normalized = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
                assert rating_normalized is not None
                assert isinstance(rating_normalized, (int, float))
                # Should be proportional: normalized = value * 100 / 255
                expected_normalized = int(value * 100 / 255)
                assert abs(rating_normalized - expected_normalized) <= 1
