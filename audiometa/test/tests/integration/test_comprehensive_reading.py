"""Comprehensive tests for metadata reading functionality using test tracks."""

import pytest
from pathlib import Path

from audiometa import (
    get_merged_app_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.TagFormat import MetadataFormat
from audiometa.utils.AppMetadataKey import AppMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestComprehensiveMetadataReading:
    """Comprehensive test cases for metadata reading functionality."""

    def test_metadata_none_files(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav):
        """Test reading metadata from files with no metadata."""
        # MP3 with no metadata
        metadata = get_merged_app_metadata(metadata_none_mp3)
        assert isinstance(metadata, dict)
        # Should have minimal or no metadata
        assert not metadata.get(AppMetadataKey.TITLE) or metadata.get(AppMetadataKey.TITLE) == ""
        
        # FLAC with no metadata
        metadata = get_merged_app_metadata(metadata_none_flac)
        assert isinstance(metadata, dict)
        
        # WAV with no metadata
        metadata = get_merged_app_metadata(metadata_none_wav)
        assert isinstance(metadata, dict)

    def test_id3v1_metadata_reading(self, metadata_id3v1_small_mp3, metadata_id3v1_small_flac, metadata_id3v1_small_wav):
        """Test reading ID3v1 metadata from various formats."""
        # MP3 with ID3v1
        metadata = get_merged_app_metadata(metadata_id3v1_small_mp3)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.TITLE in metadata
        assert metadata[AppMetadataKey.TITLE] == 'a' * 30  # ID3v1 title limit
        
        # FLAC with ID3v1
        metadata = get_merged_app_metadata(metadata_id3v1_small_flac)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.TITLE in metadata
        
        # WAV with ID3v1
        metadata = get_merged_app_metadata(metadata_id3v1_small_wav)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.TITLE in metadata

    def test_id3v2_metadata_reading(self, metadata_id3v2_small_mp3, metadata_id3v2_small_flac, metadata_id3v2_small_wav):
        """Test reading ID3v2 metadata from various formats."""
        # MP3 with ID3v2
        metadata = get_merged_app_metadata(metadata_id3v2_small_mp3)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.TITLE in metadata
        # ID3v2 can have longer titles than ID3v1
        assert len(metadata[AppMetadataKey.TITLE]) > 30
        
        # FLAC with ID3v2
        metadata = get_merged_app_metadata(metadata_id3v2_small_flac)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.TITLE in metadata
        
        # WAV with ID3v2
        metadata = get_merged_app_metadata(metadata_id3v2_small_wav)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.TITLE in metadata

    def test_riff_metadata_reading(self, metadata_riff_small_wav):
        """Test reading RIFF metadata from WAV files."""
        metadata = get_merged_app_metadata(metadata_riff_small_wav)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.TITLE in metadata
        # RIFF can have longer titles than ID3v1
        assert len(metadata[AppMetadataKey.TITLE]) > 30

    def test_vorbis_metadata_reading(self, metadata_vorbis_small_flac):
        """Test reading Vorbis metadata from FLAC files."""
        metadata = get_merged_app_metadata(metadata_vorbis_small_flac)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.TITLE in metadata
        # Vorbis can have very long titles
        assert len(metadata[AppMetadataKey.TITLE]) > 30

    def test_single_format_metadata_reading(self, metadata_id3v2_small_mp3, metadata_vorbis_small_flac, metadata_riff_small_wav):
        """Test reading metadata from specific formats only."""
        # ID3v2 from MP3
        id3v2_metadata = get_single_format_app_metadata(metadata_id3v2_small_mp3, MetadataFormat.ID3V2)
        assert isinstance(id3v2_metadata, dict)
        assert AppMetadataKey.TITLE in id3v2_metadata
        
        # Vorbis from FLAC
        vorbis_metadata = get_single_format_app_metadata(metadata_vorbis_small_flac, MetadataFormat.VORBIS)
        assert isinstance(vorbis_metadata, dict)
        assert AppMetadataKey.TITLE in vorbis_metadata
        
        # RIFF from WAV
        riff_metadata = get_single_format_app_metadata(metadata_riff_small_wav, MetadataFormat.RIFF)
        assert isinstance(riff_metadata, dict)
        assert AppMetadataKey.TITLE in riff_metadata

    def test_rating_reading_id3v2_base_100(self, rating_id3v2_base_100_0_star_wav, rating_id3v2_base_100_5_star_wav):
        """Test reading ID3v2 ratings with base 100 normalization."""
        # 0 star rating
        metadata = get_merged_app_metadata(rating_id3v2_base_100_0_star_wav, normalized_rating_max_value=100)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.RATING in metadata
        assert metadata[AppMetadataKey.RATING] == 0
        
        # 5 star rating
        metadata = get_merged_app_metadata(rating_id3v2_base_100_5_star_wav, normalized_rating_max_value=100)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.RATING in metadata
        assert metadata[AppMetadataKey.RATING] == 10  # 5 stars = 10/10

    def test_rating_reading_id3v2_base_255(self, rating_id3v2_base_255_5_star_mp3):
        """Test reading ID3v2 ratings with base 255 normalization."""
        metadata = get_merged_app_metadata(rating_id3v2_base_255_5_star_mp3, normalized_rating_max_value=255)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.RATING in metadata
        assert metadata[AppMetadataKey.RATING] == 10  # 5 stars = 10/10

    def test_rating_reading_riff_base_100(self, rating_riff_base_100_5_star_wav):
        """Test reading RIFF ratings with base 100 normalization."""
        metadata = get_merged_app_metadata(rating_riff_base_100_5_star_wav, normalized_rating_max_value=100)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.RATING in metadata
        assert metadata[AppMetadataKey.RATING] == 10  # 5 stars = 10/10

    def test_rating_reading_vorbis_base_100(self, rating_vorbis_base_100_5_star_flac):
        """Test reading Vorbis ratings with base 100 normalization."""
        metadata = get_merged_app_metadata(rating_vorbis_base_100_5_star_flac, normalized_rating_max_value=100)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.RATING in metadata
        assert metadata[AppMetadataKey.RATING] == 10  # 5 stars = 10/10

    def test_artists_reading_comma_separated(self, artists_one_two_three_comma_id3v2):
        """Test reading artists with comma separation."""
        metadata = get_merged_app_metadata(artists_one_two_three_comma_id3v2)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.ARTISTS_NAMES in metadata
        artists = metadata[AppMetadataKey.ARTISTS_NAMES]
        assert isinstance(artists, list)
        assert "One Two Three" in artists

    def test_artists_reading_semicolon_separated(self, artists_one_two_three_semicolon_id3v2):
        """Test reading artists with semicolon separation."""
        metadata = get_merged_app_metadata(artists_one_two_three_semicolon_id3v2)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.ARTISTS_NAMES in metadata
        artists = metadata[AppMetadataKey.ARTISTS_NAMES]
        assert isinstance(artists, list)
        assert "One Two Three" in artists

    def test_artists_reading_multi_tags_vorbis(self, artists_one_two_three_multi_tags_vorbis):
        """Test reading artists with multiple Vorbis metadata."""
        metadata = get_merged_app_metadata(artists_one_two_three_multi_tags_vorbis)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.ARTISTS_NAMES in metadata
        artists = metadata[AppMetadataKey.ARTISTS_NAMES]
        assert isinstance(artists, list)
        assert "One Two Three" in artists

    def test_album_reading_id3v2(self, album_koko_id3v2_mp3, album_koko_id3v2_wav):
        """Test reading album metadata from ID3v2."""
        # MP3 with ID3v2 album
        metadata = get_merged_app_metadata(album_koko_id3v2_mp3)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.ALBUM_NAME in metadata
        assert metadata[AppMetadataKey.ALBUM_NAME] == "koko"
        
        # WAV with ID3v2 album
        metadata = get_merged_app_metadata(album_koko_id3v2_wav)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.ALBUM_NAME in metadata
        assert metadata[AppMetadataKey.ALBUM_NAME] == "koko"

    def test_album_reading_vorbis(self, album_koko_vorbis_flac):
        """Test reading album metadata from Vorbis."""
        metadata = get_merged_app_metadata(album_koko_vorbis_flac)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.ALBUM_NAME in metadata
        assert metadata[AppMetadataKey.ALBUM_NAME] == "koko"

    def test_genre_reading_id3v1_codes(self, genre_code_id3v1_abstract_mp3, genre_code_id3v1_unknown_mp3):
        """Test reading ID3v1 genre codes."""
        # Abstract genre
        metadata = get_merged_app_metadata(genre_code_id3v1_abstract_mp3)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.GENRE in metadata
        # Should convert ID3v1 code to genre name
        assert metadata[AppMetadataKey.GENRE] == "Abstract"
        
        # Unknown genre
        metadata = get_merged_app_metadata(genre_code_id3v1_unknown_mp3)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.GENRE in metadata
        assert metadata[AppMetadataKey.GENRE] == "Unknown"

    def test_technical_metadata_reading(self, bitrate_320_mp3, bitrate_946_flac, bitrate_1411_wav):
        """Test reading technical metadata like bitrate."""
        # MP3 bitrate
        metadata = get_merged_app_metadata(bitrate_320_mp3)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.BITRATE in metadata
        assert metadata[AppMetadataKey.BITRATE] == 320
        
        # FLAC bitrate
        metadata = get_merged_app_metadata(bitrate_946_flac)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.BITRATE in metadata
        assert metadata[AppMetadataKey.BITRATE] == 946
        
        # WAV bitrate
        metadata = get_merged_app_metadata(bitrate_1411_wav)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.BITRATE in metadata
        assert metadata[AppMetadataKey.BITRATE] == 1411

    def test_duration_reading(self, duration_1s_mp3, duration_182s_mp3, duration_335s_flac, duration_472s_wav):
        """Test reading duration metadata."""
        # 1 second duration
        metadata = get_merged_app_metadata(duration_1s_mp3)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.DURATION in metadata
        assert abs(metadata[AppMetadataKey.DURATION] - 1.0) < 0.1
        
        # 182 seconds duration
        metadata = get_merged_app_metadata(duration_182s_mp3)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.DURATION in metadata
        assert abs(metadata[AppMetadataKey.DURATION] - 182.0) < 1.0
        
        # 335 seconds duration
        metadata = get_merged_app_metadata(duration_335s_flac)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.DURATION in metadata
        assert abs(metadata[AppMetadataKey.DURATION] - 335.0) < 1.0
        
        # 472 seconds duration
        metadata = get_merged_app_metadata(duration_472s_wav)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.DURATION in metadata
        assert abs(metadata[AppMetadataKey.DURATION] - 472.0) < 1.0

    def test_file_size_metadata(self, size_small_mp3, size_big_mp3, size_small_flac, size_big_flac, size_small_wav, size_big_wav):
        """Test reading file size metadata."""
        # Small MP3
        metadata = get_merged_app_metadata(size_small_mp3)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.FILE_SIZE in metadata
        assert metadata[AppMetadataKey.FILE_SIZE] > 0
        
        # Big MP3
        metadata = get_merged_app_metadata(size_big_mp3)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.FILE_SIZE in metadata
        assert metadata[AppMetadataKey.FILE_SIZE] > 0
        
        # Small FLAC
        metadata = get_merged_app_metadata(size_small_flac)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.FILE_SIZE in metadata
        assert metadata[AppMetadataKey.FILE_SIZE] > 0
        
        # Big FLAC
        metadata = get_merged_app_metadata(size_big_flac)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.FILE_SIZE in metadata
        assert metadata[AppMetadataKey.FILE_SIZE] > 0
        
        # Small WAV
        metadata = get_merged_app_metadata(size_small_wav)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.FILE_SIZE in metadata
        assert metadata[AppMetadataKey.FILE_SIZE] > 0
        
        # Big WAV
        metadata = get_merged_app_metadata(size_big_wav)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.FILE_SIZE in metadata
        assert metadata[AppMetadataKey.FILE_SIZE] > 0

    def test_specific_metadata_reading(self, metadata_id3v2_small_mp3):
        """Test reading specific metadata fields."""
        # Title
        title = get_specific_metadata(metadata_id3v2_small_mp3, AppMetadataKey.TITLE)
        assert isinstance(title, str)
        assert len(title) > 30  # ID3v2 can have long titles
        
        # Artists
        artists = get_specific_metadata(metadata_id3v2_small_mp3, AppMetadataKey.ARTISTS_NAMES)
        assert artists is None or isinstance(artists, list)
        
        # Album
        album = get_specific_metadata(metadata_id3v2_small_mp3, AppMetadataKey.ALBUM_NAME)
        assert album is None or isinstance(album, str)
        
        # Genre
        genre = get_specific_metadata(metadata_id3v2_small_mp3, AppMetadataKey.GENRE)
        assert genre is None or isinstance(genre, str)
        
        # Rating
        rating = get_specific_metadata(metadata_id3v2_small_mp3, AppMetadataKey.RATING)
        assert rating is None or isinstance(rating, (int, float))
        
        # Bitrate
        bitrate = get_specific_metadata(metadata_id3v2_small_mp3, AppMetadataKey.BITRATE)
        assert bitrate is None or isinstance(bitrate, int)
        
        # Duration
        duration = get_specific_metadata(metadata_id3v2_small_mp3, AppMetadataKey.DURATION)
        assert duration is None or isinstance(duration, (int, float))

    def test_audio_file_object_reading(self, metadata_id3v2_small_mp3):
        """Test reading metadata using AudioFile object."""
        audio_file = AudioFile(metadata_id3v2_small_mp3)
        
        # Test merged metadata
        metadata = get_merged_app_metadata(audio_file)
        assert isinstance(metadata, dict)
        assert AppMetadataKey.TITLE in metadata
        
        # Test specific metadata
        title = get_specific_metadata(audio_file, AppMetadataKey.TITLE)
        assert isinstance(title, str)
        
        # Test single format metadata
        id3v2_metadata = get_single_format_app_metadata(audio_file, MetadataFormat.ID3V2)
        assert isinstance(id3v2_metadata, dict)

    def test_rating_normalization_variations(self, rating_id3v2_base_100_5_star_wav):
        """Test different rating normalization values."""
        # Base 100 normalization
        metadata_100 = get_merged_app_metadata(rating_id3v2_base_100_5_star_wav, normalized_rating_max_value=100)
        assert metadata_100[AppMetadataKey.RATING] == 10
        
        # Base 255 normalization
        metadata_255 = get_merged_app_metadata(rating_id3v2_base_100_5_star_wav, normalized_rating_max_value=255)
        assert metadata_255[AppMetadataKey.RATING] == 10  # Should still be 10/10

    def test_unsupported_format_error(self, temp_audio_file):
        """Test that unsupported formats raise appropriate errors."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_merged_app_metadata(str(temp_audio_file))
        
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.ID3V2)
        
        with pytest.raises(FileTypeNotSupportedError):
            get_specific_metadata(str(temp_audio_file), AppMetadataKey.TITLE)


