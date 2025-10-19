"""Id3v2 external tool wrapper for audio metadata operations."""

from pathlib import Path

from ..common.external_tool_runner import run_external_tool
from .id3v2_metadata_deleter import ExternalMetadataToolError


class Id3v2Tool:
    """Wrapper for id3v2 external tool operations."""
    
    @staticmethod
    def delete_tag(file_path: Path, tag_name: str) -> None:
        try:
            command = ["id3v2", "--id3v2-only", "--delete", tag_name, str(file_path)]
            run_external_tool(command, "id3v2")
        except ExternalMetadataToolError:
            pass
    
    @staticmethod
    def set_title(file_path: Path, title: str) -> None:
        command = ["id3v2", "--id3v2-only", "--song", title, str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        command = ["id3v2", "--id3v2-only", "--artist", artist, str(file_path)]
        run_external_tool(command, "id3v2")