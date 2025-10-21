from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestBoundaryValuesSeparated:
    def test_empty_string_is_filtered_out(self, temp_audio_file: Path):
        metadata = {UnifiedMetadataKey.ARTISTS_NAMES: [""]}
        update_file_metadata(temp_audio_file, metadata)
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_single_space_is_filtered_out(self, temp_audio_file: Path):
        metadata = {UnifiedMetadataKey.ARTISTS_NAMES: [" "]}
        update_file_metadata(temp_audio_file, metadata)
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_single_tab_is_filtered_out(self, temp_audio_file: Path):
        metadata = {UnifiedMetadataKey.ARTISTS_NAMES: ["\t"]}
        update_file_metadata(temp_audio_file, metadata)
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_single_newline_is_filtered_out(self, temp_audio_file: Path):
        metadata = {UnifiedMetadataKey.ARTISTS_NAMES: ["\n"]}
        update_file_metadata(temp_audio_file, metadata)
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_single_carriage_return_is_filtered_out(self, temp_audio_file: Path):
        metadata = {UnifiedMetadataKey.ARTISTS_NAMES: ["\r"]}
        update_file_metadata(temp_audio_file, metadata)
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_null_character_is_preserved_or_filtered_consistently(self, temp_audio_file: Path):
        # Null characters may be treated differently by underlying format handlers.
        # The contract here is that passing a string containing a null will either
        # result in that value being filtered out or preserved as a single list
        # element; it must not crash.
        value = "\0"
        metadata = {UnifiedMetadataKey.ARTISTS_NAMES: [value]}
        update_file_metadata(temp_audio_file, metadata)
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        # Accept either None (filtered) or a list containing the null char
        assert artists is None or (isinstance(artists, list) and artists == [value])

    def test_255_char_value_is_written(self, temp_audio_file: Path):
        value = "A" * 255
        metadata = {UnifiedMetadataKey.ARTISTS_NAMES: [value]}
        update_file_metadata(temp_audio_file, metadata)
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert value in artists

    def test_256_char_value_is_written(self, temp_audio_file: Path):
        value = "A" * 256
        metadata = {UnifiedMetadataKey.ARTISTS_NAMES: [value]}
        update_file_metadata(temp_audio_file, metadata)
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert value in artists

    def test_1kb_value_is_written(self, temp_audio_file: Path):
        value = "A" * 1024
        metadata = {UnifiedMetadataKey.ARTISTS_NAMES: [value]}
        update_file_metadata(temp_audio_file, metadata)
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert value in artists

    def test_10kb_value_is_written(self, temp_audio_file: Path):
        value = "A" * 10240
        metadata = {UnifiedMetadataKey.ARTISTS_NAMES: [value]}
        update_file_metadata(temp_audio_file, metadata)
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert value in artists
