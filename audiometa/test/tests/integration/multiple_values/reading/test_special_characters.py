import pytest
from pathlib import Path
import subprocess

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


class TestSpecialCharacters:
    def test_special_characters_in_entries(self):
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

