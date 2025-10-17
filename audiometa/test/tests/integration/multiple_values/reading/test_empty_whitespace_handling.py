import pytest
import subprocess

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.test_helpers import TempFileWithMetadata


class TestEmptyWhitespaceHandling:
    def test_no_multiple_entries_returns_single_value(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Single Artist",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set single artist")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 1
            assert "Single Artist" in artists

    def test_empty_metadata_returns_none(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-all-tags", str(test_file.path)], 
                              check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to remove metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert artists is None

    def test_mixed_empty_and_valid_entries(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Valid Artist 1",
                    "--set-tag=ARTIST=",  # Empty
                    "--set-tag=ARTIST=Valid Artist 2",
                    "--set-tag=ARTIST=",  # Empty
                    "--set-tag=ARTIST=Valid Artist 3",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set mixed artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3  # Only valid artists
            assert "Valid Artist 1" in artists
            assert "Valid Artist 2" in artists
            assert "Valid Artist 3" in artists
            assert "" not in artists

    def test_whitespace_only_entries(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Valid Artist",
                    "--set-tag=ARTIST=   ",  # Whitespace only
                    "--set-tag=ARTIST=\t",   # Tab only
                    "--set-tag=ARTIST=\n",   # Newline only
                    "--set-tag=ARTIST=Another Valid Artist",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set whitespace artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 2  # Only valid artists
            assert "Valid Artist" in artists
            assert "Another Valid Artist" in artists
            
            for artist in artists:
                assert artist.strip() != ""

    def test_empty_values_after_separation(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One;;Artist Two;",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set empty-separated artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 2  # Only non-empty values
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "" not in artists

    def test_whitespace_around_separators(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One ; Artist Two , Artist Three",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set whitespace-separated artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists
            
            for artist in artists:
                assert artist == artist.strip()

    def test_only_whitespace_entries(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=   ",
                    "--set-tag=ARTIST=\t",
                    "--set-tag=ARTIST=\n",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set whitespace-only artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should return None when all values are whitespace-only
            assert artists is None

    def test_mixed_whitespace_and_valid_entries(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Valid Artist",
                    "--set-tag=ARTIST=   ",
                    "--set-tag=ARTIST=Another Valid Artist",
                    "--set-tag=ARTIST=\t",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set mixed whitespace artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 2  # Only valid artists
            assert "Valid Artist" in artists
            assert "Another Valid Artist" in artists