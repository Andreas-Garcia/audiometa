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
        """Get the raw metadata from the audio file using manual ID3v2 parsing, returning a string with frame IDs and values.
        
        Args:
            file_path: Path to the audio file.
            version: The ID3v2 version to parse ("2.3" for ID3v2.3, "2.4" for ID3v2.4). Defaults to "2.4".
        
        Returns:
            String with metadata in 'frame_id=value' format, one per line, or error string if parsing fails.
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
                    version = "2.4"  # Default to 2.4
                if version == "2.3":
                    expected_major = 3
                    expected_minor = 0
                elif version == "2.4":
                    expected_major = 4
                    expected_minor = 0
                else:
                    raise ValueError("Version must be '2.3' or '2.4'")
                if file_version[0] != expected_major or file_version[1] != expected_minor:
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

                    if expected_minor == 4:
                        frame_size = ID3v2MetadataGetter._syncsafe_decode(tag_data[pos+4:pos+8])
                    else:
                        frame_size = int.from_bytes(tag_data[pos+4:pos+8], 'big')
                    frame_flags = tag_data[pos+8:pos+10]

                    if pos + 10 + frame_size > len(tag_data):
                        break

                    frame_data = tag_data[pos+10:pos+10+frame_size]

                    # Parse text frames (those starting with encoding byte)
                    if frame_data and len(frame_data) > 1:
                        encoding = frame_data[0]
                        text_data = frame_data[1:]
                        # Decode the entire text data first
                        decoded_text = ID3v2MetadataGetter._decode_text(encoding, text_data).rstrip('\x00')
                        text = decoded_text
                        if frame_id_str not in metadata:
                            metadata[frame_id_str] = []
                        metadata[frame_id_str].append(text)
                    else:
                        # Non-text frame, just show size
                        if frame_id_str not in metadata:
                            metadata[frame_id_str] = []
                        metadata[frame_id_str].append(f"<{frame_size} bytes>")

                    pos += 10 + frame_size

                lines = []
                for k, v in metadata.items():
                    if isinstance(v, list):
                        for val in v:
                            lines.append(f"{k}={val}")
                    else:
                        lines.append(f"{k}={v}")
                return '\n'.join(lines)
        except Exception as e:
            return f"Error parsing ID3v2: {str(e)}"

    @staticmethod
    def get_artists(file_path, version=None):
        metadata_str = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if not isinstance(metadata_str, str) or metadata_str.startswith("No") or metadata_str.startswith("Error") or metadata_str.startswith("Incomplete"):
            return None
        lines = metadata_str.split('\n')
        tpe1_values = [line.split('=', 1)[1] for line in lines if line.startswith('TPE1=')]
        return tpe1_values[0] if tpe1_values else None    @staticmethod

    @staticmethod
    def get_title(file_path, version=None):
        try:
            versions_to_try = [version] if version else ['2.3', '2.4']
            for v in versions_to_try:
                metadata_str = ID3v2MetadataGetter.get_raw_metadata(file_path, v)
                if isinstance(metadata_str, str) and not metadata_str.startswith("No") and not metadata_str.startswith("Error") and not metadata_str.startswith("Incomplete"):
                    lines = metadata_str.split('\n')
                    tit2_values = [line.split('=', 1)[1] for line in lines if line.startswith('TIT2=')]
                    if tit2_values:
                        return tit2_values[0]
            return None
        except Exception:
            return None

    @staticmethod
    def get_album(file_path, version=None):
        metadata_str = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if not isinstance(metadata_str, str) or metadata_str.startswith("No") or metadata_str.startswith("Error") or metadata_str.startswith("Incomplete"):
            return None
        lines = metadata_str.split('\n')
        talb_values = [line.split('=', 1)[1] for line in lines if line.startswith('TALB=')]
        return talb_values[0] if talb_values else None

    @staticmethod
    def get_year(file_path, version=None):
        metadata_str = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if not isinstance(metadata_str, str) or metadata_str.startswith("No") or metadata_str.startswith("Error") or metadata_str.startswith("Incomplete"):
            return None
        lines = metadata_str.split('\n')
        tyer_values = [line.split('=', 1)[1] for line in lines if line.startswith('TYER=')]
        tdrc_values = [line.split('=', 1)[1] for line in lines if line.startswith('TDRC=')]
        return (tyer_values + tdrc_values)[0] if tyer_values or tdrc_values else None

    @staticmethod
    def get_genres(file_path, version=None):
        metadata_str = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if not isinstance(metadata_str, str) or metadata_str.startswith("No") or metadata_str.startswith("Error") or metadata_str.startswith("Incomplete"):
            return None
        lines = metadata_str.split('\n')
        tcon_values = [line.split('=', 1)[1] for line in lines if line.startswith('TCON=')]
        return tcon_values[0] if tcon_values else None

    @staticmethod
    def get_comment(file_path, version=None):
        metadata_str = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if not isinstance(metadata_str, str) or metadata_str.startswith("No") or metadata_str.startswith("Error") or metadata_str.startswith("Incomplete"):
            return None
        lines = metadata_str.split('\n')
        comm_values = [line.split('=', 1)[1] for line in lines if line.startswith('COMM=')]
        return comm_values[0] if comm_values else None

    @staticmethod
    def get_track(file_path, version=None):
        metadata_str = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if not isinstance(metadata_str, str) or metadata_str.startswith("No") or metadata_str.startswith("Error") or metadata_str.startswith("Incomplete"):
            return None
        lines = metadata_str.split('\n')
        trck_values = [line.split('=', 1)[1] for line in lines if line.startswith('TRCK=')]
        return trck_values[0] if trck_values else None

    @staticmethod
    def get_multiple_entries_from_raw_data(file_path, frame_id, version=None):
        metadata_str = ID3v2MetadataGetter.get_raw_metadata(file_path, version)
        if not isinstance(metadata_str, str) or metadata_str.startswith("No") or metadata_str.startswith("Error") or metadata_str.startswith("Incomplete"):
            return {'raw_output': ''}
        lines = metadata_str.split('\n')
        frame_lines = [line for line in lines if line.startswith(f'{frame_id}=')]
        return {'raw_output': '\n'.join(frame_lines)}
