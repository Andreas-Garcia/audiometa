

import pytest
from pathlib import Path
import shutil

from audiometa import delete_potential_id3_metadata_with_header


@pytest.mark.unit
class TestId3MetadataFunctions:

    def test_delete_potential_id3_metadata_with_header_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # This should not raise an error
        delete_potential_id3_metadata_with_header(temp_audio_file)

    def test_delete_potential_id3_metadata_with_header_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        # This should not raise an error
        delete_potential_id3_metadata_with_header(temp_audio_file)

    def test_delete_potential_id3_metadata_with_header_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        from audiometa import AudioFile
        audio_file = AudioFile(temp_audio_file)
        
        # This should not raise an error
        delete_potential_id3_metadata_with_header(audio_file)
