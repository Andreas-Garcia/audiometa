import struct
from typing import TypeVar, cast

import taglib

from ...audio_file import AudioFile
from ...exceptions import FileCorruptedError, MetadataNotSupportedByFormatError
from ...utils.rating_profiles import RatingWriteProfile
from ...utils.types import UnifiedMetadata, AppMetadataValue, RawMetadataDict, RawMetadataKey
from ..MetadataManager import UnifiedMetadataKey
from .RatingSupportingMetadataManager import RatingSupportingMetadataManager


T = TypeVar('T', str, int)


class VorbisManager(RatingSupportingMetadataManager):
    """
    Manages Vorbis comments for audio files.

    Vorbis comments are used to store metadata in audio files, primarily in FLAC format.
    (OGG file support is planned but not yet implemented.)
    They are more flexible and extensible compared to ID3 tags, allowing for a wide range of metadata fields.

    Vorbis comments are key-value pairs, where the key is a field name and the value is the corresponding metadata.
    Common fields are defined in the VorbisKey enum class, which includes standardized keys for metadata like
    title, artist, album, genre, rating, and more.

    Note: This implementation uses TagLib instead of mutagen because mutagen converts all Vorbis comment
    keys to lowercase during both reading and writing operations. 
    - for reading, this falsifies the raw data
    representation. 
    - for writing, converting keys to lowercase is not recommended by the Vorbis specification, which suggests 
    uppercase..

    Compatible Extensions:
    - FLAC: Fully supports Vorbis comments.

    TODO: OGG file support is planned but not yet implemented.
    """

    class VorbisKey(RawMetadataKey):
        TITLE = 'TITLE'
        ARTIST_NAME = 'ARTIST'
        ALBUM = 'ALBUM'
        ALBUM_ARTISTS = 'ALBUMARTIST'
        GENRES_NAMES = 'GENRE'
        RATING = 'RATING'
        RATING_TRAKTOR = 'RATING WMP'  # Traktor rating
        LANGUAGE = 'LANGUAGE'
        DATE = 'DATE'  # Creation/Release date
        TRACK_NUMBER = 'TRACKNUMBER'
        BPM = 'BPM'
        COMMENT = 'COMMENT'
        COMPOSERS = 'COMPOSER'
        PERFORMER = 'PERFORMER'
        COPYRIGHT = 'COPYRIGHT'
        LICENSE = 'LICENSE'
        ORGANIZATION = 'ORGANIZATION'  # Label or organization
        DESCRIPTION = 'DESCRIPTION'
        LOCATION = 'LOCATION'  # Recording location
        CONTACT = 'CONTACT'  # Contact information
        ISRC = 'ISRC'  # International Standard Recording Code
        ENCODED_BY = 'ENCODEDBY'  # Encoder software

    def __init__(self, audio_file: AudioFile, normalized_rating_max_value: int | None = None):
        metadata_keys_direct_map_read = {
            UnifiedMetadataKey.TITLE: self.VorbisKey.TITLE,
            UnifiedMetadataKey.ARTISTS: self.VorbisKey.ARTIST_NAME,
            UnifiedMetadataKey.ALBUM: self.VorbisKey.ALBUM,
            UnifiedMetadataKey.ALBUM_ARTISTS: self.VorbisKey.ALBUM_ARTISTS,
            UnifiedMetadataKey.GENRES_NAMES: self.VorbisKey.GENRES_NAMES,
            UnifiedMetadataKey.RATING: None,
            UnifiedMetadataKey.LANGUAGE: self.VorbisKey.LANGUAGE,
            UnifiedMetadataKey.RELEASE_DATE: self.VorbisKey.DATE,
            UnifiedMetadataKey.BPM: self.VorbisKey.BPM,
            UnifiedMetadataKey.COMPOSERS: self.VorbisKey.COMPOSERS,
            UnifiedMetadataKey.COPYRIGHT: self.VorbisKey.COPYRIGHT,
            UnifiedMetadataKey.COMMENT: self.VorbisKey.COMMENT,
        }
        metadata_keys_direct_map_write = {
            UnifiedMetadataKey.TITLE: self.VorbisKey.TITLE,
            UnifiedMetadataKey.ARTISTS: self.VorbisKey.ARTIST_NAME,
            UnifiedMetadataKey.ALBUM: self.VorbisKey.ALBUM,
            UnifiedMetadataKey.ALBUM_ARTISTS: self.VorbisKey.ALBUM_ARTISTS,
            UnifiedMetadataKey.GENRES_NAMES: self.VorbisKey.GENRES_NAMES,
            UnifiedMetadataKey.RATING: None,
            UnifiedMetadataKey.LANGUAGE: self.VorbisKey.LANGUAGE,
            UnifiedMetadataKey.RELEASE_DATE: self.VorbisKey.DATE,
            UnifiedMetadataKey.BPM: self.VorbisKey.BPM,
            UnifiedMetadataKey.COMPOSERS: self.VorbisKey.COMPOSERS,
            UnifiedMetadataKey.COPYRIGHT: self.VorbisKey.COPYRIGHT,
            UnifiedMetadataKey.COMMENT: self.VorbisKey.COMMENT,
        }
        super().__init__(audio_file=audio_file,
                         metadata_keys_direct_map_read=metadata_keys_direct_map_read,
                         metadata_keys_direct_map_write=metadata_keys_direct_map_write,
                         rating_write_profile=RatingWriteProfile.BASE_100_PROPORTIONAL,
                         normalized_rating_max_value=normalized_rating_max_value)

    def _extract_mutagen_metadata(self) -> dict:
        """
        Reads Vorbis comments from a FLAC file, preserving original key case.
        Returns a dict: {key: [values]}.
        """
        comments = {}
        with open(self.audio_file.get_file_path_or_object(), "rb") as f:
            # --- Step 1: Skip FLAC header ---
            header = f.read(4)
            if header != b'fLaC':
                raise ValueError("Not a valid FLAC file")

            # --- Step 2: Read metadata blocks ---
            is_last = False
            while not is_last:
                block_header = f.read(4)
                if len(block_header) < 4:
                    break
                is_last = bool(block_header[0] & 0x80)
                block_type = block_header[0] & 0x7F
                block_size = struct.unpack(">I", b'\x00' + block_header[1:])[0]
                data = f.read(block_size)

                # --- Step 3: Look for VORBIS_COMMENT block ---
                if block_type == 4:  # VORBIS_COMMENT
                    offset = 0
                    # Vendor length (32-bit LE)
                    vendor_len = struct.unpack("<I", data[offset:offset+4])[0]
                    offset += 4 + vendor_len
                    # Number of comments
                    num_comments = struct.unpack("<I", data[offset:offset+4])[0]
                    offset += 4

                    for _ in range(num_comments):
                        comment_len = struct.unpack("<I", data[offset:offset+4])[0]
                        offset += 4
                        comment_bytes = data[offset:offset+comment_len]
                        offset += comment_len
                        comment_str = comment_bytes.decode("utf-8", errors="replace")

                        # Split key=value at first '='
                        if '=' not in comment_str:
                            continue
                        key, value = comment_str.split('=', 1)
                        # Preserve original case
                        comments.setdefault(key, []).append(value)
                    break
        return comments

    def _convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(
            self, raw_mutagen_metadata: dict) -> RawMetadataDict:
        # _extract_mutagen_metadata already returns metadata with list values
        return raw_mutagen_metadata

    def _get_raw_rating_by_traktor_or_not(self, raw_clean_metadata: RawMetadataDict) -> tuple[int | None, bool]:
        rating_list = raw_clean_metadata.get(self.VorbisKey.RATING)

        if rating_list and len(rating_list) > 0 and rating_list[0] is not None:
            return int(rating_list[0]), False

        rating_list = raw_clean_metadata.get(self.VorbisKey.RATING_TRAKTOR)
        if rating_list and len(rating_list) > 0 and rating_list[0] is not None:
            return int(rating_list[0]), True

        return None, False

    def _update_formatted_value_in_raw_mutagen_metadata(self, raw_mutagen_metadata: dict,
                                                        raw_metadata_key: RawMetadataKey,
                                                        app_metadata_value: AppMetadataValue):
        if app_metadata_value is not None:
            if isinstance(app_metadata_value, list):
                # For multi-value fields, keep as separate entries
                raw_mutagen_metadata[raw_metadata_key] = [str(v) for v in app_metadata_value]
            else:
                # Convert BPM to string for Vorbis comments
                if raw_metadata_key == self.VorbisKey.BPM:
                    raw_mutagen_metadata[raw_metadata_key] = [str(app_metadata_value)]
                else:
                    raw_mutagen_metadata[raw_metadata_key] = [str(app_metadata_value)]
        elif raw_metadata_key in raw_mutagen_metadata:
            del raw_mutagen_metadata[raw_metadata_key]

    def update_metadata(self, unified_metadata: UnifiedMetadata):
        if not self.metadata_keys_direct_map_write:
            raise MetadataNotSupportedByFormatError('This format does not support metadata modification')

        # Get current metadata
        current_metadata = self._extract_mutagen_metadata()

        # Update metadata dict
        for unified_metadata_key in list(unified_metadata.keys()):
            app_metadata_value = unified_metadata[unified_metadata_key]
            if unified_metadata_key not in self.metadata_keys_direct_map_write:
                raise MetadataNotSupportedByFormatError(f'{unified_metadata_key} metadata not supported by this format')
            else:
                raw_metadata_key = self.metadata_keys_direct_map_write[unified_metadata_key]
                if raw_metadata_key:
                    self._update_formatted_value_in_raw_mutagen_metadata(
                        raw_mutagen_metadata=current_metadata, raw_metadata_key=raw_metadata_key,
                        app_metadata_value=app_metadata_value)
                else:
                    self._update_undirectly_mapped_metadata(
                        raw_mutagen_metadata=current_metadata, app_metadata_value=app_metadata_value,
                        unified_metadata_key=unified_metadata_key)

        # Write metadata using TagLib
        self._write_metadata_with_taglib(current_metadata)

    def _write_metadata_with_taglib(self, metadata: dict):
        """Write metadata to the FLAC file using TagLib."""
        file_path = self.audio_file.get_file_path_or_object()
        
        try:
            # Open file with TagLib
            file_obj = taglib.File(file_path)
            
            # Clear existing tags
            file_obj.tags.clear()
            
            # Set new tags - TagLib expects dict with string keys and list values
            file_obj.tags.update(metadata)
            
            # Save the file
            file_obj.save()
            file_obj.close()
            
        except Exception as e:
            raise FileCorruptedError(f"Failed to write metadata with TagLib: {e}")

    def get_header_info(self) -> dict:
        try:
            # Use TagLib to get file information
            file_obj = taglib.File(self.audio_file.get_file_path_or_object())
            
            # TagLib provides basic info
            info = {
                'present': True,
                'vendor_string': 'TagLib',  # TagLib doesn't provide vendor string directly
                'comment_count': sum(len(values) for values in file_obj.tags.values() if values),
                'block_size': 4096  # Default Vorbis comment block size
            }
            
            file_obj.close()
            return info
        except Exception:
            return {
                'present': False,
                'vendor_string': None,
                'comment_count': 0,
                'block_size': 0
            }

    def get_raw_metadata_info(self) -> dict:
        try:
            # Use TagLib to get metadata
            file_obj = taglib.File(self.audio_file.get_file_path_or_object())
            
            return {
                'raw_data': None,  # TagLib handles this internally
                'parsed_fields': {},
                'frames': {},
                'comments': dict(file_obj.tags),  # Convert to regular dict
                'chunk_structure': {}
            }
        except Exception:
            return {
                'raw_data': None,
                'parsed_fields': {},
                'frames': {},
                'comments': {},
                'chunk_structure': {}
            }

    def delete_metadata(self) -> bool:
        """Delete all metadata from the FLAC file by removing the VORBIS_COMMENT block."""
        import subprocess
        file_path = self.audio_file.get_file_path_or_object()
        
        try:
            # Remove all VORBIS_COMMENT blocks from the FLAC file
            result = subprocess.run(
                ['metaflac', '--remove', '--block-type=VORBIS_COMMENT', str(file_path)],
                capture_output=True, text=True, check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
