"""Mid3v2 external tool wrapper for audio metadata operations."""

import subprocess
from pathlib import Path
from typing import Dict, Any, List


class ExternalMetadataToolError(Exception):
    """Exception raised when external metadata tools fail."""
    pass


class Mid3v2Tool:
    """Wrapper for mid3v2 external tool operations."""
    
    @staticmethod
    def run_command(command: List[str]) -> subprocess.CompletedProcess:
        """Run a mid3v2 command with proper error handling."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise ExternalMetadataToolError(f"mid3v2 failed: {e}") from e
    
    @staticmethod
    def set_mp3_metadata(file_path: Path, metadata: Dict[str, Any]) -> None:
        """Set MP3 metadata using mid3v2 tool."""
        cmd = ["mid3v2"]
        
        # Map common metadata keys to mid3v2 arguments
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
        Mid3v2Tool.run_command(cmd)
    
    @staticmethod
    def delete_frame(file_path: Path, frame_id: str) -> None:
        """Delete a specific ID3v2 frame."""
        try:
            command = ["mid3v2", "--delete", frame_id, str(file_path)]
            Mid3v2Tool.run_command(command)
        except ExternalMetadataToolError:
            # Ignore if frame doesn't exist
            pass
    
    @staticmethod
    def set_multiple_values_single_frame(file_path: Path, frame_id: str, values: List[str]) -> None:
        """Set multiple values in a single ID3v2 frame using mid3v2."""
        command = ["mid3v2"]
        for value in values:
            command.extend([f"--{frame_id}", value])
        command.append(str(file_path))
        Mid3v2Tool.run_command(command)
    
    @staticmethod
    def get_metadata_info(file_path: Path) -> str:
        """Get metadata info using mid3v2 -l command."""
        command = ["mid3v2", "-l", str(file_path)]
        result = Mid3v2Tool.run_command(command)
        return result.stdout