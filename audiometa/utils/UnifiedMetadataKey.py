
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

    def may_contain_separated_values(self) -> bool:
        result = self in (UnifiedMetadataKey.ARTISTS_NAMES, UnifiedMetadataKey.ALBUM_ARTISTS_NAMES)
        if result and self.get_optional_type() != list[str]:
            raise ValueError(f'Optional type for {self} is not list')
        return result

    def get_optional_type(self) -> type:
        APP_METADATA_KEYS_OPTIONAL_TYPES_MAP = {
            UnifiedMetadataKey.TITLE: str,
            UnifiedMetadataKey.ARTISTS_NAMES: list[str],
            UnifiedMetadataKey.ALBUM_NAME: str,
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: list[str],
            UnifiedMetadataKey.GENRE_NAME: str,
            UnifiedMetadataKey.RATING: int,
            UnifiedMetadataKey.LANGUAGE: str,
            UnifiedMetadataKey.RELEASE_DATE: str,
            UnifiedMetadataKey.TRACK_NUMBER: int,
            UnifiedMetadataKey.BPM: int,
            UnifiedMetadataKey.COMPOSER: str,
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
            UnifiedMetadataKey.CONDUCTOR: str,
            UnifiedMetadataKey.COVER_ART: bytes,
            UnifiedMetadataKey.COMPILATION: bool,
            UnifiedMetadataKey.MEDIA_TYPE: str,
            UnifiedMetadataKey.FILE_OWNER: str,
            UnifiedMetadataKey.RECORDING_DATE: str,
            UnifiedMetadataKey.FILE_SIZE: int,
            UnifiedMetadataKey.ENCODER_SETTINGS: str,
            UnifiedMetadataKey.REPLAYGAIN: str,
            UnifiedMetadataKey.MUSICBRAINZ_ID: str,
            UnifiedMetadataKey.ARRANGER: str,
            UnifiedMetadataKey.VERSION: str,
            UnifiedMetadataKey.PERFORMANCE: str,
            UnifiedMetadataKey.ARCHIVAL_LOCATION: str,
            UnifiedMetadataKey.KEYWORDS: str,
            UnifiedMetadataKey.SUBJECT: str,
            UnifiedMetadataKey.ORIGINAL_ARTIST: str,
            UnifiedMetadataKey.SET_SUBTITLE: str,
            UnifiedMetadataKey.INITIAL_KEY: str,
            UnifiedMetadataKey.INVOLVED_PEOPLE: str,
            UnifiedMetadataKey.MUSICIANS: str,
            UnifiedMetadataKey.PART_OF_SET: str,
        }
        type = APP_METADATA_KEYS_OPTIONAL_TYPES_MAP.get(self)
        if not type:
            raise ValueError(f'No optional type defined for {self}')
        return type
