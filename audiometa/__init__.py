"""Audio metadata handling module.

A comprehensive Python library for reading and writing audio metadata across multiple formats
including MP3, FLAC, WAV, and more. Supports ID3v1, ID3v2, Vorbis (OGG/FLAC), and RIFF (WAV) formats
with 50+ metadata fields including title, artist, album, rating, BPM, and more.

For detailed metadata support information, see the README.md file.
"""

from mutagen.id3 import ID3

from .audio_file import AudioFile
from .exceptions import FileTypeNotSupportedError
from .utils.types import AppMetadata, AppMetadataValue
from .utils.MetadataFormat import MetadataFormat
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
        file: FILE_TYPE, tag_format: MetadataFormat | None = None, normalized_rating_max_value: int | None = None
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
        return manager_class(
            audio_file=file, normalized_rating_max_value=normalized_rating_max_value)  # type: ignore
    return manager_class(audio_file=file)


def _get_metadata_managers(
    file: FILE_TYPE, tag_formats: list[MetadataFormat] | None = None, normalized_rating_max_value: int | None = None
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
            file=file, tag_format=tag_format, normalized_rating_max_value=normalized_rating_max_value)
    return managers


def get_single_format_app_metadata(
        file: FILE_TYPE, tag_format: MetadataFormat, normalized_rating_max_value: int | None = None) -> AppMetadata:
    if not isinstance(file, AudioFile):
        file = AudioFile(file)

    manager = _get_metadata_manager(
        file=file, tag_format=tag_format, normalized_rating_max_value=normalized_rating_max_value)
    return manager.get_app_metadata()


def get_merged_unified_metadata(
        file: FILE_TYPE, normalized_rating_max_value: int | None = None) -> AppMetadata:
    if not isinstance(file, AudioFile):
        file = AudioFile(file)

    managers_prioritized = _get_metadata_managers(file=file, normalized_rating_max_value=normalized_rating_max_value)
    app_metadatas_prioritized = []

    # Get normalized metadata from each manager
    for _, manager in managers_prioritized.items():
        app_metadatas_prioritized.append(manager.get_app_metadata())

    result = {}
    for app_metadata_key in UnifiedMetadataKey:
        for app_metadata in app_metadatas_prioritized:
            if app_metadata_key in app_metadata:
                value = app_metadata[app_metadata_key]
                if value is not None:
                    result[app_metadata_key] = value
                    break
    return result


def get_specific_metadata(file: FILE_TYPE, app_metadata_key: UnifiedMetadataKey) -> AppMetadataValue:
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    return _get_metadata_manager(file).get_app_specific_metadata(app_metadata_key=app_metadata_key)


def update_file_metadata(
        file: FILE_TYPE, app_metadata: AppMetadata, normalized_rating_max_value: int | None = None) -> None:
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    prioritary_metadata_manager = _get_metadata_manager(
        file=file, normalized_rating_max_value=normalized_rating_max_value)
    prioritary_metadata_manager.update_file_metadata(app_metadata=app_metadata)


def delete_metadata(file, tag_format: MetadataFormat | None = None) -> bool:
    if not isinstance(file, AudioFile):
        file = AudioFile(file)
    return _get_metadata_manager(file, tag_format=tag_format).delete_metadata()


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
