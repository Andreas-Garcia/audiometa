"""Unit tests for raw_metadata_sanitizer (get_full_metadata binary/opaque filtering)."""

import pytest

from audiometa.utils.raw_metadata_sanitizer import sanitize_raw_info_for_full_metadata


@pytest.mark.unit
class TestSanitizeRawInfoForFullMetadata:
    def test_id3v2_binary_frame_extended_key_replaced_with_placeholder(self):
        raw_info = {
            "raw_data": None,
            "parsed_fields": {},
            "frames": {
                "PRIV:TRAKTOR4:DMRT": {"text": b"binary\x00data".decode("latin-1"), "size": 500, "flags": 0},
                "TIT2": {"text": "Money", "size": 5, "flags": 0},
            },
            "comments": {},
            "chunk_structure": {},
        }
        out = sanitize_raw_info_for_full_metadata(raw_info, "id3v2")
        assert out["frames"]["PRIV:TRAKTOR4:DMRT"]["text"] == "<Binary data: 500 bytes>"
        assert out["frames"]["PRIV:TRAKTOR4:DMRT"]["size"] == 500
        assert out["frames"]["TIT2"]["text"] == "Money"

    def test_id3v2_apic_extended_key_replaced_with_placeholder(self):
        raw_info = {
            "frames": {"APIC:cover": {"text": "<image bytes>", "size": 2048, "flags": 0}},
        }
        out = sanitize_raw_info_for_full_metadata(raw_info, "id3v2")
        assert out["frames"]["APIC:cover"]["text"] == "<Binary data: 2048 bytes>"
        assert out["frames"]["APIC:cover"]["size"] == 2048

    def test_vorbis_opaque_key_replaced_with_placeholder(self):
        raw_info = {
            "raw_data": None,
            "parsed_fields": {},
            "frames": {},
            "comments": {"TITLE": ["Money"], "TRAKTOR4": ["opaque" + "x" * 300]},
            "chunk_structure": {},
        }
        out = sanitize_raw_info_for_full_metadata(raw_info, "vorbis")
        assert out["comments"]["TITLE"] == ["Money"]
        assert len(out["comments"]["TRAKTOR4"]) == 1
        assert out["comments"]["TRAKTOR4"][0].startswith("<Binary or opaque data: ")
        assert out["comments"]["TRAKTOR4"][0].endswith(" bytes>")
        assert out["comments"]["TRAKTOR4"][0] == "<Binary or opaque data: 306 bytes>"

    def test_vorbis_binary_value_replaced_with_placeholder(self):
        raw_info = {"comments": {"CUSTOM": ["text\x00with\x01null"]}}
        out = sanitize_raw_info_for_full_metadata(raw_info, "vorbis")
        assert len(out["comments"]["CUSTOM"]) == 1
        assert out["comments"]["CUSTOM"][0].startswith("<Binary data: ")
        assert out["comments"]["CUSTOM"][0].endswith(" bytes>")

    def test_other_formats_unchanged(self):
        raw_info = {"raw_data": b"x", "parsed_fields": {"k": "v"}}
        assert sanitize_raw_info_for_full_metadata(raw_info, "id3v1") is raw_info
        assert sanitize_raw_info_for_full_metadata(raw_info, "riff") is raw_info
