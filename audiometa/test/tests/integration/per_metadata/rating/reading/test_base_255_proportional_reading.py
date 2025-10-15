import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestBase255ProportionalRatingReading:
    
    # ID3v2 BASE_255_PROPORTIONAL tests (Traktor)
    def test_base_255_proportional_1_star_mp3_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=1 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_base_255_proportional_2_star_mp3_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=2 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_base_255_proportional_3_star_mp3_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=3 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_base_255_proportional_4_star_mp3_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=4 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_base_255_proportional_5_star_mp3_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=5 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100

    def test_base_255_proportional_none_rating_mp3_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=none.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        # Traktor "none" may actually be 0, not None
        assert rating is None or rating == 0

    # Vorbis BASE_255_PROPORTIONAL tests (Traktor)
    def test_base_255_proportional_1_star_flac_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=1 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_base_255_proportional_2_star_flac_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=2 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_base_255_proportional_3_star_flac_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=3 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_base_255_proportional_4_star_flac_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=4 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_base_255_proportional_5_star_flac_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=5 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100

    def test_base_255_proportional_none_rating_flac_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=none.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is None
