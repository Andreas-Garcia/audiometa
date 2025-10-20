import pytest

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestLyricsWriting:
    def test_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_lyrics = "These are test lyrics\nWith multiple lines\nFor testing purposes"
            test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2)
            lyrics = get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS)
            assert lyrics == test_lyrics

    def test_riff(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "wav") as test_file:
            test_lyrics = "RIFF test lyrics\nWith multiple lines\nFor testing purposes"
            test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        
            # RIFF format raises exception for unsupported metadata
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.LYRICS metadata not supported by RIFF format"):
                update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.RIFF)

    def test_vorbis(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "flac") as test_file:
            test_lyrics = "Vorbis test lyrics\nWith multiple lines\nFor testing purposes"
            test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        
            # Vorbis format raises exception for unsupported metadata
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.LYRICS metadata not supported by this format"):
                update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.VORBIS)

    def test_invalid_type_raises(self):
        from audiometa.exceptions import InvalidMetadataTypeError

        with TempFileWithMetadata({}, "mp3") as test_file:
            bad_metadata = {UnifiedMetadataKey.LYRICS: 12345}
            with pytest.raises(InvalidMetadataTypeError):
                update_file_metadata(test_file.path, bad_metadata)
