from abc import abstractmethod
from typing import cast

from mutagen._file import FileType as MutagenMetadata
from mutagen.id3 import ID3

from ...audio_file import AudioFile
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from ...utils.rating_profiles import RatingWriteProfile
from ...utils.types import AppMetadataValue, RawMetadataKey
from .RatingSupportingMetadataManager import RatingSupportingMetadataManager
from ..MetadataManager import METADATA_ARTISTS_SEPARATORS


class MultiEntriesManager(RatingSupportingMetadataManager):
    """
    Base class for metadata managers that support multiple entries and smart parsing.
    
    This class provides smart parsing logic for metadata fields that can semantically
    have multiple values. The parsing behavior depends only on the number of entries:
    
    Smart Parsing Rules:
    - Multiple entries: No parsing (preserve separators in individual entries)
    - Single entry: Parse separators (legacy data detection)
    """

    def __init__(self, audio_file: AudioFile,
                 metadata_keys_direct_map_read: dict[UnifiedMetadataKey, RawMetadataKey | None],
                 metadata_keys_direct_map_write: dict[UnifiedMetadataKey, RawMetadataKey | None],
                 rating_write_profile: RatingWriteProfile,
                 normalized_rating_max_value: int | None,
                 update_using_mutagen_metadata: bool = True):
        super().__init__(audio_file, metadata_keys_direct_map_read, metadata_keys_direct_map_write,
                        rating_write_profile, normalized_rating_max_value, update_using_mutagen_metadata)

    def _should_apply_smart_parsing(self, values_list_str: list[str]) -> bool:
        """
        Determine if smart parsing should be applied based on entry count.
        
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
            
        # If we have multiple entries, don't parse (preserve separators)
        if len(non_empty_entries) > 1:
            return False
            
        # If we have a single entry, parse it (legacy data detection)
        return True

    def _apply_separator_parsing(self, values_list_str: list[str]) -> list[str]:
        """
        Apply separator parsing to split values.
        
        Args:
            values_list_str: List of string values to parse
            
        Returns:
            List of parsed values
        """
        if not values_list_str:
            return []
            
        # Get the first non-empty value
        first_value = next((val.strip() for val in values_list_str if val.strip()), "")
        if not first_value:
            return []
            
        # Try each separator in order of priority
        for separator in METADATA_ARTISTS_SEPARATORS:
            if separator in first_value:
                # Split by this separator and clean up
                parsed_values = [val.strip() for val in first_value.split(separator)]
                # Filter out empty values
                return [val for val in parsed_values if val]
                
        # No separator found, return the original value
        return [first_value]

    def get_app_specific_metadata(self, app_metadata_key: UnifiedMetadataKey) -> AppMetadataValue:
        """
        Override to apply smart parsing for multi-value fields.
        """
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
        
        if app_metadata_key_optional_type == str:
            return value[0]
        
        if app_metadata_key_optional_type == list[str]:
            if not value:
                return None
            values_list_str = cast(list[str], value)
            if app_metadata_key.can_semantically_have_multiple_values():
                # Apply smart parsing logic
                if self._should_apply_smart_parsing(values_list_str):
                    # Apply parsing
                    parsed_values = self._apply_separator_parsing(values_list_str)
                    return parsed_values if parsed_values else None
                else:
                    # No parsing - return as-is but filter empty/whitespace values
                    filtered_values = [val.strip() for val in values_list_str if val.strip()]
                    return filtered_values if filtered_values else None
            return values_list_str
        raise ValueError(f'Unsupported metadata type: {app_metadata_key_optional_type}')

    def _update_formatted_value_in_raw_mutagen_metadata(self, raw_mutagen_metadata: MutagenMetadata,
                                                      raw_metadata_key: RawMetadataKey,
                                                      app_metadata_value: AppMetadataValue):
        """
        Override to handle multiple entries for multi-value fields.
        """
        # Handle list values for multiple entries
        if (isinstance(app_metadata_value, list) and 
            all(isinstance(item, str) for item in app_metadata_value)):
            
            # Get the corresponding UnifiedMetadataKey
            app_metadata_key = None
            for key, raw_key in self.metadata_keys_direct_map_write.items():
                if raw_key == raw_metadata_key:
                    app_metadata_key = key
                    break
                    
            if app_metadata_key and app_metadata_key.can_semantically_have_multiple_values():
                # For multiple entries, delete all existing frames first, then add all new ones
                if isinstance(raw_mutagen_metadata, ID3):
                    raw_mutagen_metadata_id3 = cast(ID3, raw_mutagen_metadata)
                    raw_mutagen_metadata_id3.delall(raw_metadata_key)
                else:
                    # For non-ID3 formats, clear the field
                    if raw_metadata_key in raw_mutagen_metadata:
                        del raw_mutagen_metadata[raw_metadata_key]
                
                # Add each value as a separate frame
                for value in app_metadata_value:
                    if value is not None and value != "":
                        self._add_single_formatted_value_in_raw_mutagen_metadata(
                            raw_mutagen_metadata=raw_mutagen_metadata, 
                            raw_metadata_key=raw_metadata_key,
                            app_metadata_value=value)
                return
        
        # Single value or non-multi-value field - use single value implementation
        self._update_single_formatted_value_in_raw_mutagen_metadata(
            raw_mutagen_metadata, raw_metadata_key, app_metadata_value)

    @abstractmethod
    def _add_single_formatted_value_in_raw_mutagen_metadata(self, raw_mutagen_metadata: MutagenMetadata,
                                                          raw_metadata_key: RawMetadataKey,
                                                          app_metadata_value: str):
        """
        Add a single formatted value to raw mutagen metadata without deleting existing ones.
        This is used for adding multiple entries of the same type.
        
        Args:
            raw_mutagen_metadata: The raw mutagen metadata object
            raw_metadata_key: The raw metadata key
            app_metadata_value: The single value to add
        """
        raise NotImplementedError()

    @abstractmethod
    def _update_single_formatted_value_in_raw_mutagen_metadata(self, raw_mutagen_metadata: MutagenMetadata,
                                                             raw_metadata_key: RawMetadataKey,
                                                             app_metadata_value: AppMetadataValue):
        """
        Update a single formatted value in raw mutagen metadata.
        This is used for single values (not lists).
        
        Args:
            raw_mutagen_metadata: The raw mutagen metadata object
            raw_metadata_key: The raw metadata key
            app_metadata_value: The single value to update
        """
        raise NotImplementedError()