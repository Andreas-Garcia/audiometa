import pytest
import warnings

from audiometa import (
    update_file_metadata,
    get_merged_unified_metadata,
)
from audiometa.exceptions import MetadataNotSupportedError
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestFailBehavior:

    def test_fail_on_unsupported_field_enabled(self):
        with TempFileWithMetadata({"title": "Test"}, "wav") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.REPLAYGAIN: "89 dB"  # REPLAYGAIN is not supported by any format
            }
            
            with pytest.raises(MetadataNotSupportedError) as exc_info:
                update_file_metadata(test_file.path, test_metadata, fail_on_unsupported_field=True)
            
            assert "Fields not supported by any format" in str(exc_info.value)
            assert "REPLAYGAIN" in str(exc_info.value)

    def test_fail_on_unsupported_field_disabled_graceful_default(self):
        with TempFileWithMetadata({"title": "Test"}, "wav") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.REPLAYGAIN: "89 dB"  # REPLAYGAIN is not supported by any format
            }
            
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                update_file_metadata(test_file.path, test_metadata)  # fail_on_unsupported_field=False by default
                
                assert len(w) > 0
                warning_messages = [str(warning.message) for warning in w]
                assert any("unsupported" in msg.lower() or "not supported" in msg.lower() for msg in warning_messages)
            
            metadata = get_merged_unified_metadata(test_file)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
