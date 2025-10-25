
import pytest

from audiometa.exceptions import (
    FileCorruptedError,
    FlacMd5CheckFailedError,
    FileByteMismatchError,
    InvalidChunkDecodeError,
    DurationNotFoundError,
    FileTypeNotSupportedError,
    MetadataFieldNotSupportedByMetadataFormatError
)


@pytest.mark.unit
class TestExceptions:

    def test_file_corrupted_error(self):
        error = FileCorruptedError("Test file is corrupted")
        assert str(error) == "Test file is corrupted"
        assert isinstance(error, Exception)

    def test_flac_md5_check_failed_error(self):
        error = FlacMd5CheckFailedError()
        assert isinstance(error, FileCorruptedError)
        assert isinstance(error, Exception)

    def test_file_byte_mismatch_error(self):
        error = FileByteMismatchError("Byte mismatch detected")
        assert str(error) == "Byte mismatch detected"
        assert isinstance(error, FileCorruptedError)
        assert isinstance(error, Exception)

    def test_invalid_chunk_decode_error(self):
        error = InvalidChunkDecodeError("Invalid chunk format")
        assert str(error) == "Invalid chunk format"
        assert isinstance(error, FileCorruptedError)
        assert isinstance(error, Exception)

    def test_duration_not_found_error(self):
        error = DurationNotFoundError("Duration not found in file")
        assert str(error) == "Duration not found in file"
        assert isinstance(error, FileCorruptedError)
        assert isinstance(error, Exception)

    def test_file_type_not_supported_error(self):
        error = FileTypeNotSupportedError("File type not supported")
        assert str(error) == "File type not supported"
        assert isinstance(error, Exception)

    def test_metadata_not_supported_error(self):
        error = MetadataFieldNotSupportedByMetadataFormatError("Metadata field not supported for this format")
        assert str(error) == "Metadata field not supported for this format"
        assert isinstance(error, Exception)

    def test_exception_inheritance(self):
        # FileCorruptedError should be a base class for corruption-related errors
        assert issubclass(FlacMd5CheckFailedError, FileCorruptedError)
        assert issubclass(FileByteMismatchError, FileCorruptedError)
        assert issubclass(InvalidChunkDecodeError, FileCorruptedError)
        assert issubclass(DurationNotFoundError, FileCorruptedError)
        
        # All should be subclasses of Exception
        assert issubclass(FileCorruptedError, Exception)
        assert issubclass(FileTypeNotSupportedError, Exception)
        assert issubclass(MetadataFieldNotSupportedByMetadataFormatError, Exception)

    def test_exception_raising(self):
        with pytest.raises(FileCorruptedError):
            raise FileCorruptedError("Test corruption")
        
        with pytest.raises(FlacMd5CheckFailedError):
            raise FlacMd5CheckFailedError()
        
        with pytest.raises(FileTypeNotSupportedError):
            raise FileTypeNotSupportedError("Unsupported format")
        
        with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
            raise MetadataFieldNotSupportedByMetadataFormatError("Unsupported metadata field")

    def test_exception_with_context(self):
        error = FileCorruptedError("File corrupted during processing")
        error.context = {"file_path": "/path/to/file.mp3", "operation": "metadata_read"}
        
        assert str(error) == "File corrupted during processing"
        assert hasattr(error, 'context')
        assert error.context["file_path"] == "/path/to/file.mp3"



