"""ID3v2 and ID3v1 metadata setting operations."""

from pathlib import Path
from typing import List
from .mid3v2_tool import Mid3v2Tool
from .id3v2_tool import Id3v2Tool
from ..id3v1.id3v1_metadata_setter import ID3v1MetadataSetter


class ID3v2MetadataSetter:
    """Static utility class for ID3v2 metadata setting using external tools."""
    
    @staticmethod
    def set_comment(file_path: Path, comment: str) -> None:
        Mid3v2Tool.set_comment(file_path, comment)
    
    @staticmethod
    def set_title(file_path: Path, title: str) -> None:
        Id3v2Tool.set_id3v2_title(file_path, title)
    
    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        Id3v2Tool.set_id3v2_artist(file_path, artist)
    
    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        Mid3v2Tool.set_album(file_path, album)
    
    @staticmethod
    def set_genre(file_path: Path, genre: str) -> None:
        Mid3v2Tool.set_genre(file_path, genre)
    
    @staticmethod
    def set_lyrics(file_path: Path, lyrics: str) -> None:
        Mid3v2Tool.set_lyrics(file_path, lyrics)
    
    @staticmethod
    def set_language(file_path: Path, language: str) -> None:
        Mid3v2Tool.set_language(file_path, language)
    
    @staticmethod
    def set_bpm(file_path: Path, bpm: int) -> None:
        Mid3v2Tool.set_bpm(file_path, bpm)
    
    @staticmethod
    def set_max_metadata(file_path: Path) -> None:
        from ..common.external_tool_runner import run_script
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        run_script("set-id3v2-max-metadata.sh", file_path, scripts_dir)

    @staticmethod
    def set_separator_artists(file_path: Path, artists_string: str):
        command = ["mid3v2", "--artist", artists_string, str(file_path)]
        Mid3v2Tool.run_command(command)

    @staticmethod
    def set_separator_genres(file_path: Path, genres_string: str):
        command = ["mid3v2", "--genre", genres_string, str(file_path)]
        Mid3v2Tool.run_command(command)

    @staticmethod
    def set_separator_composers(file_path: Path, composers_string: str):
        command = ["mid3v2", "--TCOM", composers_string, str(file_path)]
        Mid3v2Tool.run_command(command)