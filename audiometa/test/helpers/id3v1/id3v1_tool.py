"""Id3v1 external tool wrapper for basic operations."""

from pathlib import Path

from ..common.external_tool_runner import run_external_tool


class Id3v1Tool:
    """Wrapper for id3v1 external tool operations."""
    
    @staticmethod
    def get_info(file_path: Path) -> str:
        """Get ID3v1 tag information."""
        command = ["id3v2", "--list", "--id3v1-only", str(file_path)]
        result = run_external_tool(command, "id3v2")
        return result.stdout