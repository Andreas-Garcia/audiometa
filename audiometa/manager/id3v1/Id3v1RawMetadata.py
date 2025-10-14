

import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mutagen._file import FileType

from ...exceptions import MetadataNotSupportedError
from .Id3v1RawMetadataKey import Id3v1RawMetadataKey


class Id3v1RawMetadata(FileType):
    """
    A custom file-like object for ID3v1 tags, providing a consistent interface similar to mutagen.

    This class encapsulates the ID3v1 128-byte structure and provides a clean interface for accessing
    and modifying tag data. It supports both reading and writing using direct file manipulation.
    """

    @dataclass
    class Id3v1Tag:
        title: str = ''
        artists_names_str: str = ''
        album_name: str = ''
        year: str = ''
        comment: str = ''
        track_number: int | None = None
        genre_code: int = 255  # 255 is undefined genre

    def __init__(self, fileobj: Any):
        self.fileobj = fileobj
        self.tags: dict[str, list[str]] | None = None
        self._load_tags()

    def _load_tags(self) -> None:
        # Handle both file objects and file paths
        if isinstance(self.fileobj, str):
            with open(self.fileobj, 'rb') as f:
                f.seek(-128, 2)  # Seek from end
                data = f.read(128)
        elif isinstance(self.fileobj, Path):
            with open(self.fileobj, 'rb') as f:
                f.seek(-128, 2)  # Seek from end
                data = f.read(128)
        else:
            self.fileobj.seek(-128, 2)  # Seek from end
            data = self.fileobj.read(128)

        if not data.startswith(b'TAG'):
            self.tags = None
            return

        # Parse the fixed structure into our tag object
        tag = self.Id3v1Tag(
            title=data[3:33].strip(b'\0').decode('latin1', 'replace'),
            artists_names_str=data[33:63].strip(b'\0').decode('latin1', 'replace'),
            album_name=data[63:93].strip(b'\0').decode('latin1', 'replace'),
            year=data[93:97].strip(b'\0').decode('latin1', 'replace'),
            genre_code=struct.unpack('B', data[127:128])[0]
        )

        # Handle ID3v1.1 track number in comment field
        try:
            comment = data[97:127].strip(b'\0')

            # Check if comment has enough length for v1.1 format
            if len(comment) >= 30:
                if comment[28] == 0 and comment[29] != 0:
                    tag.track_number = comment[29]
                    tag.comment = comment[:28].decode('latin1', 'replace')
                else:
                    tag.comment = comment[:30].decode('latin1', 'replace')
            else:
                # Handle short comment
                tag.comment = comment.decode('latin1', 'replace')
                tag.track_number = None
        except Exception as e:
            pass

        # Convert to dictionary format similar to other metadata formats
        self.tags = {}
        if tag.title:
            self.tags[Id3v1RawMetadataKey.TITLE] = [tag.title]
        if tag.artists_names_str:
            self.tags[Id3v1RawMetadataKey.ARTISTS_NAMES_STR] = [tag.artists_names_str]
        if tag.album_name:
            self.tags[Id3v1RawMetadataKey.ALBUM_NAME] = [tag.album_name]
        if tag.year:
            self.tags[Id3v1RawMetadataKey.YEAR] = [tag.year]
        if tag.genre_code:
            self.tags[Id3v1RawMetadataKey.GENRE_CODE_OR_NAME] = [str(tag.genre_code)]
        if tag.track_number and tag.track_number != 0:
            self.tags[Id3v1RawMetadataKey.TRACK_NUMBER] = [str(tag.track_number)]
        if tag.comment:
            self.tags[Id3v1RawMetadataKey.COMMENT] = [tag.comment]

    def save(self) -> None:
        """Save ID3v1 metadata to file using direct file manipulation."""
        if not self.tags:
            return
        
        # Read the entire file
        if hasattr(self.fileobj, 'read'):
            # File object
            self.fileobj.seek(0)
            file_data = bytearray(self.fileobj.read())
        else:
            # File path
            with open(self.fileobj, 'rb') as f:
                file_data = bytearray(f.read())
        
        # Create ID3v1 tag data
        tag_data = self._create_id3v1_tag_data()
        
        # Remove existing ID3v1 tag if present
        self._remove_existing_id3v1_tag(file_data)
        
        # Append new ID3v1 tag
        file_data.extend(tag_data)
        
        # Write back to file
        if hasattr(self.fileobj, 'write'):
            # File object
            self.fileobj.seek(0)
            self.fileobj.write(file_data)
            self.fileobj.truncate()
        else:
            # File path
            with open(self.fileobj, 'wb') as f:
                f.write(file_data)

    def _create_id3v1_tag_data(self) -> bytes:
        """Create 128-byte ID3v1 tag data from current tags."""
        # Initialize with null bytes
        tag_data = bytearray(128)
        
        # TAG identifier (bytes 0-2)
        tag_data[0:3] = b'TAG'
        
        # Title (bytes 3-32, 30 chars max)
        title = self.tags.get(Id3v1RawMetadataKey.TITLE, [''])[0]
        title_bytes = self._truncate_string(title, 30).encode('latin-1', errors='ignore')
        tag_data[3:3+len(title_bytes)] = title_bytes
        
        # Artist (bytes 33-62, 30 chars max)
        artist = self.tags.get(Id3v1RawMetadataKey.ARTISTS_NAMES_STR, [''])[0]
        artist_bytes = self._truncate_string(artist, 30).encode('latin-1', errors='ignore')
        tag_data[33:33+len(artist_bytes)] = artist_bytes
        
        # Album (bytes 63-92, 30 chars max)
        album = self.tags.get(Id3v1RawMetadataKey.ALBUM_NAME, [''])[0]
        album_bytes = self._truncate_string(album, 30).encode('latin-1', errors='ignore')
        tag_data[63:63+len(album_bytes)] = album_bytes
        
        # Year (bytes 93-96, 4 chars max)
        year = self.tags.get(Id3v1RawMetadataKey.YEAR, [''])[0]
        year_bytes = self._truncate_string(year, 4).encode('latin-1', errors='ignore')
        tag_data[93:93+len(year_bytes)] = year_bytes
        
        # Comment and track number (bytes 97-126, 28 chars for comment + 2 for track)
        comment = self.tags.get(Id3v1RawMetadataKey.COMMENT, [''])[0]
        comment_bytes = self._truncate_string(comment, 28).encode('latin-1', errors='ignore')
        tag_data[97:97+len(comment_bytes)] = comment_bytes
        
        # Track number (bytes 125-126 for ID3v1.1)
        track_number = self.tags.get(Id3v1RawMetadataKey.TRACK_NUMBER, ['0'])[0]
        if track_number and track_number != '0':
            track_num = max(0, min(255, int(track_number)))
            if track_num > 0:
                tag_data[125] = 0  # Null byte to indicate track number presence
                tag_data[126] = track_num
        
        # Genre (byte 127)
        genre_code = self.tags.get(Id3v1RawMetadataKey.GENRE_CODE_OR_NAME, ['255'])[0]
        try:
            tag_data[127] = int(genre_code)
        except ValueError:
            tag_data[127] = 255  # Unknown genre
        
        return bytes(tag_data)

    def _remove_existing_id3v1_tag(self, file_data: bytearray) -> bool:
        """Remove existing ID3v1 tag from file data if present.
        
        Returns:
            bool: True if a tag was removed, False otherwise
        """
        if len(file_data) >= 128:
            # Check if last 128 bytes contain ID3v1 tag
            last_128 = file_data[-128:]
            if last_128[:3] == b'TAG':
                # Remove the last 128 bytes
                del file_data[-128:]
                return True
        return False

    def _truncate_string(self, text: str, max_length: int) -> str:
        """Truncate string to maximum length, handling encoding properly."""
        if len(text) <= max_length:
            return text
        return text[:max_length]

    @property
    def mime(self) -> list[str]:
        """Return a list of MIME types this file type could be."""
        return ["audio/mpeg"]  # ID3v1 is typically used with MP3 files

    def add_tags(self) -> None:
        """Add a new ID3v1 tag to the file."""
        if self.tags is None:
            self.tags = {}

    def delete(self, filename: str) -> None:
        """Remove tags from a file."""
        try:
            # Read the entire file
            with open(filename, 'rb') as f:
                file_data = bytearray(f.read())
            
            # Remove existing ID3v1 tag if present
            if self._remove_existing_id3v1_tag(file_data):
                # Write back to file
                with open(filename, 'wb') as f:
                    f.write(file_data)
        except Exception:
            pass  # Ignore errors during deletion

    @staticmethod
    def score(filename: str, fileobj: Any, header: Any) -> float:
        """Return a score indicating how likely this class can handle the file."""
        return 0.0  # We don't want this to be auto-detected by mutagen
