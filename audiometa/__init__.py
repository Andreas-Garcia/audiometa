"""Audio metadata handling module.

A comprehensive Python library for reading and writing audio metadata across multiple formats
including MP3, FLAC, WAV, and more. Supports ID3v1, ID3v2, Vorbis (FLAC), and RIFF (WAV) formats
with 50+ metadata fields including title, artist, album, rating, BPM, and more.

Note: OGG file support is planned but not yet implemented.

For detailed metadata support information, see the README.md file.
"""

import warnings
from mutagen.id3 import ID3

from .audio_file import AudioFile
from .exceptions import FileTypeNotSupportedError, MetadataNotSupportedError, MetadataWritingConflictParametersError
from .utils.types import AppMetadata, AppMetadataValue
from .utils.MetadataFormat import MetadataFormat
from .utils.MetadataWritingStrategy import MetadataWritingStrategy
from .utils.UnifiedMetadataKey import UnifiedMetadataKey
from .manager.id3v1.Id3v1Manager import Id3v1Manager
from .manager.MetadataManager import MetadataManager
from .manager.rating_supporting.RatingSupportingMetadataManager import RatingSupportingMetadataManager
from .manager.rating_supporting.Id3v2Manager import Id3v2Manager
from .manager.rating_supporting.RiffManager import RiffManager
from .manager.rating_supporting.VorbisManager import VorbisManager


FILE_EXTENSION_NOT_HANDLED_MESSAGE = "The file's format is not handled by the service."

TAG_FORMAT_MANAGER_CLASS_MAP = {
    MetadataFormat.ID3V1: Id3v1Manager,
    MetadataFormat.ID3V2: Id3v2Manager,
    MetadataFormat.VORBIS: VorbisManager,
    MetadataFormat.RIFF: RiffManager
}

FILE_TYPE = AudioFile | str


def _get_metadata_manager(
        file: FILE_TYPE, tag_format: MetadataFormat | None = None, normalized_rating_max_value: int | None = None, id3v2_version: tuple[int, int, int] | None = None
) -> MetadataManager:
    if not isinstance(file, AudioFile):
        file = AudioFile(file)

    audio_file_prioritized_tag_formats = MetadataFormat.get_priorities().get(file.file_extension)
    if not audio_file_prioritized_tag_formats:
        raise FileTypeNotSupportedError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)

    if not tag_format:
        tag_format = audio_file_prioritized_tag_formats[0]
    else:
        if tag_format not in audio_file_prioritized_tag_formats:
            raise FileTypeNotSupportedError(
                f"Tag format {tag_format} not supported for file extension {file.file_extension}")

    manager_class = TAG_FORMAT_MANAGER_CLASS_MAP[tag_format]
    if issubclass(manager_class, RatingSupportingMetadataManager):
        if manager_class == Id3v2Manager and id3v2_version is not None:
            return manager_class(
                audio_file=file, normalized_rating_max_value=normalized_rating_max_value, id3v2_version=id3v2_version)  # type: ignore
        else:
            return manager_class(
                audio_file=file, normalized_rating_max_value=normalized_rating_max_value)  # type: ignore
    return manager_class(audio_file=file)


def _get_metadata_managers(
    file: FILE_TYPE, tag_formats: list[MetadataFormat] | None = None, normalized_rating_max_value: int | None = None, id3v2_version: tuple[int, int, int] | None = None
) -> dict[MetadataFormat, MetadataManager]:
    if not isinstance(file, AudioFile):
        file = AudioFile(file)

    managers = {}

    if not tag_formats:
        tag_formats = MetadataFormat.get_priorities().get(file.file_extension)
        if not tag_formats:
            raise FileTypeNotSupportedError(FILE_EXTENSION_NOT_HANDLED_MESSAGE)

    for tag_format in tag_formats:
        managers[tag_format] = _get_metadata_manager(
            file=file, tag_format=tag_format, normalized_rating_max_value=normalized_rating_max_value, id3v2_version=id3v2_version)
    return managers


