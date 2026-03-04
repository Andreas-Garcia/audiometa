"""Tests that get_full_metadata raw_metadata includes tags per format.

ID3v2 and Vorbis expose all frames/comments (including custom/unsupported).
ID3v1 has no extensible tags. RIFF INFO exposes all INFO chunk FourCCs (known and custom).
BWF (bext) is exposed under RIFF chunk_structure.
"""

import pytest

from audiometa import get_full_metadata
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter
from audiometa.test.helpers.riff.riff_manual_metadata_creator import ManualRIFFMetadataCreator
from audiometa.test.helpers.riff.riff_metadata_setter import RIFFMetadataSetter
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.test.helpers.vorbis.vorbis_metadata_setter import VorbisMetadataSetter
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestGetFullMetadataRawMetadataIncludesUnsupportedTags:
    def test_id3v2_raw_metadata_includes_custom_txxx_frame(self):
        with temp_file_with_metadata({"title": "Track"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_custom_txxx(test_file, "MYCUSTOMKEY", "custom value")
            result = get_full_metadata(test_file)
            frames = result.get("raw_metadata", {}).get("id3v2", {}).get("frames", {})
            assert "TXXX:MYCUSTOMKEY" in frames
            frame_data = frames["TXXX:MYCUSTOMKEY"]
            assert "text" in frame_data
            assert "custom value" in frame_data["text"]

    def test_vorbis_raw_metadata_includes_custom_comment(self):
        with temp_file_with_metadata({"title": "Track"}, "flac") as test_file:
            VorbisMetadataSetter.set_tag(test_file, "MYCUSTOMKEY", "custom value")
            result = get_full_metadata(test_file)
            comments = result.get("raw_metadata", {}).get("vorbis", {}).get("comments", {})
            assert "MYCUSTOMKEY" in comments
            assert comments["MYCUSTOMKEY"] == ["custom value"]

    def test_id3v1_raw_metadata_includes_parsed_fields(self):
        with temp_file_with_metadata(
            {"title": "ID3v1 Title", "artist": "ID3v1 Artist"},
            "id3v1",
        ) as test_file:
            result = get_full_metadata(test_file)
            parsed = result.get("raw_metadata", {}).get("id3v1", {}).get("parsed_fields", {})
            assert UnifiedMetadataKey.TITLE in parsed
            assert parsed[UnifiedMetadataKey.TITLE] == "ID3v1 Title"
            assert UnifiedMetadataKey.ARTISTS in parsed
            assert parsed[UnifiedMetadataKey.ARTISTS] == "ID3v1 Artist"

    def test_riff_raw_metadata_includes_known_info_tags(self):
        with temp_file_with_metadata(
            {"title": "RIFF Title", "artist": "RIFF Artist"},
            "wav",
        ) as test_file:
            result = get_full_metadata(test_file)
            parsed = result.get("raw_metadata", {}).get("riff", {}).get("parsed_fields", {})
            assert "INAM" in parsed
            assert parsed["INAM"] == "RIFF Title"
            assert "IART" in parsed
            assert parsed["IART"] == "RIFF Artist"

    def test_riff_raw_metadata_includes_custom_fourcc(self):
        with temp_file_with_metadata({}, "wav") as test_file:
            ManualRIFFMetadataCreator.add_custom_info_field(test_file, "CUST", "custom value")
            result = get_full_metadata(test_file)
            parsed = result.get("raw_metadata", {}).get("riff", {}).get("parsed_fields", {})
            assert "CUST" in parsed
            assert parsed["CUST"] == "custom value"

    def test_riff_raw_metadata_includes_bext_in_chunk_structure(self):
        with temp_file_with_metadata({}, "wav") as test_file:
            RIFFMetadataSetter.set_bext_description(test_file, "BWF Description")
            RIFFMetadataSetter.set_bext_originator(test_file, "BWF Originator")
            result = get_full_metadata(test_file)
            chunk_structure = result.get("raw_metadata", {}).get("riff", {}).get("chunk_structure", {})
            assert "bext" in chunk_structure
            bext = chunk_structure["bext"]
            assert bext["Description"] == "BWF Description"
            assert bext["Originator"] == "BWF Originator"
