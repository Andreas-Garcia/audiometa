"""
id3v2_metadata_getter.py
Helper for extracting ID3v2 metadata from audio files.
"""

from audiometa.test.helpers.common.external_tool_runner import run_external_tool

class ID3v2MetadataGetter:
    """Helper class to get ID3v2 metadata from audio files using manual parsing."""

    @staticmethod
    def _syncsafe_decode(data: bytes) -> int:
        """Decode a 4-byte syncsafe integer."""
        return ((data[0] & 0x7F) << 21) | ((data[1] & 0x7F) << 14) | ((data[2] & 0x7F) << 7) | (data[3] & 0x7F)

    @staticmethod
    def _decode_text(encoding: int, data: bytes) -> str:
        """Decode text based on encoding."""
        if encoding == 0:  # ISO-8859-1
            return data.decode('latin1', errors='ignore')
        elif encoding == 1:  # UTF-16 with BOM
            return data.decode('utf-16', errors='ignore')
        elif encoding == 2:  # UTF-16BE without BOM
            return data.decode('utf-16be', errors='ignore')
        elif encoding == 3:  # UTF-8
            return data.decode('utf-8', errors='ignore')
        else:
            return data.decode('latin1', errors='ignore')  # fallback

    @staticmethod
    def get_raw_metadata(file_path, version=None):
        """Get the raw metadata from the audio file using manual ID3v2 parsing, returning a dict of frame IDs to values.
        
        Args:
            file_path: Path to the audio file.
            version: The ID3v2 version to parse (3 for ID3v2.3, 4 for ID3v2.4). Must be specified.
        
        Returns:
            Dict of frame IDs to values, or error string if parsing fails.
        """
        try:
            with open(file_path, 'rb') as f:
                # Read ID3v2 header (10 bytes)
                header = f.read(10)
                if len(header) < 10 or header[:3] != b'ID3':
                    return "No ID3v2 tag found"

                # Parse header
                file_version = (header[3], header[4])
                if version is None:
                    raise ValueError("Version must be specified (3 for ID3v2.3 or 4 for ID3v2.4)")
                elif file_version[0] != version:
                    return None
                flags = header[5]
                tag_size = ID3v2MetadataGetter._syncsafe_decode(header[6:10])

                # Read tag data
                tag_data = f.read(tag_size)
                if len(tag_data) != tag_size:
                    return "Incomplete ID3v2 tag"

                metadata = {}
                pos = 0
                while pos < len(tag_data) - 10:
                    # Parse frame header (10 bytes)
                    frame_id = tag_data[pos:pos+4]
                    if frame_id == b'\x00\x00\x00\x00':
                        break  # Padding or end
                    try:
                        frame_id_str = frame_id.decode('ascii')
                    except UnicodeDecodeError:
                        break

                    if version == 4:
                        frame_size = ID3v2MetadataGetter._syncsafe_decode(tag_data[pos+4:pos+8])
                    elif version == 3:
                        frame_size = int.from_bytes(tag_data[pos+4:pos+8], 'big')
                    else:
                        return None
                    frame_flags = tag_data[pos+8:pos+10]

                    if pos + 10 + frame_size > len(tag_data):
                        break

                    frame_data = tag_data[pos+10:pos+10+frame_size]

                    # Parse text frames (those starting with encoding byte)
                    if frame_data and len(frame_data) > 1:
                        encoding = frame_data[0]
                        text_data = frame_data[1:]
                        # Split on appropriate null bytes based on encoding
                        null = b'\x00\x00' if encoding in (1, 2) else b'\x00'
                        texts = text_data.split(null)
                        decoded_texts = [ID3v2MetadataGetter._decode_text(encoding, t) for t in texts if t]
                        text = decoded_texts[0] if decoded_texts else ''
                        metadata[frame_id_str] = text
                    else:
                        # Non-text frame, just show size
                        metadata[frame_id_str] = f"<{frame_size} bytes>"

                    pos += 10 + frame_size

                return metadata
        except Exception as e:
            return f"Error parsing ID3v2: {str(e)}"

    @staticmethod
    def get_artists(file_path, version=None):
        metadata = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if metadata is None:
            return None
        return metadata.get('TPE1')

    @staticmethod
    def get_title(file_path, version=None):
        metadata = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if metadata is None:
            return None
        return metadata.get('TIT2')

    @staticmethod
    def get_album(file_path, version=None):
        metadata = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if metadata is None:
            return None
        return metadata.get('TALB')

    @staticmethod
    def get_year(file_path, version=None):
        metadata = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if metadata is None:
            return None
        return metadata.get('TYER') or metadata.get('TDRC')

    @staticmethod
    def get_genres(file_path, version=None):
        metadata = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if metadata is None:
            return None
        return metadata.get('TCON')

    @staticmethod
    def get_comment(file_path, version=None):
        metadata = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if metadata is None:
            return None
        return metadata.get('COMM')

    @staticmethod
    def get_track(file_path, version=None):
        metadata = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if metadata is None:
            return None
        return metadata.get('TRCK')
