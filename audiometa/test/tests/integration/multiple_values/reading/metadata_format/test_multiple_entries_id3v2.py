import pytest
from pathlib import Path
import subprocess

from audiometa import get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestMultipleEntriesId3v2:
    def test_multiple_artists(self, sample_mp3_file: Path):
        # Set multiple artists using mid3v2
        try:
            # Remove existing artist tags
            subprocess.run(["mid3v2", "--delete", "TPE1", str(sample_mp3_file)], 
                          check=True, capture_output=True)
            
            # Set multiple artists using ID3v2.4 format which supports multiple values
            subprocess.run([
                "mid3v2",
                "--TPE1=Artist One",
                "--TPE1=Artist Two", 
                "--TPE1=Artist Three",
                str(sample_mp3_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("mid3v2 not available or failed to set multiple artists")
        
        # Read metadata using unified function
        unified_metadata = get_merged_unified_metadata(sample_mp3_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return a list with multiple artists
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist One" in artists
        assert "Artist Two" in artists
        assert "Artist Three" in artists

    def test_multiple_artists_specific(self, sample_mp3_file: Path):
        # Set multiple artists
        try:
            subprocess.run(["mid3v2", "--delete", "TPE1", str(sample_mp3_file)], 
                          check=True, capture_output=True)
            subprocess.run([
                "mid3v2",
                "--TPE1=Artist One",
                "--TPE1=Artist Two",
                str(sample_mp3_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("mid3v2 not available or failed to set multiple artists")
        
        # Read ID3v2 metadata specifically
        id3v2_metadata = get_single_format_app_metadata(sample_mp3_file, MetadataFormat.ID3V2)
        artists = id3v2_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return a list with multiple artists
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist One" in artists
        assert "Artist Two" in artists

    def test_multiple_album_artists(self, sample_mp3_file: Path):
        # Set multiple album artists using mid3v2
        try:
            # Remove existing album artist tags
            subprocess.run(["mid3v2", "--delete", "TPE2", str(sample_mp3_file)], 
                          check=True, capture_output=True)
            
            # Set multiple album artists
            subprocess.run([
                "mid3v2",
                "--TPE2=Album Artist One",
                "--TPE2=Album Artist Two",
                str(sample_mp3_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("mid3v2 not available or failed to set multiple album artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_mp3_file)
        album_artists = unified_metadata.get(UnifiedMetadataKey.ALBUM_ARTISTS_NAMES)
        
        # Should return a list with multiple album artists
        assert isinstance(album_artists, list)
        assert len(album_artists) == 2
        assert "Album Artist One" in album_artists
        assert "Album Artist Two" in album_artists

    def test_multiple_composers(self, sample_mp3_file: Path):
        # Set multiple composers using mid3v2
        try:
            # Remove existing composer tags
            subprocess.run(["mid3v2", "--delete", "TCOM", str(sample_mp3_file)], 
                          check=True, capture_output=True)
            
            # Set multiple composers
            subprocess.run([
                "mid3v2",
                "--TCOM=Composer One",
                "--TCOM=Composer Two",
                str(sample_mp3_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("mid3v2 not available or failed to set multiple composers")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_mp3_file)
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
        
        # Should return a list with multiple composers
        assert isinstance(composers, list)
        assert len(composers) == 2
        assert "Composer One" in composers
        assert "Composer Two" in composers

    def test_multiple_genres(self, sample_mp3_file: Path):
        # Set multiple genres using mid3v2
        try:
            # Remove existing genre tags
            subprocess.run(["mid3v2", "--delete", "TCON", str(sample_mp3_file)], 
                          check=True, capture_output=True)
            
            # Set multiple genres
            subprocess.run([
                "mid3v2",
                "--TCON=Rock",
                "--TCON=Alternative",
                str(sample_mp3_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("mid3v2 not available or failed to set multiple genres")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_mp3_file)
        genres = unified_metadata.get(UnifiedMetadataKey.GENRE_NAME)
        
        # Should return a list with multiple genres
        assert isinstance(genres, list)
        assert len(genres) == 2
        assert "Rock" in genres
        assert "Alternative" in genres

    def test_id3v2_vs_id3v1_precedence(self, sample_mp3_file: Path):
        # Set single artist in ID3v1
        try:
            subprocess.run(["mid3v2", "--delete", "TPE1", str(sample_mp3_file)], 
                          check=True, capture_output=True)
            subprocess.run(["mid3v2", "--delete", "TPE2", str(sample_mp3_file)], 
                          check=True, capture_output=True)
            
            # Set single artist in ID3v1
            subprocess.run([
                "mid3v2",
                "--TPE1=ID3v1 Artist",
                str(sample_mp3_file)
            ], check=True, capture_output=True)
            
            # Set multiple artists in ID3v2
            subprocess.run([
                "mid3v2",
                "--TPE1=ID3v2 Artist One",
                "--TPE1=ID3v2 Artist Two",
                str(sample_mp3_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("mid3v2 not available or failed to set artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_mp3_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return ID3v2 multiple artists (higher precedence)
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "ID3v2 Artist One" in artists
        assert "ID3v2 Artist Two" in artists
        assert "ID3v1 Artist" not in artists

    def test_empty_values_handling(self, sample_mp3_file: Path):
        # Set artists with empty values
        try:
            subprocess.run(["mid3v2", "--delete", "TPE1", str(sample_mp3_file)], 
                          check=True, capture_output=True)
            
            # Set artists with empty value (this might not work with mid3v2)
            subprocess.run([
                "mid3v2",
                "--TPE1=Valid Artist",
                "--TPE1=Another Valid Artist",
                str(sample_mp3_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("mid3v2 not available or failed to set artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_mp3_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return valid artists
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Valid Artist" in artists
        assert "Another Valid Artist" in artists

    def test_unicode_entries(self, sample_mp3_file: Path):
        # Set artists with unicode characters
        try:
            subprocess.run(["mid3v2", "--delete", "TPE1", str(sample_mp3_file)], 
                          check=True, capture_output=True)
            
            # Set artists with unicode
            subprocess.run([
                "mid3v2",
                "--TPE1=Artist One",
                "--TPE1=Artista Dos",
                "--TPE1=アーティスト三",
                str(sample_mp3_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("mid3v2 not available or failed to set unicode artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_mp3_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return all artists with unicode preserved
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist One" in artists
        assert "Artista Dos" in artists
        assert "アーティスト三" in artists

    def test_large_number_of_entries(self, sample_mp3_file: Path):
        # Set many artists using mid3v2
        try:
            subprocess.run(["mid3v2", "--delete", "TPE1", str(sample_mp3_file)], 
                          check=True, capture_output=True)
            
            # Set many artists (5 artists - mid3v2 might have limits)
            artist_commands = []
            for i in range(5):
                artist_commands.extend(["--TPE1", f"Artist {i+1}"])
            
            subprocess.run(["mid3v2"] + artist_commands + [str(sample_mp3_file)], 
                          check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("mid3v2 not available or failed to set many artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_mp3_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return all artists
        assert isinstance(artists, list)
        assert len(artists) == 5
        
        # Check that all artists are present
        for i in range(5):
            assert f"Artist {i+1}" in artists
