"""FLAC-specific ID3v2 handler using external tools."""

import contextlib
import subprocess
from typing import TYPE_CHECKING

from audiometa.exceptions import FileCorruptedError, MetadataFieldNotSupportedByMetadataFormatError
from audiometa.utils.tool_path_resolver import get_tool_path
from audiometa.utils.types import UnifiedMetadata
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey

if TYPE_CHECKING:
    from ._Id3v2Manager import _Id3v2Manager

from ._id3v2_constants import ID3V2_VERSION_3


class _Id3v2FlacHandler:
    """Helper class for handling ID3v2 metadata in FLAC files using external tools."""

    def __init__(self, manager: "_Id3v2Manager"):
        """Initialize FLAC handler with reference to manager.

        Args:
            manager: The ID3v2 manager instance
        """
        self.manager = manager

    def update_metadata_for_flac(self, unified_metadata: UnifiedMetadata) -> None:
        """Update ID3v2 metadata for FLAC files using external tools to avoid file corruption.

        Args:
            unified_metadata: Unified metadata dictionary to write

        Raises:
            MetadataFieldNotSupportedByMetadataFormatError: If format doesn't support modification
            FileCorruptedError: If external tool fails or is not found
        """
        if not self.manager.metadata_keys_direct_map_write:
            msg = "This format does not support metadata modification"
            raise MetadataFieldNotSupportedByMetadataFormatError(msg)

        self.manager._validate_and_process_rating(unified_metadata)

        # Use external tools to write ID3v2 metadata to FLAC files
        # This avoids the file corruption that occurs with mutagen's ID3 class
        # Determine the tool and version based on the configured ID3v2 version
        if self.manager.id3v2_version[1] == ID3V2_VERSION_3:
            tool = "id3v2"
            cmd = [get_tool_path("id3v2"), "--id3v2-only"]
        else:  # ID3v2.4
            tool = "mid3v2"
            cmd = [get_tool_path("mid3v2")]

        # Map unified metadata keys to external tool arguments
        key_mapping = {
            UnifiedMetadataKey.TITLE: "--song",
            UnifiedMetadataKey.ARTISTS: "--artist",
            UnifiedMetadataKey.ALBUM: "--album",
            UnifiedMetadataKey.ALBUM_ARTISTS: "--TPE2",
            UnifiedMetadataKey.GENRES_NAMES: "--genre",
            UnifiedMetadataKey.COMMENT: "--comment",
            UnifiedMetadataKey.TRACK_NUMBER: "--track",
            UnifiedMetadataKey.BPM: "--TBPM",
            UnifiedMetadataKey.COMPOSERS: "--TCOM",
            UnifiedMetadataKey.COPYRIGHT: "--TCOP",
            UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: "--USLT",
            UnifiedMetadataKey.LANGUAGE: "--TLAN",
            UnifiedMetadataKey.PUBLISHER: "--TPUB",
        }

        # Build command with metadata
        # First, remove frames for keys explicitly set to None
        frames_to_remove = []
        for unified_key, value in unified_metadata.items():
            if unified_key in self.manager.metadata_keys_direct_map_write:
                raw_key = self.manager.metadata_keys_direct_map_write[unified_key]
                if raw_key and value is None:
                    frames_to_remove.append(raw_key)

        try:
            if frames_to_remove:
                if self.manager.id3v2_version[1] == ID3V2_VERSION_3:
                    # id3v2 supports removing a single frame at a time via -r
                    for frame in frames_to_remove:
                        with contextlib.suppress(subprocess.CalledProcessError):
                            subprocess.run(
                                [get_tool_path("id3v2"), "-r", frame, self.manager.audio_file.file_path],
                                check=True,
                                capture_output=True,
                            )
                else:
                    # mid3v2 supports deleting multiple frames with --delete-frames
                    frames_arg = ",".join(frames_to_remove)
                    with contextlib.suppress(subprocess.CalledProcessError):
                        subprocess.run(
                            [
                                get_tool_path("mid3v2"),
                                f"--delete-frames={frames_arg}",
                                self.manager.audio_file.file_path,
                            ],
                            check=True,
                            capture_output=True,
                        )
        except FileNotFoundError:
            # If removal tool not found, proceed and hope save will remove frames
            pass

        # Build command with metadata (only non-None values)
        for unified_key, value in unified_metadata.items():
            if unified_key in key_mapping and value is not None:
                tool_arg = key_mapping[unified_key]

                processed_value = value
                if unified_key == UnifiedMetadataKey.ARTISTS and isinstance(value, list):
                    # Handle multiple artists by joining with semicolon
                    processed_value = ";".join(value)
                elif unified_key == UnifiedMetadataKey.GENRES_NAMES and isinstance(value, list):
                    # Handle multiple genres by joining with semicolon
                    processed_value = ";".join(value)
                elif unified_key == UnifiedMetadataKey.COMPOSERS and isinstance(value, list):
                    # Handle multiple composers by joining with semicolon
                    processed_value = ";".join(value)
                elif unified_key == UnifiedMetadataKey.ALBUM_ARTISTS and isinstance(value, list):
                    # Handle multiple album artists by joining with semicolon
                    processed_value = ";".join(value)

                cmd.extend([tool_arg, str(processed_value)])

        # Add file path and execute
        cmd.append(self.manager.audio_file.file_path)

        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            msg = f"Failed to write ID3v2 metadata with {tool}: {e}"
            raise FileCorruptedError(msg) from e
        except FileNotFoundError as e:
            msg = f"External tool {tool} not found. Please install it to write ID3v2 metadata to FLAC files."
            raise FileCorruptedError(msg) from e
