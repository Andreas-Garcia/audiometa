import pytest

from audiometa import update_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.vorbis.vorbis_metadata_getter import VorbisMetadataGetter
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2.id3v2_metadata_getter import ID3v2MetadataGetter
from audiometa.test.helpers.id3v1.id3v1_metadata_getter import ID3v1MetadataGetter


@pytest.mark.integration
class TestFlacWriting:
    def test_vorbis_metadata_writing_flac(self):
        with TempFileWithMetadata({}, "flac") as temp_flac_file:
            metadata = {UnifiedMetadataKey.TITLE: "Test Title Vorbis"}
            update_metadata(temp_flac_file, metadata, metadata_format=MetadataFormat.VORBIS)
            title = VorbisMetadataGetter.get_title(temp_flac_file.path)
            assert title == "Test Title Vorbis"

    def test_id3v2_3_metadata_writing_flac(self):
        with TempFileWithMetadata({}, "flac") as temp_flac_file:
            metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v2.3"}
            update_metadata(temp_flac_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            title = ID3v2MetadataGetter.get_title(temp_flac_file.path)
            assert title == "Test Title ID3v2.3"

    def test_id3v2_4_metadata_writing_flac(self):
        with TempFileWithMetadata({}, "flac") as temp_flac_file:
            metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v2.4"}
            update_metadata(temp_flac_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            title = ID3v2MetadataGetter.get_title(temp_flac_file.path)
            assert title == "Test Title ID3v2.4"

    def test_id3v1_metadata_writing_flac(self):
        with TempFileWithMetadata({}, "flac") as temp_flac_file:
            metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v1"}
            update_metadata(temp_flac_file, metadata, metadata_format=MetadataFormat.ID3V1)
            title = ID3v1MetadataGetter.get_title(temp_flac_file.path)
            assert title == "Test Title ID3v1"