

import pytest

from audiometa import (
    get_unified_metadata,
    get_single_format_app_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestVorbisReading:

    def test_vorbis_metadata_capabilities(self, metadata_vorbis_small_flac, metadata_vorbis_big_flac):
        # Small Vorbis file
        metadata = get_unified_metadata(metadata_vorbis_small_flac)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # Vorbis can have longer titles
        
        # Big Vorbis file
        metadata = get_unified_metadata(metadata_vorbis_big_flac)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # Vorbis can have longer titles

    def test_vorbis_metadata_reading(self, metadata_vorbis_small_flac):
        metadata = get_unified_metadata(metadata_vorbis_small_flac)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # Vorbis can have very long titles
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30

    def test_single_format_vorbis_extraction(self, metadata_vorbis_small_flac):
        vorbis_metadata = get_single_format_app_metadata(metadata_vorbis_small_flac, MetadataFormat.VORBIS)
        assert isinstance(vorbis_metadata, dict)
        assert UnifiedMetadataKey.TITLE in vorbis_metadata

    def test_metadata_none_files(self, metadata_none_flac):
        # FLAC with no metadata
        metadata = get_unified_metadata(metadata_none_flac)
        assert isinstance(metadata, dict)

    def test_audio_file_object_reading(self, metadata_vorbis_small_flac):
        audio_file = AudioFile(metadata_vorbis_small_flac)
        
        # Test merged metadata
        metadata = get_unified_metadata(audio_file)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_flac_md5_validation(self, sample_flac_file):
        audio_file = AudioFile(sample_flac_file)
        
        # This should not raise an exception
        is_valid = audio_file.is_flac_file_md5_valid()
        assert isinstance(is_valid, bool)

    def test_flac_md5_validation_non_flac(self, sample_mp3_file):
        audio_file = AudioFile(sample_mp3_file)
        
        with pytest.raises(FileTypeNotSupportedError):
            audio_file.is_flac_file_md5_valid()
