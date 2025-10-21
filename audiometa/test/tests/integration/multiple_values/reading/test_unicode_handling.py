import pytest

from audiometa import get_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestUnicodeHandling:
    def test_unicode_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists([
                "Artist Café",
                "Artist 音乐",
                "Artist 🎵"
            ])
            
            unified_metadata = get_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist Café" in artists
            assert "Artist 音乐" in artists
            assert "Artist 🎵" in artists
