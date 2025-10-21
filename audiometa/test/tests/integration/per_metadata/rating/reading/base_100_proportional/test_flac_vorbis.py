import pytest
from pathlib import Path

from audiometa import get_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestBase100ProportionalVorbisFlacRatingReading:
    
    def test_base_100_proportional_0_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=0 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 0

    def test_base_100_proportional_0_5_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=0.5 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 10

    def test_base_100_proportional_1_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=1 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_base_100_proportional_1_5_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=1.5 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 30

    def test_base_100_proportional_2_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=2 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_base_100_proportional_2_5_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=2.5 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 50

    def test_base_100_proportional_3_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=3 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_base_100_proportional_3_5_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=3.5 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 70

    def test_base_100_proportional_4_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=4 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_base_100_proportional_4_5_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=4.5 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 90

    def test_base_100_proportional_5_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=5 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100
