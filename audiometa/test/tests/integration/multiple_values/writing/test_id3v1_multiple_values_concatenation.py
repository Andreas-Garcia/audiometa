import pytest
from pathlib import Path
import shutil

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestId3v1MultipleValuesConcatenation:
    def test_id3v1_artists_concatenation(self, temp_audio_file: Path, sample_mp3_file: Path):
        # Copy sample file to preserve existing metadata
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # ID3v1 should concatenate multiple artists with commas
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Artist Three"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify ID3v1 specific behavior
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        artists = id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # ID3v1 should return concatenated string, not list
        assert isinstance(artists, str)
        assert "Artist One" in artists
        assert "Artist Two" in artists
        assert "Artist Three" in artists
        # Should be concatenated with commas
        assert ", " in artists or "," in artists

    def test_id3v1_album_artists_concatenation(self, temp_audio_file: Path, sample_mp3_file: Path):
        # Copy sample file to preserve existing metadata
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # ID3v1 should concatenate multiple album artists with commas
        metadata = {
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: ["Album Artist One", "Album Artist Two"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify ID3v1 specific behavior
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        album_artists = id3v1_metadata.get(UnifiedMetadataKey.ALBUM_ARTISTS_NAMES)
        
        # ID3v1 should return concatenated string, not list
        assert isinstance(album_artists, str)
        assert "Album Artist One" in album_artists
        assert "Album Artist Two" in album_artists
        # Should be concatenated with commas
        assert ", " in album_artists or "," in album_artists

    def test_id3v1_composers_concatenation(self, temp_audio_file: Path, sample_mp3_file: Path):
        # Copy sample file to preserve existing metadata
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # ID3v1 should concatenate multiple composers with commas
        metadata = {
            UnifiedMetadataKey.COMPOSER: ["Composer One", "Composer Two", "Composer Three"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify ID3v1 specific behavior
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        composers = id3v1_metadata.get(UnifiedMetadataKey.COMPOSER)
        
        # ID3v1 should return concatenated string, not list
        assert isinstance(composers, str)
        assert "Composer One" in composers
        assert "Composer Two" in composers
        assert "Composer Three" in composers
        # Should be concatenated with commas
        assert ", " in composers or "," in composers

    def test_id3v1_genres_concatenation(self, temp_audio_file: Path, sample_mp3_file: Path):
        # Copy sample file to preserve existing metadata
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # ID3v1 should concatenate multiple genres with commas
        metadata = {
            UnifiedMetadataKey.GENRE_NAME: ["Rock", "Alternative", "Indie"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify ID3v1 specific behavior
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        genres = id3v1_metadata.get(UnifiedMetadataKey.GENRE_NAME)
        
        # ID3v1 should return concatenated string, not list
        assert isinstance(genres, str)
        assert "Rock" in genres
        assert "Alternative" in genres
        assert "Indie" in genres
        # Should be concatenated with commas
        assert ", " in genres or "," in genres

    def test_id3v1_field_length_limitations_with_concatenation(self, temp_audio_file: Path, sample_mp3_file: Path):
        # Copy sample file to preserve existing metadata
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test ID3v1 field length limitations with concatenated values
        long_artists = ["A" * 10, "B" * 10, "C" * 10]  # Total would be > 30 chars
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: long_artists
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify ID3v1 specific behavior
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        artists = id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should be truncated to ID3v1 limits
        assert isinstance(artists, str)
        assert len(artists) <= 30  # ID3v1 artist field is 30 characters max

    def test_id3v1_concatenation_with_special_characters(self, temp_audio_file: Path, sample_mp3_file: Path):
        # Copy sample file to preserve existing metadata
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test ID3v1 concatenation with special characters
        special_artists = ["Artist; with; semicolons", "Artist, with, commas", "Artist | with | pipes"]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: special_artists
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify ID3v1 specific behavior
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        artists = id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should be concatenated string
        assert isinstance(artists, str)
        assert "Artist; with; semicolons" in artists
        assert "Artist, with, commas" in artists
        assert "Artist | with | pipes" in artists

    def test_id3v1_concatenation_with_empty_strings(self, temp_audio_file: Path, sample_mp3_file: Path):
        # Copy sample file to preserve existing metadata
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test ID3v1 concatenation with empty strings
        mixed_artists = ["", "Valid Artist", "", "Another Valid Artist", ""]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: mixed_artists
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify ID3v1 specific behavior
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        artists = id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should be concatenated string with empty strings filtered out
        assert isinstance(artists, str)
        assert "Valid Artist" in artists
        assert "Another Valid Artist" in artists
        # Should not contain empty strings
        assert "" not in artists

    def test_id3v1_concatenation_with_whitespace_strings(self, temp_audio_file: Path, sample_mp3_file: Path):
        # Copy sample file to preserve existing metadata
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test ID3v1 concatenation with whitespace strings
        whitespace_artists = ["   ", "Valid Artist", "\t\t\t", "Another Valid Artist", "\n\n\n"]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: whitespace_artists
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify ID3v1 specific behavior
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        artists = id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should be concatenated string with whitespace strings filtered out
        assert isinstance(artists, str)
        assert "Valid Artist" in artists
        assert "Another Valid Artist" in artists
        # Should not contain whitespace-only strings
        assert "   " not in artists
        assert "\t\t\t" not in artists
        assert "\n\n\n" not in artists

    def test_id3v1_concatenation_with_single_value(self, temp_audio_file: Path, sample_mp3_file: Path):
        # Copy sample file to preserve existing metadata
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test ID3v1 concatenation with single value
        single_artist = ["Single Artist"]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: single_artist
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify ID3v1 specific behavior
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        artists = id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should be single string, not concatenated
        assert isinstance(artists, str)
        assert artists == "Single Artist"

    def test_id3v1_concatenation_with_very_long_values(self, temp_audio_file: Path, sample_mp3_file: Path):
        # Copy sample file to preserve existing metadata
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test ID3v1 concatenation with very long values
        long_artists = ["A" * 15, "B" * 15, "C" * 15]  # Total would be > 30 chars
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: long_artists
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify ID3v1 specific behavior
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        artists = id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should be truncated to ID3v1 limits
        assert isinstance(artists, str)
        assert len(artists) <= 30  # ID3v1 artist field is 30 characters max

    def test_id3v1_concatenation_with_unicode_values(self, temp_audio_file: Path, sample_mp3_file: Path):
        # Copy sample file to preserve existing metadata
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test ID3v1 concatenation with Unicode values
        unicode_artists = ["ASCII Artist", "Unicode Artist: 艺术家", "Emoji Artist: 🎵"]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: unicode_artists
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify ID3v1 specific behavior
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        artists = id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should be concatenated string
        assert isinstance(artists, str)
        assert "ASCII Artist" in artists
        assert "Unicode Artist: 艺术家" in artists
        assert "Emoji Artist: 🎵" in artists

    def test_id3v1_concatenation_consistency_across_fields(self, temp_audio_file: Path, sample_mp3_file: Path):
        # Copy sample file to preserve existing metadata
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test ID3v1 concatenation consistency across different fields
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"],
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: ["Album Artist One", "Album Artist Two"],
            UnifiedMetadataKey.COMPOSER: ["Composer One", "Composer Two"],
            UnifiedMetadataKey.GENRE_NAME: ["Rock", "Alternative"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify ID3v1 specific behavior for all fields
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        
        artists = id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        album_artists = id3v1_metadata.get(UnifiedMetadataKey.ALBUM_ARTISTS_NAMES)
        composers = id3v1_metadata.get(UnifiedMetadataKey.COMPOSER)
        genres = id3v1_metadata.get(UnifiedMetadataKey.GENRE_NAME)
        
        # All should be concatenated strings
        assert isinstance(artists, str)
        assert isinstance(album_artists, str)
        assert isinstance(composers, str)
        assert isinstance(genres, str)
        
        # All should contain the expected values
        assert "Artist One" in artists
        assert "Artist Two" in artists
        assert "Album Artist One" in album_artists
        assert "Album Artist Two" in album_artists
        assert "Composer One" in composers
        assert "Composer Two" in composers
        assert "Rock" in genres
        assert "Alternative" in genres
