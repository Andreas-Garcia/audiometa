import pytest
from pathlib import Path

from audiometa import get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestFormatSpecificReading:

    def test_get_single_format_app_metadata_id3v2(self, sample_mp3_file: Path):
        metadata = get_single_format_app_metadata(sample_mp3_file, MetadataFormat.ID3V2)
        assert isinstance(metadata, dict)

    def test_get_single_format_app_metadata_vorbis(self, sample_flac_file: Path):
        metadata = get_single_format_app_metadata(sample_flac_file, MetadataFormat.VORBIS)
        assert isinstance(metadata, dict)

    def test_get_single_format_app_metadata_riff(self, sample_wav_file: Path):
        metadata = get_single_format_app_metadata(sample_wav_file, MetadataFormat.RIFF)
        assert isinstance(metadata, dict)

    def test_get_single_format_app_metadata_unsupported_format(self, sample_mp3_file: Path):
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(sample_mp3_file, MetadataFormat.VORBIS)
