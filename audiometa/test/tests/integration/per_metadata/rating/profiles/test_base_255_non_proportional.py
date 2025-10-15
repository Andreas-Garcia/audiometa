import pytest

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.rating_profiles import RatingReadProfile
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestBase255NonProportionalProfile:
    
    def test_write_read_profile_values(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        profile_values = RatingReadProfile.BASE_255_NON_PROPORTIONAL.value
        
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

    def test_profile_specific_values(self):
        profile = RatingReadProfile.BASE_255_NON_PROPORTIONAL.value
        
        # Test specific values from the compatibility table
        assert profile[0] == 0    # 0 stars
        assert profile[2] == 1    # 1 star
        assert profile[4] == 64   # 2 stars
        assert profile[6] == 128  # 3 stars
        assert profile[8] == 196  # 4 stars
        assert profile[10] == 255 # 5 stars

    def test_profile_value_ranges(self):
        profile = RatingReadProfile.BASE_255_NON_PROPORTIONAL.value
        
        # All values should be integers in range 0-255
        for value in profile:
            assert isinstance(value, int)
            assert 0 <= value <= 255

    def test_profile_value_uniqueness(self):
        profile = RatingReadProfile.BASE_255_NON_PROPORTIONAL.value
        
        # All values should be unique
        assert len(profile) == len(set(profile))
