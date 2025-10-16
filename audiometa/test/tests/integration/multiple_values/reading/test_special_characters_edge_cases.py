import pytest
from pathlib import Path
import subprocess

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


class TestSpecialCharactersEdgeCases:
    def test_special_characters_in_entries(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist & Co.",
                    "--set-tag=ARTIST=Artist (feat. Guest)",
                    "--set-tag=ARTIST=Artist vs. Other",
                    "--set-tag=ARTIST=Artist + Collaborator",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set special character artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 4
            assert "Artist & Co." in artists
            assert "Artist (feat. Guest)" in artists
            assert "Artist vs. Other" in artists
            assert "Artist + Collaborator" in artists

    def test_numeric_entries(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist 1",
                    "--set-tag=ARTIST=Artist 2",
                    "--set-tag=ARTIST=123",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set numeric artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist 1" in artists
            assert "Artist 2" in artists
            assert "123" in artists

    def test_case_sensitivity_preservation(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One",
                    "--set-tag=ARTIST=ARTIST TWO",
                    "--set-tag=ARTIST=artist three",
                    "--set-tag=ARTIST=ArTiSt FoUr",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set case-sensitive artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 4
            assert "Artist One" in artists
            assert "ARTIST TWO" in artists
            assert "artist three" in artists
            assert "ArTiSt FoUr" in artists

    def test_duplicate_entries_preservation(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One",
                    "--set-tag=ARTIST=Artist Two",
                    "--set-tag=ARTIST=Artist One",  # Duplicate
                    "--set-tag=ARTIST=Artist Three",
                    "--set-tag=ARTIST=Artist Two",  # Another duplicate
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set duplicate artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 5  # Including duplicates
            assert artists.count("Artist One") == 2
            assert artists.count("Artist Two") == 2
            assert artists.count("Artist Three") == 1

    def test_order_preservation(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=First Artist",
                    "--set-tag=ARTIST=Second Artist",
                    "--set-tag=ARTIST=Third Artist",
                    "--set-tag=ARTIST=Fourth Artist",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set ordered artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 4
            assert artists[0] == "First Artist"
            assert artists[1] == "Second Artist"
            assert artists[2] == "Third Artist"
            assert artists[3] == "Fourth Artist"

    def test_unicode_characters(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist Café",
                    "--set-tag=ARTIST=Artist 音乐",
                    "--set-tag=ARTIST=Artist 🎵",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set unicode artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist Café" in artists
            assert "Artist 音乐" in artists
            assert "Artist 🎵" in artists

    def test_separator_in_artist_name(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist & Co.;Artist vs. Other;Artist + Collaborator",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set special character artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist & Co." in artists
            assert "Artist vs. Other" in artists
            assert "Artist + Collaborator" in artists

    def test_very_long_single_entry(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            long_artist = "A" * 10000  # 10,000 character artist name
            
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    f"--set-tag=ARTIST={long_artist}",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set long artist")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 1
            assert artists[0] == long_artist

    def test_mixed_metadata_types(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-all-tags", str(test_file.path)], 
                              check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One",
                    "--set-tag=ARTIST=Artist Two",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=GENRE=Rock",
                    "--set-tag=GENRE=Alternative",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=TITLE=Single Title",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set mixed metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Artist One" in artists
            assert "Artist Two" in artists
            
            genres = unified_metadata.get(UnifiedMetadataKey.GENRE_NAME)
            assert isinstance(genres, list)
            assert len(genres) == 2
            assert "Rock" in genres
            assert "Alternative" in genres
            
            title = unified_metadata.get(UnifiedMetadataKey.TITLE)
            assert isinstance(title, str)
            assert title == "Single Title"

    def test_corrupted_multiple_entries(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            unified_metadata = get_merged_unified_metadata(test_file.path)
            
            assert isinstance(unified_metadata, dict)
            
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            if artists is not None:
                assert isinstance(artists, list)