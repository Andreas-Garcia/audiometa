import pytest
from pathlib import Path

from audiometa import get_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestBase255ProportionalVorbisFlacRatingReading:
    
    def test_base_255_proportional_1_star_flac_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=1 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_base_255_proportional_2_star_flac_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=2 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_base_255_proportional_3_star_flac_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=3 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_base_255_proportional_4_star_flac_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=4 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_base_255_proportional_5_star_flac_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=5 star.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100

    def test_base_255_proportional_none_rating_flac_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=none.flac"
        metadata = get_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is None
