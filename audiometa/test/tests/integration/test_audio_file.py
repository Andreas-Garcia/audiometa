

import pytest
from pathlib import Path

from audiometa import (
    AudioFile,
    get_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestAudioFileIntegration:


    def test_audio_file_object_integration(self, sample_mp3_file: Path):
        audio_file = AudioFile(sample_mp3_file)
        
        # Test that AudioFile object works with functional APIs
        metadata = get_unified_metadata(audio_file)
        assert isinstance(metadata, dict)
        
        # Test single format with AudioFile object
        id3v2_metadata = get_single_format_app_metadata(audio_file, MetadataFormat.ID3V2)
        assert isinstance(id3v2_metadata, dict)
        
        # Test specific metadata with AudioFile object
        title = get_specific_metadata(audio_file, UnifiedMetadataKey.TITLE)
        assert title is None or isinstance(title, str)



