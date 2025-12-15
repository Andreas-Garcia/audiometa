"""ID3v1 preservation helper for ID3v2 manager."""

import contextlib
import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, cast

from mutagen.id3 import ID3

if TYPE_CHECKING:
    from ._Id3v2Manager import _Id3v2Manager


class _Id3v1Preserver:
    """Helper class for preserving ID3v1 metadata when saving ID3v2 tags."""

    def __init__(self, manager: "_Id3v2Manager"):
        """Initialize preserver with reference to manager.

        Args:
            manager: The ID3v2 manager instance
        """
        self.manager = manager

    def preserve_id3v1_metadata(self, file_path: str) -> bytes | None:
        """Read and preserve existing ID3v1 metadata from the end of the file.

        Args:
            file_path: Path to the audio file

        Returns:
            The 128-byte ID3v1 tag data if present, None otherwise
        """
        with Path(file_path).open("rb") as f:
            f.seek(-128, 2)  # Seek to last 128 bytes
            data = f.read(128)
            if data.startswith(b"TAG"):
                return data
        return None

    def save_with_id3v1_preservation(self, file_path: str, id3v1_data: bytes | None) -> None:
        """Save ID3v2 metadata while preserving ID3v1 data.

        Args:
            file_path: Path to the audio file
            id3v1_data: The 128-byte ID3v1 tag data to preserve, or None
        """
        if self.manager.raw_mutagen_metadata is not None:
            # Extract the major version number from the tuple (2, 3, 0) -> 3
            version_major = self.manager.id3v2_version[1]
            id3_metadata: ID3 = cast(ID3, self.manager.raw_mutagen_metadata)

            if id3v1_data:
                # Save to a temporary file first
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                    temp_path = temp_file.name

                try:
                    # Copy the original file to temp file first
                    shutil.copy2(file_path, temp_path)

                    # Save ID3v2 to temp file (this will overwrite ID3v2 tags in the copy)
                    id3_metadata.save(temp_path, v2_version=version_major)

                    # Read the temp file and append ID3v1 data
                    with Path(temp_path).open("rb") as f:
                        temp_data = f.read()

                    # Append ID3v1 data to the temp file
                    final_data = temp_data + id3v1_data

                    # Write the final file
                    with Path(file_path).open("wb") as f:
                        f.write(final_data)

                finally:
                    # Clean up temp file
                    with contextlib.suppress(OSError):
                        Path(temp_path).unlink()
            else:
                # No ID3v1 data to preserve, save normally
                id3_metadata.save(file_path, v2_version=version_major)

    def save_with_version(self, file_path: str) -> None:
        """Save ID3 tags with the specified version, preserving existing ID3v1 metadata.

        Args:
            file_path: Path to the audio file
        """
        if self.manager.raw_mutagen_metadata is not None:
            # Preserve existing ID3v1 metadata before saving ID3v2
            id3v1_data = self.preserve_id3v1_metadata(file_path)
            self.save_with_id3v1_preservation(file_path, id3v1_data)
