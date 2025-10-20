
from audiometa import get_specific_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.vorbis.vorbis_metadata_setter import VorbisMetadataSetter
from audiometa.test.helpers.vorbis.vorbis_metadata_verifier import VorbisMetadataVerifier
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestVorbis:

    def test_semicolon_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_multiple_artists(test_file.path, ["Artist One;Artist Two;Artist Three"])
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists
    
    def test_mixed_single_and_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_multiple_artists(test_file.path, ["Artist 1;Artist 2", "Artist 3", "Artist 4"])
            
            verification = VorbisMetadataVerifier.verify_multiple_entries_in_raw_data(test_file.path, "ARTIST", expected_count=3)
            
            assert "ARTIST=Artist 1;Artist" in verification['raw_output'] 
            assert "ARTIST=Artist 3" in verification['raw_output']
            assert "ARTIST=Artist 4" in verification['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            assert "Artist 4" in artists            

    def test_multiple_comment_entries_returns_first_value(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_multiple_comments(test_file.path, ["First comment", "Second comment", "Third comment"])

            comment = get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(comment, str)
            assert comment == "First comment"