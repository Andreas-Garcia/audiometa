

import pytest

from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestArtistsWriting:
    def test_id3v2(self):
        test_artists = ["Test Artist 1", "Test Artist 2"]
        test_metadata = {UnifiedMetadataKey.ARTISTS_NAMES: test_artists}
        with TempFileWithMetadata({}, "mp3") as test_file:
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2)
            metadata = get_merged_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == test_artists

    def test_riff(self):
        test_artists = ["RIFF Artist 1", "RIFF Artist 2"]
        test_metadata = {UnifiedMetadataKey.ARTISTS_NAMES: test_artists}
        with TempFileWithMetadata({}, "wav") as test_file:
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.RIFF)
            metadata = get_merged_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == test_artists

    def test_vorbis(self):
        test_artists = ["Vorbis Artist 1", "Vorbis Artist 2"]
        test_metadata = {UnifiedMetadataKey.ARTISTS_NAMES: test_artists}
        with TempFileWithMetadata({}, "flac") as test_file:
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.VORBIS)
            metadata = get_merged_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == test_artists

    def test_id3v1(self):
        test_artists = ["ID3v1 Artist"]
        test_metadata = {UnifiedMetadataKey.ARTISTS_NAMES: test_artists}
        with TempFileWithMetadata({}, "mp3") as test_file:
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V1)
            metadata = get_merged_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == test_artists
