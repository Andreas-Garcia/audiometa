"""Id3v2 external tool wrapper for audio metadata operations."""

import subprocess
from pathlib import Path
from typing import Dict, Any, List

from .mid3v2_tool import ExternalMetadataToolError


class Id3v2Tool:
    """Wrapper for id3v2 external tool operations."""
    
    @staticmethod
    def run_command(command: List[str]) -> subprocess.CompletedProcess:
        """Run an id3v2 command with proper error handling."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise ExternalMetadataToolError(f"id3v2 failed: {e}") from e
    
    @staticmethod
    def set_id3v1_metadata(file_path: Path, metadata: Dict[str, Any]) -> None:
        """Set ID3v1 metadata using id3v2 tool."""
        cmd = ["id3v2", "--id3v1-only"]
        
        # Map common metadata keys to id3v2 arguments
        key_mapping = {
            'title': '--song',
            'artist': '--artist', 
            'album': '--album',
            'year': '--year',
            'genre': '--genre',
            'comment': '--comment',
            'track': '--track'
        }
        
        for key, value in metadata.items():
            if key.lower() in key_mapping:
                cmd.extend([key_mapping[key.lower()], str(value)])
        
        cmd.append(str(file_path))
        Id3v2Tool.run_command(cmd)