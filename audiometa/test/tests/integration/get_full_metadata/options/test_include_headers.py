"""Tests for get_full_metadata include_headers option."""

from pathlib import Path

import pytest

from audiometa import get_full_metadata


@pytest.mark.integration
class TestGetFullMetadataIncludeHeaders:
    def test_get_full_metadata_exclude_headers(self, sample_mp3_file: Path):
        result = get_full_metadata(sample_mp3_file, include_headers=False)

        assert "unified_metadata" in result
        assert "technical_info" in result
        assert "metadata_format" in result
        assert "format_priorities" in result

        assert "headers" in result
        assert result["headers"] == {}

        assert "raw_metadata" in result
        assert result["raw_metadata"] == {}

        assert result["technical_info"] != {}
        assert "duration_seconds" in result["technical_info"]
        assert "bitrate_bps" in result["technical_info"]

        assert isinstance(result["unified_metadata"], dict)
        assert isinstance(result["metadata_format"], dict)
        assert "id3v2" in result["metadata_format"]
        assert "id3v1" in result["metadata_format"]

    def test_get_full_metadata_exclude_headers_flac(self, sample_flac_file: Path):
        result = get_full_metadata(sample_flac_file, include_headers=False)

        assert "unified_metadata" in result
        assert "technical_info" in result
        assert "metadata_format" in result
        assert "format_priorities" in result

        assert "headers" in result
        assert result["headers"] == {}

        assert "raw_metadata" in result
        assert result["raw_metadata"] == {}

        assert result["technical_info"] != {}
        assert "is_flac_md5_valid" in result["technical_info"]

        assert isinstance(result["metadata_format"], dict)
        assert "vorbis" in result["metadata_format"]

    def test_get_full_metadata_exclude_headers_wav(self, sample_wav_file: Path):
        result = get_full_metadata(sample_wav_file, include_headers=False)

        assert "unified_metadata" in result
        assert "technical_info" in result
        assert "metadata_format" in result
        assert "format_priorities" in result

        assert "headers" in result
        assert result["headers"] == {}

        assert "raw_metadata" in result
        assert result["raw_metadata"] == {}

        assert result["technical_info"] != {}
        assert result["technical_info"]["file_extension"] == ".wav"

        assert isinstance(result["metadata_format"], dict)
        assert "riff" in result["metadata_format"]

    def test_get_full_metadata_exclude_both_headers_and_technical(self, sample_mp3_file: Path):
        result = get_full_metadata(sample_mp3_file, include_headers=False, include_technical=False)

        assert "unified_metadata" in result
        assert "metadata_format" in result
        assert "format_priorities" in result

        assert "headers" in result
        assert result["headers"] == {}

        assert "raw_metadata" in result
        assert result["raw_metadata"] == {}

        assert "technical_info" in result
        assert result["technical_info"] == {}

        assert isinstance(result["unified_metadata"], dict)
        assert isinstance(result["metadata_format"], dict)

    def test_get_full_metadata_exclude_options(self, sample_mp3_file: Path):
        result = get_full_metadata(sample_mp3_file, include_headers=False, include_technical=False)

        assert "unified_metadata" in result
        assert "metadata_format" in result
        assert "format_priorities" in result

        assert result["headers"] == {}
        assert result["raw_metadata"] == {}
        assert result["technical_info"] == {}

        assert isinstance(result["unified_metadata"], dict)
        assert isinstance(result["metadata_format"], dict)
