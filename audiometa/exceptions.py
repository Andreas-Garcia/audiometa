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


class MetadataNotSupportedError(Exception):
    """Raised when attempting to read or write metadata not supported by the format.

    This error indicates a format limitation (e.g., trying to write BPM to RIFF),
    not a code error. The format simply does not support the requested metadata field.

    Examples:
        - Trying to write ratings to WAV (RIFF) files
        - Trying to write BPM to ID3v1 tags
        - Trying to write album artist to ID3v1 tags
    """


class ConfigurationError(Exception):
    """Raised when there's a configuration error in the metadata manager."""
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
