"""Tests for binary data filtering in get_full_metadata function output."""

import pytest

from audiometa import get_full_metadata

_ID3V2_BINARY_FRAME_PREFIXES = frozenset(
    {
        "APIC:",
        "GEOB:",
        "AENC:",
        "RVA2:",
        "RVRB:",
        "EQU2:",
        "PCNT:",
        "POPM:",
        "RBUF:",
        "LINK:",
        "POSS:",
        "SYLT:",
        "USLT:",
        "SYTC:",
        "ETCO:",
        "MLLT:",
        "OWNE:",
        "COMR:",
        "ENCR:",
        "GRID:",
        "PRIV:",
        "SIGN:",
        "SEEK:",
        "ASPI:",
    }
)


def _is_binary_frame(frame_id: str) -> bool:
    return any(frame_id.startswith(prefix) for prefix in _ID3V2_BINARY_FRAME_PREFIXES)


@pytest.mark.integration
class TestGetFullMetadataBinaryDataFiltering:
    """Test that get_full_metadata function properly filters binary data from raw metadata output."""

    def test_get_full_metadata_id3v2_binary_frames_filtered(self, sample_mp3_file):
        """Test that get_full_metadata filters ID3v2 binary frames and replaces with size info."""
        result = get_full_metadata(sample_mp3_file)
        raw_metadata = result.get("raw_metadata", {})
        id3v2_frames = raw_metadata.get("id3v2", {}).get("frames", {})

        for frame_id, frame_data in id3v2_frames.items():
            text = frame_data.get("text", "")

            assert not any(ord(c) < 32 and c not in "\t\n\r" for c in text), (
                f"Frame {frame_id} contains binary data in text: {text[:50]!r}"
            )

            if _is_binary_frame(frame_id):
                assert text.startswith("<Binary data:"), (
                    f"Binary frame {frame_id} should have placeholder text, got: {text}"
                )
                assert text.endswith(" bytes>"), f"Binary frame {frame_id} should end with ' bytes>', got: {text}"

    def test_get_full_metadata_id3v2_binary_frames_sanitized(self, sample_mp3_file):
        """Get_full_metadata sanitizes ID3v2 binary frames (including extended keys like PRIV:owner:desc)."""
        result = get_full_metadata(sample_mp3_file)
        frames = result.get("raw_metadata", {}).get("id3v2", {}).get("frames", {})

        for frame_id, frame_data in frames.items():
            text = frame_data.get("text", "")
            if _is_binary_frame(frame_id):
                assert text.startswith("<Binary data:"), f"Binary frame {frame_id} should have placeholder text"
                assert text.endswith(" bytes>"), f"Binary frame {frame_id} should end with ' bytes>'"
            else:
                assert not any(ord(c) < 32 and c not in "\t\n\r" for c in text), (
                    f"Text frame {frame_id} contains binary data: {text[:50]!r}"
                )

    def test_get_full_metadata_vorbis_no_binary_data(self, sample_flac_file):
        """Test that get_full_metadata Vorbis comments don't contain binary data."""
        result = get_full_metadata(sample_flac_file)
        raw_metadata = result.get("raw_metadata", {})
        vorbis_comments = raw_metadata.get("vorbis", {}).get("comments", {})

        for key, values in vorbis_comments.items():
            assert isinstance(values, list), f"Vorbis comment {key} should be a list"
            for value in values:
                assert isinstance(value, str), f"Vorbis comment {key} value should be string"
                assert not any(ord(c) < 32 and c not in "\t\n\r" for c in value), (
                    f"Vorbis comment {key} contains binary data: {value[:50]!r}"
                )

    def test_get_full_metadata_vorbis_opaque_comment_sanitized(self):
        """TRAKTOR4 and other opaque Vorbis comment keys are replaced with size placeholder."""
        from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
        from audiometa.test.helpers.vorbis.vorbis_metadata_setter import VorbisMetadataSetter

        opaque_value = 'dlVHB8hIC"AAAA4wlZhtBAC"BAAA::<y~XAAAAAAAA' + "x" * 200
        with temp_file_with_metadata({"title": "Money"}, "flac") as test_file:
            VorbisMetadataSetter.set_tag(test_file, "TRAKTOR4", opaque_value)
            result = get_full_metadata(test_file)

        vorbis_comments = result.get("raw_metadata", {}).get("vorbis", {}).get("comments", {})
        assert "TITLE" in vorbis_comments
        assert "TRAKTOR4" in vorbis_comments
        assert len(vorbis_comments["TRAKTOR4"]) == 1
        placeholder = vorbis_comments["TRAKTOR4"][0]
        assert placeholder.startswith("<Binary or opaque data: ")
        assert placeholder.endswith(" bytes>")
        expected_size = len(opaque_value.encode("utf-8"))
        assert placeholder == f"<Binary or opaque data: {expected_size} bytes>"

    def test_get_full_metadata_include_raw_binary_data_true_returns_unsanitized(self):
        """With include_raw_binary_data=True, opaque comment values are included as-is."""
        from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
        from audiometa.test.helpers.vorbis.vorbis_metadata_setter import VorbisMetadataSetter

        opaque_value = "opaque_traktor_data" + "x" * 100
        with temp_file_with_metadata({"title": "Money"}, "flac") as test_file:
            VorbisMetadataSetter.set_tag(test_file, "TRAKTOR4", opaque_value)
            result = get_full_metadata(test_file, include_raw_binary_data=True)

        vorbis_comments = result.get("raw_metadata", {}).get("vorbis", {}).get("comments", {})
        assert vorbis_comments["TRAKTOR4"] == [opaque_value]

    def test_get_full_metadata_riff_no_binary_data(self, sample_wav_file):
        """Test that get_full_metadata RIFF metadata doesn't contain binary data."""
        result = get_full_metadata(sample_wav_file)
        raw_metadata = result.get("raw_metadata", {})
        riff_fields = raw_metadata.get("riff", {}).get("parsed_fields", {})

        # RIFF parsed fields should only contain text
        for key, value in riff_fields.items():
            assert isinstance(value, str), f"RIFF field {key} should be string"
            # Check for binary data patterns
            assert not any(ord(c) < 32 and c not in "\t\n\r" for c in value), (
                f"RIFF field {key} contains binary data: {value[:50]!r}"
            )

    def test_get_full_metadata_id3v1_no_binary_data(self, sample_mp3_file):
        """Test that get_full_metadata ID3v1 metadata doesn't contain binary data."""
        result = get_full_metadata(sample_mp3_file)
        raw_metadata = result.get("raw_metadata", {})
        id3v1_fields = raw_metadata.get("id3v1", {}).get("parsed_fields", {})

        # ID3v1 parsed fields should only contain text
        for key, value in id3v1_fields.items():
            assert isinstance(value, str), f"ID3v1 field {key} should be string"
            # Check for binary data patterns
            assert not any(ord(c) < 32 and c not in "\t\n\r" for c in value), (
                f"ID3v1 field {key} contains binary data: {value[:50]!r}"
            )

    def test_cli_output_no_binary_data(self, sample_mp3_file):
        """Test that CLI output doesn't contain binary data."""
        import subprocess
        import sys

        # Test JSON output
        result = subprocess.run(
            [sys.executable, "-m", "audiometa", "read", str(sample_mp3_file), "--format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"CLI failed: {result.stderr}"

        # Check for binary data patterns in output
        output = result.stdout
        binary_patterns = ["\\xff", "\\x00", "\\x01", "\\x02", "\\x03"]

        for pattern in binary_patterns:
            assert pattern not in output, f"CLI output contains binary pattern {pattern}"

        # Should be valid JSON
        import json

        data = json.loads(output)
        assert isinstance(data, dict)

    def test_binary_frame_size_preserved(self, sample_mp3_file):
        """Sanitized binary frames in get_full_metadata still report size and flags."""
        result = get_full_metadata(sample_mp3_file)
        frames = result.get("raw_metadata", {}).get("id3v2", {}).get("frames", {})
        for frame_id, frame_data in frames.items():
            if _is_binary_frame(frame_id):
                size = frame_data.get("size")
                flags = frame_data.get("flags")

                # Size and flags should still be present
                assert isinstance(size, int), f"Binary frame {frame_id} size should be int"
                assert isinstance(flags, int), f"Binary frame {frame_id} flags should be int"

                # Size should be reasonable (not negative)
                assert size >= 0, f"Binary frame {frame_id} size should be non-negative"

    def test_text_frames_unchanged(self, sample_mp3_file):
        """Text frames in get_full_metadata are not replaced by placeholders."""
        result = get_full_metadata(sample_mp3_file)
        frames = result.get("raw_metadata", {}).get("id3v2", {}).get("frames", {})
        text_frame_types = {"TIT2", "TALB", "TPE1", "TDRC", "COMM", "TENC", "TSSE"}

        for frame_id, frame_data in frames.items():
            if any(frame_id.startswith(prefix) for prefix in text_frame_types):
                text = frame_data.get("text", "")

                # Text frames should have actual content, not placeholder
                assert not text.startswith("<Binary data:"), f"Text frame {frame_id} should not have binary placeholder"

                # Should have reasonable content
                assert len(text) > 0, f"Text frame {frame_id} should have content"
