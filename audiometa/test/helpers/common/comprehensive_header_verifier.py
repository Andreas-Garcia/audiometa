"""Comprehensive metadata verification utilities for testing audio file metadata."""

from pathlib import Path
from typing import Dict, List

from ..id3v2 import ID3V2HeaderVerifier
from ..id3v1 import ID3v1HeaderVerifier
from ..vorbis import VorbisHeaderVerifier 
from ..riff import RIFFHeaderVerifier


class ComprehensiveHeaderVerifier:
    """Utilities for comprehensive metadata verification across all formats."""
    
    @staticmethod
    def get_metadata_headers_present(file_path: Path) -> Dict[str, bool]:
        """Get a comprehensive report of all metadata headers present in the file.
        
        Returns:
            Dict mapping format names to boolean indicating presence:
            - 'id3v2': ID3v2 header present
            - 'id3v1': ID3v1 header present  
            - 'vorbis': Vorbis comments present
            - 'riff': RIFF INFO chunk present
        """
        return {
            'id3v2': ID3V2HeaderVerifier.has_id3v2_header(file_path),
            'id3v1': ID3v1HeaderVerifier.has_id3v1_header(file_path),
            'vorbis': VorbisHeaderVerifier.has_vorbis_comments(file_path),
            'riff': RIFFHeaderVerifier.has_riff_info_chunk(file_path)
        }
    
    @staticmethod
    def verify_headers_removed(file_path: Path, expected_removed: List[str] = None) -> Dict[str, bool]:
        """Verify that specified metadata headers have been removed.
        
        Args:
            file_path: Path to the audio file
            expected_removed: List of format names that should be removed.
                             If None, checks all formats.
        
        Returns:
            Dictionary with format names as keys and removal status as values
        """
        if expected_removed is None:
            expected_removed = ['id3v2', 'id3v1', 'vorbis', 'riff']
        
        headers_present = ComprehensiveHeaderVerifier.get_metadata_headers_present(file_path)
        
        return {
            format_name: not headers_present.get(format_name, False)
            for format_name in expected_removed
        }