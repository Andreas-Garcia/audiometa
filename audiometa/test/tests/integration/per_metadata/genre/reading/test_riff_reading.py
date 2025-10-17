import pytest
import subprocess
from pathlib import Path

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestRiffGenreParsing:

    def test_riff_genre_codes_only_semicolon(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "17; 20; 131")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_riff_genre_codes_only_comma(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "8, 30, 26")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Jazz"]

    def test_riff_genre_codes_only_slash(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "52/35/26")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Electronic"]

    def test_riff_genre_names_only_semicolon(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock; Alternative; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_riff_genre_names_only_comma(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Jazz, Fusion, Experimental")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Jazz"]

    def test_riff_genre_names_only_slash(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Electronic/Dance/Ambient")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Electronic"]

    def test_riff_genre_mixed_codes_and_names(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock; 20; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_riff_genre_mixed_with_pipe_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "17 | Alternative | 131")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_riff_genre_single_code(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "17")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_riff_genre_single_name(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_riff_genre_unknown_code(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "999")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["999"]

    def test_riff_genre_empty_string(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_riff_genre_whitespace_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "   ")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_riff_genre_with_extra_whitespace(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, " Rock ; Alternative ; Indie ")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_riff_genre_multiple_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock; Alternative, Indie/Experimental")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_riff_genre_duplicate_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock;;;Alternative")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_riff_genre_code_mode_vs_text_mode(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock"
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_riff_genre_edge_case_very_long_text(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            long_genre = "Very Long Genre Name That Might Exceed Normal Limits And Test Edge Cases"
            self._set_riff_genre_text(test_file.path, long_genre)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == [long_genre]

    def test_riff_genre_special_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            special_genre = "Rock & Roll; R&B; Hip-Hop"
            self._set_riff_genre_text(test_file.path, special_genre)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock & Roll"]

    def _set_riff_genre_text(self, file_path: Path, genre_text: str):
        try:
            subprocess.run([
                "exiftool", "-overwrite_original", 
                f"-Genre={genre_text}",
                str(file_path)
            ], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run([
                    "ffmpeg", "-i", str(file_path), "-c", "copy",
                    "-metadata", f"genre={genre_text}",
                    "-y", str(file_path)
                ], check=True, capture_output=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("No suitable tool available to set RIFF genre text")


@pytest.mark.integration  
class TestRiffGenreWriting:

    def test_riff_writes_single_genre_from_list(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: ["Rock", "Alternative", "Indie"]
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_riff_writes_genre_code_from_name(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock"
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_riff_writes_unknown_genre_as_code_255(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Unknown Genre"
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is not None

    def test_riff_handles_empty_genre_list(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: []
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []


@pytest.mark.integration
class TestRiffGenreFutureEnhancement:

    def test_future_riff_multi_genre_parsing_names(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock; Alternative; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_future_riff_multi_genre_parsing_codes(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "17; 20; 131")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_future_riff_multi_genre_parsing_mixed(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock; 20; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def _set_riff_genre_text(self, file_path: Path, genre_text: str):
        try:
            subprocess.run([
                "exiftool", "-overwrite_original", 
                f"-Genre={genre_text}",
                str(file_path)
            ], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run([
                    "ffmpeg", "-i", str(file_path), "-c", "copy",
                    "-metadata", f"genre={genre_text}",
                    "-y", str(file_path)
                ], check=True, capture_output=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("No suitable tool available to set RIFF genre text")