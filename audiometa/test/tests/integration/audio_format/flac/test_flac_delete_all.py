import pytest

from audiometa import delete_all_metadata, get_unified_metadata
from audiometa.test.helpers.vorbis.vorbis_metadata_setter import VorbisMetadataSetter
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter
from audiometa.test.helpers.id3v1 import ID3v1MetadataSetter
from audiometa.exceptions import MetadataFormatNotSupportedByAudioFormatError


@pytest.mark.integration
class TestDeleteAllMetadataFormatSpecificFLAC:
    
    def test_delete_all_metadata_formats_flac(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Add ID3v1 metadata using external tools for proper test isolation
            ID3v1MetadataSetter.set_metadata(test_file.path, {"title": "ID3v1 Title", "artist": "ID3v1 Artist"})
            
            # Verify ID3v1 has metadata before adding ID3v2
            id3v1_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            
            # Add ID3v2 metadata using external tools for proper test isolation
            ID3v2MetadataSetter.set_metadata(test_file.path, {"title": "ID3v2 Title", "artist": "ID3v2 Artist"})
            
            # Verify ID3v2 has metadata
            id3v2_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Add Vorbis metadata using external tools for proper test isolation
            VorbisMetadataSetter.add_title(test_file.path, "Vorbis Title")
            
            # Verify Vorbis has metadata
            vorbis_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.VORBIS)
            assert vorbis_before.get(UnifiedMetadataKey.TITLE) == "Vorbis Title"
            
            # Delete all metadata
            result = delete_all_metadata(test_file.path)
            assert result is True
            
            # Verify both formats were deleted
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            id3v1_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            vorbis_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.VORBIS)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None
            assert vorbis_after.get(UnifiedMetadataKey.TITLE) is None

    def test_vorbis(self):
        with TempFileWithMetadata({"title": "Test Vorbis Title", "artist": "Test Vorbis Artist"}, "flac") as test_file:
            # Verify Vorbis metadata is set
            vorbis_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.VORBIS)
            assert vorbis_before.get(UnifiedMetadataKey.TITLE) == "Test Vorbis Title"

            result = delete_all_metadata(test_file.path, metadata_format=MetadataFormat.VORBIS)
            assert result is True

            # Verify Vorbis metadata is deleted
            vorbis_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.VORBIS)
            assert vorbis_after.get(UnifiedMetadataKey.TITLE) is None

    def test_id3v2(self):
        with TempFileWithMetadata({"title": "Test Vorbis Title", "artist": "Test Vorbis Artist"}, "flac") as test_file:
            # Add ID3V2 metadata
            ID3v2MetadataSetter.set_metadata(test_file.path, {"title": "ID3V2 Title", "artist": "ID3V2 Artist"})

            # Verify ID3V2 metadata is set
            id3v2_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3V2 Title"

            result = delete_all_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert result is True

            # Verify ID3V2 metadata is deleted
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None

    def test_id3v1(self):
        with TempFileWithMetadata({"title": "Test Vorbis Title", "artist": "Test Vorbis Artist"}, "flac") as test_file:
            # Add ID3V1 metadata
            ID3v1MetadataSetter.set_metadata(test_file.path, {"title": "ID3V1 Title", "artist": "ID3V1 Artist"})

            # Verify ID3V1 metadata is set
            id3v1_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3V1 Title"

            result = delete_all_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert result is True

            # Verify ID3V1 metadata is deleted
            id3v1_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None

    def test_riff(self):
        with TempFileWithMetadata({"title": "Test Vorbis Title", "artist": "Test Vorbis Artist"}, "flac") as test_file:
            with pytest.raises(MetadataFormatNotSupportedByAudioFormatError):
                delete_all_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)