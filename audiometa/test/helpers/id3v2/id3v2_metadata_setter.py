"""ID3v2 and ID3v1 metadata setting operations."""

from pathlib import Path
from typing import List, Dict, Any
from ..id3v1.id3v1_metadata_setter import ID3v1MetadataSetter
from ..common.external_tool_runner import run_external_tool


class ID3v2MetadataSetter:
    """Static utility class for ID3v2 metadata setting using external tools."""
    
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
    def set_comment(file_path: Path, comment: str) -> None:
        """Set ID3v2 comment using mid3v2 tool."""
        command = ["mid3v2", "--comment", comment, str(file_path)]
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_title(file_path: Path, title: str) -> None:
        command = ["id3v2", "--id3v2-only", "--song", title, str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        command = ["id3v2", "--id3v2-only", "--artist", artist, str(file_path)]
        run_external_tool(command, "id3v2")
    
    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        command = ["mid3v2", "--album", album, str(file_path)]
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_genre(file_path: Path, genre: str) -> None:
        command = ["mid3v2", "--genre", genre, str(file_path)]
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_lyrics(file_path: Path, lyrics: str) -> None:
        command = ["mid3v2", "--USLT", f"eng:{lyrics}", str(file_path)]
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_language(file_path: Path, language: str) -> None:
        command = ["mid3v2", "--TLAN", language, str(file_path)]
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_bpm(file_path: Path, bpm: int) -> None:
        command = ["mid3v2", "--TBPM", str(bpm), str(file_path)]
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_max_metadata(file_path: Path) -> None:
        from ..common.external_tool_runner import run_script
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        run_script("set-id3v2-max-metadata.sh", file_path, scripts_dir)

    @staticmethod
    def set_separator_artists(file_path: Path, artists_string: str):
        command = ["mid3v2", "--artist", artists_string, str(file_path)]
        run_external_tool(command, "mid3v2")

    @staticmethod
    def set_separator_genres(file_path: Path, genres_string: str):
        command = ["mid3v2", "--genre", genres_string, str(file_path)]
        run_external_tool(command, "mid3v2")

    @staticmethod
    def set_separator_composers(file_path: Path, composers_string: str):
        command = ["mid3v2", "--TCOM", composers_string, str(file_path)]
        run_external_tool(command, "mid3v2")