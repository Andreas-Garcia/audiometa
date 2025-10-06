"""Audio metadata handling module.

A comprehensive Python library for reading and writing audio metadata across multiple formats
including MP3, FLAC, WAV, and more. Supports ID3v1, ID3v2, Vorbis (FLAC), and RIFF (WAV) formats
with 50+ metadata fields including title, artist, album, rating, BPM, and more.

Note: OGG file support is planned but not yet implemented.

For detailed metadata support information, see the README.md file.
"""

from mutagen.id3 import ID3

from .audio_file import AudioFile
from .exceptions import FileTypeNotSupportedError
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
    if not isinstance(file, AudioFile):
        file = AudioFile(file)

    manager = _get_metadata_manager(
        file=file, tag_format=tag_format, normalized_rating_max_value=normalized_rating_max_value, id3v2_version=id3v2_version)
    return manager.get_app_metadata()


def get_merged_unified_metadata(
        file: FILE_TYPE, normalized_rating_max_value: int | None = None, id3v2_version: tuple[int, int, int] | None = None) -> AppMetadata:
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


def get_specific_metadata(file: FILE_TYPE, app_metadata_key: UnifiedMetadataKey, id3v2_version: tuple[int, int, int] | None = None) -> AppMetadataValue:
    if not isinstance(file, AudioFile):
        file = AudioFile(file)

    managers_prioritized = _get_metadata_managers(file=file, id3v2_version=id3v2_version)
    
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
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    
    # Default to PRESERVE strategy if not specified
    if metadata_strategy is None:
        metadata_strategy = MetadataWritingStrategy.PRESERVE
    
    # Handle strategy-specific behavior before writing
    if metadata_strategy in [MetadataWritingStrategy.CLEANUP, MetadataWritingStrategy.SYNC, MetadataWritingStrategy.PRESERVE]:
        _handle_metadata_strategy(file, app_metadata, metadata_strategy, normalized_rating_max_value, id3v2_version, metadata_format)
    else:
        # For IGNORE strategy, just write to the target format
        if metadata_format:
            target_manager = _get_metadata_manager(
                file=file, tag_format=metadata_format, normalized_rating_max_value=normalized_rating_max_value, id3v2_version=id3v2_version)
        else:
            target_manager = _get_metadata_manager(
                file=file, normalized_rating_max_value=normalized_rating_max_value, id3v2_version=id3v2_version)
        
        target_manager.update_file_metadata(app_metadata=app_metadata)


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
        target_manager.update_file_metadata(app_metadata)
        
        # Then sync all other available formats
        # Note: We need to be careful about the order to avoid conflicts
        for fmt, manager in other_managers.items():
            try:
                manager.update_file_metadata(app_metadata)
            except Exception:
                # Some managers might not support writing or might fail
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
            except Exception:
                # Some managers might not support writing or might fail
                pass


def delete_metadata(file, tag_format: MetadataFormat | None = None, id3v2_version: tuple[int, int, int] | None = None) -> bool:
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    return _get_metadata_manager(file, tag_format=tag_format, id3v2_version=id3v2_version).delete_metadata()


def get_bitrate(file: FILE_TYPE) -> int:
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    return file.get_bitrate()


def get_duration_in_sec(file: FILE_TYPE) -> float:
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    return file.get_duration_in_sec()


def is_flac_md5_valid(file: FILE_TYPE) -> bool:
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
    if not isinstance(file, AudioFile):
        audio_file = AudioFile(file)
    try:
        id_metadata = ID3(audio_file.get_file_path_or_object())
        id_metadata.delete()
    except Exception:
        pass
