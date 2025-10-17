
import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    AudioFile,
    update_file_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestId3v23Reading:

    def test_id3v2_3_extended_metadata(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # Set maximum metadata using the script helper
            test_file.set_id3v2_3_max_metadata()
            
            metadata = get_merged_unified_metadata(test_file.path)
            title = metadata.get(UnifiedMetadataKey.TITLE)
            assert len(title) > 30  # ID3v2.3 can have longer titles than ID3v1

    def test_id3v2_3_metadata_reading_mp3(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # Set test metadata
            test_file.set_id3v2_3_max_metadata()
            
            metadata = get_merged_unified_metadata(test_file.path)
            assert isinstance(metadata, dict)
            assert UnifiedMetadataKey.TITLE in metadata
            # ID3v2.3 can have longer titles than ID3v1
            assert len(metadata[UnifiedMetadataKey.TITLE]) > 30

    def test_single_format_id3v2_3_extraction(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # Set test metadata
            test_file.set_id3v2_3_max_metadata()
            
            id3v2_3_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2_3)
            assert isinstance(id3v2_3_metadata, dict)
            assert UnifiedMetadataKey.TITLE in id3v2_3_metadata

    def test_audio_file_object_reading(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # Set test metadata
            test_file.set_id3v2_3_max_metadata()
            
            audio_file = AudioFile(test_file.path)
            
            # Test merged metadata
            metadata = get_merged_unified_metadata(audio_file)
            assert isinstance(metadata, dict)
            assert UnifiedMetadataKey.TITLE in metadata
            
            # Test specific metadata
            title = get_specific_metadata(audio_file, UnifiedMetadataKey.TITLE)
            assert isinstance(title, str)
            
            # Test single format metadata
            id3v2_3_metadata = get_single_format_app_metadata(audio_file, MetadataFormat.ID3V2_3)
            assert isinstance(id3v2_3_metadata, dict)

    def test_id3v2_3_version_specific_behavior(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # Set test metadata
            test_file.set_id3v2_3_max_metadata()
            
            # Test that ID3v2.3 specific metadata is present
            metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2_3)
            assert isinstance(metadata, dict)
            
            # ID3v2.3 uses TYER for year instead of ID3v2.4's TDRC
            # This test verifies that the library correctly handles version differences
            if UnifiedMetadataKey.YEAR in metadata:
                assert isinstance(metadata[UnifiedMetadataKey.YEAR], str)

    def test_id3v2_3_multiple_artists_support(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # Set multiple artists
            artists = ["Artist One", "Artist Two", "Artist Three"]
            test_file.set_id3v2_3_multiple_artists(artists)
            
            metadata = get_merged_unified_metadata(test_file.path)
            retrieved_artists = metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(retrieved_artists, list)
            assert len(retrieved_artists) == 3
            assert all(artist in retrieved_artists for artist in artists)

    def test_id3v2_3_error_handling(self, temp_audio_file: Path):
        # Test ID3v2.3 with unsupported file type
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.ID3V2_3)

    def test_id3v2_3_with_other_formats(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # First, add ID3v2.3 metadata
            test_file.set_id3v2_3_max_metadata()
            
            # Then add ID3v1 metadata using the library
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v1 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v1 Album"
            }
            update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Test that we can read both ID3v2.3 and ID3v1 metadata
            id3v2_3_metadata_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2_3)
            id3v1_metadata_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            
            # Verify ID3v2.3 metadata is present
            assert id3v2_3_metadata_result is not None
            assert UnifiedMetadataKey.TITLE in id3v2_3_metadata_result
            # ID3v2.3 title should be the long one from the script
            assert len(id3v2_3_metadata_result[UnifiedMetadataKey.TITLE]) > 30
            
            # Verify ID3v1 metadata is present
            assert id3v1_metadata_result is not None
            assert UnifiedMetadataKey.TITLE in id3v1_metadata_result
            assert id3v1_metadata_result[UnifiedMetadataKey.TITLE] == "ID3v1 Title"
            
            # Test merged metadata (should prioritize ID3v2.3 over ID3v1)
            merged_metadata = get_merged_unified_metadata(test_file.path)
            assert merged_metadata is not None
            assert UnifiedMetadataKey.TITLE in merged_metadata
            # Should prefer ID3v2.3 title since it's more comprehensive
            assert len(merged_metadata[UnifiedMetadataKey.TITLE]) > 30

    def test_id3v2_3_encoding_support(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # Set test metadata with special characters
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Título with Accénts",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artîst Namé"],
                UnifiedMetadataKey.ALBUM_NAME: "Albüm Naïme"
            }
            
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            # Verify the metadata was written and can be read back
            metadata = get_merged_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Título with Accénts"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Artîst Namé"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Albüm Naïme"