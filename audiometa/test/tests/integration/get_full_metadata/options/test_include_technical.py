"""Tests for get_full_metadata include_technical option."""

from pathlib import Path

import pytest

from audiometa import get_full_metadata


@pytest.mark.integration
class TestGetFullMetadataIncludeTechnical:
    def test_get_full_metadata_exclude_technical(self, sample_mp3_file: Path):
        result = get_full_metadata(sample_mp3_file, include_technical=False)

        assert "unified_metadata" in result
        assert "metadata_format" in result
        assert "headers" in result
        assert "raw_metadata" in result
        assert "format_priorities" in result

        assert "technical_info" in result
        assert result["technical_info"] == {}

        assert result["headers"] != {}
        assert "id3v2" in result["headers"]
        assert "id3v1" in result["headers"]

        assert result["raw_metadata"] != {}
        assert "id3v2" in result["raw_metadata"]
        assert "id3v1" in result["raw_metadata"]

        assert isinstance(result["unified_metadata"], dict)
        assert isinstance(result["metadata_format"], dict)

    def test_get_full_metadata_exclude_technical_flac(self, sample_flac_file: Path):
        result = get_full_metadata(sample_flac_file, include_technical=False)

        assert "unified_metadata" in result
        assert "metadata_format" in result
        assert "headers" in result
        assert "raw_metadata" in result
        assert "format_priorities" in result

        assert "technical_info" in result
        assert result["technical_info"] == {}

        assert result["headers"] != {}
        assert "vorbis" in result["headers"]

        assert result["raw_metadata"] != {}
        assert "vorbis" in result["raw_metadata"]

    def test_get_full_metadata_exclude_technical_wav(self, sample_wav_file: Path):
        result = get_full_metadata(sample_wav_file, include_technical=False)

        assert "unified_metadata" in result
        assert "metadata_format" in result
        assert "headers" in result
        assert "raw_metadata" in result
        assert "format_priorities" in result

        assert "technical_info" in result
        assert result["technical_info"] == {}

        assert result["headers"] != {}
        assert "riff" in result["headers"]

        assert result["raw_metadata"] != {}
        assert "riff" in result["raw_metadata"]
