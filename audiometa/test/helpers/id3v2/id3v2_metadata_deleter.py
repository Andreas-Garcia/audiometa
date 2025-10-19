"""ID3v2 metadata deletion operations."""

from pathlib import Path
from typing import List
from ..common.external_tool_runner import run_external_tool


class ExternalMetadataToolError(Exception):
    """Exception raised when external metadata tools fail."""
    pass


class ID3v2MetadataDeleter:
    """Static utility class for ID3v2 metadata deletion using external tools."""
    
    @staticmethod
    def delete_frame(file_path: Path, frame_id: str) -> None:
        """Delete a specific ID3v2 frame."""
        try:
            command = ["mid3v2", "--delete", frame_id, str(file_path)]
            run_external_tool(command, "mid3v2")
        except Exception:
            # Ignore if frame doesn't exist
            pass
    
    @staticmethod
    def set_multiple_values_single_frame(file_path: Path, frame_id: str, values: List[str]) -> None:
        """Set multiple values in a single ID3v2 frame using mid3v2."""
        command = ["mid3v2"]
        for value in values:
            command.extend([f"--{frame_id}", value])
        command.append(str(file_path))
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def delete_comment(file_path: Path) -> None:
        ID3v2MetadataDeleter.delete_frame(file_path, "COMM")
    
    @staticmethod
    def delete_title(file_path: Path) -> None:
        ID3v2MetadataDeleter.delete_frame(file_path, "TIT2")
    
    @staticmethod
    def delete_artist(file_path: Path) -> None:
        ID3v2MetadataDeleter.delete_frame(file_path, "TPE1")
    
    @staticmethod
    def delete_album(file_path: Path) -> None:
        ID3v2MetadataDeleter.delete_frame(file_path, "TALB")
    
    @staticmethod
    def delete_genre(file_path: Path) -> None:
        ID3v2MetadataDeleter.delete_frame(file_path, "TCON")
    
    @staticmethod
    def delete_lyrics(file_path: Path) -> None:
        ID3v2MetadataDeleter.delete_frame(file_path, "USLT")
    
    @staticmethod
    def delete_language(file_path: Path) -> None:
        ID3v2MetadataDeleter.delete_frame(file_path, "TLAN")
    
    @staticmethod
    def delete_bpm(file_path: Path) -> None:
        ID3v2MetadataDeleter.delete_frame(file_path, "TBPM")
    
    @staticmethod
    def delete_tag(file_path: Path, tag_name: str) -> None:
        command = ["id3v2", "--id3v2-only", "--delete", tag_name, str(file_path)]
        run_external_tool(command, "id3v2")