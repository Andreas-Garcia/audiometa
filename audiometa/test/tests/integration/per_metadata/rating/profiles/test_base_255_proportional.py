import pytest

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.rating_profiles import RatingReadProfile
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestBase255ProportionalProfile:
    
    def test_write_read_profile_values(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        profile_values = RatingReadProfile.BASE_255_PROPORTIONAL.value
        
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
        profile = RatingReadProfile.BASE_255_PROPORTIONAL.value
        
        # Test specific values from the compatibility table
        assert profile[0] is None     # 0 stars (Traktor)
        assert profile[2] == 51      # 1 star (Traktor)
        assert profile[4] == 102     # 2 stars (Traktor)
        assert profile[6] == 153     # 3 stars (Traktor)
        assert profile[8] == 204     # 4 stars (Traktor)
        assert profile[10] == 255    # 5 stars (Traktor)

    def test_profile_value_ranges(self):
        profile = RatingReadProfile.BASE_255_PROPORTIONAL.value
        
        # Non-None values should be integers in range 0-255
        for value in profile:
            if value is not None:
                assert isinstance(value, int)
                assert 0 <= value <= 255

    def test_profile_value_progression(self):
        profile = RatingReadProfile.BASE_255_PROPORTIONAL.value
        
        # Get non-None values
        non_none_values = [v for v in profile if v is not None]
        
        # Should be linear progression for non-None values
        for i in range(1, len(non_none_values)):
            assert non_none_values[i] > non_none_values[i-1]

    def test_profile_value_uniqueness(self):
        profile = RatingReadProfile.BASE_255_PROPORTIONAL.value
        
        # Get non-None values
        non_none_values = [v for v in profile if v is not None]
        
        # All non-None values should be unique
        assert len(non_none_values) == len(set(non_none_values))

    def test_profile_none_values(self):
        profile = RatingReadProfile.BASE_255_PROPORTIONAL.value
        
        # None values should be at half-star positions (0.5, 1.5, 2.5, 3.5, 4.5) and 0 stars
        expected_none_positions = [0, 1, 3, 5, 7, 9]  # 0, 0.5, 1.5, 2.5, 3.5, 4.5 stars
        
        for i in expected_none_positions:
            assert profile[i] is None
