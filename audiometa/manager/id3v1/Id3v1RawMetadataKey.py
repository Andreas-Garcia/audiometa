
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from ...utils.types import RawMetadataKey


class Id3v1RawMetadataKey(RawMetadataKey):
    TITLE = UnifiedMetadataKey.TITLE
    ARTISTS_NAMES_STR = UnifiedMetadataKey.ARTISTS
    ALBUM_NAME = UnifiedMetadataKey.ALBUM_NAME
    GENRE_CODE_OR_NAME = 'genre_code'
    YEAR = 'year'
    TRACK_NUMBER = 'track_number'
    COMMENT = 'comment'
