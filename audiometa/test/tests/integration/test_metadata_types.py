"""Tests for specific metadata types using test tracks."""

import pytest
from pathlib import Path

from audiometa import get_merged_app_metadata, update_file_metadata
from audiometa.utils.AppMetadataKey import AppMetadataKey


@pytest.mark.integration
class TestMetadataTypes:
    """Test cases for specific metadata types."""

    def test_artists_metadata_reading(self, artists_one_two_three_comma_id3v2, artists_one_two_three_semicolon_id3v2, artists_one_two_three_multi_tags_vorbis):
        """Test reading artists metadata from different formats."""
        # Comma-separated artists (ID3v2)
        metadata = get_merged_app_metadata(artists_one_two_three_comma_id3v2)
        artists = metadata.get(AppMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert "One Two Three" in artists
        
        # Semicolon-separated artists (ID3v2)
        metadata = get_merged_app_metadata(artists_one_two_three_semicolon_id3v2)
        artists = metadata.get(AppMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert "One Two Three" in artists
        
        # Multi-tags artists (Vorbis)
        metadata = get_merged_app_metadata(artists_one_two_three_multi_tags_vorbis)
        artists = metadata.get(AppMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert "One Two Three" in artists

    def test_artists_metadata_writing(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test writing artists metadata to different formats."""
        import shutil
        
        # Test MP3
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_artists = ["Artist One", "Artist Two", "Artist Three"]
        update_file_metadata(temp_audio_file, {AppMetadataKey.ARTISTS_NAMES: test_artists})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == test_artists
        
        # Test FLAC
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_artists = ["Single Artist"]
        update_file_metadata(temp_audio_file, {AppMetadataKey.ARTISTS_NAMES: test_artists})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == test_artists
        
        # Test WAV
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_artists = ["Artist A", "Artist B"]
        update_file_metadata(temp_audio_file, {AppMetadataKey.ARTISTS_NAMES: test_artists})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == test_artists

    def test_album_metadata_reading(self, album_koko_id3v2_mp3, album_koko_id3v2_wav, album_koko_vorbis_flac):
        """Test reading album metadata from different formats."""
        # ID3v2 album (MP3)
        metadata = get_merged_app_metadata(album_koko_id3v2_mp3)
        assert metadata.get(AppMetadataKey.ALBUM_NAME) == "koko"
        
        # ID3v2 album (WAV)
        metadata = get_merged_app_metadata(album_koko_id3v2_wav)
        assert metadata.get(AppMetadataKey.ALBUM_NAME) == "koko"
        
        # Vorbis album (FLAC)
        metadata = get_merged_app_metadata(album_koko_vorbis_flac)
        assert metadata.get(AppMetadataKey.ALBUM_NAME) == "koko"

    def test_album_metadata_writing(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test writing album metadata to different formats."""
        import shutil
        
        # Test MP3
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_album = "Test Album MP3"
        update_file_metadata(temp_audio_file, {AppMetadataKey.ALBUM_NAME: test_album})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.ALBUM_NAME) == test_album
        
        # Test FLAC
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_album = "Test Album FLAC"
        update_file_metadata(temp_audio_file, {AppMetadataKey.ALBUM_NAME: test_album})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.ALBUM_NAME) == test_album
        
        # Test WAV
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_album = "Test Album WAV"
        update_file_metadata(temp_audio_file, {AppMetadataKey.ALBUM_NAME: test_album})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.ALBUM_NAME) == test_album

    def test_genre_metadata_reading(self, genre_code_id3v1_abstract_mp3, genre_code_id3v1_unknown_mp3):
        """Test reading genre metadata from ID3v1 codes."""
        # Abstract genre
        metadata = get_merged_app_metadata(genre_code_id3v1_abstract_mp3)
        assert metadata.get(AppMetadataKey.GENRE) == "Abstract"
        
        # Unknown genre
        metadata = get_merged_app_metadata(genre_code_id3v1_unknown_mp3)
        assert metadata.get(AppMetadataKey.GENRE) == "Unknown"

    def test_genre_metadata_writing(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test writing genre metadata to different formats."""
        import shutil
        
        # Test MP3
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_genre = "Test Genre MP3"
        update_file_metadata(temp_audio_file, {AppMetadataKey.GENRE: test_genre})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.GENRE) == test_genre
        
        # Test FLAC
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_genre = "Test Genre FLAC"
        update_file_metadata(temp_audio_file, {AppMetadataKey.GENRE: test_genre})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.GENRE) == test_genre
        
        # Test WAV
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_genre = "Test Genre WAV"
        update_file_metadata(temp_audio_file, {AppMetadataKey.GENRE: test_genre})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.GENRE) == test_genre

    def test_title_metadata_reading(self, metadata_id3v1_small_mp3, metadata_id3v2_small_mp3, metadata_riff_small_wav, metadata_vorbis_small_flac):
        """Test reading title metadata from different formats."""
        # ID3v1 title (limited to 30 characters)
        metadata = get_merged_app_metadata(metadata_id3v1_small_mp3)
        title = metadata.get(AppMetadataKey.TITLE)
        assert isinstance(title, str)
        assert len(title) == 30  # ID3v1 limit
        assert title == 'a' * 30
        
        # ID3v2 title (can be longer)
        metadata = get_merged_app_metadata(metadata_id3v2_small_mp3)
        title = metadata.get(AppMetadataKey.TITLE)
        assert isinstance(title, str)
        assert len(title) > 30  # ID3v2 can be longer
        
        # RIFF title (can be longer)
        metadata = get_merged_app_metadata(metadata_riff_small_wav)
        title = metadata.get(AppMetadataKey.TITLE)
        assert isinstance(title, str)
        assert len(title) > 30  # RIFF can be longer
        
        # Vorbis title (can be longer)
        metadata = get_merged_app_metadata(metadata_vorbis_small_flac)
        title = metadata.get(AppMetadataKey.TITLE)
        assert isinstance(title, str)
        assert len(title) > 30  # Vorbis can be longer

    def test_title_metadata_writing(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test writing title metadata to different formats."""
        import shutil
        
        # Test short title
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        short_title = "Short Title"
        update_file_metadata(temp_audio_file, {AppMetadataKey.TITLE: short_title})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.TITLE) == short_title
        
        # Test long title
        shutil.copy2(metadata_none_flac, temp_audio_file)
        long_title = "A" * 100  # Very long title
        update_file_metadata(temp_audio_file, {AppMetadataKey.TITLE: long_title})
        metadata = get_merged_app_metadata(temp_audio_file)
        # Should handle long titles (possibly truncated)
        assert metadata.get(AppMetadataKey.TITLE) is not None
        assert len(metadata.get(AppMetadataKey.TITLE)) > 0
        
        # Test empty title
        shutil.copy2(metadata_none_wav, temp_audio_file)
        empty_title = ""
        update_file_metadata(temp_audio_file, {AppMetadataKey.TITLE: empty_title})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.TITLE) == empty_title

    def test_technical_metadata_reading(self, bitrate_320_mp3, bitrate_946_flac, bitrate_1411_wav, duration_182s_mp3, duration_335s_flac, duration_472s_wav):
        """Test reading technical metadata."""
        # Bitrate tests
        metadata = get_merged_app_metadata(bitrate_320_mp3)
        assert metadata.get(AppMetadataKey.BITRATE) == 320
        
        metadata = get_merged_app_metadata(bitrate_946_flac)
        assert metadata.get(AppMetadataKey.BITRATE) == 946
        
        metadata = get_merged_app_metadata(bitrate_1411_wav)
        assert metadata.get(AppMetadataKey.BITRATE) == 1411
        
        # Duration tests
        metadata = get_merged_app_metadata(duration_182s_mp3)
        assert abs(metadata.get(AppMetadataKey.DURATION) - 182.0) < 1.0
        
        metadata = get_merged_app_metadata(duration_335s_flac)
        assert abs(metadata.get(AppMetadataKey.DURATION) - 335.0) < 1.0
        
        metadata = get_merged_app_metadata(duration_472s_wav)
        assert abs(metadata.get(AppMetadataKey.DURATION) - 472.0) < 1.0

    def test_file_size_metadata_reading(self, size_small_mp3, size_big_mp3, size_small_flac, size_big_flac, size_small_wav, size_big_wav):
        """Test reading file size metadata."""
        # Small files
        metadata = get_merged_app_metadata(size_small_mp3)
        assert metadata.get(AppMetadataKey.FILE_SIZE) > 0
        
        metadata = get_merged_app_metadata(size_small_flac)
        assert metadata.get(AppMetadataKey.FILE_SIZE) > 0
        
        metadata = get_merged_app_metadata(size_small_wav)
        assert metadata.get(AppMetadataKey.FILE_SIZE) > 0
        
        # Big files
        metadata = get_merged_app_metadata(size_big_mp3)
        assert metadata.get(AppMetadataKey.FILE_SIZE) > 0
        
        metadata = get_merged_app_metadata(size_big_flac)
        assert metadata.get(AppMetadataKey.FILE_SIZE) > 0
        
        metadata = get_merged_app_metadata(size_big_wav)
        assert metadata.get(AppMetadataKey.FILE_SIZE) > 0

    def test_metadata_consistency_across_formats(self, metadata_id3v2_small_mp3, metadata_id3v2_small_flac, metadata_id3v2_small_wav):
        """Test that metadata is consistent across different formats."""
        # All these files should have similar metadata structure
        mp3_metadata = get_merged_app_metadata(metadata_id3v2_small_mp3)
        flac_metadata = get_merged_app_metadata(metadata_id3v2_small_flac)
        wav_metadata = get_merged_app_metadata(metadata_id3v2_small_wav)
        
        # All should have title metadata
        assert AppMetadataKey.TITLE in mp3_metadata
        assert AppMetadataKey.TITLE in flac_metadata
        assert AppMetadataKey.TITLE in wav_metadata
        
        # All should have similar structure
        assert isinstance(mp3_metadata, dict)
        assert isinstance(flac_metadata, dict)
        assert isinstance(wav_metadata, dict)


