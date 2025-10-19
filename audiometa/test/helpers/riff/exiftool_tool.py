"""Exiftool external tool wrapper for RIFF metadata operations."""

from pathlib import Path
from typing import List

from ..common.external_tool_runner import run_external_tool


class ExiftoolTool:
    """Wrapper for exiftool external tool operations."""
    
    @staticmethod
    def set_riff_genre(file_path: Path, genre: str) -> None:
        """Set RIFF genre using exiftool."""
        command = [
            "exiftool", "-overwrite_original", 
            f"-Genre={genre}",
            str(file_path)
        ]
        run_external_tool(command, "exiftool")
    
    @staticmethod
    def get_riff_metadata_info(file_path: Path) -> str:
        """Get RIFF metadata info using exiftool."""
        command = ["exiftool", "-a", "-G", str(file_path)]
        result = run_external_tool(command, "exiftool")
        return result.stdout