def get_single_format_app_metadata(
        file: FILE_TYPE, tag_format: MetadataFormat, normalized_rating_max_value: int | None = None, id3v2_version: tuple[int, int, int] | None = None) -> AppMetadata:
    """
    Get metadata from a specific format only.
    
    This function reads metadata from only the specified format, unlike
    get_merged_unified_metadata which reads from all available formats.
    
    Args:
        file: Audio file path or AudioFile object
        tag_format: Specific metadata format to read from
        normalized_rating_max_value: Maximum value for rating normalization (0-10 scale).
            When provided, ratings are normalized to this scale. Defaults to None (raw values).
        id3v2_version: ID3v2 version tuple for ID3v2-specific operations
        
    Returns:
        Dictionary containing metadata from the specified format only
        
    Raises:
        FileTypeNotSupportedError: If the file format is not supported
        FileNotFoundError: If the file does not exist
        
    Examples:
        # Get only ID3v2 metadata
        metadata = get_single_format_app_metadata("song.mp3", MetadataFormat.ID3V2)
        print(metadata.get(UnifiedMetadataKey.TITLE))
        
        # Get only Vorbis metadata from FLAC
        metadata = get_single_format_app_metadata("song.flac", MetadataFormat.VORBIS)
        print(metadata.get(UnifiedMetadataKey.ARTISTS_NAMES))
        
        # Get ID3v2 metadata with normalized ratings
        metadata = get_single_format_app_metadata("song.mp3", MetadataFormat.ID3V2, normalized_rating_max_value=100)
        print(metadata.get(UnifiedMetadataKey.RATING))  # Returns 0-100
    """
    if not isinstance(file, AudioFile):
        file = AudioFile(file)

    manager = _get_metadata_manager(
        file=file, tag_format=tag_format, normalized_rating_max_value=normalized_rating_max_value, id3v2_version=id3v2_version)
    return manager.get_app_metadata()


def get_merged_unified_metadata(
        file: FILE_TYPE, normalized_rating_max_value: int | None = None, id3v2_version: tuple[int, int, int] | None = None) -> AppMetadata:
    """
    Get all available metadata from an audio file, merging data from multiple formats.
    
    This function reads metadata from all available formats (ID3v1, ID3v2, Vorbis, RIFF)
    and returns a unified dictionary with the best available data for each field.
    
    Args:
        file: Audio file path or AudioFile object
        normalized_rating_max_value: Maximum value for rating normalization (0-10 scale).
            When provided, ratings are normalized to this scale. Defaults to None (raw values).
        id3v2_version: ID3v2 version tuple for ID3v2-specific operations
        
    Returns:
        Dictionary containing all available metadata fields
        
    Raises:
        FileTypeNotSupportedError: If the file format is not supported
        FileNotFoundError: If the file does not exist
        
    Examples:
        # Get all metadata with raw rating values
        metadata = get_merged_unified_metadata("song.mp3")
        print(metadata.get(UnifiedMetadataKey.TITLE))
        
        # Get all metadata with normalized ratings (0-100 scale)
        metadata = get_merged_unified_metadata("song.mp3", normalized_rating_max_value=100)
        print(metadata.get(UnifiedMetadataKey.RATING))  # Returns 0-100
        
        # Get metadata from FLAC file
        metadata = get_merged_unified_metadata("song.flac")
        print(metadata.get(UnifiedMetadataKey.ARTISTS_NAMES))
    """
    if not isinstance(file, AudioFile):
        file = AudioFile(file)

    # Get all available managers for this file type
    all_managers = _get_metadata_managers(file=file, normalized_rating_max_value=normalized_rating_max_value, id3v2_version=id3v2_version)
    
    # Get file-specific format priorities
    available_formats = MetadataFormat.get_priorities().get(file.file_extension, [])
    managers_by_precedence = []
    
    for format_type in available_formats:
        if format_type in all_managers:
            managers_by_precedence.append((format_type, all_managers[format_type]))

    result = {}
    for app_metadata_key in UnifiedMetadataKey:
        for format_type, manager in managers_by_precedence:
            try:
                app_metadata = manager.get_app_metadata()
                if app_metadata_key in app_metadata:
                    value = app_metadata[app_metadata_key]
                    if value is not None:
                        result[app_metadata_key] = value
                        break
            except Exception:
                # If this manager fails, continue to the next one
                continue
    return result


