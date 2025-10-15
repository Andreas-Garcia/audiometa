import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestRiffRatingReading:
    
    def test_riff_base_100_proportional_1_star_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_base 100_kid3=1 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_riff_base_100_proportional_2_star_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_base 100_kid3=2 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_riff_base_100_proportional_3_star_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_base 100_kid3=3 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_riff_base_100_proportional_4_star_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_base 100_kid3=4 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_riff_base_100_proportional_5_star_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_base 100_kid3=5 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100

    def test_riff_none_rating_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_kid3=none.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is None
