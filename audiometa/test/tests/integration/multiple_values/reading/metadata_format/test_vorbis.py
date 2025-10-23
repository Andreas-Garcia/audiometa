
from audiometa import get_specific_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.vorbis.vorbis_metadata_setter import VorbisMetadataSetter
from audiometa.test.helpers.vorbis.vorbis_metadata_getter import VorbisMetadataGetter
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestVorbis:

    def test_semicolon_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_artists(test_file.path, ["Artist One;Artist Two;Artist Three"])
            
            raw_metadata = VorbisMetadataGetter.get_raw_metadata(test_file.path, "ARTIST")
            assert "ARTIST=Artist One;Artist Two;Artist Three" in raw_metadata
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists
            
    def test_multiple_artists_in_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_artists(test_file.path, ["One", "Two", "Three"])
            
            raw_metadata = VorbisMetadataGetter.get_raw_metadata(test_file.path, "ARTIST")
            assert "ARTIST=One" in raw_metadata['raw_output']
            assert "ARTIST=Two" in raw_metadata['raw_output']
            assert "ARTIST=Three" in raw_metadata['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.VORBIS)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists
    
    def test_mixed_single_and_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_artists(test_file.path, ["Artist 1;Artist 2", "Artist 3", "Artist 4"])
            
            raw_metadata = VorbisMetadataGetter.get_raw_metadata(test_file.path, "ARTIST")

            assert "ARTIST=Artist 1;Artist" in raw_metadata
            assert "ARTIST=Artist 3" in raw_metadata
            assert "ARTIST=Artist 4" in raw_metadata

            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            assert "Artist 4" in artists            

    def test_multiple_comment_entries_returns_first_value(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_multiple_comments(test_file.path, ["First comment", "Second comment", "Third comment"])
            
            raw_metadata = VorbisMetadataGetter.get_raw_metadata(test_file.path)
            assert "COMMENT=First comment" in raw_metadata
            assert "COMMENT=Second comment" in raw_metadata
            assert "COMMENT=Third comment" in raw_metadata

            comment = get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(comment, str)
            assert comment == "First comment"