def get_specific_metadata(file: FILE_TYPE, app_metadata_key: UnifiedMetadataKey, normalized_rating_max_value: int | None = None, id3v2_version: tuple[int, int, int] | None = None) -> AppMetadataValue:
    """
    Get a specific metadata field from an audio file.
    
    Args:
        file: Audio file path or AudioFile object
        app_metadata_key: The metadata field to retrieve
        normalized_rating_max_value: Maximum value for rating normalization (0-10 scale).
            Only used when app_metadata_key is RATING. For other metadata fields,
            this parameter is ignored. Defaults to None (no normalization).
        id3v2_version: ID3v2 version tuple for ID3v2-specific operations
        
    Returns:
        The metadata value or None if not found
        
    Examples:
        # Get title (normalized_rating_max_value ignored)
        title = get_specific_metadata("song.mp3", UnifiedMetadataKey.TITLE)
        
        # Get rating without normalization
        rating = get_specific_metadata("song.mp3", UnifiedMetadataKey.RATING)
        
        # Get rating with 0-100 normalization
        rating = get_specific_metadata("song.mp3", UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
    """
    if not isinstance(file, AudioFile):
        file = AudioFile(file)

    managers_prioritized = _get_metadata_managers(file=file, normalized_rating_max_value=normalized_rating_max_value, id3v2_version=id3v2_version)
    
    # Try each manager in priority order until we find a value
    for _, manager in managers_prioritized.items():
        try:
            value = manager.get_app_specific_metadata(app_metadata_key=app_metadata_key)
            if value is not None:
                return value
        except Exception:
            # If this manager doesn't support the key or fails, try the next one
            continue
    
    return None


def update_file_metadata(
        file: FILE_TYPE, app_metadata: AppMetadata, normalized_rating_max_value: int | None = None, 
        id3v2_version: tuple[int, int, int] | None = None, metadata_strategy: MetadataWritingStrategy | None = None,
        metadata_format: MetadataFormat | None = None) -> None:
    """
    Update metadata in an audio file.
    
    This function writes metadata to the specified audio file using the appropriate
    format manager. It supports multiple writing strategies and format selection.
    
    Args:
        file: Audio file path or AudioFile object
        app_metadata: Dictionary containing metadata to write
        normalized_rating_max_value: Maximum value for rating normalization (0-10 scale).
            When provided, ratings are normalized to this scale. Defaults to None (raw values).
        id3v2_version: ID3v2 version tuple for ID3v2-specific operations
        metadata_strategy: Writing strategy (SYNC, PRESERVE, CLEANUP). Defaults to SYNC.
            Ignored when metadata_format is specified.
        metadata_format: Specific format to write to. If None, uses the file's native format.
            When specified, strategy is ignored and metadata is written only to this format.
        
    Returns:
        None
        
    Raises:
        FileTypeNotSupportedError: If the file format is not supported
        FileNotFoundError: If the file does not exist
        MetadataNotSupportedError: If the metadata field is not supported by the format (only for PRESERVE, CLEANUP strategies)
        MetadataWritingConflictParametersError: If both metadata_strategy and metadata_format are specified
        InvalidRatingValueError: If invalid rating values are provided
        
    Note:
        Cannot specify both metadata_strategy and metadata_format simultaneously. Choose one approach:
        
        - Use metadata_strategy for multi-format management (SYNC, PRESERVE, CLEANUP)
        - Use metadata_format for single-format writing (writes only to specified format)
        
        When metadata_format is specified, metadata is written only to that format and unsupported
        fields will raise MetadataNotSupportedError.
        
        When metadata_strategy is used (default SYNC), unsupported metadata fields are handled
        gracefully with warnings, while other strategies raise MetadataNotSupportedError.
        
    Examples:
        # Basic metadata update
        metadata = {
            UnifiedMetadataKey.TITLE: "New Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist Name"]
        }
        update_file_metadata("song.mp3", metadata)
        
        # Update with rating normalization
        metadata = {
            UnifiedMetadataKey.TITLE: "New Title",
            UnifiedMetadataKey.RATING: 75  # Will be normalized to 0-100 scale
        }
        update_file_metadata("song.mp3", metadata, normalized_rating_max_value=100)
        
        # Clean up other formats (remove ID3v1, keep only ID3v2)
        update_file_metadata("song.mp3", metadata, metadata_strategy=MetadataWritingStrategy.CLEANUP)
        
        # Write to specific format
        update_file_metadata("song.mp3", metadata, metadata_format=MetadataFormat.ID3V2)
    """
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    
    # Validate that both parameters are not specified simultaneously
    if metadata_strategy is not None and metadata_format is not None:
        raise MetadataWritingConflictParametersError(
            "Cannot specify both metadata_strategy and metadata_format. "
            "When metadata_format is specified, strategy is not applicable. "
            "Choose either: use metadata_strategy for multi-format management, "
            "or metadata_format for single-format writing."
        )
    
    # Default to SYNC strategy if not specified
    if metadata_strategy is None:
        metadata_strategy = MetadataWritingStrategy.SYNC
    
    # Handle strategy-specific behavior before writing
    _handle_metadata_strategy(file, app_metadata, metadata_strategy, normalized_rating_max_value, id3v2_version, metadata_format)


