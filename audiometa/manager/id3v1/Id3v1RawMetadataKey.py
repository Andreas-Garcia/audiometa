
from ...utils.AppMetadataKey import AppMetadataKey
from ...utils.types import RawMetadataKey


class Id3v1RawMetadataKey(RawMetadataKey):
    TITLE = AppMetadataKey.TITLE
    ARTISTS_NAMES_STR = AppMetadataKey.ARTISTS_NAMES
    ALBUM_NAME = AppMetadataKey.ALBUM_NAME
    GENRE_CODE_OR_NAME = 'genre_code'
    YEAR = 'year'
    TRACK_NUMBER = 'track_number'
    COMMENT = 'comment'
