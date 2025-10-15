import pytest

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.rating_profiles import RatingReadProfile
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestBase100ProportionalProfile:
    
    def test_write_read_profile_values(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        profile_values = RatingReadProfile.BASE_100_PROPORTIONAL.value
        
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

    def test_profile_specific_values(self):
        profile = RatingReadProfile.BASE_100_PROPORTIONAL.value
        
        # Test specific values from the compatibility table
        assert profile[0] == 0    # 0 stars
        assert profile[2] == 20   # 1 star
        assert profile[4] == 40   # 2 stars
        assert profile[6] == 60   # 3 stars
        assert profile[8] == 80   # 4 stars
        assert profile[10] == 100 # 5 stars

    def test_profile_value_ranges(self):
        profile = RatingReadProfile.BASE_100_PROPORTIONAL.value
        
        # All values should be integers in range 0-100
        for value in profile:
            assert isinstance(value, int)
            assert 0 <= value <= 100

    def test_profile_value_progression(self):
        profile = RatingReadProfile.BASE_100_PROPORTIONAL.value
        
        # Should be linear progression
        for i in range(1, len(profile)):
            assert profile[i] > profile[i-1]

    def test_profile_value_uniqueness(self):
        profile = RatingReadProfile.BASE_100_PROPORTIONAL.value
        
        # All values should be unique
        assert len(profile) == len(set(profile))
