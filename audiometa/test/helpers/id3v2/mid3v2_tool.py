"""Mid3v2 external tool wrapper for audio metadata operations."""

from pathlib import Path
from typing import Dict, Any, List

from ..common.external_tool_runner import run_external_tool


class ExternalMetadataToolError(Exception):
    """Exception raised when external metadata tools fail."""
    pass


class Mid3v2Tool:
    """Wrapper for mid3v2 external tool operations."""
    
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
        run_external_tool(cmd, "mid3v2")
    
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
    def get_metadata_info(file_path: Path) -> str:
        """Get metadata info using mid3v2 -l command."""
        command = ["mid3v2", "-l", str(file_path)]
        result = run_external_tool(command, "mid3v2")
        return result.stdout
    
    @staticmethod
    def set_comment(file_path: Path, comment: str) -> None:
        """Set ID3v2 comment using mid3v2 tool."""
        command = ["mid3v2", "--comment", comment, str(file_path)]
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        """Set ID3v2 album using mid3v2 tool."""
        command = ["mid3v2", "--album", album, str(file_path)]
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_genre(file_path: Path, genre: str) -> None:
        """Set ID3v2 genre using mid3v2 tool."""
        command = ["mid3v2", "--genre", genre, str(file_path)]
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_lyrics(file_path: Path, lyrics: str) -> None:
        """Set ID3v2 lyrics using mid3v2 tool."""
        command = ["mid3v2", "--USLT", f"eng:{lyrics}", str(file_path)]
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_language(file_path: Path, language: str) -> None:
        """Set ID3v2 language using mid3v2 tool."""
        command = ["mid3v2", "--TLAN", language, str(file_path)]
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_bpm(file_path: Path, bpm: int) -> None:
        """Set ID3v2 BPM using mid3v2 tool."""
        command = ["mid3v2", "--TBPM", str(bpm), str(file_path)]
        run_external_tool(command, "mid3v2")