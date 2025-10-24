
from audiometa import get_unified_metadata, get_unified_metadata_field
from audiometa.utils import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestEmptyWhitespaceHandling:
    def test_no_multiple_entries_returns_single_value(self):

        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_artist("Single Artist")
            
            artists = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ARTISTS, MetadataFormat.VORBIS)
            
            assert isinstance(artists, list)
            assert len(artists) == 1
            assert "Single Artist" in artists

    def test_empty_metadata_returns_none(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.delete_vorbis_all()
            
            artists = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ARTISTS, MetadataFormat.VORBIS)
            
            assert artists is None

    def test_mixed_empty_and_valid_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists(["Valid Artist 1", "", "Valid Artist 2", "", "Valid Artist 3"])
            
            unified_metadata = get_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS)
            
            assert isinstance(artists, list)
            assert len(artists) == 3  # Only valid artists
            assert "Valid Artist 1" in artists
            assert "Valid Artist 2" in artists
            assert "Valid Artist 3" in artists
            assert "" not in artists

    def test_whitespace_only_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists(["Valid Artist", "   ", "\t", "\n", "Another Valid Artist"])
            
            artists = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ARTISTS, MetadataFormat.VORBIS)
            
            assert isinstance(artists, list)
            assert len(artists) == 2  # Only valid artists
            assert "Valid Artist" in artists
            assert "Another Valid Artist" in artists
            
            for artist in artists:
                assert artist.strip() != ""

    def test_empty_values_after_separation(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists(["Artist One;;Artist Two;"])
            
            artists = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ARTISTS, MetadataFormat.VORBIS)
            
            assert isinstance(artists, list)
            assert len(artists) == 2  # Only non-empty values
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "" not in artists

    def test_whitespace_around_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists(["Artist One ; Artist Two ; Artist Three"])
            
            artists = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ARTISTS, MetadataFormat.VORBIS)
            
            assert artists == ["Artist One", "Artist Two", "Artist Three"]

    def test_only_whitespace_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists(["   ", "\t", "\n"])
            
            artists = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ARTISTS, MetadataFormat.VORBIS)
            
            assert artists is None

    def test_mixed_whitespace_and_valid_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists(["Valid Artist", "   ", "Another Valid Artist", "\t"])
            
            artists = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ARTISTS, MetadataFormat.VORBIS)
            
            assert artists == ["Valid Artist", "Another Valid Artist"]