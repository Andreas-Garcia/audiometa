"""Id3v1 external tool wrapper for audio metadata operations."""

from pathlib import Path
from typing import Dict, Any

from ..common.external_tool_runner import run_external_tool
from ..id3v2.mid3v2_tool import ExternalMetadataToolError


class Id3v1Tool:
    """Wrapper for id3v1 external tool operations."""
    
    @staticmethod
    def set_metadata(file_path: Path, metadata: Dict[str, Any]) -> None:
        cmd = ["id3v2", "--id3v1-only"]
        
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
    def delete_tag(file_path: Path, tag_name: str) -> None:
        try:
            command = ["id3v2", "--id3v1-only", "--delete", tag_name, str(file_path)]
            run_external_tool(command, "id3v2")
        except ExternalMetadataToolError:
            pass
    
    @staticmethod
    def set_genre(file_path: Path, genre_code: str) -> None:
        command = ["id3v2", "--id3v1-only", f"--genre={genre_code}", str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_comment(file_path: Path, comment: str) -> None:
        command = ["id3v2", "--id3v1-only", "--comment", comment, str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_title(file_path: Path, title: str) -> None:
        command = ["id3v2", "--id3v1-only", "--song", title, str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        command = ["id3v2", "--id3v1-only", "--artist", artist, str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        command = ["id3v2", "--id3v1-only", "--album", album, str(file_path)]
        run_external_tool(command, "id3v2")