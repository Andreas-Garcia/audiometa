import pytest
import subprocess

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


class TestUnicodeHandling:
    def test_unicode_characters(self):
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
