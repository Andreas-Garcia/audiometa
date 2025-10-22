import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter
from audiometa.test.helpers.id3v2.id3v2_metadata_getter import ID3v2MetadataGetter
from audiometa.test.helpers.vorbis.vorbis_metadata_getter import VorbisMetadataGetter
from audiometa.test.helpers.vorbis.vorbis_metadata_setter import VorbisMetadataSetter


@pytest.mark.integration
class TestID3v2GenreReadingStrategies:

    def test_single_entry_codes_without_separators_id3v2(self):
        """Test single genre entry with codes without separators: '(17)(6)' -> ['Rock', 'Grunge']"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            # Set genre with codes without separators
            ID3v2MetadataSetter.set_genres(test_file.path, ["(17)(6)"], version="2.4")
            
            # Validate raw metadata
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "(17)(6)" in raw_metadata

            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Grunge"]
            
    def test_single_entry_codes_without_separators_vorbis(self):
        """Test single genre entry with codes without separators in Vorbis: '(17)(6)' -> ['Rock', 'Grunge']"""
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Set genre with codes without separators
            VorbisMetadataSetter.set_genres(test_file.path, ["(17)(6)"])
            
            # Validate raw metadata
            raw_metadata = VorbisMetadataGetter.get_raw_metadata(test_file.path)
            assert "(17)(6)" in raw_metadata

            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            assert genres == ["Rock", "Grunge"]
            
    def test_code_text_then_text_part_even_if_different(self):
        """Test code+text: '(17)Rock' -> 'Rock' (text part only)"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            # Set genre with code+text
            ID3v2MetadataSetter.set_genres(test_file.path, ["(17)Rock"], version="2.4")
            
            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_single_entry_code_text_without_separators(self):
        """Test single genre entry with code+text without separators: '(17)Rock(6)Blues' -> ['Rock', 'Grunge']"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            # Set genre with code+text without separators
            ID3v2MetadataSetter.set_genres(test_file.path, ["(17)Rock(6)Blues"], version="2.4")
            
            # Validate raw metadata
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            
            assert "(17)Rock(6)Blues" in raw_metadata
            
            # assert no null separators in raw metadata genre
            assert '\x00' not in raw_metadata
            
            
            
            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Blues"]

    def test_one_code_and_one_code_text_in_single_entry(self):
        """Test one code and one code+text: '(17)', '(6)Grunge' -> ['Rock', 'Grunge']"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            # Set genre with one code and one code+text
            ID3v2MetadataSetter.set_genres(test_file.path, ["(17)(6)Grunge"], version="2.4")
            
            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Grunge"]
            
    def test_one_code_and_one_code_text_in_multi_entries(self):
        """Test one code and one code+text: '(17)', '(6)Grunge' -> ['Rock', 'Grunge']"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            # Set genre with one code and one code+text
            ID3v2MetadataSetter.set_genres(test_file.path, ["(17)", "(6)Grunge"], in_separate_frames=True, version="2.4")
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)

            assert "TCON(encoding=<Encoding.UTF8: 3>, text=['(17)'])" in raw_metadata
            assert "TCON(encoding=<Encoding.UTF8: 3>, text=['(6)Grunge'])" in raw_metadata

            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Grunge"]

    def test_single_entry_text_with_slash_separators(self):
        """Test single genre entry with text with slash separators: 'Rock/Blues' -> ['Rock', 'Blues']"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            # Set genre with text with separators
            ID3v2MetadataSetter.set_genres(test_file.path, ["Rock/Blues"], version="2.4")
            
            # Validate raw metadata
            assert 'Rock/Blues' in ID3v2MetadataGetter.get_raw_metadata(test_file.path)

            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Blues"]

    def test_single_entry_text_with_semicolon_separators(self):
        """Test single genre entry with text with semicolon separators: 'Rock; Alternative' -> ['Rock', 'Alternative']"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            # Set genre with text with separators
            ID3v2MetadataSetter.set_genres(test_file.path, ["Rock; Alternative"], version="2.4")
            
            # Validate raw metadata
            assert 'Rock; Alternative' in ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            
            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative"]

    def test_multi_codes_with_text_with_separators(self):
        """Test single genre entry with mixed separators: '(17)Rock/(6)Blues' -> ['Rock', 'Blues']"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            # Set genre with mixed separators
            ID3v2MetadataSetter.set_genres(test_file.path, ["(17)Rock/(6)Blues"], version="2.4")
            
            # Validate raw metadata
            assert '(17)Rock/(6)Blues' in ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            
            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Blues"]

    def test_multiple_entries_return_as_is(self):
        """Test multiple genre entries: separate TCON frames, return as-is without parsing"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            # Set multiple genres in separate frames
            ID3v2MetadataSetter.set_genres(test_file.path, ["Rock/Grunge", "Blues"], in_separate_frames=True, version="2.4")
            
            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            # Should return as-is without parsing
            assert set(genres) == {"Rock/Grunge", "Blues"}

    def test_code_to_name_conversion_with_unknown_code(self):
        """Test code conversion: '(17)' -> 'Rock', (unknown code) -> unknown code in parentheses should be converted as 'Unknown'"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            # Set genre with known and unknown codes
            ID3v2MetadataSetter.set_genres(test_file.path, ["(17)", "(999)"], version="2.4")
            
            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "(999)"]

    def test_code_text_uses_text_part(self):
        """Test code+text: '(199)Rock' -> 'Rock' (text part only)"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            # Set genre with code+text
            ID3v2MetadataSetter.set_genres(test_file.path, ["(199)Rock"], version="2.4")
            
            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_unique_genre_names(self):
        """Test unique genres: duplicates removed"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            # Set genre with duplicates
            ID3v2MetadataSetter.set_genres(test_file.path, ["Rock/Rock"], version="2.4")
            
            # Read via API
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_edge_cases_empty_string(self):
        """Test edge case: empty string"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            ID3v2MetadataSetter.set_genres(test_file.path, [""], version="2.4")
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            assert genres is None

    def test_edge_cases_whitespace_only(self):
        """Test edge case: whitespace only"""
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            ID3v2MetadataSetter.set_genres(test_file.path, ["   "], version="2.4")
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            assert genres is None