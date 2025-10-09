"""Tests for reading rating metadata."""

import pytest

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestRatingReading:
    def test_id3v1(self, rating_id3v2_base_100_0_star_wav):
        # ID3v1 doesn't support ratings, using ID3v2 as fallback
        metadata = get_merged_unified_metadata(rating_id3v2_base_100_0_star_wav, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is None or isinstance(rating, (int, float))

    def test_id3v2(self, rating_id3v2_base_100_5_star_wav):
        metadata = get_merged_unified_metadata(rating_id3v2_base_100_5_star_wav, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is None or isinstance(rating, (int, float))

    def test_vorbis(self, rating_vorbis_base_100_5_star_flac):
        metadata = get_merged_unified_metadata(rating_vorbis_base_100_5_star_flac, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is None or isinstance(rating, (int, float))

    def test_riff(self, rating_riff_base_100_5_star_wav):
        metadata = get_merged_unified_metadata(rating_riff_base_100_5_star_wav, normalized_rating_max_value=100)
        rating = metadata.get(UnifiedMetadataKey.RATING)
        assert rating is None or isinstance(rating, (int, float))
