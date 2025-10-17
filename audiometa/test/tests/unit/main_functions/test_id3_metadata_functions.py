

import pytest
from pathlib import Path

from audiometa import delete_potential_id3_metadata_with_header
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.unit
class TestId3MetadataFunctions:

    def test_delete_potential_id3_metadata_with_header_mp3(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # This should not raise an error
            delete_potential_id3_metadata_with_header(test_file.path)

    def test_delete_potential_id3_metadata_with_header_flac(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # This should not raise an error
            delete_potential_id3_metadata_with_header(test_file.path)

    def test_delete_potential_id3_metadata_with_header_with_audio_file_object(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            from audiometa import AudioFile
            audio_file = AudioFile(test_file.path)
            
            # This should not raise an error
            delete_potential_id3_metadata_with_header(audio_file)
