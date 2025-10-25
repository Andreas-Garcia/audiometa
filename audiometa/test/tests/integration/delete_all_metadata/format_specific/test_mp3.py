import pytest

from audiometa import delete_all_metadata, get_unified_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.exceptions import MetadataFormatNotSupportedByAudioFormatError


@pytest.mark.integration
class TestDeleteAllMetadataFormatSpecificMP3:

    def test_id3v2(self):
        with TempFileWithMetadata({"title": "Test Title", "artist": "Test Artist"}, "mp3") as test_file:
            # Verify metadata is set
            id3v2_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "Test Title"

            result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.ID3V2)
            assert result is True

            # Verify ID3V2 metadata is deleted
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None

    def test_id3v1(self):
        with TempFileWithMetadata({"title": "Test Title", "artist": "Test Artist"}, "mp3") as test_file:
            # Add ID3V1 metadata
            from audiometa.test.helpers.id3v1 import ID3v1MetadataSetter
            ID3v1MetadataSetter.set_metadata(test_file.path, {"title": "ID3V1 Title", "artist": "ID3V1 Artist"})

            # Verify ID3V1 metadata is set
            id3v1_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3V1 Title"

            result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.ID3V1)
            assert result is True

            # Verify ID3V1 metadata is deleted
            id3v1_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None

    def test_vorbis(self):
        with TempFileWithMetadata({"title": "Test Title", "artist": "Test Artist"}, "mp3") as test_file:
            with pytest.raises(MetadataFormatNotSupportedByAudioFormatError):
                delete_all_metadata(test_file.path, tag_format=MetadataFormat.VORBIS)

    def test_riff(self):
        with TempFileWithMetadata({"title": "Test Title", "artist": "Test Artist"}, "mp3") as test_file:
            with pytest.raises(MetadataFormatNotSupportedByAudioFormatError):
                delete_all_metadata(test_file.path, tag_format=MetadataFormat.RIFF)