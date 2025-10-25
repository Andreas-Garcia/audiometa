import pytest

from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa import get_unified_metadata_field, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter
from audiometa.test.helpers.vorbis import VorbisMetadataSetter


@pytest.mark.integration
class TestBpmDeleting:
    def test_delete_bpm_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_bpm(test_file.path, 120)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.BPM) == 120
        
            # Delete metadata using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.BPM) is None

    def test_delete_bpm_id3v1(self):
        from audiometa.exceptions import MetadataNotSupportedByFormatError
        
        with TempFileWithMetadata({}, "mp3") as test_file:            
            # Deleting should fail since the field isn't supported
            with pytest.raises(MetadataNotSupportedByFormatError):
                update_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.ID3V1)

    def test_delete_bpm_riff(self):
        from audiometa.exceptions import MetadataNotSupportedByFormatError
        
        with TempFileWithMetadata({}, "wav") as test_file:            
            # Deleting should fail since the field isn't supported
            with pytest.raises(MetadataNotSupportedByFormatError):
                update_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.RIFF)

    def test_delete_bpm_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_bpm(test_file.path, 120)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.BPM) == 120
        
            # Delete metadata using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.BPM) is None

    def test_delete_bpm_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_bpm(test_file.path, 120)
            ID3v2MetadataSetter.set_title(test_file.path, "Test Title")
            ID3v2MetadataSetter.set_artists(test_file.path, "Test Artist")
        
            # Delete only BPM using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.ID3V2)
        
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.BPM) is None
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ARTISTS) == ["Test Artist"]

    def test_delete_bpm_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete BPM that doesn't exist
            update_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.BPM) is None

    def test_delete_bpm_zero(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_bpm(test_file.path, 0)
            # Delete the zero BPM using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.BPM: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.BPM) is None
