
from typing import TypeVar, cast

from mutagen._file import FileType as MutagenMetadata
from mutagen.flac import FLAC, VCFLACDict

from ...audio_file import AudioFile
from ...exceptions import ConfigurationError, FileCorruptedError, InvalidChunkDecodeError
from ...utils.rating_profiles import RatingWriteProfile
from ...utils.types import AppMetadataValue, RawMetadataDict, RawMetadataKey
from ..MetadataManager import UnifiedMetadataKey
from .RatingSupportingMetadataManager import RatingSupportingMetadataManager


T = TypeVar('T', str, int)


class VorbisManager(RatingSupportingMetadataManager):
    """
    Manages Vorbis comments for audio files.

    Vorbis comments are used to store metadata in audio files, primarily in FLAC format.
    (OGG file support is planned but not yet implemented.)
    They are more flexible and extensible compared to ID3 tags, allowing for a wide range of metadata fields.

    Genre Support:
    Like ID3v2 but unlike ID3v1 and RIFF, Vorbis comments support:
    - Custom genre names as free text
    - Multiple genres (comma-separated)
    - No length limitations
    - Unicode support for international genres
    - No predefined genre list restrictions

    Vorbis comments are key-value pairs, where the key is a field name and the value is the corresponding metadata.
    Common fields are defined in the VorbisKey enum class, which includes standardized keys for metadata like
    title, artist, album, genre, rating, and more.

    Compatible Extensions:
    - FLAC: Fully supports Vorbis comments.

    TODO: OGG file support is planned but not yet implemented.
    
    Note: This class assumes that the audio files being managed are primarily in FLAC format that supports Vorbis comments.
    """

    class VorbisKey(RawMetadataKey):
        TITLE = 'title'
        ARTIST_NAME = 'artist'
        ALBUM_NAME = 'album'
        ALBUM_ARTISTS_NAMES = 'albumartist'
        GENRE_NAME = 'genre'
        RATING = 'rating'
        RATING_TRAKTOR = 'rating wmp'  # Traktor rating
        LANGUAGE = 'language'
        DATE = 'date'  # Creation/Release date
        TRACK_NUMBER = 'tracknumber'
        BPM = 'bpm'
        COMMENT = 'comment'
        COMPOSER = 'composer'
        PERFORMER = 'performer'
        COPYRIGHT = 'copyright'
        LICENSE = 'license'
        ORGANIZATION = 'organization'  # Label or organization
        DESCRIPTION = 'description'
        LOCATION = 'location'  # Recording location
        CONTACT = 'contact'  # Contact information
        ISRC = 'isrc'  # International Standard Recording Code
        ENCODED_BY = 'encodedby'  # Encoder software

    def __init__(self, audio_file: AudioFile, normalized_rating_max_value: int | None = None):
        metadata_keys_direct_map_read = {
            UnifiedMetadataKey.TITLE: self.VorbisKey.TITLE,
            UnifiedMetadataKey.ARTISTS_NAMES: self.VorbisKey.ARTIST_NAME,
            UnifiedMetadataKey.ALBUM_NAME: self.VorbisKey.ALBUM_NAME,
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: self.VorbisKey.ALBUM_ARTISTS_NAMES,
            UnifiedMetadataKey.GENRE_NAME: self.VorbisKey.GENRE_NAME,
            UnifiedMetadataKey.RATING: None,
            UnifiedMetadataKey.LANGUAGE: self.VorbisKey.LANGUAGE,
            UnifiedMetadataKey.RELEASE_DATE: self.VorbisKey.DATE,
            UnifiedMetadataKey.BPM: self.VorbisKey.BPM,
        }
        metadata_keys_direct_map_write = {
            UnifiedMetadataKey.TITLE: self.VorbisKey.TITLE,
            UnifiedMetadataKey.ARTISTS_NAMES: self.VorbisKey.ARTIST_NAME,
            UnifiedMetadataKey.ALBUM_NAME: self.VorbisKey.ALBUM_NAME,
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: self.VorbisKey.ALBUM_ARTISTS_NAMES,
            UnifiedMetadataKey.GENRE_NAME: self.VorbisKey.GENRE_NAME,
            UnifiedMetadataKey.RATING: None,
            UnifiedMetadataKey.LANGUAGE: self.VorbisKey.LANGUAGE,
            UnifiedMetadataKey.RELEASE_DATE: self.VorbisKey.DATE,
            UnifiedMetadataKey.BPM: self.VorbisKey.BPM,
        }
        super().__init__(audio_file=audio_file,
                         metadata_keys_direct_map_read=metadata_keys_direct_map_read,
                         metadata_keys_direct_map_write=metadata_keys_direct_map_write,
                         rating_write_profile=RatingWriteProfile.BASE_100_PROPORTIONAL,
                         normalized_rating_max_value=normalized_rating_max_value)

    def _extract_mutagen_metadata(self) -> MutagenMetadata:
        try:
            return FLAC(self.audio_file.get_file_path_or_object())
        except Exception as error:
            error_str = str(error)
            if "InvalidChunk" in error_str and "UnicodeDecodeError" in error_str:
                raise InvalidChunkDecodeError(error_str)
            if "file said" in error_str and "bytes, read" in error_str:
                raise FileCorruptedError(f"File size mismatch: {error_str}")
            raise

    def _convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(
            self, raw_mutagen_metadata: MutagenMetadata) -> RawMetadataDict:
        raw_mutagen_metadata_flac: FLAC = cast(FLAC, raw_mutagen_metadata)
        metadata = raw_mutagen_metadata_flac.tags
        if isinstance(metadata, dict):
            return metadata
        elif isinstance(metadata, VCFLACDict):
            return dict(metadata)
        elif not metadata:
            return {}
        else:
            raise FileCorruptedError(f"Invalid Vorbis metadata type: {type(metadata)}")

    def _get_raw_rating_by_traktor_or_not(self, raw_clean_metadata: RawMetadataDict) -> tuple[int | None, bool]:
        rating_list = raw_clean_metadata.get(self.VorbisKey.RATING)

        if rating_list and len(rating_list) > 0 and rating_list[0] is not None:
            return int(rating_list[0]), False

        rating_list = raw_clean_metadata.get(self.VorbisKey.RATING_TRAKTOR)
        if rating_list and len(rating_list) > 0 and rating_list[0] is not None:
            return int(rating_list[0]), True

        return None, False

    def _update_formatted_value_in_raw_mutagen_metadata(self, raw_mutagen_metadata: MutagenMetadata,
                                                        raw_metadata_key: RawMetadataKey,
                                                        app_metadata_value: AppMetadataValue):
        if app_metadata_value is not None:
            if raw_metadata_key not in raw_mutagen_metadata:
                raw_mutagen_metadata[raw_metadata_key] = [1]
            # Convert BPM to string for Vorbis comments
            if raw_metadata_key == self.VorbisKey.BPM:
                raw_mutagen_metadata[raw_metadata_key] = str(app_metadata_value)
            else:
                raw_mutagen_metadata[raw_metadata_key] = app_metadata_value
        elif raw_metadata_key in raw_mutagen_metadata:
            del raw_mutagen_metadata[raw_metadata_key]

    def _update_undirectly_mapped_metadata(self, raw_mutagen_metadata: MutagenMetadata,
                                           app_metadata_value: AppMetadataValue,
                                           app_metadata_key: UnifiedMetadataKey):
        if app_metadata_key == UnifiedMetadataKey.RATING:
            if app_metadata_value is not None:
                app_metadata_value = str(app_metadata_value)
            self._update_formatted_value_in_raw_mutagen_metadata(raw_mutagen_metadata=raw_mutagen_metadata,
                                                                 raw_metadata_key=self.VorbisKey.RATING,
                                                                 app_metadata_value=app_metadata_value)
        else:
            raise ConfigurationError('Metadata key not handled')
