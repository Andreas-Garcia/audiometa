"""Id3v2 external tool wrapper for audio metadata operations."""

from pathlib import Path
from typing import Dict, Any

from ..common.external_tool_runner import run_external_tool
from .mid3v2_tool import ExternalMetadataToolError


class Id3v2Tool:
    """Wrapper for id3v2 external tool operations."""
    
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
        run_external_tool(cmd, "id3v2")
    
    @staticmethod
    def delete_id3v1_tag(file_path: Path, tag_name: str) -> None:
        """Delete a specific ID3v1 tag using id3v2 tool."""
        try:
            command = ["id3v2", "--id3v1-only", "--delete", tag_name, str(file_path)]
            run_external_tool(command, "id3v2")
        except ExternalMetadataToolError:
            # Ignore if tag doesn't exist
            pass
    
    @staticmethod
    def delete_id3v2_tag(file_path: Path, tag_name: str) -> None:
        """Delete a specific ID3v2 tag using id3v2 tool with --id3v2-only flag."""
        try:
            command = ["id3v2", "--id3v2-only", "--delete", tag_name, str(file_path)]
            run_external_tool(command, "id3v2")
        except ExternalMetadataToolError:
            # Ignore if tag doesn't exist
            pass
    
    @staticmethod
    def set_id3v2_title(file_path: Path, title: str) -> None:
        """Set ID3v2 title using id3v2 tool with --id3v2-only flag."""
        command = ["id3v2", "--id3v2-only", "--song", title, str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_id3v2_artist(file_path: Path, artist: str) -> None:
        """Set ID3v2 artist using id3v2 tool with --id3v2-only flag."""
        command = ["id3v2", "--id3v2-only", "--artist", artist, str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_id3v1_genre(file_path: Path, genre_code: str) -> None:
        """Set ID3v1 genre using id3v2 tool."""
        command = ["id3v2", "--id3v1-only", f"--genre={genre_code}", str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_id3v1_comment(file_path: Path, comment: str) -> None:
        """Set ID3v1 comment using id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--comment", comment, str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_id3v1_title(file_path: Path, title: str) -> None:
        """Set ID3v1 title using id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--song", title, str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_id3v1_artist(file_path: Path, artist: str) -> None:
        """Set ID3v1 artist using id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--artist", artist, str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_id3v1_album(file_path: Path, album: str) -> None:
        """Set ID3v1 album using id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--album", album, str(file_path)]
        run_external_tool(command, "id3v2")