def _handle_metadata_strategy(file: AudioFile, app_metadata: AppMetadata, strategy: MetadataWritingStrategy, 
                             normalized_rating_max_value: int | None, id3v2_version: tuple[int, int, int] | None,
                             target_format: MetadataFormat | None = None) -> None:
    """Handle metadata strategy-specific behavior for all strategies."""
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    
    # Get the target format (specified format or native format)
    if target_format:
        target_format_actual = target_format
    else:
        target_format_actual = MetadataFormat.get_priorities().get(file.file_extension)[0]
    
    # When a specific format is forced, ignore strategy and write only to that format
    if target_format:
        all_managers = _get_metadata_managers(
            file=file, tag_formats=[target_format_actual], normalized_rating_max_value=normalized_rating_max_value, id3v2_version=id3v2_version)
        target_manager = all_managers[target_format_actual]
        target_manager.update_file_metadata(app_metadata)
        return
    
    # Get all available managers for this file type
    all_managers = _get_metadata_managers(
        file=file, normalized_rating_max_value=normalized_rating_max_value, id3v2_version=id3v2_version)
    
    # Get other formats (non-target)
    other_managers = {fmt: mgr for fmt, mgr in all_managers.items() if fmt != target_format_actual}
    
    if strategy == MetadataWritingStrategy.CLEANUP:
        # First, clean up non-target formats
        for fmt, manager in other_managers.items():
            try:
                manager.delete_metadata()
            except Exception:
                # Some managers might not support deletion or might fail
                pass
        
        # Then write to target format
        target_manager = all_managers[target_format_actual]
        target_manager.update_file_metadata(app_metadata)
        
    elif strategy == MetadataWritingStrategy.SYNC:
        # For SYNC, we need to write to all available formats
        # Write to target format first
        target_manager = all_managers[target_format_actual]
        try:
            target_manager.update_file_metadata(app_metadata)
        except MetadataNotSupportedError as e:
            # For SYNC strategy, log warning but continue with other formats
            warnings.warn(f"Format {target_format_actual} doesn't support some metadata fields: {e}")
        except Exception as e:
            # Re-raise user errors (like InvalidRatingValueError) immediately
            from .exceptions import InvalidRatingValueError, ConfigurationError
            if isinstance(e, (InvalidRatingValueError, ConfigurationError)):
                raise
            # Some managers might not support writing or might fail for other reasons
            pass
        
        # Then sync all other available formats
        # Note: We need to be careful about the order to avoid conflicts
        for fmt, manager in other_managers.items():
            try:
                manager.update_file_metadata(app_metadata)
            except MetadataNotSupportedError as e:
                # For SYNC strategy, log warning but continue with other formats
                warnings.warn(f"Format {fmt} doesn't support some metadata fields: {e}")
                continue
            except Exception:
                # Some managers might not support writing or might fail for other reasons
                pass
                
    elif strategy == MetadataWritingStrategy.PRESERVE:
        # For PRESERVE, we need to save existing metadata from other formats first
        preserved_metadata = {}
        for fmt, manager in other_managers.items():
            try:
                existing_metadata = manager.get_app_metadata()
                if existing_metadata:
                    preserved_metadata[fmt] = existing_metadata
            except Exception:
                pass
        
        # Write to target format
        target_manager = all_managers[target_format_actual]
        target_manager.update_file_metadata(app_metadata)
        
        # Restore preserved metadata from other formats
        for fmt, metadata in preserved_metadata.items():
            try:
                manager = other_managers[fmt]
                manager.update_file_metadata(metadata)
            except MetadataNotSupportedError:
                # Re-raise unsupported metadata errors - they should not be silently ignored
                raise
            except Exception:
                # Some managers might not support writing or might fail for other reasons
                pass


