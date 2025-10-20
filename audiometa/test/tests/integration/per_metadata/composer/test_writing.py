import pytest



from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestComposerWriting:
    def test_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_composer = "Test Composer ID3v2"
            test_metadata = {UnifiedMetadataKey.COMPOSERS: test_composer}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2)
            composer = get_specific_metadata(test_file.path, UnifiedMetadataKey.COMPOSERS)
            assert composer == test_composer

    def test_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            test_composer = "Test Composer RIFF"
            test_metadata = {UnifiedMetadataKey.COMPOSERS: test_composer}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.RIFF)
            composer = get_specific_metadata(test_file.path, UnifiedMetadataKey.COMPOSERS)
            assert composer == test_composer

    def test_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            test_composer = "Test Composer Vorbis"
            test_metadata = {UnifiedMetadataKey.COMPOSERS: test_composer}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.VORBIS)
            composer = get_specific_metadata(test_file.path, UnifiedMetadataKey.COMPOSERS)
            assert composer == test_composer
