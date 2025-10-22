import pytest

from audiometa import get_specific_metadata, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.riff import RIFFMetadataSetter


@pytest.mark.integration
class TestRiffGenreParsing:

    def test_riff_genre_codes_only_semicolon(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "17; 20; 131")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["17", "20", "131"]

    def test_riff_genre_codes_only_comma(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "8, 30, 26")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["8", "30", "26"]

    def test_riff_genre_codes_only_slash(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "52/35/26")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["52", "35", "26"]

    def test_riff_genre_names_only_semicolon(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "Rock; Alternative; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_riff_genre_names_only_comma(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "Jazz, Fusion, Experimental")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Jazz", "Fusion", "Experimental"]

    def test_riff_genre_names_only_slash(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "Electronic/Dance/Ambient")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Electronic", "Dance", "Ambient"]

    def test_riff_genre_mixed_codes_and_names(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "Rock; 20; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "20", "Indie"]

    def test_riff_genre_mixed_with_pipe_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "17 | Alternative | 131")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["17 | Alternative | 131"]

    def test_riff_genre_single_code(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "17")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["17"]

    def test_riff_genre_single_name(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "Rock")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_unknown_code(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "999")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["999"]

    def test_riff_genre_empty_string(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_riff_genre_whitespace_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "   ")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_riff_genre_with_extra_whitespace(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, " Rock ; Alternative ; Indie ")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_riff_genre_multiple_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "Rock; Alternative, Indie/Experimental")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative, Indie/Experimental"]

    def test_riff_genre_duplicate_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "Rock;;;Alternative")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative"]

    def test_riff_genre_code_mode_vs_text_mode(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: ["Rock"]
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["17"]

    def test_riff_genre_very_long_text(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            long_genre = "Very Long Genre Name That Might Exceed Normal Limits And Test Edge Cases"
            RIFFMetadataSetter.set_genre_text(test_file.path, long_genre)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == [long_genre]

    def test_riff_genre_special_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            special_genre = "Rock & Roll; R&B; Hip-Hop"
            RIFFMetadataSetter.set_genre_text(test_file.path, special_genre)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock & Roll", "R&B", "Hip-Hop"]

    def test_riff_writes_single_genre_from_list(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Alternative", "Indie"]
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["17", "20", "131"]

    def test_riff_writes_genre_code_from_name(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: ["Rock"]
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["17"]

    def test_riff_writes_unknown_genre_as_code_255(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: ["Unknown Genre"]
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["12"]

    def test_riff_handles_empty_genre_list(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: []
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_future_riff_multi_genre_parsing_names(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "Rock; Alternative; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_future_riff_multi_genre_parsing_codes(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "17; 20; 131")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["17", "20", "131"]

    def test_future_riff_multi_genre_parsing_mixed(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_genre_text(test_file.path, "Rock; 20; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "20", "Indie"]