def delete_metadata(file, tag_format: MetadataFormat | None = None, id3v2_version: tuple[int, int, int] | None = None) -> bool:
    """
    Delete all metadata from an audio file.
    
    This function removes all metadata tags from the specified audio file.
    If a specific format is provided, only that format's metadata is deleted.
    
    Args:
        file: Audio file path or AudioFile object
        tag_format: Specific format to delete metadata from. If None, deletes from native format.
        id3v2_version: ID3v2 version tuple for ID3v2-specific operations
        
    Returns:
        True if metadata was successfully deleted, False otherwise
        
    Raises:
        FileTypeNotSupportedError: If the file format is not supported
        FileNotFoundError: If the file does not exist
        
    Examples:
        # Delete all metadata from native format
        success = delete_metadata("song.mp3")
        
        # Delete only ID3v2 metadata (keep ID3v1)
        success = delete_metadata("song.mp3", tag_format=MetadataFormat.ID3V2)
        
        # Delete Vorbis metadata from FLAC
        success = delete_metadata("song.flac", tag_format=MetadataFormat.VORBIS)
    """
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    return _get_metadata_manager(file, tag_format=tag_format, id3v2_version=id3v2_version).delete_metadata()


def get_bitrate(file: FILE_TYPE) -> int:
    """
    Get the bitrate of an audio file.
    
    Args:
        file: Audio file path or AudioFile object
        
    Returns:
        Bitrate in bits per second
        
    Raises:
        FileTypeNotSupportedError: If the file format is not supported
        FileNotFoundError: If the file does not exist
        
    Examples:
        bitrate = get_bitrate("song.mp3")
        print(f"Bitrate: {bitrate} bps")
    """
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    return file.get_bitrate()


def get_duration_in_sec(file: FILE_TYPE) -> float:
    """
    Get the duration of an audio file in seconds.
    
    Args:
        file: Audio file path or AudioFile object
        
    Returns:
        Duration in seconds as a float
        
    Raises:
        FileTypeNotSupportedError: If the file format is not supported
        FileNotFoundError: If the file does not exist
        
    Examples:
        duration = get_duration_in_sec("song.mp3")
        print(f"Duration: {duration:.2f} seconds")
        
        # Convert to minutes
        minutes = duration / 60
        print(f"Duration: {minutes:.2f} minutes")
    """
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    return file.get_duration_in_sec()


def is_flac_md5_valid(file: FILE_TYPE) -> bool:
    """
    Check if a FLAC file's MD5 signature is valid.
    
    This function verifies the integrity of a FLAC file by checking its MD5 signature.
    Only works with FLAC files.
    
    Args:
        file: Audio file path or AudioFile object (must be FLAC)
        
    Returns:
        True if MD5 signature is valid, False otherwise
        
    Raises:
        FileTypeNotSupportedError: If the file is not a FLAC file
        FileNotFoundError: If the file does not exist
        
    Examples:
        # Check FLAC file integrity
        is_valid = is_flac_md5_valid("song.flac")
        if is_valid:
            print("FLAC file is intact")
        else:
            print("FLAC file may be corrupted")
    """
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    return file.is_flac_file_md5_valid()


def fix_md5_checking(file: FILE_TYPE) -> str:
    """
    Returns a temporary file with corrected MD5 signature.

    Args:
        file: The file to fix MD5 for. Can be AudioFile or str path.

    Returns:
        str: Path to a temporary file containing the corrected audio data.

    Raises:
        FileTypeNotSupportedError: If the file is not a FLAC file
        FileCorruptedError: If the FLAC file is corrupted or cannot be corrected
        RuntimeError: If the FLAC command fails to execute
    """
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    return file.get_file_with_corrected_md5(delete_original=True)


def delete_potential_id3_metadata_with_header(file: FILE_TYPE) -> None:
    """
    Delete ID3 metadata headers from an audio file.
    
    This function attempts to remove ID3 metadata headers from the file.
    It's a low-level operation that directly manipulates the file structure.
    
    Args:
        file: Audio file path or AudioFile object
        
    Returns:
        None
        
    Raises:
        FileNotFoundError: If the file does not exist
        
    Examples:
        # Remove ID3 headers from MP3 file
        delete_potential_id3_metadata_with_header("song.mp3")
        
        # This is typically used for cleanup operations
        # when you want to remove all ID3 metadata
    """
    if not isinstance(file, AudioFile):
        audio_file = AudioFile(file)
    try:
        id_metadata = ID3(audio_file.get_file_path_or_object())
        id_metadata.delete()
    except Exception:
        pass
