import pytest
import subprocess

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestId3v2_3Separators:
    def test_semicolon_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.3") as test_file:
            try:
                subprocess.run(["mid3v2", "--remove-all", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "mid3v2",
                    "--artist=Artist One;Artist Two;Artist Three",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("mid3v2 not available or failed to set semicolon-separated artists")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists