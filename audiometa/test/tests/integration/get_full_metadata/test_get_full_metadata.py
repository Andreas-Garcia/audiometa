"""Basic structure tests for get_full_metadata function."""

from pathlib import Path

import pytest

from audiometa import UnifiedMetadataKey, get_full_metadata, get_unified_metadata_field_schema


@pytest.mark.integration
class TestGetFullMetadata:
    def test_get_full_metadata_basic_structure(self, sample_mp3_file: Path):
        """Test that get_full_metadata returns the expected basic structure."""
        result = get_full_metadata(sample_mp3_file)

        # Check all required top-level keys are present
        assert "unified_metadata" in result
        assert "technical_info" in result
        assert "metadata_format" in result
        assert "headers" in result
        assert "raw_metadata" in result
        assert "format_priorities" in result
        assert "unified_metadata_field_schema" in result
        assert "supported_unified_metadata_field_ids" in result

        # Check that each section is a dictionary
        assert isinstance(result["unified_metadata"], dict)
        assert isinstance(result["technical_info"], dict)
        assert isinstance(result["metadata_format"], dict)
        assert isinstance(result["headers"], dict)
        assert isinstance(result["raw_metadata"], dict)
        assert isinstance(result["format_priorities"], dict)
        schema = result["unified_metadata_field_schema"]
        assert isinstance(schema, list)
        assert len(schema) == len(UnifiedMetadataKey)
        assert {item["id"] for item in schema} == {k.value for k in UnifiedMetadataKey}
        supported = result["supported_unified_metadata_field_ids"]
        assert isinstance(supported, list)
        assert all(isinstance(x, str) for x in supported)
        assert set(supported) <= {k.value for k in UnifiedMetadataKey}
        assert schema == get_unified_metadata_field_schema()

    def test_get_full_metadata_format_priorities_structure(self, sample_mp3_file: Path):
        """Test that format_priorities has the expected structure."""
        result = get_full_metadata(sample_mp3_file)

        priorities = result["format_priorities"]
        assert "file_extension" in priorities
        assert "reading_order" in priorities
        assert "writing_format" in priorities

        assert isinstance(priorities["file_extension"], str)
        assert isinstance(priorities["reading_order"], list)
        assert isinstance(priorities["writing_format"], str)
