
from typing import Type, cast

from mutagen._file import FileType as MutagenMetadata
from mutagen.id3 import ID3
from mutagen.id3._frames import COMM, POPM, TALB, TBPM, TCOM, TCON, TCOP, TDRC, TENC, TIT2, TKEY, TLAN, TMOO, TPE1, TPE2, TPUB, TRCK, TSRC, TYER, USLT, WOAR
from mutagen.id3._util import ID3NoHeaderError


from ...audio_file import AudioFile
from ...utils.AppMetadataKey import AppMetadataKey
from ...utils.rating_profiles import RatingWriteProfile
from ...utils.types import AppMetadataValue, RawMetadataDict, RawMetadataKey
from .RatingSupportingMetadataManager import RatingSupportingMetadataManager


class Id3v2Manager(RatingSupportingMetadataManager):
    """ID3v2 metadata manager for audio files.

    ID3v2 Version Compatibility Table:
    +---------------+----------+----------+----------+
    | Player/Device | ID3v2.2  | ID3v2.3  | ID3v2.4  |
    +---------------+----------+----------+----------+
    | Windows Media Player                           |
    |  - WMP 9-12   |    ✓     |    ✓     |    ~     |
    |  - WMP 7-8    |    ✓     |    ✓     |          |
    +---------------+----------+----------+----------+
    | iTunes                                         |
    |  - 12.x+      |    ✓     |    ✓     |    ✓     |
    |  - 7.x-11.x   |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Winamp                                         |
    |  - 5.x+       |    ✓     |    ✓     |    ✓     |
    |  - 2.x-4.x    |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | MusicBee                                       |
    |  - 3.x+       |    ✓     |    ✓     |    ✓     |
    |  - 2.x        |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | VLC                                            |
    |  - 2.x+       |    ✓     |    ✓     |    ✓     |
    |  - 1.x        |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Smartphones                                    |
    |  - iOS 7+     |    ✓     |    ✓     |    ✓     |
    |  - Android 4+ |    ✓     |    ✓     |    ✓     |
    |  - Windows    |    ✓     |    ✓     |    ✓     |
    |  - Blackberry |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Network Players                                |
    |  - Sonos      |    ✓     |    ✓     |    ✓     |
    |  - Roku       |    ✓     |    ✓     |    ~     |
    |  - Chromecast |    ✓     |    ✓     |    ✓     |
    |  - Apple TV   |    ✓     |    ✓     |    ✓     |
    +---------------+----------+----------+----------+
    |iPods/MP3 Players                               |
    |  - iPod 5G+   |    ✓     |    ✓     |    ✓     |
    |  - iPod 1-4G  |    ✓     |    ✓     |    ~     |
    |  - Zune       |    ✓     |    ✓     |    ~     |
    |  - Sony       |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Car Systems                                    |
    |  - Post-2010  |    ✓     |    ✓     |    ~     |
    |  - Pre-2010   |    ✓     |    ~     |          |
    +---------------+----------+----------+----------+
    | Home Audio Systems                             |
    |  - Post-2000  |    ✓     |    ✓     |    ~     |
    |  - Pre-2000   |    ✓     |    ~     |          |
    +---------------+----------+----------+----------+
    | DJ Software                                    |
    |  - Traktor    |    ✓     |    ✓     |    ✓     |
    |  - Serato     |    ✓     |    ✓     |    ~     |
    |  - VirtualDJ  |    ✓     |    ✓     |    ~     |
    |  - Rekordbox  |    ✓     |    ✓     |    ~     |
    |  - Mixxx      |    ✓     |    ✓     |    ~     |
    |  - Cross DJ   |    ✓     |    ✓     |    ~     |
    |  - djay Pro   |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Web Browsers                                   |
    |  - Chrome     |    ✓     |    ✓     |    ✓     |
    |  - Firefox    |    ✓     |    ✓     |    ✓     |
    |  - Safari     |    ✓     |    ✓     |    ✓     |
    |  - Edge       |    ✓     |    ✓     |    ✓     |
    +---------------+----------+----------+----------+
    | Gaming Consoles                                |
    |  - PS4/PS5    |    ✓     |    ✓     |    ✓     |
    |  - Xbox Series|    ✓     |    ✓     |    ✓     |
    |  - PS3        |    ✓     |    ✓     |    ~     |
    |  - Xbox 360   |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Smart TVs                                      |
    |  - Samsung    |    ✓     |    ✓     |    ~     |
    |  - LG         |    ✓     |    ✓     |    ~     |
    |  - Sony       |    ✓     |    ✓     |    ~     |
    |  - Android TV |    ✓     |    ✓     |    ✓     |
    +---------------+----------+----------+----------+

    Legend:
    ✓ = Full support
    ~ = Partial support/May have issues
      = No support

    Notes:
    - ID3v2.4 introduced UTF-8 encoding and unsync changes
    - Older players may have issues with ID3v2.4's changes
    - For maximum compatibility, ID3v2.3 is recommended

    - ID3:
        - Writing Policy:
            * The app always writes ID3v2 tags in v2.4 format
            * When updating an existing file:
                - v2.4 tags are updated in place
                - v2.3 or v2.2 tags are upgraded to v2.4
                - Frame IDs are automatically converted
                - All text is encoded in UTF-8
            * Reading supports all versions (v2.2, v2.3, v2.4)
            * Only one ID3v2 version can exist in a file at a time
            * Native format for MP3 files

        - ID3v1:
            * Fixed 128-byte format at end of file
            * ASCII only, no Unicode
            * Limited to 30 chars for text fields
            * Single byte for track number (v1.1 only)
            * Genre limited to predefined codes (0-147)
            * Legacy format, read-only support

        - ID3v2:
            * v2.2:
                - Introduced in 1998
                - Three-character frame IDs (TT2, TP1, etc.)
                - ISO-8859-1 or UCS-2 text encoding
                - All standard fields supported
                - Simpler header structure than v2.3/v2.4
                - Basic support for embedded images
                - Less common but equally functional

            * v2.3:
                - Introduced in 1999
                - TYER+TDAT frames for date (year and date separately)
                - UTF-16/UTF-16BE text encoding
                - Basic unsynchronization
                - All metadata fields supported
                - Better support for embedded images and other binary data
                - Most widely used version

            * v2.4:
                - Introduced in 2000
                - TDRC frame for full timestamps (YYYY-MM-DD)
                - UTF-8 text encoding
                - Extended header features
                - Unsynchronization per frame
                - All metadata fields supported
                - New frames for more detailed metadata (e.g., TDRC for recording time, TDRL for release time)
                - Preferred version for new tags

    For the most compatibility, ID3v2.3 will be used as the version for writing metadata.
    Thus when reading/updating an existing file, the ID3 tags will be updated to v2.3 format.
    """

    ID3_RATING_APP_EMAIL = "audiometa-python@audiometa.dev"

    class Id3TextFrame(RawMetadataKey):
        TITLE = 'TIT2'
        ARTISTS_NAMES = 'TPE1'
        ALBUM_NAME = 'TALB'
        ALBUM_ARTISTS_NAMES = 'TPE2'
        GENRE_NAME = 'TCON'

        # In cleaned metadata, the rating is stored as a tuple the potential identifier (e.g. 'Traktor') and the rating
        # value
        RATING = 'POPM'
        LANGUAGE = 'TLAN'
        RECORDING_TIME = 'TDRC'  # ID3v2.4 recording time
        YEAR = 'TYER'  # ID3v2.3 year
        TRACK_NUMBER = 'TRCK'
        BPM = 'TBPM'
        
        # Additional metadata fields
        COMPOSER = 'TCOM'
        PUBLISHER = 'TPUB'
        COPYRIGHT = 'TCOP'
        LYRICS = 'USLT'  # Unsynchronized lyrics frame
        COMMENT = 'COMM'  # Comment frame
        ENCODER = 'TENC'
        URL = 'WOAR'  # Official artist/performer webpage
        ISRC = 'TSRC'
        MOOD = 'TMOO'
        KEY = 'TKEY'

    ID3_TEXT_FRAME_CLASS_MAP: dict[RawMetadataKey, Type] = {
        Id3TextFrame.TITLE: TIT2,
        Id3TextFrame.ARTISTS_NAMES: TPE1,
        Id3TextFrame.ALBUM_NAME: TALB,
        Id3TextFrame.ALBUM_ARTISTS_NAMES: TPE2,
        Id3TextFrame.GENRE_NAME: TCON,
        Id3TextFrame.LANGUAGE: TLAN,
        Id3TextFrame.RECORDING_TIME: TDRC,
        Id3TextFrame.YEAR: TYER,
        Id3TextFrame.TRACK_NUMBER: TRCK,
        Id3TextFrame.BPM: TBPM,
        Id3TextFrame.RATING: POPM,
        Id3TextFrame.COMPOSER: TCOM,
        Id3TextFrame.PUBLISHER: TPUB,
        Id3TextFrame.COPYRIGHT: TCOP,
        Id3TextFrame.LYRICS: USLT,
        Id3TextFrame.COMMENT: COMM,
        Id3TextFrame.ENCODER: TENC,
        Id3TextFrame.URL: WOAR,
        Id3TextFrame.ISRC: TSRC,
        Id3TextFrame.MOOD: TMOO,
        Id3TextFrame.KEY: TKEY,
    }

    def __init__(self, audio_file: AudioFile, normalized_rating_max_value: int | None = None):
        metadata_keys_direct_map_read = {
            AppMetadataKey.TITLE: self.Id3TextFrame.TITLE,
            AppMetadataKey.ARTISTS_NAMES: self.Id3TextFrame.ARTISTS_NAMES,
            AppMetadataKey.ALBUM_NAME: self.Id3TextFrame.ALBUM_NAME,
            AppMetadataKey.ALBUM_ARTISTS_NAMES: self.Id3TextFrame.ALBUM_ARTISTS_NAMES,
            AppMetadataKey.GENRE_NAME: self.Id3TextFrame.GENRE_NAME,
            AppMetadataKey.RATING: None,
            AppMetadataKey.LANGUAGE: self.Id3TextFrame.LANGUAGE,
            AppMetadataKey.COMPOSER: self.Id3TextFrame.COMPOSER,
            AppMetadataKey.PUBLISHER: self.Id3TextFrame.PUBLISHER,
            AppMetadataKey.COPYRIGHT: self.Id3TextFrame.COPYRIGHT,
            AppMetadataKey.LYRICS: self.Id3TextFrame.LYRICS,
            AppMetadataKey.COMMENT: self.Id3TextFrame.COMMENT,
            AppMetadataKey.ENCODER: self.Id3TextFrame.ENCODER,
            AppMetadataKey.URL: self.Id3TextFrame.URL,
            AppMetadataKey.ISRC: self.Id3TextFrame.ISRC,
            AppMetadataKey.MOOD: self.Id3TextFrame.MOOD,
            AppMetadataKey.KEY: self.Id3TextFrame.KEY,
        }
        metadata_keys_direct_map_write: dict = {
            AppMetadataKey.TITLE: self.Id3TextFrame.TITLE,
            AppMetadataKey.ARTISTS_NAMES: self.Id3TextFrame.ARTISTS_NAMES,
            AppMetadataKey.ALBUM_NAME: self.Id3TextFrame.ALBUM_NAME,
            AppMetadataKey.ALBUM_ARTISTS_NAMES: self.Id3TextFrame.ALBUM_ARTISTS_NAMES,
            AppMetadataKey.GENRE_NAME: self.Id3TextFrame.GENRE_NAME,
            AppMetadataKey.RATING: self.Id3TextFrame.RATING,
            AppMetadataKey.LANGUAGE: self.Id3TextFrame.LANGUAGE,
            AppMetadataKey.COMPOSER: self.Id3TextFrame.COMPOSER,
            AppMetadataKey.PUBLISHER: self.Id3TextFrame.PUBLISHER,
            AppMetadataKey.COPYRIGHT: self.Id3TextFrame.COPYRIGHT,
            AppMetadataKey.LYRICS: self.Id3TextFrame.LYRICS,
            AppMetadataKey.COMMENT: self.Id3TextFrame.COMMENT,
            AppMetadataKey.ENCODER: self.Id3TextFrame.ENCODER,
            AppMetadataKey.URL: self.Id3TextFrame.URL,
            AppMetadataKey.ISRC: self.Id3TextFrame.ISRC,
            AppMetadataKey.MOOD: self.Id3TextFrame.MOOD,
            AppMetadataKey.KEY: self.Id3TextFrame.KEY,
        }

        super().__init__(audio_file=audio_file,
                         metadata_keys_direct_map_read=metadata_keys_direct_map_read,
                         metadata_keys_direct_map_write=metadata_keys_direct_map_write,
                         rating_write_profile=RatingWriteProfile.BASE_255_NON_PROPORTIONAL,
                         normalized_rating_max_value=normalized_rating_max_value)

    def _extract_mutagen_metadata(self) -> MutagenMetadata:
        try:
            return ID3(self.audio_file.get_file_path_or_object(), load_v1=False)  # type: ignore[return-value]
        except ID3NoHeaderError:
            try:
                id3 = ID3(self.audio_file.get_file_path_or_object(), load_v1=True)
                id3.clear()  # Exclude ID3v1 tags
                return id3  # type: ignore[return-value]
            except ID3NoHeaderError:
                id3 = ID3()
                id3.save(self.audio_file.get_file_path_or_object(), v2_version=3)
                return id3  # type: ignore[return-value]

    def _convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(
            self, raw_mutagen_metadata: MutagenMetadata) -> RawMetadataDict:
        raw_metadata_id3: ID3 = cast(ID3, raw_mutagen_metadata)
        result = {}

        for frame_key in self.Id3TextFrame:
            if frame_key == self.Id3TextFrame.RATING:
                for raw_mutagen_frame in raw_mutagen_metadata.items():
                    popm_key = raw_mutagen_frame[0]
                    if popm_key.startswith(self.Id3TextFrame.RATING):
                        popm: POPM = raw_mutagen_frame[1]
                        popm_key_without_prefixes = popm_key.replace(f'{self.Id3TextFrame.RATING}:', '')
                        result[self.Id3TextFrame.RATING] = [
                            popm_key_without_prefixes, popm.rating]  # type: ignore[index]
                        break
            elif frame_key == self.Id3TextFrame.COMMENT:
                # Handle COMM frames (comment frames)
                for raw_mutagen_frame in raw_mutagen_metadata.items():
                    if raw_mutagen_frame[0].startswith('COMM'):
                        comm_frame = raw_mutagen_frame[1]
                        result[frame_key] = comm_frame.text
                        break
            elif frame_key == self.Id3TextFrame.LYRICS:
                # Handle USLT frames (unsynchronized lyrics frames)
                for raw_mutagen_frame in raw_mutagen_metadata.items():
                    if raw_mutagen_frame[0].startswith('USLT'):
                        uslt_frame = raw_mutagen_frame[1]
                        result[frame_key] = [uslt_frame.text]
                        break
            elif frame_key == self.Id3TextFrame.URL:
                # Handle WOAR frames (official artist/performer webpage)
                for raw_mutagen_frame in raw_mutagen_metadata.items():
                    if raw_mutagen_frame[0].startswith('WOAR'):
                        woar_frame = raw_mutagen_frame[1]
                        result[frame_key] = [woar_frame.url]
                        break
            else:
                frame_value = frame_key in raw_metadata_id3 and raw_metadata_id3[frame_key]
                if not frame_value:
                    continue

                if not frame_value.text:
                    continue

                result[frame_key] = frame_value.text

        return result

    def _get_raw_rating_by_traktor_or_not(self, raw_clean_metadata: RawMetadataDict) -> tuple[int | None, bool]:
        for raw_metadata_key, raw_metadata_values in raw_clean_metadata.items():
            if raw_metadata_values and len(raw_metadata_values) > 0:
                if raw_metadata_key == self.Id3TextFrame.RATING:
                    first_popm = cast(list, raw_metadata_values)
                    first_popm_identifier = first_popm[0]
                    first_popm_rating = first_popm[1]
                    if first_popm_identifier.find("Traktor") != -1:
                        return int(first_popm_rating), True
                    return int(first_popm_rating), False

        return None, False

    def _update_formatted_value_in_raw_mutagen_metadata(self, raw_mutagen_metadata: RawMetadataDict,
                                                        raw_metadata_key: RawMetadataKey,
                                                        app_metadata_value: AppMetadataValue):
        raw_mutagen_metadata_id3: ID3 = cast(ID3, raw_mutagen_metadata)
        raw_mutagen_metadata_id3.delall(raw_metadata_key)
        text_frame_class = self.ID3_TEXT_FRAME_CLASS_MAP[raw_metadata_key]

        if raw_metadata_key == self.Id3TextFrame.RATING:
            raw_mutagen_metadata_id3.add(text_frame_class(email=self.ID3_RATING_APP_EMAIL, rating=app_metadata_value))
        elif raw_metadata_key == self.Id3TextFrame.COMMENT:
            # Handle COMM frames (comment frames)
            raw_mutagen_metadata_id3.add(text_frame_class(encoding=3, lang='eng', desc='', text=app_metadata_value))
        elif raw_metadata_key == self.Id3TextFrame.LYRICS:
            # Handle USLT frames (unsynchronized lyrics frames)
            raw_mutagen_metadata_id3.add(text_frame_class(encoding=3, lang='eng', desc='', text=app_metadata_value))
        elif raw_metadata_key == self.Id3TextFrame.URL:
            # Handle WOAR frames (official artist/performer webpage)
            raw_mutagen_metadata_id3.add(text_frame_class(url=app_metadata_value))
        else:
            raw_mutagen_metadata_id3.add(text_frame_class(encoding=3, text=app_metadata_value))

    def delete_metadata(self) -> bool:
        """Delete all ID3v2 metadata from the audio file.

        This removes all ID3v2 frames from the file while preserving the audio data.
        Uses ID3.delete() which is more reliable than deleting individual frames,
        especially for non-MP3 files like FLAC that might have ID3v2 tags.

        Returns:
            bool: True if metadata was successfully deleted, False otherwise
        """
        try:
            # Create a new ID3 instance and use delete() to remove all ID3v2 tags
            id3 = ID3(self.audio_file.file_path)
            id3.delete()
            return True
        except ID3NoHeaderError:
            # No ID3 tags present, consider this a success
            return True
        except Exception:
            return False
