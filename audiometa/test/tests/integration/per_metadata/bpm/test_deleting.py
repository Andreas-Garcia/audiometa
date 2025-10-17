import pytest

from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestBpmDeleting:
    def test_delete_bpm_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set metadata using helper method
            test_file.set_id3v2_bpm(120)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) == 120
        
            # Delete metadata using helper method
            test_file.delete_id3v2_bpm()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) is None

    def test_delete_bpm_id3v1(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "mp3") as test_file:
            # ID3v1 doesn't support BPM, so writing should fail
            with pytest.raises(MetadataNotSupportedError):
                test_file.set_id3v1_bpm(120)
            
            # Deleting should also fail since the field isn't supported
            with pytest.raises(MetadataNotSupportedError):
                test_file.delete_id3v1_bpm()

    def test_delete_bpm_riff(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "wav") as test_file:
            # RIFF doesn't support BPM, so writing should fail
            with pytest.raises(MetadataNotSupportedError):
                test_file.set_riff_bpm(120)
            
            # Deleting should also fail since the field isn't supported
            with pytest.raises(MetadataNotSupportedError):
                test_file.delete_riff_bpm()

    def test_delete_bpm_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Set metadata using helper method
            test_file.set_vorbis_bpm(120)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) == 120
        
            # Delete metadata using helper method
            test_file.delete_vorbis_bpm()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) is None

    def test_delete_bpm_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set multiple metadata fields using helper methods
            test_file.set_id3v2_bpm(120)
            test_file.set_id3v2_title("Test Title")
            test_file.set_id3v2_artist("Test Artist")
        
            # Delete only BPM using helper method
            test_file.delete_id3v2_bpm()
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_bpm_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete BPM that doesn't exist
            test_file.delete_id3v2_bpm()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) is None

    def test_delete_bpm_zero(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set zero BPM using helper method
            test_file.set_id3v2_bpm(0)
            # Delete the zero BPM
            test_file.delete_id3v2_bpm()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM) is None
