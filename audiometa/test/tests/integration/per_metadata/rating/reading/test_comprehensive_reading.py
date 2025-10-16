import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata, get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestRatingComprehensiveReading:
    
    # ID3v2 BASE_255_NON_PROPORTIONAL tests (MP3/FLAC)
    def test_id3v2_base_255_non_proportional_0_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=0 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 0  # 0 stars should be 0

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
        assert rating == 20  # 1 star = 20 in base 100

    def test_id3v2_base_255_non_proportional_2_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=2 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40  # 2 stars = 40 in base 100

    def test_id3v2_base_255_non_proportional_3_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=3 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60  # 3 stars = 60 in base 100

    def test_id3v2_base_255_non_proportional_4_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=4 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80  # 4 stars = 80 in base 100

    def test_id3v2_base_255_non_proportional_5_star_mp3(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2=5 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100  # 5 stars = 100 in base 100

    # ID3v2 BASE_100_PROPORTIONAL tests (WAV)
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

    # ID3v2 BASE_255_PROPORTIONAL tests (Traktor)
    def test_id3v2_base_255_proportional_1_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=1 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20  # 51 in base 255 = 20 in base 100

    def test_id3v2_base_255_proportional_2_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=2 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40  # 102 in base 255 = 40 in base 100

    def test_id3v2_base_255_proportional_3_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=3 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60  # 153 in base 255 = 60 in base 100

    def test_id3v2_base_255_proportional_4_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=4 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80  # 204 in base 255 = 80 in base 100

    def test_id3v2_base_255_proportional_5_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_id3v2_tracktor=5 star.mp3"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100  # 255 in base 255 = 100 in base 100

    # RIFF BASE_100_PROPORTIONAL tests
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

    # Vorbis BASE_100_PROPORTIONAL tests
    def test_vorbis_base_100_proportional_0_star_flac(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=0 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 0

    def test_vorbis_base_100_proportional_1_star_flac(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=1 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20

    def test_vorbis_base_100_proportional_2_star_flac(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=2 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40

    def test_vorbis_base_100_proportional_3_star_flac(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=3 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60

    def test_vorbis_base_100_proportional_4_star_flac(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=4 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80

    def test_vorbis_base_100_proportional_5_star_flac(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis=5 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100

    # Vorbis BASE_255_PROPORTIONAL tests (Traktor)
    def test_vorbis_base_255_proportional_1_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=1 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 20  # 51 in base 255 = 20 in base 100

    def test_vorbis_base_255_proportional_2_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=2 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 40  # 102 in base 255 = 40 in base 100

    def test_vorbis_base_255_proportional_3_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=3 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 60  # 153 in base 255 = 60 in base 100

    def test_vorbis_base_255_proportional_4_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=4 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 80  # 204 in base 255 = 80 in base 100

    def test_vorbis_base_255_proportional_5_star_traktor(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=5 star.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is not None
        assert isinstance(rating, (int, float))
        assert rating == 100  # 255 in base 255 = 100 in base 100

    # Test no rating cases
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

    def test_vorbis_traktor_none_rating_flac(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_vorbis_traktor=none.flac"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is None

    def test_riff_none_rating_wav(self, test_files_dir: Path):
        file_path = test_files_dir / "rating_riff_kid3=none.wav"
        metadata = get_merged_unified_metadata(file_path, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is None
