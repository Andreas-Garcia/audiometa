import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestId3v2RatingReading:
    
    def test_id3v2_base_255_non_proportional_0_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=0 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 0

    def test_id3v2_base_255_non_proportional_0_star_flac(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=0 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 0

    def test_id3v2_base_255_non_proportional_1_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=1 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_id3v2_base_255_non_proportional_2_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=2 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_id3v2_base_255_non_proportional_3_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=3 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_id3v2_base_255_non_proportional_4_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=4 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_id3v2_base_255_non_proportional_5_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=5 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100

    def test_id3v2_base_100_proportional_0_star_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=0 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 0

    def test_id3v2_base_100_proportional_1_star_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=1 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_id3v2_base_100_proportional_2_star_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=2 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_id3v2_base_100_proportional_3_star_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=3 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_id3v2_base_100_proportional_4_star_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=4 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_id3v2_base_100_proportional_5_star_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=5 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100

    def test_id3v2_base_255_proportional_1_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=1 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_id3v2_base_255_proportional_2_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=2 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_id3v2_base_255_proportional_3_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=3 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_id3v2_base_255_proportional_4_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=4 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_id3v2_base_255_proportional_5_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=5 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100

    def test_id3v2_none_rating_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=none.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is None

    def test_id3v2_traktor_none_rating_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=none.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        # Traktor "none" may actually be 0, not None
        assert rating is None or rating == 0
