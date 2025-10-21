
from enum import Enum


class UnifiedMetadataKey(str, Enum):
    TITLE = 'title'
    ARTISTS = 'artists'
    ALBUM_NAME = 'album_name'
    ALBUM_ARTISTS = 'album_artists_names'
    GENRES_NAMES = 'genre_name'
    RATING = 'rating'
    LANGUAGE = 'language'
    RELEASE_DATE = 'release_date'
    TRACK_NUMBER = 'track_number'
    BPM = 'bpm'
    COMPOSERS = 'composer'
    PUBLISHER = 'publisher'
    COPYRIGHT = 'copyright'
    LYRICS = 'lyrics'
    COMMENT = 'comment'

    def can_semantically_have_multiple_values(self) -> bool:
        # Fields that can contain multiple values (lists) - only semantically meaningful ones
        multi_value_fields = {
            UnifiedMetadataKey.ARTISTS,
            UnifiedMetadataKey.ALBUM_ARTISTS,
            UnifiedMetadataKey.GENRES_NAMES,
            UnifiedMetadataKey.COMPOSERS,
        }
        
        result = self in multi_value_fields
        if result and self.get_optional_type() != list[str]:
            raise ValueError(f'Optional type for {self} is not list')
        return result

    def get_optional_type(self) -> type:
        APP_METADATA_KEYS_OPTIONAL_TYPES_MAP = {
            UnifiedMetadataKey.TITLE: str,
            UnifiedMetadataKey.ARTISTS: list[str],
            UnifiedMetadataKey.ALBUM_NAME: str,
            UnifiedMetadataKey.ALBUM_ARTISTS: list[str],
            UnifiedMetadataKey.GENRES_NAMES: list[str],
            UnifiedMetadataKey.RATING: int,
            UnifiedMetadataKey.LANGUAGE: str,
            UnifiedMetadataKey.RELEASE_DATE: str,
            UnifiedMetadataKey.TRACK_NUMBER: int,
            UnifiedMetadataKey.BPM: int,
            UnifiedMetadataKey.COMPOSERS: list[str],
            UnifiedMetadataKey.PUBLISHER: str,
            UnifiedMetadataKey.COPYRIGHT: str,
            UnifiedMetadataKey.LYRICS: str,
            UnifiedMetadataKey.COMMENT: str,
        }
        type = APP_METADATA_KEYS_OPTIONAL_TYPES_MAP.get(self)
        if not type:
            raise ValueError(f'No optional type defined for {self}')
        return type
