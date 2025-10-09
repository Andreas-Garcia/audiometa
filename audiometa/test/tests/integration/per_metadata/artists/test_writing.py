

import pytest
import shutil

from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestArtistsWriting:
    def test_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_artists = ["Test Artist 1", "Test Artist 2"]
        test_metadata = {UnifiedMetadataKey.ARTISTS_NAMES: test_artists}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == test_artists

    def test_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        test_artists = ["RIFF Artist 1", "RIFF Artist 2"]
        test_metadata = {UnifiedMetadataKey.ARTISTS_NAMES: test_artists}
        update_file_metadata(temp_wav_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        metadata = get_merged_unified_metadata(temp_wav_file)
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == test_artists

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        test_artists = ["Vorbis Artist 1", "Vorbis Artist 2"]
        test_metadata = {UnifiedMetadataKey.ARTISTS_NAMES: test_artists}
        update_file_metadata(temp_flac_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        metadata = get_merged_unified_metadata(temp_flac_file)
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == test_artists
