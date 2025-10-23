
from audiometa import get_specific_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.vorbis.vorbis_metadata_setter import VorbisMetadataSetter
from audiometa.test.helpers.vorbis.vorbis_metadata_getter import VorbisMetadataGetter
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestVorbis:
    
    def test_null_value_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_artists(test_file.path, ["Artist One", "Artist Two", "Artist Three"], in_single_entry=True)
            
            raw_metadata = VorbisMetadataGetter.get_raw_metadata(test_file.path)
            assert "ARTIST=Artist One\x00Artist Two\x00Artist Three" in raw_metadata
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_semicolon_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_artists(test_file.path, ["Artist One;Artist Two;Artist Three"])
            
            raw_metadata = VorbisMetadataGetter.get_raw_metadata(test_file.path)
            assert "ARTIST=Artist One;Artist Two;Artist Three" in raw_metadata
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists
            
    def test_artists_in_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_artists(test_file.path, ["One", "Two", "Three"])
            
            raw_metadata = VorbisMetadataGetter.get_raw_metadata(test_file.path)
            assert "ARTIST=One" in raw_metadata
            assert "ARTIST=Two" in raw_metadata
            assert "ARTIST=Three" in raw_metadata
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.VORBIS)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists
            
    def test_artists_in_multiple_entries_with_different_key_casings(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_artists(test_file.path, ["Artist A", "Artist B"])
            VorbisMetadataSetter.set_artists(test_file.path, ["Artist C", "Artist D"], removing_existing=False, key_lower_case=True)
            
            raw_metadata = VorbisMetadataGetter.get_raw_metadata(test_file.path)
            assert "ARTIST=Artist A" in raw_metadata
            assert "ARTIST=Artist B" in raw_metadata
            assert "artist=Artist C" in raw_metadata
            assert "artist=Artist D" in raw_metadata
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.VORBIS)
            
            assert isinstance(artists, list)
            assert len(artists) == 4
            assert "Artist A" in artists
            assert "Artist B" in artists
            assert "Artist C" in artists
            assert "Artist D" in artists
    
    def test_mixed_single_and_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_artists(test_file.path, ["Artist 1;Artist 2", "Artist 3", "Artist 4"])
            
            raw_metadata = VorbisMetadataGetter.get_raw_metadata(test_file.path)

            assert "ARTIST=Artist 1;Artist" in raw_metadata
            assert "ARTIST=Artist 3" in raw_metadata
            assert "ARTIST=Artist 4" in raw_metadata

            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            assert "Artist 4" in artists            

    def test_multiple_title_entries_returns_first_value(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            VorbisMetadataSetter.add_title(test_file.path, "Title One")
            VorbisMetadataSetter.add_title(test_file.path, "Title Two")
            VorbisMetadataSetter.add_title(test_file.path, "Title Three")

            raw_metadata = VorbisMetadataGetter.get_raw_metadata(test_file.path)
            assert "TITLE=Title One" in raw_metadata
            assert "TITLE=Title Two" in raw_metadata
            assert "TITLE=Title Three" in raw_metadata

            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.VORBIS)
            assert title == "Title One"