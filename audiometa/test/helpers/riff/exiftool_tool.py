"""Exiftool external tool wrapper for RIFF metadata operations."""

import subprocess
from pathlib import Path
from typing import List

from ..id3v2.mid3v2_tool import ExternalMetadataToolError


class ExiftoolTool:
    """Wrapper for exiftool external tool operations."""
    
    @staticmethod
    def run_command(command: List[str]) -> subprocess.CompletedProcess:
        """Run an exiftool command with proper error handling."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise ExternalMetadataToolError(f"exiftool failed: {e}") from e
    
    @staticmethod
    def set_riff_genre(file_path: Path, genre: str) -> None:
        """Set RIFF genre using exiftool."""
        command = [
            "exiftool", "-overwrite_original", 
            f"-Genre={genre}",
            str(file_path)
        ]
        ExiftoolTool.run_command(command)
    
    @staticmethod
    def get_riff_metadata_info(file_path: Path) -> str:
        """Get RIFF metadata info using exiftool."""
        command = ["exiftool", "-a", "-G", str(file_path)]
        result = ExiftoolTool.run_command(command)
        return result.stdout