import pytest

from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestBpmDeleting:
    def test_delete_bpm_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_file.set_id3v2_bpm(120)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) == 120
        
            # Delete metadata using library API
            update_file_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) is None

    def test_delete_bpm_id3v1(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "mp3") as test_file:            
            # Deleting should fail since the field isn't supported
            with pytest.raises(MetadataNotSupportedError):
                update_file_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.ID3V1)

    def test_delete_bpm_riff(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "wav") as test_file:            
            # Deleting should fail since the field isn't supported
            with pytest.raises(MetadataNotSupportedError):
                update_file_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.RIFF)

    def test_delete_bpm_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            test_file.set_vorbis_bpm(120)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) == 120
        
            # Delete metadata using library API
            update_file_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) is None

    def test_delete_bpm_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_file.set_id3v2_bpm(120)
            test_file.set_id3v2_title("Test Title")
            test_file.set_id3v2_artist("Test Artist")
        
            # Delete only BPM using library API
            update_file_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.ID3V2)
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_bpm_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete BPM that doesn't exist
            update_file_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) is None

    def test_delete_bpm_zero(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_file.set_id3v2_bpm(0)
            # Delete the zero BPM using library API
            update_file_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) is None
