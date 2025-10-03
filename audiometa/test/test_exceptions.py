"""Tests for exception classes."""

import pytest
from pathlib import Path

from audiometa.exceptions import (
    FileCorruptedError,
    FlacMd5CheckFailedError,
    FileByteMismatchError,
    InvalidChunkDecodeError,
    DurationNotFoundError,
    FileTypeNotSupportedError,
    MetadataNotSupportedError
)


class TestExceptions:
    """Test cases for exception classes."""

    def test_file_corrupted_error(self):
        """Test FileCorruptedError exception."""
        error = FileCorruptedError("Test file is corrupted")
        assert str(error) == "Test file is corrupted"
        assert isinstance(error, Exception)

    def test_flac_md5_check_failed_error(self):
        """Test FlacMd5CheckFailedError exception."""
        error = FlacMd5CheckFailedError()
        assert isinstance(error, FileCorruptedError)
        assert isinstance(error, Exception)

    def test_file_byte_mismatch_error(self):
        """Test FileByteMismatchError exception."""
        error = FileByteMismatchError("Byte mismatch detected")
        assert str(error) == "Byte mismatch detected"
        assert isinstance(error, FileCorruptedError)
        assert isinstance(error, Exception)

    def test_invalid_chunk_decode_error(self):
        """Test InvalidChunkDecodeError exception."""
        error = InvalidChunkDecodeError("Invalid chunk format")
        assert str(error) == "Invalid chunk format"
        assert isinstance(error, FileCorruptedError)
        assert isinstance(error, Exception)

    def test_duration_not_found_error(self):
        """Test DurationNotFoundError exception."""
        error = DurationNotFoundError("Duration not found in file")
        assert str(error) == "Duration not found in file"
        assert isinstance(error, FileCorruptedError)
        assert isinstance(error, Exception)

    def test_file_type_not_supported_error(self):
        """Test FileTypeNotSupportedError exception."""
        error = FileTypeNotSupportedError("File type not supported")
        assert str(error) == "File type not supported"
        assert isinstance(error, Exception)

    def test_metadata_not_supported_error(self):
        """Test MetadataNotSupportedError exception."""
        error = MetadataNotSupportedError("Metadata field not supported for this format")
        assert str(error) == "Metadata field not supported for this format"
        assert isinstance(error, Exception)

    def test_exception_inheritance(self):
        """Test that exception inheritance is correct."""
        # FileCorruptedError should be a base class for corruption-related errors
        assert issubclass(FlacMd5CheckFailedError, FileCorruptedError)
        assert issubclass(FileByteMismatchError, FileCorruptedError)
        assert issubclass(InvalidChunkDecodeError, FileCorruptedError)
        assert issubclass(DurationNotFoundError, FileCorruptedError)
        
        # All should be subclasses of Exception
        assert issubclass(FileCorruptedError, Exception)
        assert issubclass(FileTypeNotSupportedError, Exception)
        assert issubclass(MetadataNotSupportedError, Exception)

    def test_exception_raising(self):
        """Test that exceptions can be raised and caught properly."""
        with pytest.raises(FileCorruptedError):
            raise FileCorruptedError("Test corruption")
        
        with pytest.raises(FlacMd5CheckFailedError):
            raise FlacMd5CheckFailedError()
        
        with pytest.raises(FileTypeNotSupportedError):
            raise FileTypeNotSupportedError("Unsupported format")
        
        with pytest.raises(MetadataNotSupportedError):
            raise MetadataNotSupportedError("Unsupported metadata field")

    def test_exception_with_context(self):
        """Test exceptions with additional context."""
        error = FileCorruptedError("File corrupted during processing")
        error.context = {"file_path": "/path/to/file.mp3", "operation": "metadata_read"}
        
        assert str(error) == "File corrupted during processing"
        assert hasattr(error, 'context')
        assert error.context["file_path"] == "/path/to/file.mp3"



