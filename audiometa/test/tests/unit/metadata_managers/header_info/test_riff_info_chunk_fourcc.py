"""Unit tests for RIFF INFO chunk FourCC validation."""

import pytest

from audiometa.manager._rating_supporting.riff._riff_info_chunk import _is_valid_fourcc, extract_riff_metadata_directly


@pytest.mark.unit
class TestRiffInfoChunkFourCCValidation:
    @pytest.mark.parametrize(
        "fourcc_bytes",
        [
            b"INAM",
            b"IART",
            b"CUST",
            b"    ",
            b"0123",
            b"AB\x20\x7e",
        ],
    )
    def test_valid_fourcc_accepted(self, fourcc_bytes: bytes):
        assert _is_valid_fourcc(fourcc_bytes) is True

    @pytest.mark.parametrize(
        "fourcc_bytes",
        [
            b"IN\x00M",
            b"\x00NAM",
            b"INAM\x00",
            b"\x1fABC",
            b"AB\x7f\x43",
            b"",
            b"I",
            b"INA",
            b"INAMX",
        ],
    )
    def test_invalid_fourcc_rejected(self, fourcc_bytes: bytes):
        assert _is_valid_fourcc(fourcc_bytes) is False

    def test_extract_includes_valid_fourcc_excludes_invalid(self):
        def no_skip(data: bytes) -> bytes:
            return data

        # Minimal RIFF WAVE with LIST INFO: one valid (INAM) and one invalid (IN\x00M) subchunk
        inam_data = b"Title\x00"
        invalid_data = b"X\x00"
        inam_size = len(inam_data)
        invalid_size = len(invalid_data)
        if inam_size % 2:
            inam_size += 1
        if invalid_size % 2:
            invalid_size += 1
        list_payload = b"INFO" b"INAM" + inam_size.to_bytes(4, "little") + inam_data.ljust(
            inam_size, b"\x00"
        ) + b"IN\x00M" + invalid_size.to_bytes(4, "little") + invalid_data.ljust(invalid_size, b"\x00")
        list_size = len(list_payload)
        if list_size % 2:
            list_payload += b"\x00"
            list_size += 1
        riff_body_size = 4 + 8 + list_size
        riff = (
            b"RIFF" + riff_body_size.to_bytes(4, "little") + b"WAVE"
            b"LIST" + list_size.to_bytes(4, "little") + list_payload
        )
        result = extract_riff_metadata_directly(riff, no_skip)
        assert "INAM" in result
        assert result["INAM"] == ["Title"]
        for key in result:
            assert key == "INAM", f"Only INAM should appear, got key {key!r}"
