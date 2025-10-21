

from audiometa import get_specific_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.id3v2.id3v2_metadata_getter import ID3v2MetadataGetter
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2 import ID3V2HeaderVerifier
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter


class TestId3v23:
    
    def test_semicolon_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_artists(test_file.path, ["Artist One;Artist Two;Artist Three"], in_separate_frames=False, version="2.3")
            
            assert ID3V2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 3, 0)
            
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "TPE1=Artist One;Artist Two;Artist Three" in raw_metadata

            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.ID3V2)

            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists
            
    def test_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_artists(test_file.path, ["One", "Two", "Three"], version="2.3", in_separate_frames=True)
            
            assert ID3V2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 3, 0)

            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            # Extract TPE1 value from raw_metadata string
            tpe1_lines = [line for line in raw_metadata.splitlines() if line.startswith("TPE1=")]
            tpe1_value = tpe1_lines[0][5:] if tpe1_lines else ""
            verification = {'raw_output': tpe1_value}
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.ID3V2)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists
            
    def test_mixed_separators_and_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.3") as test_file:
            ID3v2MetadataSetter.set_artists(test_file.path, ["Artist 1;Artist 2", "Artist 3"], version="2.3", in_separate_frames=True)
            
            assert ID3V2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 3, 0)

            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "TPE1=Artist 1;Artist 2" in raw_metadata
            assert "TPE1=Artist 3" in raw_metadata
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.ID3V2)
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            
    def test_multiple_title_entries_then_first_one(self):
        with TempFileWithMetadata({"title": "Initial Title"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_titles(test_file.path, ["Title One", "Title Two", "Title Three"], version="2.3", in_separate_frames=True)
            
            assert ID3V2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 3, 0)

            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            tit2_lines = [line for line in raw_metadata.splitlines() if line.startswith("TIT2=")]
            tit2_value = tit2_lines[0][5:] if tit2_lines else ""
            verification = {'raw_output': tit2_value}
            
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.ID3V2)
            
            assert isinstance(title, str)
            assert title == "Title One"