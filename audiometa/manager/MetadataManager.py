from abc import abstractmethod
from typing import TypeVar, cast

from mutagen._file import FileType as MutagenMetadata

from ..audio_file import AudioFile
from ..utils.id3v1_genre_code_map import ID3V1_GENRE_CODE_MAP

from ..exceptions import MetadataNotSupportedError
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from ..utils.types import UnifiedMetadata, AppMetadataValue, RawMetadataDict, RawMetadataKey


# Separators in order of priority for multi-value metadata fields
METADATA_MULTI_VALUE_SEPARATORS = ("\x00", "//", "\\\\", "\\", ";", "/", ",")


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

    @staticmethod 
    def find_safe_separator(values: list[str]) -> str:
        """
        Find a separator that doesn't appear in any of the provided values.
        
        Args:
            values: List of string values to check for separator conflicts
            
        Returns:
            A separator string that doesn't appear in any value, or the last 
            separator (comma) as fallback if no separator is safe
        """
        # Find a separator that doesn't appear in any of the values
        for sep in METADATA_MULTI_VALUE_SEPARATORS:
            if not any(sep in value for value in values):
                return sep
        
        # If no separator is safe, use the last one (comma)
        return METADATA_MULTI_VALUE_SEPARATORS[-1]

    @abstractmethod
    def _extract_mutagen_metadata(self) -> MutagenMetadata:
        raise NotImplementedError()

    @abstractmethod
    def _convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(
            self, raw_mutagen_metadata: MutagenMetadata) -> RawMetadataDict:
        raise NotImplementedError()

    @abstractmethod
    def _get_undirectly_mapped_metadata_value_from_raw_clean_metadata(
            self, raw_clean_metadata: RawMetadataDict, unified_metadata_key: UnifiedMetadataKey) -> AppMetadataValue:
        raise NotImplementedError()

    @abstractmethod
    def _update_undirectly_mapped_metadata(self, raw_mutagen_metadata: MutagenMetadata,
                                           app_metadata_value: AppMetadataValue,
                                           unified_metadata_key: UnifiedMetadataKey):
        raise NotImplementedError()

    @abstractmethod
    def _update_formatted_value_in_raw_mutagen_metadata(self, raw_mutagen_metadata: MutagenMetadata,
                                                        raw_metadata_key: RawMetadataKey,
                                                        app_metadata_value: AppMetadataValue):
        raise NotImplementedError()

    @abstractmethod
    def _update_not_using_mutagen_metadata(self, unified_metadata: UnifiedMetadata):
        raise NotImplementedError()

    def _get_cleaned_raw_metadata_from_file(self) -> RawMetadataDict:
        self.raw_mutagen_metadata = self._extract_mutagen_metadata()
        raw_metadata_with_potential_duplicate_keys = \
            self._convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(self.raw_mutagen_metadata)
        return self._extract_and_regroup_raw_metadata_unique_entries(raw_metadata_with_potential_duplicate_keys)

    def _should_apply_smart_parsing(self, values_list_str: list[str]) -> bool:
        """
        Determine if smart parsing should be applied based on entry count and null separators.
        
        Args:
            values_list_str: List of string values from the metadata
            
        Returns:
            True if parsing should be applied, False otherwise
        """
        if not values_list_str:
            return False
            
        # Count non-empty entries
        non_empty_entries = [val.strip() for val in values_list_str if val.strip()]
        
        if len(non_empty_entries) == 0:
            return False
            
        # Check if any entry contains null separators
        has_null_separators = any('\x00' in entry for entry in non_empty_entries)
        
        # If null separators are present, always apply parsing (null separation logic)
        if has_null_separators:
            return True
            
        # If we have multiple entries without null separators, don't parse (preserve separators)
        if len(non_empty_entries) > 1:
            return False
            
        # If we have a single entry without null separators, parse it (legacy data detection)
        return True

    def _apply_smart_parsing(self, values_list_str: list[str]) -> list[str]:
        """
        Apply smart parsing to split values.
        
        Args:
            values_list_str: List of string values to parse
            
        Returns:
            List of parsed values
        """
        if not values_list_str:
            return []
            
        # Get non-empty values
        non_empty_values = [val.strip() for val in values_list_str if val.strip()]
        if not non_empty_values:
            return []
            
        # Check if any entry contains null separators
        has_null_separators = any('\x00' in entry for entry in non_empty_values)
        
        if has_null_separators:
            # Apply null separation logic across all entries
            result = []
            for entry in non_empty_values:
                if '\x00' in entry:
                    # Split on null separator and add non-empty parts
                    parts = [p.strip() for p in entry.split('\x00') if p.strip()]
                    result.extend(parts)
                else:
                    # Entry without null separator, add as-is
                    result.append(entry)
            return result
        
        # No null separators - use logic for single entry
        first_value = non_empty_values[0]
        
        # Find the highest-priority separator that actually exists in the value.
        # We should only split on that separator (single-entry fields that
        # used one specific separator) rather than splitting on every known
        # separator sequentially which can produce incorrect fragmentation when
        # lower-priority separators appear inside values.
        for separator in METADATA_MULTI_VALUE_SEPARATORS:
            if separator in first_value:
                parts = [p.strip() for p in first_value.split(separator) if p.strip()]
                return parts

        # No known separator found; return the single trimmed value as list
        return [first_value.strip()]

    def _extract_and_regroup_raw_metadata_unique_entries(
            self, raw_metadata_with_potential_duplicate_keys: RawMetadataDict):
        raw_clean_metadata = {}

        for raw_metadata_key, raw_metadata_value in raw_metadata_with_potential_duplicate_keys.items():
            raw_clean_metadata[raw_metadata_key] = \
                raw_metadata_value if isinstance(raw_metadata_value, list) else [raw_metadata_value]

        return raw_clean_metadata

    def _get_genre_name_from_raw_clean_metadata_id3v1(
            self, raw_clean_metadata: RawMetadataDict, raw_metadata_ket: RawMetadataKey) -> AppMetadataValue:
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
                genre_name = ID3V1_GENRE_CODE_MAP.get(genre_code_or_name)
            except ValueError:
                genre_name = cast(str, raw_value)
            
            # Return as list since GENRES_NAMES is a multi-value field
            return [genre_name] if genre_name else None
        return None

    def _get_genres_from_raw_clean_metadata(self, raw_clean_metadata: RawMetadataDict, raw_metadata_key: RawMetadataKey) -> AppMetadataValue:
        """
        Extract and process genre entries from raw metadata according to the intelligent genre reading logic.

        This method implements the comprehensive genre reading strategy that handles:
        1. Multiple genre entries from the file
        2. Separator parsing for single entries (text with separators, codes, code+text)
        3. ID3v1 genre code conversion
        4. Consistent list output of genre names

        Args:
            raw_clean_metadata: Dictionary of raw metadata values
            raw_metadata_key: The raw metadata key for genres

        Returns:
            List of genre names, or None if no genres found
        """
        if raw_metadata_key not in raw_clean_metadata:
            return None

        raw_value_list = raw_clean_metadata.get(raw_metadata_key)
        if not raw_value_list:
            return None

        # Step 1: Extract all genre entries from the file
        genre_entries = [entry.strip() for entry in raw_value_list if entry.strip()]

        if not genre_entries:
            return None

        # Step 2: Process entries based on count
        if len(genre_entries) == 1:
            # Single entry - apply separator parsing if needed
            single_entry = genre_entries[0]

            # Check for codes or code+text without separators (e.g., "(17)(6)", "(17)Rock(6)Blues")
            if self._has_genre_separators(single_entry):
                parsed_genres = self._parse_genre_separators(single_entry)
            elif self._has_genre_codes_without_separators(single_entry):
                parsed_genres = self._parse_genre_codes_and_text(single_entry)
            # Check for text with separators (e.g., "Rock/Blues", "Rock; Alternative")
            else:
                # No special parsing needed
                parsed_genres = [single_entry]
        else:
            # Multiple entries - use as-is (no separator parsing)
            parsed_genres = genre_entries

        # Step 3: Convert any genre codes or codes + names to names using ID3v1 genre code map
        converted_genres = []
        for genre in parsed_genres:
            converted = self._convert_genre_code_or_text_to_name(genre)
            if converted:
                converted_genres.append(converted)

        # Step 4: Return list of genre names (remove duplicates while preserving order)
        unique_genres = []
        for genre in converted_genres:
            if genre not in unique_genres:
                unique_genres.append(genre)
        return unique_genres if unique_genres else None

    def _has_genre_codes_without_separators(self, genre_string: str) -> bool:
        """
        Check if a genre string contains genre codes without separators.
        Examples: "(17)(6)", "(17)Rock(6)Blues", "(17)Rock(6)"
        """
        import re
        # Pattern matches parentheses with digits, optionally followed by text, repeated
        pattern = r'^\(\d+\)(?:\w*\(\d+\))*\w*$'
        return bool(re.match(pattern, genre_string))

    def _has_genre_separators(self, genre_string: str) -> bool:
        """
        Check if a genre string contains separators for multiple genres.
        Examples: "Rock/Blues", "Rock; Alternative", "(17)Rock/(6)Blues"
        """
        # Check for common separators

        return any(sep in genre_string for sep in METADATA_MULTI_VALUE_SEPARATORS)

    def _parse_genre_codes_and_text(self, genre_string: str) -> list[str]:
        """
        Parse genre codes and code+text combinations without separators.
        Examples: "(17)(6)" -> ["(17)", "(6)"]
                  "(17)Rock(6)Blues" -> ["(17)Rock", "(6)Blues"]
        """
        import re
        # Find all consecutive (number)text patterns
        # Each match is a complete code or code+text unit
        pattern = r'\(\d+\)[^(\d]*'
        matches = re.findall(pattern, genre_string)
        
        if matches:
            # Filter out any empty matches
            return [match for match in matches if match]
        
        # Fallback: if no matches, return the original string
        return [genre_string]

    def _parse_genre_separators(self, genre_string: str) -> list[str]:
        """
        Parse genre strings with separators using smart separator logic.
        Examples: "Rock/Blues" -> ["Rock", "Blues"]
                  "(17)Rock/(6)Blues" -> ["(17)Rock", "(6)Blues"]
        """
        # Use the same separator priority as multi-value parsing
        for separator in METADATA_MULTI_VALUE_SEPARATORS:
            if separator in genre_string:
                parts = [part.strip() for part in genre_string.split(separator) if part.strip()]
                return parts
        # No separator found
        return [genre_string]

    def _convert_genre_code_or_text_to_name(self, genre_entry: str) -> str | None:
        """
        Convert a genre code or code+text entry to a genre name using ID3V1_GENRE_CODE_MAP.
        For code + text entries, use text part only for more flexibility.

        Examples:
        - "(17)" -> "Rock"
        - "(17)Rock" -> "Rock" (text part preferred)
        - "Rock" -> "Rock"
        - "(999)" -> None (invalid code)
        """
        import re

        # Check for code + text pattern: (number)text
        code_text_match = re.match(r'^\((\d+)\)(.+)$', genre_entry)
        if code_text_match:
            code = int(code_text_match.group(1))
            text_part = code_text_match.group(2).strip()
            # For code + text entries, use text part only for more flexibility
            if text_part:
                return text_part

        # Check for code only pattern: (number)
        code_only_match = re.match(r'^\((\d+)\)$', genre_entry)
        if code_only_match:
            code = int(code_only_match.group(1))
            genre_name = ID3V1_GENRE_CODE_MAP.get(code)
            return genre_name

        # No code found, return as-is
        return genre_entry if genre_entry else None

    def get_unified_metadata(self) -> UnifiedMetadata:
        if self.raw_clean_metadata is None:
            self.raw_clean_metadata = self._get_cleaned_raw_metadata_from_file()

        unified_metadata = {}
        for metadata_key in self.metadata_keys_direct_map_read:
            app_metadata_value = self.get_specific_metadata(metadata_key)
            if app_metadata_value is not None:
                unified_metadata[metadata_key] = app_metadata_value
        return unified_metadata

    def get_specific_metadata(self, unified_metadata_key: UnifiedMetadataKey) -> AppMetadataValue:
        if self.raw_clean_metadata is None:
            self.raw_clean_metadata = self._get_cleaned_raw_metadata_from_file()

        if unified_metadata_key not in self.metadata_keys_direct_map_read:
            raise MetadataNotSupportedError(f'{unified_metadata_key} metadata not supported by this format')

        raw_metadata_key = self.metadata_keys_direct_map_read[unified_metadata_key]
        if not raw_metadata_key:
            return self._get_undirectly_mapped_metadata_value_from_raw_clean_metadata(
                raw_clean_metadata=self.raw_clean_metadata, unified_metadata_key=unified_metadata_key)

        value = self.raw_clean_metadata.get(raw_metadata_key)

        if not value or not len(value):
            return None
        
        # For string types, we need to distinguish between None (not present) and empty string (present but empty)
        app_metadata_key_optional_type = unified_metadata_key.get_optional_type()
        if app_metadata_key_optional_type == str and value[0] == "":
            return ""
        
        if not value[0]:
            return None
        if app_metadata_key_optional_type == int:
            # Handle ID3v2 track number format "track/total" (e.g., "99/99")
            if unified_metadata_key == UnifiedMetadataKey.TRACK_NUMBER and "/" in str(value[0]):
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
            if unified_metadata_key == UnifiedMetadataKey.GENRES_NAMES:
                # Use specialized genre reading logic
                return self._get_genres_from_raw_clean_metadata(self.raw_clean_metadata, raw_metadata_key)
            elif unified_metadata_key.can_semantically_have_multiple_values():
                # Apply smart parsing logic for semantically multi-value fields
                if self._should_apply_smart_parsing(values_list_str):
                    # Apply parsing for single entry (legacy data detection)
                    parsed_values = self._apply_smart_parsing(values_list_str)
                    return parsed_values if parsed_values else None
                else:
                    # No parsing - return as-is but filter empty/whitespace values
                    filtered_values = [val.strip() for val in values_list_str if val.strip()]
                    return filtered_values if filtered_values else None
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

    def update_metadata(self, unified_metadata: UnifiedMetadata):
        if not self.metadata_keys_direct_map_write:
            raise MetadataNotSupportedError('This format does not support metadata modification')

        if not self.update_using_mutagen_metadata:
            self._update_not_using_mutagen_metadata(unified_metadata)
        else:
            if self.raw_mutagen_metadata is None:
                self.raw_mutagen_metadata = self._extract_mutagen_metadata()

            for unified_metadata_key in list(unified_metadata.keys()):
                app_metadata_value = unified_metadata[unified_metadata_key]
                if unified_metadata_key not in self.metadata_keys_direct_map_write:
                    raise MetadataNotSupportedError(f'{unified_metadata_key} metadata not supported by this format')
                else:
                    raw_metadata_key = self.metadata_keys_direct_map_write[unified_metadata_key]
                    if raw_metadata_key:
                        self._update_formatted_value_in_raw_mutagen_metadata(
                            raw_mutagen_metadata=self.raw_mutagen_metadata, raw_metadata_key=raw_metadata_key,
                            app_metadata_value=app_metadata_value)
                    else:
                        self._update_undirectly_mapped_metadata(
                            raw_mutagen_metadata=self.raw_mutagen_metadata, app_metadata_value=app_metadata_value,
                            unified_metadata_key=unified_metadata_key)
            self.raw_mutagen_metadata.save(self.audio_file.get_file_path_or_object())

    def delete_metadata(self) -> bool:
        if self.raw_mutagen_metadata is None:
            self.raw_mutagen_metadata = self._extract_mutagen_metadata()

        try:
            self.raw_mutagen_metadata.delete()
            return True
        except Exception:
            return False
