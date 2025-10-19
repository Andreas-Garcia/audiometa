"""Metadata header verification utilities for audio files."""

import subprocess
from pathlib import Path
from typing import Dict


class MetadataHeaderVerifier:
    """Utilities for verifying metadata headers in audio files."""
    
    @staticmethod
    def has_id3v2_header(file_path: Path) -> bool:
        """Check if file has ID3v2 header by reading the first 10 bytes."""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(10)
                return header[:3] == b'ID3'
        except (IOError, OSError):
            return False
    
    @staticmethod
    def has_id3v1_header(file_path: Path) -> bool:
        """Check if file has ID3v1 header by reading the last 128 bytes."""
        try:
            with open(file_path, 'rb') as f:
                f.seek(-128, 2)  # Seek to last 128 bytes
                header = f.read(128)
                return header[:3] == b'TAG'
        except (IOError, OSError):
            return False
    
    @staticmethod
    def has_vorbis_comments(file_path: Path) -> bool:
        """Check if file has Vorbis comments using metaflac."""
        try:
            result = subprocess.run(
                ['metaflac', '--list', str(file_path)],
                capture_output=True, text=True, check=True
            )
            return 'VORBIS_COMMENT' in result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    @staticmethod
    def has_riff_info_chunk(file_path: Path) -> bool:
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
                            # Found RIFF header, check for LIST chunk containing INFO
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
    
    @staticmethod
    def get_metadata_headers_present(file_path: Path) -> Dict[str, bool]:
        """Get a comprehensive report of all metadata headers present in the file."""
        return {
            'id3v2': MetadataHeaderVerifier.has_id3v2_header(file_path),
            'id3v1': MetadataHeaderVerifier.has_id3v1_header(file_path),
            'vorbis': MetadataHeaderVerifier.has_vorbis_comments(file_path),
            'riff': MetadataHeaderVerifier.has_riff_info_chunk(file_path)
        }