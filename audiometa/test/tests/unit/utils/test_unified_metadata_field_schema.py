"""Tests for unified metadata field schema helpers."""

from audiometa import UnifiedMetadataKey, get_unified_metadata_field_schema
from audiometa.utils.unified_metadata_field_schema import describe_unified_metadata_field


def test_schema_covers_all_enum_members() -> None:
    schema = get_unified_metadata_field_schema()
    ids = {entry["id"] for entry in schema}
    assert ids == {k.value for k in UnifiedMetadataKey}


def test_describe_required_keys() -> None:
    d = describe_unified_metadata_field(UnifiedMetadataKey.TITLE)
    assert d["id"] == "title"
    assert d["label"] == "Title"
    assert d["multiple"] is False
    assert d["value_type"] == "string"
    assert d["optional_value"] is False


def test_multi_value_field() -> None:
    d = describe_unified_metadata_field(UnifiedMetadataKey.ARTISTS)
    assert d["multiple"] is True
    assert d["value_type"] == "strings"
