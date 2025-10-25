class FileCorruptedError(Exception):
    pass


class FlacMd5CheckFailedError (FileCorruptedError):
    pass


class FileByteMismatchError(FileCorruptedError):
    pass


class InvalidChunkDecodeError(FileCorruptedError):
    pass


class DurationNotFoundError(FileCorruptedError):
    pass


class FileTypeNotSupportedError(Exception):
    pass


class ConfigurationError(Exception):
    """Raised when there is a configuration error in the metadata manager.
    
    This error indicates that the metadata manager was not properly configured
    or initialized with the required parameters.
    """
    pass


class MetadataNotSupportedByFormatError(Exception):
    """Raised when attempting to read or write metadata not supported by the format.

    This error indicates a format limitation (e.g., trying to write BPM to RIFF),
    not a code error. The format simply does not support the requested metadata field.

    Examples:
        - Trying to read/write ratings to RIFF
        - Trying to read/write BPM to ID3v1
        - Trying to read/write album artist to ID3v1
    """
    pass


class FieldNotSupportedByLib(Exception):
    """Raised when attempting to read or write a metadata field that is not supported by the library at all.

    This error indicates that the requested metadata field is not implemented or supported
    by any format in the library, regardless of the audio file format.

    Examples:
        - Trying to read/write a custom field that doesn't exist in UnifiedMetadataKey
        - Trying to read/write a field that is not implemented in any metadata manager
    """
    pass
class MetadataWritingConflictParametersError(Exception):
    """Raised when conflicting metadata writing parameters are specified.
    
    This error indicates that the user has provided parameters that cannot
    be used together for metadata writing operations.
    
    Examples:
        - Specifying both metadata_strategy and metadata_format
        - Other mutually exclusive metadata writing parameters
    """
    pass


class InvalidRatingValueError(Exception):
    """Raised when an invalid rating value is provided.
    
    This error indicates that the rating value cannot be converted to a valid
    numeric rating or is not in the expected format.
    
    Examples:
        - Non-numeric string values like "invalid" or "abc"
        - Values that cannot be converted to integers
        - None values when a rating is expected
    """
    pass


class InvalidMetadataFieldTypeError(TypeError):
    """Raised when a metadata field value has an unexpected type.

    Attributes:
        field: str - the unified metadata field name (e.g. 'artists')
        expected_type: str - human-readable expected type (e.g. 'list[str]')
        actual_type: str - name of the actual type received
        value: object - the actual value passed
    """
    def __init__(self, field: str, expected_type: str, actual_value):
        actual_type = type(actual_value).__name__
        message = (
            f"Invalid type for metadata field '{field}': expected {expected_type}, "
            f"got {actual_type} (value={actual_value!r})"
        )
        super().__init__(message)
        self.field = field
        self.expected_type = expected_type
        self.actual_type = actual_type
        self.value = actual_value
