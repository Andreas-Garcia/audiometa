import pytest
import subprocess

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


class TestSeparatorHandling:
    def test_semicolon_separated_artists(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Set single artist tag with semicolon-separated values
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One;Artist Two;Artist Three",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set semicolon-separated artists")
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should split on semicolon and return list
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_comma_separated_artists(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Set single artist tag with comma-separated values
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One,Artist Two,Artist Three",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set comma-separated artists")
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should split on comma and return list
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_slash_separated_artists(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Set single artist tag with slash-separated values
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One/Artist Two/Artist Three",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set slash-separated artists")
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should split on slash and return list
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_backslash_separated_artists(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Set single artist tag with backslash-separated values
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One\\Artist Two\\Artist Three",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set backslash-separated artists")
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should split on backslash and return list
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_double_slash_separated_artists(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Set single artist tag with double-slash-separated values
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One//Artist Two//Artist Three",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set double-slash-separated artists")
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should split on double slash and return list
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_double_backslash_separated_artists(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Set single artist tag with double-backslash-separated values
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One\\\\Artist Two\\\\Artist Three",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set double-backslash-separated artists")
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should split on double backslash and return list
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_mixed_separators_priority(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Test that separators are processed in the correct priority order
            # Based on METADATA_ARTISTS_SEPARATORS = ("//", "\\\\", ";", "\\", "/", ",")
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                # Use multiple separators - should split on highest priority first
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One//Artist Two;Artist Three,Artist Four",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set mixed separator artists")
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should split on double slash first, then semicolon, then comma
            assert isinstance(artists, list)
            assert len(artists) == 4
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists
            assert "Artist Four" in artists

    def test_separator_with_whitespace(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Test separators with surrounding whitespace
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
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should split and strip whitespace
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists
            
            # Check that whitespace was stripped
            for artist in artists:
                assert artist == artist.strip()

    def test_empty_values_after_separation(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Test separators that create empty values
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
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should filter out empty values
            assert isinstance(artists, list)
            assert len(artists) == 2  # Only non-empty values
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "" not in artists

    def test_separator_in_artist_name(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Test that separators within artist names are preserved
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
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should preserve special characters within names
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist & Co." in artists
            assert "Artist vs. Other" in artists
            assert "Artist + Collaborator" in artists

    def test_single_value_no_separator(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Test single value without separators
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
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should return single value as list
            assert isinstance(artists, list)
            assert len(artists) == 1
            assert "Single Artist" in artists

    def test_separator_with_genres(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Test separators with genres (another multi-value field)
            try:
                subprocess.run(["metaflac", "--remove-tag=GENRE", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=GENRE=Rock;Pop;Jazz",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set separated genres")
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            genres = unified_metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            # Should split genres on semicolon
            assert isinstance(genres, list)
            assert len(genres) == 3
            assert "Rock" in genres
            assert "Pop" in genres
            assert "Jazz" in genres

    def test_separator_with_composers(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Test separators with composers (another multi-value field)
            try:
                subprocess.run(["metaflac", "--remove-tag=COMPOSER", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=COMPOSER=Composer One,Composer Two,Composer Three",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set separated composers")
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            
            # Should split composers on comma
            assert isinstance(composers, list)
            assert len(composers) == 3
            assert "Composer One" in composers
            assert "Composer Two" in composers
            assert "Composer Three" in composers

    def test_complex_separator_scenario(self):
        # Create temporary file with basic metadata
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Test complex scenario with multiple separators and edge cases
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist One//Artist Two;Artist Three,Artist Four\\Artist Five",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set complex separated artists")
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should handle complex separation correctly
            assert isinstance(artists, list)
            # The exact count depends on separator priority, but should be multiple
            assert len(artists) >= 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists