"""Comprehensive metadata verification utilities for testing audio file metadata."""

import subprocess
from pathlib import Path
from typing import Dict, Any, List

from .metadata_header_verifier import MetadataHeaderVerifier


class ComprehensiveMetadataVerifier:
    """Utilities for comprehensive metadata verification across all formats."""
    
    @staticmethod
    def check_metadata_with_external_tools(file_path: Path) -> Dict[str, Any]:
        """Check metadata using external tools for comprehensive verification.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary with tool results
        """
        results = {}
        
        # Check with mid3v2
        try:
            result = subprocess.run(
                ['mid3v2', '-l', str(file_path)],
                capture_output=True, text=True, check=True
            )
            results['mid3v2'] = {
                'success': True,
                'output': result.stdout,
                'has_id3v2': 'ID3v2 tag' in result.stdout and 'No ID3v2 tag found' not in result.stdout,
                'has_id3v1': 'ID3v1 tag' in result.stdout and 'No ID3v1 tag found' not in result.stdout
            }
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            results['mid3v2'] = {'success': False, 'error': str(e)}
        
        # Check with mutagen-inspect
        try:
            result = subprocess.run(
                ['mutagen-inspect', str(file_path)],
                capture_output=True, text=True, check=True
            )
            results['mutagen_inspect'] = {
                'success': True,
                'output': result.stdout,
                'has_metadata': 'No tags' not in result.stdout
            }
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            results['mutagen_inspect'] = {'success': False, 'error': str(e)}
        
        # Check with metaflac (for FLAC files)
        if file_path.suffix.lower() == '.flac':
            try:
                result = subprocess.run(
                    ['metaflac', '--list', str(file_path)],
                    capture_output=True, text=True, check=True
                )
                results['metaflac'] = {
                    'success': True,
                    'output': result.stdout,
                    'has_vorbis': 'VORBIS_COMMENT' in result.stdout
                }
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                results['metaflac'] = {'success': False, 'error': str(e)}
        
        return results
    
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
        
        headers_present = MetadataHeaderVerifier.get_metadata_headers_present(file_path)
        
        return {
            format_name: not headers_present.get(format_name, False)
            for format_name in expected_removed
        }