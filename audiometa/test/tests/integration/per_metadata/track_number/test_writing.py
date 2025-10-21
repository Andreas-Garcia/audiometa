import pytest



from audiometa import get_specific_metadata, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestTrackNumberWriting:
    def test_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_track_number = 1
            test_metadata = {UnifiedMetadataKey.TRACK_NUMBER: test_track_number}
            update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2)
            track_number = get_specific_metadata(test_file.path, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number == test_track_number

    def test_riff(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "wav") as test_file:
            test_track_number = 2
            test_metadata = {UnifiedMetadataKey.TRACK_NUMBER: test_track_number}
        
            # RIFF format raises exception for unsupported metadata
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.TRACK_NUMBER metadata not supported by RIFF format"):
                update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.RIFF)

    def test_vorbis(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "flac") as test_file:
            test_track_number = 3
            test_metadata = {UnifiedMetadataKey.TRACK_NUMBER: test_track_number}
        
            # Vorbis format raises exception for unsupported metadata
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.TRACK_NUMBER metadata not supported by this format"):
                update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.VORBIS)

    def test_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_track_number = 5
            test_metadata = {UnifiedMetadataKey.TRACK_NUMBER: test_track_number}
            update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V1)
            track_number = get_specific_metadata(test_file.path, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number == test_track_number

    def test_invalid_type_raises(self):
        from audiometa.exceptions import InvalidMetadataTypeError

        with TempFileWithMetadata({}, "mp3") as test_file:
            bad_metadata = {UnifiedMetadataKey.TRACK_NUMBER: "not-an-int"}
            with pytest.raises(InvalidMetadataTypeError):
                update_metadata(test_file.path, bad_metadata)
