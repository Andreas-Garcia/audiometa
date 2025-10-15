import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestBase100ProportionalRatingReading:
    
    # ID3v2 BASE_100_PROPORTIONAL tests
    def test_base_100_proportional_0_star_wav_id3v2(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=0 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 0

    def test_base_100_proportional_0_5_star_wav_id3v2(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=0.5 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 10

    def test_base_100_proportional_1_star_wav_id3v2(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=1 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_base_100_proportional_1_5_star_wav_id3v2(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=1.5 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 30

    def test_base_100_proportional_2_star_wav_id3v2(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=2 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_base_100_proportional_2_5_star_wav_id3v2(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=2.5 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 50

    def test_base_100_proportional_3_star_wav_id3v2(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=3 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_base_100_proportional_3_5_star_wav_id3v2(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=3.5 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 70

    def test_base_100_proportional_4_star_wav_id3v2(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=4 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_base_100_proportional_4_5_star_wav_id3v2(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=4.5 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 90

    def test_base_100_proportional_5_star_wav_id3v2(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_base 100=5 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100

    # RIFF BASE_100_PROPORTIONAL tests
    def test_base_100_proportional_1_star_wav_riff(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_base 100_kid3=1 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_base_100_proportional_2_star_wav_riff(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_base 100_kid3=2 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_base_100_proportional_3_star_wav_riff(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_base 100_kid3=3 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_base_100_proportional_4_star_wav_riff(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_base 100_kid3=4 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_base_100_proportional_5_star_wav_riff(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_base 100_kid3=5 star.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100

    def test_base_100_proportional_none_rating_wav_riff(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_kid3=none.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is None

    # Vorbis BASE_100_PROPORTIONAL tests
    def test_base_100_proportional_0_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=0 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 0

    def test_base_100_proportional_0_5_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=0.5 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 10

    def test_base_100_proportional_1_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=1 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_base_100_proportional_1_5_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=1.5 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 30

    def test_base_100_proportional_2_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=2 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_base_100_proportional_2_5_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=2.5 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 50

    def test_base_100_proportional_3_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=3 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_base_100_proportional_3_5_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=3.5 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 70

    def test_base_100_proportional_4_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=4 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_base_100_proportional_4_5_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=4.5 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 90

    def test_base_100_proportional_5_star_flac_vorbis(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=5 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100
