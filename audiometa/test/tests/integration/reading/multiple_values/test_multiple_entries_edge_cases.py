import pytest
from pathlib import Path
import subprocess

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestMultipleEntriesEdgeCases:
    def test_no_multiple_entries_returns_single_value(self, sample_flac_file: Path):
        # Set single artist
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Single Artist",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set single artist")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return a list with single artist
        assert isinstance(artists, list)
        assert len(artists) == 1
        assert "Single Artist" in artists

    def test_empty_metadata_returns_none(self, sample_flac_file: Path):
        # Remove all metadata
        try:
            subprocess.run(["metaflac", "--remove-all-tags", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to remove metadata")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return None for missing metadata
        assert artists is None

    def test_mixed_empty_and_valid_entries(self, sample_flac_file: Path):
        # Set artists with empty values mixed in
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set artists with empty values
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Valid Artist 1",
                "--set-tag=ARTIST=",  # Empty
                "--set-tag=ARTIST=Valid Artist 2",
                "--set-tag=ARTIST=",  # Empty
                "--set-tag=ARTIST=Valid Artist 3",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set mixed artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should filter out empty values
        assert isinstance(artists, list)
        assert len(artists) == 3  # Only valid artists
        assert "Valid Artist 1" in artists
        assert "Valid Artist 2" in artists
        assert "Valid Artist 3" in artists
        assert "" not in artists

    def test_whitespace_only_entries(self, sample_flac_file: Path):
        # Set artists with whitespace-only values
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set artists with whitespace
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Valid Artist",
                "--set-tag=ARTIST=   ",  # Whitespace only
                "--set-tag=ARTIST=\t",   # Tab only
                "--set-tag=ARTIST=\n",   # Newline only
                "--set-tag=ARTIST=Another Valid Artist",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set whitespace artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should filter out whitespace-only values
        assert isinstance(artists, list)
        assert len(artists) == 2  # Only valid artists
        assert "Valid Artist" in artists
        assert "Another Valid Artist" in artists
        
        # Check that whitespace-only values are filtered out
        for artist in artists:
            assert artist.strip() != ""

    def test_very_long_single_entry(self, sample_flac_file: Path):
        # Create very long artist name
        long_artist = "A" * 10000  # 10,000 character artist name
        
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set very long artist
            subprocess.run([
                "metaflac",
                f"--set-tag=ARTIST={long_artist}",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set long artist")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return the very long artist
        assert isinstance(artists, list)
        assert len(artists) == 1
        assert artists[0] == long_artist

    def test_special_characters_in_entries(self, sample_flac_file: Path):
        # Set artists with special characters
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set artists with special characters
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Artist & Co.",
                "--set-tag=ARTIST=Artist (feat. Guest)",
                "--set-tag=ARTIST=Artist vs. Other",
                "--set-tag=ARTIST=Artist + Collaborator",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set special character artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return all artists with special characters preserved
        assert isinstance(artists, list)
        assert len(artists) == 4
        assert "Artist & Co." in artists
        assert "Artist (feat. Guest)" in artists
        assert "Artist vs. Other" in artists
        assert "Artist + Collaborator" in artists

    def test_numeric_entries(self, sample_flac_file: Path):
        # Set artists with numeric values
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set artists with numeric values
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Artist 1",
                "--set-tag=ARTIST=Artist 2",
                "--set-tag=ARTIST=123",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set numeric artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return all artists including numeric ones
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist 1" in artists
        assert "Artist 2" in artists
        assert "123" in artists

    def test_case_sensitivity_preservation(self, sample_flac_file: Path):
        # Set artists with different cases
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set artists with different cases
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Artist One",
                "--set-tag=ARTIST=ARTIST TWO",
                "--set-tag=ARTIST=artist three",
                "--set-tag=ARTIST=ArTiSt FoUr",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set case-sensitive artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return all artists with case preserved
        assert isinstance(artists, list)
        assert len(artists) == 4
        assert "Artist One" in artists
        assert "ARTIST TWO" in artists
        assert "artist three" in artists
        assert "ArTiSt FoUr" in artists

    def test_duplicate_entries_preservation(self, sample_flac_file: Path):
        # Set duplicate artists
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set duplicate artists
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Artist One",
                "--set-tag=ARTIST=Artist Two",
                "--set-tag=ARTIST=Artist One",  # Duplicate
                "--set-tag=ARTIST=Artist Three",
                "--set-tag=ARTIST=Artist Two",  # Another duplicate
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set duplicate artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return all artists including duplicates
        assert isinstance(artists, list)
        assert len(artists) == 5  # Including duplicates
        assert artists.count("Artist One") == 2
        assert artists.count("Artist Two") == 2
        assert artists.count("Artist Three") == 1

    def test_order_preservation(self, sample_flac_file: Path):
        # Set artists in specific order
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set artists in specific order
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=First Artist",
                "--set-tag=ARTIST=Second Artist",
                "--set-tag=ARTIST=Third Artist",
                "--set-tag=ARTIST=Fourth Artist",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set ordered artists")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should return artists in the same order
        assert isinstance(artists, list)
        assert len(artists) == 4
        assert artists[0] == "First Artist"
        assert artists[1] == "Second Artist"
        assert artists[2] == "Third Artist"
        assert artists[3] == "Fourth Artist"

    def test_mixed_metadata_types(self, sample_flac_file: Path):
        # Set different types of metadata with multiple values
        try:
            subprocess.run(["metaflac", "--remove-all-tags", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set multiple artists
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Artist One",
                "--set-tag=ARTIST=Artist Two",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
            # Set multiple genres
            subprocess.run([
                "metaflac",
                "--set-tag=GENRE=Rock",
                "--set-tag=GENRE=Alternative",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
            # Set single title
            subprocess.run([
                "metaflac",
                "--set-tag=TITLE=Single Title",
                str(sample_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set mixed metadata")
        
        # Read metadata
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        
        # Artists should be multiple
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist One" in artists
        assert "Artist Two" in artists
        
        # Genres should be multiple
        genres = unified_metadata.get(UnifiedMetadataKey.GENRE_NAME)
        assert isinstance(genres, list)
        assert len(genres) == 2
        assert "Rock" in genres
        assert "Alternative" in genres
        
        # Title should be single
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        assert isinstance(title, str)
        assert title == "Single Title"

    def test_corrupted_multiple_entries(self, sample_flac_file: Path):
        # This test is more of a smoke test since we can't easily create
        # corrupted Vorbis comments without breaking the file
        
        # Read metadata from a file that might have issues
        unified_metadata = get_merged_unified_metadata(sample_flac_file)
        
        # Should handle gracefully without crashing
        assert isinstance(unified_metadata, dict)
        
        # Artists should be handled gracefully
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        if artists is not None:
            assert isinstance(artists, list)

    def test_performance_with_many_entries(self, sample_flac_file: Path):
        # Set many artists
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(sample_flac_file)], 
                          check=True, capture_output=True)
            
            # Set many artists (20 artists)
            artist_commands = []
            for i in range(20):
                artist_commands.extend(["--set-tag", f"ARTIST=Artist {i+1}"])
            
            subprocess.run(["metaflac"] + artist_commands + [str(sample_flac_file)], 
                          check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set many artists")
        
        # Read metadata multiple times to test performance
        for _ in range(5):
            unified_metadata = get_merged_unified_metadata(sample_flac_file)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should return all artists
            assert isinstance(artists, list)
            assert len(artists) == 20
