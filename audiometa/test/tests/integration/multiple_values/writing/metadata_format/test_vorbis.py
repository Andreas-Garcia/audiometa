
from audiometa import update_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.vorbis.vorbis_metadata_getter import VorbisMetadataGetter
from audiometa.test.helpers.vorbis.vorbis_metadata_setter import VorbisMetadataSetter


class TestMultipleValuesVorbis:
    def test_write_multiple_artists(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Write multiple artists using update_metadata
            metadata = {
                UnifiedMetadataKey.ARTISTS: ["Artist One", "Artist Two", "Artist Three"]
            }
            
            update_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)
            VorbisMetadataSetter.add_title(test_file.path, "Test Song")
            raw_metadata = VorbisMetadataGetter.get_raw_metadata(test_file.path)
            assert "ARTIST=Artist One" in raw_metadata
            assert "ARTIST=Artist Two" in raw_metadata
            assert "ARTIST=Artist Three" in raw_metadata
            
    def test_with_existing_artists_fields(self):
        # Start with an existing artist field
        with TempFileWithMetadata({}, "flac") as test_file:
            # create an existing value using setter
            VorbisMetadataSetter.set_artists(test_file.path, ["Existing 1; Existing 2"])
            verification = VorbisMetadataGetter.get_raw_metadata(test_file.path, "ARTIST")
            raw_output = verification['raw_output']
            assert "Existing 1; Existing 2" in raw_output

            metadata = {UnifiedMetadataKey.ARTISTS: ["Existing 1", "New 2"]}
            update_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)

            verification = VorbisMetadataGetter.get_raw_metadata(test_file.path, "ARTIST")
            assert verification['actual_count'] == 2
            raw_output = verification['raw_output']
            assert "Existing 1" in raw_output
            assert "New 2" in raw_output
            assert "Existing 2" not in raw_output
            
            
            