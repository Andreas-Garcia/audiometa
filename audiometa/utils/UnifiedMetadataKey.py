
from enum import Enum


class UnifiedMetadataKey(str, Enum):
    TITLE = 'title'
    ARTISTS_NAMES = 'artists_names'
    ALBUM_NAME = 'album_name'
    ALBUM_ARTISTS_NAMES = 'album_artists_names'
    GENRE_NAME = 'genre_name'
    RATING = 'rating'
    LANGUAGE = 'language'
    RELEASE_DATE = 'release_date'
    TRACK_NUMBER = 'track_number'
    BPM = 'bpm'
    COMPOSER = 'composer'
    PUBLISHER = 'publisher'
    COPYRIGHT = 'copyright'
    LYRICS = 'lyrics'
    COMMENT = 'comment'
    ENCODER = 'encoder'
    URL = 'url'
    ISRC = 'isrc'
    MOOD = 'mood'
    KEY = 'key'
    ORIGINAL_DATE = 'original_date'
    REMIXER = 'remixer'
    CONDUCTOR = 'conductor'
    COVER_ART = 'cover_art'
    COMPILATION = 'compilation'
    MEDIA_TYPE = 'media_type'
    FILE_OWNER = 'file_owner'
    RECORDING_DATE = 'recording_date'
    FILE_SIZE = 'file_size'
    ENCODER_SETTINGS = 'encoder_settings'
    REPLAYGAIN = 'replaygain'
    MUSICBRAINZ_ID = 'musicbrainz_id'
    ARRANGER = 'arranger'
    VERSION = 'version'
    PERFORMANCE = 'performance'
    ARCHIVAL_LOCATION = 'archival_location'
    KEYWORDS = 'keywords'
    SUBJECT = 'subject'
    ORIGINAL_ARTIST = 'original_artist'
    SET_SUBTITLE = 'set_subtitle'
    INITIAL_KEY = 'initial_key'
    INVOLVED_PEOPLE = 'involved_people'
    MUSICIANS = 'musicians'
    PART_OF_SET = 'part_of_set'

    def can_semantically_have_multiple_values(self) -> bool:
        # Fields that can contain multiple values (lists) - only semantically meaningful ones
        multi_value_fields = {
            UnifiedMetadataKey.ARTISTS_NAMES,
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES,
            # Only fields that semantically make sense to have multiple values
            UnifiedMetadataKey.GENRE_NAME,  # Multiple genres make sense
            UnifiedMetadataKey.COMPOSER,    # Multiple composers make sense
            UnifiedMetadataKey.MUSICIANS,   # Multiple musicians make sense
            UnifiedMetadataKey.CONDUCTOR,   # Multiple conductors make sense
            UnifiedMetadataKey.ARRANGER,    # Multiple arrangers make sense
        }
        
        result = self in multi_value_fields
        if result and self.get_optional_type() != list[str]:
            raise ValueError(f'Optional type for {self} is not list')
        return result

    def get_optional_type(self) -> type:
        APP_METADATA_KEYS_OPTIONAL_TYPES_MAP = {
            UnifiedMetadataKey.TITLE: str,
            UnifiedMetadataKey.ARTISTS_NAMES: list[str],
            UnifiedMetadataKey.ALBUM_NAME: str,
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: list[str],
            UnifiedMetadataKey.GENRE_NAME: list[str],
            UnifiedMetadataKey.RATING: int,
            UnifiedMetadataKey.LANGUAGE: str,
            UnifiedMetadataKey.RELEASE_DATE: str,
            UnifiedMetadataKey.TRACK_NUMBER: int,
            UnifiedMetadataKey.BPM: int,
            UnifiedMetadataKey.COMPOSER: list[str],
            UnifiedMetadataKey.PUBLISHER: str,
            UnifiedMetadataKey.COPYRIGHT: str,
            UnifiedMetadataKey.LYRICS: str,
            UnifiedMetadataKey.COMMENT: str,
            UnifiedMetadataKey.ENCODER: str,
            UnifiedMetadataKey.URL: str,
            UnifiedMetadataKey.ISRC: str,
            UnifiedMetadataKey.MOOD: str,
            UnifiedMetadataKey.KEY: str,
            UnifiedMetadataKey.ORIGINAL_DATE: str,
            UnifiedMetadataKey.REMIXER: str,
            UnifiedMetadataKey.CONDUCTOR: list[str],
            UnifiedMetadataKey.COVER_ART: bytes,
            UnifiedMetadataKey.COMPILATION: bool,
            UnifiedMetadataKey.MEDIA_TYPE: str,
            UnifiedMetadataKey.FILE_OWNER: str,
            UnifiedMetadataKey.RECORDING_DATE: str,
            UnifiedMetadataKey.FILE_SIZE: int,
            UnifiedMetadataKey.ENCODER_SETTINGS: str,
            UnifiedMetadataKey.REPLAYGAIN: str,
            UnifiedMetadataKey.MUSICBRAINZ_ID: str,
            UnifiedMetadataKey.ARRANGER: list[str],
            UnifiedMetadataKey.VERSION: str,
            UnifiedMetadataKey.PERFORMANCE: str,
            UnifiedMetadataKey.ARCHIVAL_LOCATION: str,
            UnifiedMetadataKey.KEYWORDS: str,
            UnifiedMetadataKey.SUBJECT: str,
            UnifiedMetadataKey.ORIGINAL_ARTIST: str,
            UnifiedMetadataKey.SET_SUBTITLE: str,
            UnifiedMetadataKey.INITIAL_KEY: str,
            UnifiedMetadataKey.INVOLVED_PEOPLE: str,
            UnifiedMetadataKey.MUSICIANS: list[str],
            UnifiedMetadataKey.PART_OF_SET: str,
        }
        type = APP_METADATA_KEYS_OPTIONAL_TYPES_MAP.get(self)
        if not type:
            raise ValueError(f'No optional type defined for {self}')
        return type
