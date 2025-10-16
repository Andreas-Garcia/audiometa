import pytest
from pathlib import Path
import subprocess
import os

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_full_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestMultipleEntriesVorbis:
    def test_multiple_artists_reading(self, sample_flac_file: Path):
        # Set multiple artists using the existing script
        script_path = Path(__file__).parent.parent.parent.parent.parent.parent.parent / "audiometa" / "test" / "data" / "scripts" / "set-artists-One-Two-Three-vorbis.sh"
        
        # Make script executable and run it
        os.chmod(script_path, 0o755)
        result = subprocess.run([str(script_path), str(sample_flac_file)], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            pytest.skip(f"Failed to set multiple artists: {result.stderr}")
        
        # Read metadata using unified function
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return a list with multiple artists
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "One" in artists
        assert "Two" in artists
        assert "Three" in artists

    def test_multiple_artists_vorbis_specific(self, sample_flac_file: Path):
        # Set multiple artists
        script_path = Path(__file__).parent.parent.parent.parent.parent.parent.parent / "audiometa" / "test" / "data" / "scripts" / "set-artists-One-Two-Three-vorbis.sh"
        os.chmod(script_path, 0o755)
        result = subprocess.run([str(script_path), str(sample_flac_file)], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            pytest.skip(f"Failed to set multiple artists: {result.stderr}")
        
        # Read Vorbis metadata specifically
        vorbis_metadata = get_single_format_app_metadata(sample_flac_file, MetadataFormat.VORBIS)
        artists = vorbis_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return a list with multiple artists
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "One" in artists
        assert "Two" in artists
        assert "Three" in artists

    def test_multiple_artists_full_metadata(self, sample_flac_file: Path):
        # Set multiple artists
        script_path = Path(__file__).parent.parent.parent.parent.parent.parent.parent / "audiometa" / "test" / "data" / "scripts" / "set-artists-One-Two-Three-vorbis.sh"
        os.chmod(script_path, 0o755)
        result = subprocess.run([str(script_path), str(sample_flac_file)], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            pytest.skip(f"Failed to set multiple artists: {result.stderr}")
        
        # Read full metadata
        full_metadata = get_full_metadata(sample_flac_file)
        
        # Check unified metadata
        unified_artists = full_metadata['unified_metadata'].get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(unified_artists, list)
        assert len(unified_artists) == 3
        assert "One" in unified_artists
        assert "Two" in unified_artists
        assert "Three" in unified_artists
        
        # Check Vorbis-specific metadata
        vorbis_artists = full_metadata['format_metadata']['vorbis'].get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(vorbis_artists, list)
        assert len(vorbis_artists) == 3
        assert "One" in vorbis_artists
        assert "Two" in vorbis_artists
        assert "Three" in vorbis_artists

    def test_multiple_genres_reading(self, sample_flac_file: Path):
        # Set multiple genres using metaflac
        try:
            # Remove existing genre tags
            subprocess.run(["metaflac", "--remove-tag=GENRE", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set multiple genres
            subprocess.run([
                "metaflac",
                "--set-tag=GENRE=Rock",
                "--set-tag=GENRE=Alternative",
                "--set-tag=GENRE=Indie",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set multiple genres")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        genres = unified_metadata.get(UnifiedMetadataKey.GENRE_NAME)
        
        # Should return a list with multiple genres
        assert isinstance(genres, list)
        assert len(genres) == 3
        assert "Rock" in genres
        assert "Alternative" in genres
        assert "Indie" in genres

    def test_multiple_composers_reading(self, sample_flac_file: Path):
        # Set multiple composers using metaflac
        try:
            # Remove existing composer tags
            subprocess.run(["metaflac", "--remove-tag=COMPOSER", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set multiple composers
            subprocess.run([
                "metaflac",
                "--set-tag=COMPOSER=Composer One",
                "--set-tag=COMPOSER=Composer Two",
                "--set-tag=COMPOSER=Composer Three",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set multiple composers")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
        
        # Should return a list with multiple composers
        assert isinstance(composers, list)
        assert len(composers) == 3
        assert "Composer One" in composers
        assert "Composer Two" in composers
        assert "Composer Three" in composers

    def test_multiple_album_artists_reading(self, sample_flac_file: Path):
        # Set multiple album artists using metaflac
        try:
            # Remove existing album artist tags
            subprocess.run(["metaflac", "--remove-tag=ALBUMARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set multiple album artists
            subprocess.run([
                "metaflac",
                "--set-tag=ALBUMARTIST=Album Artist One",
                "--set-tag=ALBUMARTIST=Album Artist Two",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set multiple album artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        album_artists = unified_metadata.get(UnifiedMetadataKey.ALBUM_ARTISTS_NAMES)
        
        # Should return a list with multiple album artists
        assert isinstance(album_artists, list)
        assert len(album_artists) == 2
        assert "Album Artist One" in album_artists
        assert "Album Artist Two" in album_artists

    def test_multiple_performers_reading(self, sample_flac_file: Path):
        # Set multiple performers using metaflac
        try:
            # Remove existing performer tags
            subprocess.run(["metaflac", "--remove-tag=PERFORMER", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set multiple performers
            subprocess.run([
                "metaflac",
                "--set-tag=PERFORMER=Performer One",
                "--set-tag=PERFORMER=Performer Two",
                "--set-tag=PERFORMER=Performer Three",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set multiple performers")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        performers = unified_metadata.get(UnifiedMetadataKey.MUSICIANS)
        
        # Should return a list with multiple performers
        assert isinstance(performers, list)
        assert len(performers) == 3
        assert "Performer One" in performers
        assert "Performer Two" in performers
        assert "Performer Three" in performers

    def test_multiple_comments_reading(self, sample_flac_file: Path):
        # Set multiple comments using metaflac
        try:
            # Remove existing comment tags
            subprocess.run(["metaflac", "--remove-tag=COMMENT", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set multiple comments
            subprocess.run([
                "metaflac",
                "--set-tag=COMMENT=First comment",
                "--set-tag=COMMENT=Second comment",
                "--set-tag=COMMENT=Third comment",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set multiple comments")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        comments = unified_metadata.get(UnifiedMetadataKey.COMMENT)
        
        # COMMENT field should return the first value as a string (not a list)
        assert isinstance(comments, str)
        assert comments == "First comment"  # Should return the first value

    def test_empty_values_in_multiple_entries(self, sample_flac_file: Path):
        # Set multiple artists with some empty values
        try:
            # Remove existing artist tags
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set multiple artists with empty value
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Valid Artist",
                "--set-tag=ARTIST=",  # Empty value
                "--set-tag=ARTIST=Another Valid Artist",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set artists with empty values")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should filter out empty values
        assert isinstance(artists, list)
        assert len(artists) == 2  # Empty value should be filtered out
        assert "Valid Artist" in artists
        assert "Another Valid Artist" in artists
        assert "" not in artists

    def test_large_number_of_entries(self, sample_flac_file: Path):
        # Set many artists using metaflac
        try:
            # Remove existing artist tags
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set many artists (10 artists)
            artist_commands = []
            for i in range(10):
                artist_commands.extend(["--set-tag", f"ARTIST=Artist {i+1}"])
            
            subprocess.run(["metaflac"] + artist_commands + [str(sample_flac_file)], 
                          check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set many artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return all artists
        assert isinstance(artists, list)
        assert len(artists) == 10
        
        # Check that all artists are present
        for i in range(10):
            assert f"Artist {i+1}" in artists

    def test_mixed_case_tags(self, sample_flac_file: Path):
        # Set artists with different case variations
        try:
            # Remove existing artist tags
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set artists with different cases
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Artist One",
                "--set-tag=artist=Artist Two",  # lowercase
                "--set-tag=Artist=Artist Three",  # mixed case
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set mixed case artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return all artists (Vorbis is case-insensitive)
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist One" in artists
        assert "Artist Two" in artists
        assert "Artist Three" in artists

    def test_unicode_entries(self, sample_flac_file: Path):
        # Set artists with unicode characters
        try:
            # Remove existing artist tags
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set artists with unicode
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Artist One",
                "--set-tag=ARTIST=Artista Dos",  # Spanish
                "--set-tag=ARTIST=アーティスト三",  # Japanese
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set unicode artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return all artists with unicode preserved
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist One" in artists
        assert "Artista Dos" in artists
        assert "アーティスト三" in artists

    def test_very_long_entries(self, sample_flac_file: Path):
        # Create very long artist names
        long_artist1 = "A" * 1000  # 1000 character artist name
        long_artist2 = "B" * 500   # 500 character artist name
        
        try:
            # Remove existing artist tags
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set very long artists
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Short Artist",
                f"--set-tag=ARTIST={long_artist1}",
                f"--set-tag=ARTIST={long_artist2}",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set long artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return all artists including very long ones
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Short Artist" in artists
        assert long_artist1 in artists
        assert long_artist2 in artists

    def test_duplicate_entries_handling(self, sample_flac_file: Path):
        # Set duplicate artists
        try:
            # Remove existing artist tags
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set duplicate artists
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Artist One",
                "--set-tag=ARTIST=Artist Two",
                "--set-tag=ARTIST=Artist One",  # Duplicate
                "--set-tag=ARTIST=Artist Three",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set duplicate artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return all artists including duplicates
        # (Vorbis allows duplicates, so we should preserve them)
        assert isinstance(artists, list)
        assert len(artists) == 4  # Including the duplicate
        assert artists.count("Artist One") == 2  # Should have the duplicate
        assert "Artist Two" in artists
        assert "Artist Three" in artists
