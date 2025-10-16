
from abc import abstractmethod
from typing import TypeVar, cast

from mutagen._file import FileType as MutagenMetadata

from ..audio_file import AudioFile
from ..utils.id3v1_genre_code_map import ID3V1_GENRE_CODE_MAP

from ..exceptions import MetadataNotSupportedError
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from ..utils.types import AppMetadata, AppMetadataValue, RawMetadataDict, RawMetadataKey


# Separators in order of priority
METADATA_ARTISTS_SEPARATORS = ("//", "\\\\", ";", "\\", "/", ",")


T = TypeVar('T', str, int)


class MetadataManager:

    audio_file: AudioFile
    metadata_keys_direct_map_read: dict[UnifiedMetadataKey, RawMetadataKey | None]
    metadata_keys_direct_map_write: dict[UnifiedMetadataKey, RawMetadataKey | None] | None
    raw_mutagen_metadata: MutagenMetadata | None = None
    raw_clean_metadata: RawMetadataDict | None = None
    update_using_mutagen_metadata: bool

    def __init__(self, audio_file: AudioFile,
                 metadata_keys_direct_map_read: dict[UnifiedMetadataKey, RawMetadataKey | None],
                 metadata_keys_direct_map_write: dict[UnifiedMetadataKey, RawMetadataKey | None] | None = None,
                 update_using_mutagen_metadata: bool = True):
        self.audio_file = audio_file
        self.metadata_keys_direct_map_read = metadata_keys_direct_map_read
        self.metadata_keys_direct_map_write = metadata_keys_direct_map_write
        self.update_using_mutagen_metadata = update_using_mutagen_metadata

    @abstractmethod
    def _extract_mutagen_metadata(self) -> MutagenMetadata:
        raise NotImplementedError()

    @abstractmethod
    def _convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(
            self, raw_mutagen_metadata: MutagenMetadata) -> RawMetadataDict:
        raise NotImplementedError()

    @abstractmethod
    def _get_undirectly_mapped_metadata_value_from_raw_clean_metadata(
            self, raw_clean_metadata: RawMetadataDict, app_metadata_key: UnifiedMetadataKey) -> AppMetadataValue:
        raise NotImplementedError()

    @abstractmethod
    def _update_undirectly_mapped_metadata(self, raw_mutagen_metadata: MutagenMetadata,
                                           app_metadata_value: AppMetadataValue,
                                           app_metadata_key: UnifiedMetadataKey):
        raise NotImplementedError()

    @abstractmethod
    def _update_formatted_value_in_raw_mutagen_metadata(self, raw_mutagen_metadata: MutagenMetadata,
                                                        raw_metadata_key: RawMetadataKey,
                                                        app_metadata_value: AppMetadataValue):
        raise NotImplementedError()

    @abstractmethod
    def _update_not_using_mutagen_metadata(self, app_metadata: AppMetadata):
        raise NotImplementedError()

    def _get_cleaned_raw_metadata_from_file(self) -> RawMetadataDict:
        self.raw_mutagen_metadata = self._extract_mutagen_metadata()
        raw_metadata_with_potential_duplicate_keys = \
            self._convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(self.raw_mutagen_metadata)
        return self._extract_and_regroup_raw_metadata_unique_entries(raw_metadata_with_potential_duplicate_keys)

    def _extract_and_regroup_raw_metadata_unique_entries(
            self, raw_metadata_with_potential_duplicate_keys: RawMetadataDict):
        raw_clean_metadata = {}

        for raw_metadata_key, raw_metadata_value in raw_metadata_with_potential_duplicate_keys.items():
            raw_clean_metadata[raw_metadata_key] = \
                raw_metadata_value if isinstance(raw_metadata_value, list) else [raw_metadata_value]

        return raw_clean_metadata

    def _get_genre_name_from_raw_clean_metadata_id3v1(
            self, raw_clean_metadata: RawMetadataDict, raw_metadata_ket: RawMetadataKey) -> str | None:
        """
        RIFF and ID3v1 files typically contain a genre code.
        that corresponds to the ID3v1 genre list. This method converts
        the code to a human-readable genre name.
        """
        if raw_metadata_ket in raw_clean_metadata:
            raw_value_list = raw_clean_metadata.get(raw_metadata_ket)
            if not raw_value_list or len(raw_value_list) == 0:
                return None
            raw_value = raw_value_list[0]
            try:
                genre_code_or_name = int(cast(int, raw_value))
                return ID3V1_GENRE_CODE_MAP.get(genre_code_or_name)
            except ValueError:
                return cast(str, raw_value)
        return None

    def get_app_metadata(self) -> AppMetadata:
        if self.raw_clean_metadata is None:
            self.raw_clean_metadata = self._get_cleaned_raw_metadata_from_file()

        app_metadata = {}
        for metadata_key in self.metadata_keys_direct_map_read:
            app_metadata_value = self.get_app_specific_metadata(metadata_key)
            if app_metadata_value is not None:
                app_metadata[metadata_key] = app_metadata_value
        return app_metadata

    def get_app_specific_metadata(self, app_metadata_key: UnifiedMetadataKey) -> AppMetadataValue:
        if self.raw_clean_metadata is None:
            self.raw_clean_metadata = self._get_cleaned_raw_metadata_from_file()

        if app_metadata_key not in self.metadata_keys_direct_map_read:
            raise MetadataNotSupportedError(f'{app_metadata_key} metadata not supported by this format')

        raw_metadata_key = self.metadata_keys_direct_map_read[app_metadata_key]
        if not raw_metadata_key:
            return self._get_undirectly_mapped_metadata_value_from_raw_clean_metadata(
                raw_clean_metadata=self.raw_clean_metadata, app_metadata_key=app_metadata_key)

        value = self.raw_clean_metadata.get(raw_metadata_key)

        if not value or not len(value):
            return None
        
        # For string types, we need to distinguish between None (not present) and empty string (present but empty)
        app_metadata_key_optional_type = app_metadata_key.get_optional_type()
        if app_metadata_key_optional_type == str and value[0] == "":
            return ""
        
        if not value[0]:
            return None
        if app_metadata_key_optional_type == int:
            # Handle ID3v2 track number format "track/total" (e.g., "99/99")
            if app_metadata_key == UnifiedMetadataKey.TRACK_NUMBER and "/" in str(value[0]):
                track_str = str(value[0]).split("/")[0].strip()
                return int(track_str) if track_str.isdigit() else None
            return int(value[0]) if value else None
        if app_metadata_key_optional_type == float:
            return float(value[0]) if value else None
        if app_metadata_key_optional_type == str:
            return str(value[0]) if value else None
        if app_metadata_key_optional_type == list[str]:
            if not value:
                return None
            values_list_str = cast(list[str], value)
            if app_metadata_key.can_semantically_have_multiple_values():
                values_list_str_with_separated_values_processed: list[str] = []
                for str_with_potential_separated_values in values_list_str:
                    # Try each separator in order
                    current_values = [str_with_potential_separated_values]
                    for separator in METADATA_ARTISTS_SEPARATORS:
                        new_values = []
                        for val in current_values:
                            new_values.extend(val.split(separator))
                        current_values = new_values
                    values_list_str_with_separated_values_processed.extend(
                        [val.strip() for val in current_values if val.strip()]
                    )
                return values_list_str_with_separated_values_processed
            return values_list_str
        raise ValueError(f'Unsupported metadata type: {app_metadata_key_optional_type}')

    def get_header_info(self) -> dict:
        """
        Get header information for this metadata format.
        
        Returns:
            Dictionary containing header information
        """
        return {
            'present': False,
            'version': None,
            'size_bytes': 0,
            'position': None,
            'flags': {},
            'extended_header': {}
        }

    def get_raw_metadata_info(self) -> dict:
        """
        Get raw metadata information for this format.
        
        Returns:
            Dictionary containing raw metadata details
        """
        return {
            'raw_data': None,
            'parsed_fields': {},
            'frames': {},
            'comments': {},
            'chunk_structure': {}
        }

    def update_file_metadata(self, app_metadata: AppMetadata):
        if not self.metadata_keys_direct_map_write:
            raise MetadataNotSupportedError('This format does not support metadata modification')

        if not self.update_using_mutagen_metadata:
            self._update_not_using_mutagen_metadata(app_metadata)
        else:
            if self.raw_mutagen_metadata is None:
                self.raw_mutagen_metadata = self._extract_mutagen_metadata()

            for app_metadata_key in list(app_metadata.keys()):
                app_metadata_value = app_metadata[app_metadata_key]
                if app_metadata_key not in self.metadata_keys_direct_map_write:
                    raise MetadataNotSupportedError(f'{app_metadata_key} metadata not supported by this format')
                else:
                    raw_metadata_key = self.metadata_keys_direct_map_write[app_metadata_key]
                    if raw_metadata_key:
                        self._update_formatted_value_in_raw_mutagen_metadata(
                            raw_mutagen_metadata=self.raw_mutagen_metadata, raw_metadata_key=raw_metadata_key,
                            app_metadata_value=app_metadata_value)
                    else:
                        self._update_undirectly_mapped_metadata(
                            raw_mutagen_metadata=self.raw_mutagen_metadata, app_metadata_value=app_metadata_value,
                            app_metadata_key=app_metadata_key)
            self.raw_mutagen_metadata.save(self.audio_file.get_file_path_or_object())

    def delete_metadata(self) -> bool:
        if self.raw_mutagen_metadata is None:
            self.raw_mutagen_metadata = self._extract_mutagen_metadata()

        try:
            self.raw_mutagen_metadata.delete()
            return True
        except Exception:
            return False
