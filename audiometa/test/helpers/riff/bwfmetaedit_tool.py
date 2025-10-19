"""Bwfmetaedit external tool wrapper for WAV metadata operations."""

import subprocess
from pathlib import Path
from typing import Dict, Any, List

from ..id3v2.mid3v2_tool import ExternalMetadataToolError


class BwfmetaeditTool:
    """Wrapper for bwfmetaedit external tool operations."""
    
    @staticmethod
    def run_command(command: List[str]) -> subprocess.CompletedProcess:
        """Run a bwfmetaedit command with proper error handling."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise ExternalMetadataToolError(f"bwfmetaedit failed: {e}") from e
    
    @staticmethod
    def set_wav_metadata(file_path: Path, metadata: Dict[str, Any]) -> None:
        """Set WAV metadata using bwfmetaedit tool."""
        cmd = ["bwfmetaedit"]
        
        # Map common metadata keys to bwfmetaedit arguments
        key_mapping = {
            'title': '--INAM',
            'artist': '--IART',
            'album': '--IPRD',
            'genre': '--IGNR',
            'date': '--ICRD',
            'comment': '--ICMT',
            'track': '--ITRK'
        }
        
        for key, value in metadata.items():
            if key.lower() in key_mapping:
                cmd.extend([f"{key_mapping[key.lower()]}={value}"])
        
        cmd.append(str(file_path))
        BwfmetaeditTool.run_command(cmd)
    
    @staticmethod
    def remove_chunk(file_path: Path, chunk_name: str) -> None:
        """Remove a specific RIFF chunk."""
        try:
            command = ["bwfmetaedit", f"--remove-chunks=INFO/{chunk_name}", str(file_path)]
            BwfmetaeditTool.run_command(command)
        except ExternalMetadataToolError:
            # Ignore if chunk doesn't exist
            pass