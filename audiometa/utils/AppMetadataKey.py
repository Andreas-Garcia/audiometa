
from enum import Enum


class AppMetadataKey(str, Enum):
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
        result = self in (AppMetadataKey.ARTISTS_NAMES, AppMetadataKey.ALBUM_ARTISTS_NAMES)
        if result and self.get_optional_type() != list[str]:
            raise ValueError(f'Optional type for {self} is not list')
        return result

    def get_optional_type(self) -> type:
        APP_METADATA_KEYS_OPTIONAL_TYPES_MAP = {
            AppMetadataKey.TITLE: str,
            AppMetadataKey.ARTISTS_NAMES: list[str],
            AppMetadataKey.ALBUM_NAME: str,
            AppMetadataKey.ALBUM_ARTISTS_NAMES: list[str],
            AppMetadataKey.GENRE_NAME: str,
            AppMetadataKey.RATING: int,
            AppMetadataKey.LANGUAGE: str,
            AppMetadataKey.RELEASE_DATE: str,
            AppMetadataKey.TRACK_NUMBER: int,
            AppMetadataKey.BPM: int,
            AppMetadataKey.COMPOSER: str,
            AppMetadataKey.PUBLISHER: str,
            AppMetadataKey.COPYRIGHT: str,
            AppMetadataKey.LYRICS: str,
            AppMetadataKey.COMMENT: str,
            AppMetadataKey.ENCODER: str,
            AppMetadataKey.URL: str,
            AppMetadataKey.ISRC: str,
            AppMetadataKey.MOOD: str,
            AppMetadataKey.KEY: str,
            AppMetadataKey.ORIGINAL_DATE: str,
            AppMetadataKey.REMIXER: str,
            AppMetadataKey.CONDUCTOR: str,
            AppMetadataKey.COVER_ART: bytes,
            AppMetadataKey.COMPILATION: bool,
            AppMetadataKey.MEDIA_TYPE: str,
            AppMetadataKey.FILE_OWNER: str,
            AppMetadataKey.RECORDING_DATE: str,
            AppMetadataKey.FILE_SIZE: int,
            AppMetadataKey.ENCODER_SETTINGS: str,
            AppMetadataKey.REPLAYGAIN: str,
            AppMetadataKey.MUSICBRAINZ_ID: str,
            AppMetadataKey.ARRANGER: str,
            AppMetadataKey.VERSION: str,
            AppMetadataKey.PERFORMANCE: str,
            AppMetadataKey.ARCHIVAL_LOCATION: str,
            AppMetadataKey.KEYWORDS: str,
            AppMetadataKey.SUBJECT: str,
            AppMetadataKey.ORIGINAL_ARTIST: str,
            AppMetadataKey.SET_SUBTITLE: str,
            AppMetadataKey.INITIAL_KEY: str,
            AppMetadataKey.INVOLVED_PEOPLE: str,
            AppMetadataKey.MUSICIANS: str,
            AppMetadataKey.PART_OF_SET: str,
        }
        type = APP_METADATA_KEYS_OPTIONAL_TYPES_MAP.get(self)
        if not type:
            raise ValueError(f'No optional type defined for {self}')
        return type
