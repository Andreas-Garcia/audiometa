"""Helper class for RIFF metadata operations using external tools."""

from pathlib import Path
from .base_helper import BaseHelper


class RiffHelper(BaseHelper):
    """Helper class for RIFF metadata operations (WAV)."""
    
    @staticmethod
    def set_max_metadata(file_path: Path):
        """Set maximum RIFF metadata using external script."""
        return RiffHelper._run_script("set-riff-max-metadata.sh", file_path)
    
    @staticmethod
    def set_genre_text(file_path: Path, genre_text: str):
        """Set RIFF genre using external exiftool or bwfmetaedit tool."""
        try:
            # Try exiftool first
            command = [
                "exiftool", "-overwrite_original", 
                f"-Genre={genre_text}",
                str(file_path)
            ]
            return RiffHelper._run_external_tool(command)
        except RuntimeError:
            try:
                # Fallback to bwfmetaedit
                command = [
                    "bwfmetaedit", f"--IGNR={genre_text}", str(file_path)
                ]
                return RiffHelper._run_external_tool(command)
            except RuntimeError as e:
                raise RuntimeError(f"Failed to set RIFF genre: {e}") from e
    
    @staticmethod
    def remove_metadata(file_path: Path):
        """Remove RIFF metadata using external script."""
        return RiffHelper._run_script("remove_riff.py", file_path)
    
    @staticmethod
    def has_info_chunk(file_path: Path) -> bool:
        """Check if file has RIFF INFO chunk by reading file structure."""
        try:
            with open(file_path, 'rb') as f:
                # Read first few bytes to check for ID3v2 tags
                first_bytes = f.read(10)
                f.seek(0)  # Reset to beginning
                
                if first_bytes.startswith(b'ID3'):
                    # File has ID3v2 tags, find RIFF header after them
                    data = f.read()
                    pos = 0
                    while pos < len(data) - 8:
                        if data[pos:pos+4] == b'RIFF':
                            # Found RIFF header, check for INFO chunk
                            riff_size = int.from_bytes(data[pos+4:pos+8], 'little')
                            riff_data = data[pos+8:pos+8+riff_size]
                            
                            # Search for LIST chunk containing INFO in RIFF data
                            # Skip the WAVE chunk header (4 bytes)
                            info_pos = 4
                            while info_pos < len(riff_data) - 8:
                                chunk_id = riff_data[info_pos:info_pos+4]
                                chunk_size = int.from_bytes(riff_data[info_pos+4:info_pos+8], 'little')
                                
                                if chunk_id == b'LIST':
                                    # Check if this LIST chunk contains INFO
                                    list_data = riff_data[info_pos+8:info_pos+8+chunk_size]
                                    if len(list_data) >= 4 and list_data[:4] == b'INFO':
                                        return True
                                
                                # Move to next chunk (chunk size + padding)
                                info_pos += 8 + chunk_size
                                if chunk_size % 2 == 1:  # Odd size needs padding
                                    info_pos += 1
                            return False
                        pos += 1
                    return False
                else:
                    # File starts with RIFF header
                    riff_header = f.read(12)
                    if riff_header[:4] != b'RIFF':
                        return False
                    
                    # Look for LIST chunk containing INFO
                    chunk_size = int.from_bytes(riff_header[4:8], 'little')
                    data = f.read(chunk_size)
                    
                    # Search for LIST chunk containing INFO
                    pos = 0
                    while pos < len(data) - 8:
                        chunk_id = data[pos:pos+4]
                        chunk_size = int.from_bytes(data[pos+4:pos+8], 'little')
                        
                        if chunk_id == b'LIST':
                            # Check if this LIST chunk contains INFO
                            list_data = data[pos+8:pos+8+chunk_size]
                            if len(list_data) >= 4 and list_data[:4] == b'INFO':
                                return True
                        
                        # Move to next chunk (chunk size + padding)
                        pos += 8 + chunk_size
                        if chunk_size % 2 == 1:  # Odd size needs padding
                            pos += 1
                    
                    return False
        except (IOError, OSError, ValueError):
            return False
