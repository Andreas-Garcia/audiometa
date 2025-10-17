from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestVorbisMultipleEntriesWriting:
    def test_write_multiple_values_creates_separate_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Set up initial metadata with single entry containing separators
            test_file.set_vorbis_genre("Rock;Alternative")
            test_file.set_vorbis_comment("Composer A;Composer B")
            test_file.set_vorbis_artist("Artist One;Artist Two;Artist Three")
            
            # Write new multiple values - should create separate Vorbis entries
            new_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["New Artist 1", "New Artist 2", "New Artist 3"],
                UnifiedMetadataKey.COMPOSER: ["New Composer X", "New Composer Y"],
                UnifiedMetadataKey.GENRES_NAMES: ["Jazz", "Fusion", "Experimental"]
            }
            
            update_file_metadata(test_file.path, new_metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Verify final state using our library functions
            final_metadata = get_merged_unified_metadata(test_file.path)
            
            # Should see separate ARTIST entries
            artists = final_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "New Artist 1" in artists
            assert "New Artist 2" in artists
            assert "New Artist 3" in artists
            
            # Should see separate COMPOSER entries
            composers = final_metadata.get(UnifiedMetadataKey.COMPOSER)
            assert isinstance(composers, list)
            assert len(composers) == 2
            assert "New Composer X" in composers
            assert "New Composer Y" in composers
            
            # Should see separate GENRE entries
            genres = final_metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            assert isinstance(genres, list)
            assert len(genres) == 3
            assert "Jazz" in genres
            assert "Fusion" in genres
            assert "Experimental" in genres