"""Audio metadata handling module.

Metadata Support by Format:
+-----------------+---------------+---------------+---------------+---------------+----------------+
| Field           |    ID3v1      |     ID3v2     |     Vorbis    |     RIFF      |   App Support  |
+-----------------+---------------+---------------+---------------+---------------+----------------+
| Text Encoding   |    ASCII      | UTF-8/16/ISO  |    UTF-8      | ASCII/UTF-8   |    UTF-8       |
| Max Text Length | 30 chars      | ~8M chars     | ~8M chars     | ~1M chars     |    255 chars   |
| Rating Range    | Not supported | 0-255#        | 0-100#        | Not supported |    0-100#      |
| Track Number    | 0-255#        | 0-255#        | Unlimited#    | Unlimited#    |    0-999#      |
| Disc Number     | Not supported | 0-255#        | Unlimited#    | Not supported |    0-999#      |
+-----------------+---------------+---------------+---------------+---------------+----------------+
| Operations      |       R       |      R/W      |      R/W      |     R/W       |        ✓       |
| supported       |(W using v2.4) |(W using v2.4) |               |               |                |
+-----------------+---------------+---------------+---------------+---------------+----------------+
| Technical Info  |               |               |               |               |                |
| - Duration      |       ✓       |        ✓      |        ✓      |       ✓       |                |
| - Bitrate       |       ✓       |        ✓      |        ✓      |       ✓       |        ✓       |
| - Sample Rate   |       ✓       |        ✓      |        ✓      |       ✓       |                |
| - Channels      |    ✓ (1-2)    |    ✓ (1-255)  |    ✓ (1-255)  |    ✓ (1-2)    |                |
| - File Size     |       ✓       |        ✓      |        ✓      |       ✓       |        ✓       |
| - Format Info   |       ✓       |        ✓      |        ✓      |       ✓       |                |
| - MD5 Checksum  |               |               |        ✓      |               |    ✓ (Flac)    |
+-----------------+---------------+---------------+---------------+---------------+----------------+
| Title           |     ✓ (30)    |   ✓ (256)     |    ✓ (256)    |   ✓ (256)     |    ✓ (256)     |
| Artist          |     ✓ (30)    |   ✓ (256)     |    ✓ (256)    |   ✓ (256)     |    ✓ (256)     |
| Album           |     ✓ (30)    |   ✓ (256)     |    ✓ (256)    |   ✓ (256)     |    ✓ (256)     |
| Album Artist    |               |   ✓ (256)     |    ✓ (256)    |               |    ✓ (256)     |
| Genre           |     ✓ (1#)    |   ✓ (256)     |    ✓ (256)    |   ✓ (256)     |    ✓ (256)     |
| Release Date    |     ✓ (4)     |   ✓ (10)      |    ✓ (10)     |   ✓ (10)      |      (10)      |
| Track Number    |     ✓ (1#)    |   ✓ (0-255#)  |   ✓ (Unlim#)  |  ✓ (Unlim#)   |      (0-999#)  |
| Rating          |               |   ✓ (0-255#)  |    ✓ (0-100#) |               |    ✓ (0-10#)   |
| BPM             |               |   ✓ (0-65535#)|   ✓ (0-65535#)|               |      (0-999#)  |
| Language        |               |   ✓ (3)       |    ✓ (3)      |               |    ✓ (3)       |
| Composer        |               |   ✓ (256)     |    ✓ (256)    |   ✓ (256)     |      (256)     |
| Publisher       |               |   ✓ (256)     |    ✓ (256)    |               |      (256)     |
| Copyright       |               |   ✓ (256)     |    ✓ (256)    |   ✓ (256)     |      (256)     |
| Lyrics          |               |   ✓ (2000)    |    ✓ (2000)   |               |      (2000)    |
| Comment         |     ✓ (28)    |   ✓ (1000)    |    ✓ (1000)   |   ✓ (1000)    |      (1000)    |
| Encoder         |               |   ✓ (256)     |    ✓ (256)    |   ✓ (256)     |      (256)     |
| URL             |               |    ✓ (2048)   |    ✓ (2048)   |               |      (2048)    |
| ISRC            |               |    ✓ (12)     |    ✓ (12)     |               |      (12)      |
| Mood            |               |   ✓ (256)     |    ✓ (256)    |               |      (256)     |
| Key             |               |    ✓ (3)      |    ✓ (3)      |               |      (3)       |
| Original Date   |               |    ✓ (10)     |    ✓ (10)     |               |      (10)      |
| Remixer         |               |   ✓ (256)     |    ✓ (256)    |               |      (256)     |
| Conductor       |               |   ✓ (256)     |    ✓ (256)    |   ✓ (256)     |      (256)     |
| Cover Art       |               |   ✓ (10MB#)   |    ✓ (10MB#)  |               |      (10MB#)   |
| Compilation     |               |    ✓ (1#)     |    ✓ (1#)     |               |      (1#)      |
| Media Type      |               |   ✓ (256)     |    ✓ (256)    |   ✓ (256)     |      (256)     |
| File Owner      |               |   ✓ (256)     |    ✓ (256)    |               |      (256)     |
| Recording Date  |               |    ✓ (10)     |    ✓ (10)     |               |      (10)      |
| File Size       |               |    ✓ (16#)    |               |               |      (16#)     |
| Encoder Settings|               |   ✓ (1000)    |    ✓ (1000)   |               |      (1000)    |
| ReplayGain      |               |    ✓ (8#)     |    ✓ (8#)     |               |      (8#)      |
| MusicBrainz ID  |               |    ✓ (36)     |    ✓ (36)     |               |      (36)      |
| Arranger        |               |   ✓ (256)     |    ✓ (256)    |               |      (256)     |
| Version         |               |   ✓ (256)     |    ✓ (256)    |               |      (256)     |
| Performance     |               |   ✓ (256)     |    ✓ (256)    |               |      (256)     |
| Archival Location|              |               |               |   ✓ (256)     |      (256)     |
| Keywords        |               |               |               |   ✓ (256)     |      (256)     |
| Subject         |               |               |               |   ✓ (256)     |      (256)     |
| Original Artist |               |   ✓ (256)     |    ✓ (256)    |               |      (256)     |
| Set Subtitle    |               |   ✓ (256)     |    ✓ (256)    |               |      (256)     |
| Initial Key     |               |    ✓ (3)      |    ✓ (3)      |               |      (3)       |
| Involved People |               |   ✓ (1000)    |    ✓ (1000)   |               |      (1000)    |
| Musicians       |               |   ✓ (1000)    |    ✓ (1000)   |               |      (1000)    |
| Part of Set     |               |   ✓ (256)     |    ✓ (256)    |               |      (256)     |
+-----------------+---------------+---------------+---------------+---------------+----------------+
Legend:
- ✓: Supported
- (30): Fixed 30-character field
- (#): Numeric value or code
- (255): Maximum 255 characters
- (1000): Maximum 1000 characters
- (2000): Maximum 2000 characters
- (10MB#): Maximum 10 megabytes binary data
- (~8M): Approximately 8 million characters (format limit)
- (~1M): Approximately 1 million characters (format limit)
"""

from mutagen.id3 import ID3

from .audio_file import AudioFile
from .exceptions import FileTypeNotSupportedError
from .utils.types import AppMetadata, AppMetadataValue
from .utils.TagFormat import MetadataFormat
from .utils.AppMetadataKey import AppMetadataKey
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


def get_merged_app_metadata(
        file: FILE_TYPE, normalized_rating_max_value: int | None = None) -> AppMetadata:
    if not isinstance(file, AudioFile):
        file = AudioFile(file)

    managers_prioritized = _get_metadata_managers(file=file, normalized_rating_max_value=normalized_rating_max_value)
    app_metadatas_prioritized = []

    # Get normalized metadata from each manager
    for _, manager in managers_prioritized.items():
        app_metadatas_prioritized.append(manager.get_app_metadata())

    result = {}
    for app_metadata_key in AppMetadataKey:
        for app_metadata in app_metadatas_prioritized:
            if app_metadata_key in app_metadata:
                value = app_metadata[app_metadata_key]
                if value is not None:
                    result[app_metadata_key] = value
                    break
    return result


def get_specific_metadata(file: FILE_TYPE, app_metadata_key: AppMetadataKey) -> AppMetadataValue:
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
