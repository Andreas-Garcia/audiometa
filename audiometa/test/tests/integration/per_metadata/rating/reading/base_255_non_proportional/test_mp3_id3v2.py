import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestBase255NonProportionalId3v2Mp3RatingReading:
    
    def test_base_255_non_proportional_0_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=0 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 0

    def test_base_255_non_proportional_0_5_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=0.5 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 10

    def test_base_255_non_proportional_1_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=1 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_base_255_non_proportional_1_5_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=1.5 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 30

    def test_base_255_non_proportional_2_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=2 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_base_255_non_proportional_2_5_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=2.5 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 50

    def test_base_255_non_proportional_3_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=3 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_base_255_non_proportional_3_5_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=3.5 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 70

    def test_base_255_non_proportional_4_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=4 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_base_255_non_proportional_4_5_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=4.5 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 90

    def test_base_255_non_proportional_5_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=5 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100
