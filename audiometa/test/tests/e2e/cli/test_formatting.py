import json

import pytest

from audiometa import UnifiedMetadataKey
from audiometa.cli import format_as_table, format_output


@pytest.mark.e2e
class TestCLIFormatting:
    def test_format_output_json(self):
        data = {"title": "Test Song", "artist": "Test Artist"}
        result = format_output(data, "json")
        parsed = json.loads(result)
        assert parsed == data

    def test_format_output_yaml(self):
        data = {"title": "Test Song", "artist": "Test Artist"}
        result = format_output(data, "yaml")
        # Should fall back to JSON if PyYAML not available
        assert "Test Song" in result

    def test_format_output_table(self):
        data = {
            "unified_metadata": {"title": "Test Song", "artist": "Test Artist"},
            "technical_info": {"duration_seconds": 180, "bitrate_bps": 320000},
        }
        result = format_as_table(data)
        assert "Test Song" in result
        assert "Test Artist" in result
        assert "180" in result
        assert "320" in result

    def test_format_output_table_displays_key_labels_not_enum_repr(self):
        data = {
            "unified_metadata": {
                UnifiedMetadataKey.TITLE: "Song Title",
                UnifiedMetadataKey.ALBUM_ARTISTS: ["Album Artist"],
            },
            "metadata_format": {
                "id3v2": {
                    UnifiedMetadataKey.TITLE: "Song Title",
                    UnifiedMetadataKey.ALBUM_ARTISTS: ["Album Artist"],
                },
            },
        }
        result = format_as_table(data)
        assert "UnifiedMetadataKey." not in result
        assert "title" in result
        assert "album_artists" in result
        assert "Song Title" in result
        assert "Album Artist" in result or "['Album Artist']" in result
