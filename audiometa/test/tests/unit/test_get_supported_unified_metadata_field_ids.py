"""Tests for get_supported_unified_metadata_field_ids."""

from pathlib import Path

import pytest

from audiometa import FileTypeNotSupportedError, get_full_metadata, get_supported_unified_metadata_field_ids


@pytest.mark.unit
class TestGetSupportedUnifiedMetadataFieldIds:
    @pytest.mark.parametrize(
        "fixture_name",
        [
            pytest.param("sample_mp3_file", id="mp3"),
            pytest.param("sample_flac_file", id="flac"),
            pytest.param("sample_wav_file", id="wav"),
        ],
    )
    def test_returns_sorted_ids(self, fixture_name: str, request: pytest.FixtureRequest) -> None:
        path: Path = request.getfixturevalue(fixture_name)
        supported = get_supported_unified_metadata_field_ids(path)
        assert supported == sorted(supported)

    @pytest.mark.parametrize(
        "fixture_name",
        [
            pytest.param("sample_mp3_file", id="mp3"),
            pytest.param("sample_flac_file", id="flac"),
            pytest.param("sample_wav_file", id="wav"),
        ],
    )
    def test_matches_get_full_metadata(self, fixture_name: str, request: pytest.FixtureRequest) -> None:
        path: Path = request.getfixturevalue(fixture_name)
        direct = get_supported_unified_metadata_field_ids(path)
        from_full = get_full_metadata(path)["supported_unified_metadata_field_ids"]
        assert direct == from_full

    def test_accepts_str_path(self, sample_mp3_file: Path) -> None:
        a = get_supported_unified_metadata_field_ids(str(sample_mp3_file))
        b = get_supported_unified_metadata_field_ids(sample_mp3_file)
        assert a == b

    def test_unsupported_extension_raises(self, tmp_path: Path) -> None:
        p = tmp_path / "x.txt"
        p.write_bytes(b"not audio")
        with pytest.raises(FileTypeNotSupportedError):
            get_supported_unified_metadata_field_ids(p)
