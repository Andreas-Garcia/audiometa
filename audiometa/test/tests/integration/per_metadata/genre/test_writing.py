import pytest



from audiometa import get_unified_metadata, update_file_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestGenreWriting:
    def test_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_genre = "Test Genre ID3v2"
            test_metadata = {UnifiedMetadataKey.GENRES_NAMES: test_genre}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2)
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == [test_genre]

    def test_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            test_genre = "Rock"
            test_metadata = {UnifiedMetadataKey.GENRES_NAMES: test_genre}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.RIFF)
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == [test_genre]

    def test_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            test_genre = "Test Genre Vorbis"
            test_metadata = {UnifiedMetadataKey.GENRES_NAMES: test_genre}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.VORBIS)
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == [test_genre]

    def test_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_genre = "Rock"
            test_metadata = {UnifiedMetadataKey.GENRES_NAMES: test_genre}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V1)
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == [test_genre]

    def test_invalid_type_raises(self):
        from audiometa.exceptions import InvalidMetadataTypeError

        with TempFileWithMetadata({}, "mp3") as test_file:
            bad_metadata = {UnifiedMetadataKey.GENRES_NAMES: 123}
            with pytest.raises(InvalidMetadataTypeError):
                update_file_metadata(test_file.path, bad_metadata)
