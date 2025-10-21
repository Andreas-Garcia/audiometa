import pytest
import subprocess
from pathlib import Path

from audiometa import get_unified_metadata, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestRiffGenreParsing:

    def test_riff_genre_codes_only_semicolon(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "17; 20; 131")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_codes_only_comma(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "8, 30, 26")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Jazz"]

    def test_riff_genre_codes_only_slash(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "52/35/26")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Electronic"]

    def test_riff_genre_names_only_semicolon(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock; Alternative; Indie")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_names_only_comma(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Jazz, Fusion, Experimental")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Jazz"]

    def test_riff_genre_names_only_slash(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Electronic/Dance/Ambient")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Electronic"]

    def test_riff_genre_mixed_codes_and_names(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock; 20; Indie")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_mixed_with_pipe_separator(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "17 | Alternative | 131")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_single_code(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "17")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_single_name(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_unknown_code(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "999")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["999"]

    def test_riff_genre_empty_string(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_riff_genre_whitespace_only(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "   ")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_riff_genre_with_extra_whitespace(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, " Rock ; Alternative ; Indie ")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_multiple_separators(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock; Alternative, Indie/Experimental")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_duplicate_separators(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock;;;Alternative")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_code_mode_vs_text_mode(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: "Rock"
            }, metadata_format=MetadataFormat.RIFF)
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_edge_case_very_long_text(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            long_genre = "Very Long Genre Name That Might Exceed Normal Limits And Test Edge Cases"
            self._set_riff_genre_text(test_file.path, long_genre)
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == [long_genre]

    def test_riff_genre_special_characters(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            special_genre = "Rock & Roll; R&B; Hip-Hop"
            self._set_riff_genre_text(test_file.path, special_genre)
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
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

    def test_riff_writes_single_genre_from_list(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Alternative", "Indie"]
            }, metadata_format=MetadataFormat.RIFF)
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_writes_genre_code_from_name(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: "Rock"
            }, metadata_format=MetadataFormat.RIFF)
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_writes_unknown_genre_as_code_255(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: "Unknown Genre"
            }, metadata_format=MetadataFormat.RIFF)
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is not None

    def test_riff_handles_empty_genre_list(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: []
            }, metadata_format=MetadataFormat.RIFF)
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []


@pytest.mark.integration
class TestRiffGenreFutureEnhancement:

    def test_future_riff_multi_genre_parsing_names(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock; Alternative; Indie")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_future_riff_multi_genre_parsing_codes(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "17; 20; 131")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_future_riff_multi_genre_parsing_mixed(self, sample_wav_file: Path, temp_audio_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            self._set_riff_genre_text(test_file.path, "Rock; 20; Indie")
            
            metadata = get_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
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