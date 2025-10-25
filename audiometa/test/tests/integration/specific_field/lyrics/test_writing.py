import pytest

from audiometa import update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2.id3v2_metadata_getter import ID3v2MetadataGetter
from audiometa.test.helpers.riff.riff_metadata_getter import RIFFMetadataGetter

@pytest.mark.integration
class TestLyricsWriting:
    def test_id3v2_3(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_lyrics = "These are test lyrics\nWith multiple lines\nFor testing purposes"
            test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
            update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path, version='2.3')
            assert f"USLT={test_lyrics}" in raw_metadata

    def test_id3v2_4(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_lyrics = "These are test lyrics\nWith multiple lines\nFor testing purposes"
            test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
            update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path, version='2.4')
            assert f"USLT={test_lyrics}" in raw_metadata
            
    def test_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            test_lyrics = "RIFF test lyrics\nWith multiple lines\nFor testing purposes"
            test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
            update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.RIFF)
            
            raw_metadata = RIFFMetadataGetter.get_raw_metadata(test_file.path)
            assert f"USLT={test_lyrics}" in raw_metadata

    def test_vorbis(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "flac") as test_file:
            test_lyrics = "Vorbis test lyrics\nWith multiple lines\nFor testing purposes"
            test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        
            # Vorbis format raises exception for unsupported metadata
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.LYRICS metadata not supported by this format"):
                update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.VORBIS)

    def test_invalid_type_raises(self):
        from audiometa.exceptions import InvalidMetadataTypeError

        with TempFileWithMetadata({}, "mp3") as test_file:
            bad_metadata = {UnifiedMetadataKey.LYRICS: 12345}
            with pytest.raises(InvalidMetadataTypeError):
                update_metadata(test_file.path, bad_metadata)
