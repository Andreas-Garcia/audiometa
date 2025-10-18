from audiometa import get_merged_unified_metadata, get_specific_metadata, update_file_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestVorbisMixed:
    def test_mixed_single_and_multiple_values(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists(["Artist 1;Artist 2", "Artist 3", "Artist 4"])
            verification = test_file.verify_vorbis_multiple_entries_in_raw_data("ARTIST", expected_count=3)
            
            assert "ARTIST=Artist 1;Artist" in verification['raw_output'] 
            assert "ARTIST=Artist 3" in verification['raw_output']
            assert "ARTIST=Artist 4" in verification['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            assert "Artist 4" in artists