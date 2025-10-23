"""Vorbis metadata setting operations."""

from pathlib import Path
from typing import Dict, Any, List

from ..common.external_tool_runner import run_external_tool


class VorbisMetadataSetter:
    """Static utility class for Vorbis metadata setting using external tools."""
    
    @staticmethod
    def set_multiple_tags(file_path: Path, tag_name: str, values: List[str]) -> None:
        """Set multiple Vorbis comment tags with the same name."""
        # First remove existing tags
        try:
            command = ["metaflac", "--remove-tag", tag_name, str(file_path)]
            run_external_tool(command, "metaflac")
        except Exception:
            # Ignore if tags don't exist
            pass
        
        # Add each value as a separate tag
        for value in values:
            command = ["metaflac", "--set-tag", f"{tag_name}={value}", str(file_path)]
            run_external_tool(command, "metaflac")
    
    @staticmethod
    def set_flac_metadata(file_path: Path, metadata: Dict[str, Any]) -> None:
        """Set FLAC metadata using metaflac tool."""
        cmd = ["metaflac"]
        
        # Map common metadata keys to metaflac arguments
        key_mapping = {
            'title': 'TITLE',
            'artist': 'ARTIST',
            'album': 'ALBUM',
            'date': 'DATE',
            'genre': 'GENRE',
            'comment': 'COMMENT',
            'tracknumber': 'TRACKNUMBER'
        }
        
        for key, value in metadata.items():
            if key.lower() in key_mapping:
                cmd.extend([f"--set-tag={key_mapping[key.lower()]}={value}"])
        
        cmd.append(str(file_path))
        run_external_tool(cmd, "metaflac")
    
    @staticmethod
    def set_genre(file_path: Path, genre_text: str) -> None:
        command = ["metaflac", "--set-tag", f"GENRE={genre_text}", str(file_path)]
        run_external_tool(command, "metaflac")
    
    @staticmethod
    def set_comment(file_path: Path, comment: str) -> None:
        command = ["metaflac", "--set-tag", f"COMMENT={comment}", str(file_path)]
        run_external_tool(command, "metaflac")
    
    @staticmethod
    def add_title(file_path: Path, title: str) -> None:
        command = ["metaflac", "--set-tag", f"TITLE={title}", str(file_path)]
        run_external_tool(command, "metaflac")
    
    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        command = ["metaflac", "--set-tag", f"ARTIST={artist}", str(file_path)]
        run_external_tool(command, "metaflac")
    
    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        command = ["metaflac", "--set-tag", f"ALBUM={album}", str(file_path)]
        run_external_tool(command, "metaflac")
    
    @staticmethod
    def set_lyrics(file_path: Path, lyrics: str) -> None:
        command = ["metaflac", "--set-tag", f"LYRICS={lyrics}", str(file_path)]
        run_external_tool(command, "metaflac")
    
    @staticmethod
    def set_language(file_path: Path, language: str) -> None:
        command = ["metaflac", "--set-tag", f"LANGUAGE={language}", str(file_path)]
        run_external_tool(command, "metaflac")
    
    @staticmethod
    def set_bpm(file_path: Path, bpm: int) -> None:
        command = ["metaflac", "--set-tag", f"BPM={bpm}", str(file_path)]
        run_external_tool(command, "metaflac")
    
    @staticmethod
    def set_max_metadata(file_path: Path) -> None:
        from ..common.external_tool_runner import run_script
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        run_script("set-vorbis-max-metadata.sh", file_path, scripts_dir)
    
    @staticmethod
    def set_artists_one_two_three(file_path: Path) -> None:
        from ..common.external_tool_runner import run_script
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        run_script("set-artists-One-Two-Three-vorbis.sh", file_path, scripts_dir)
    
    @staticmethod
    def set_artists(file_path: Path, artists: List[str]):
        """Set multiple Vorbis artists using external metaflac tool."""
        VorbisMetadataSetter.set_multiple_tags(file_path, "ARTIST", artists)
    
    @staticmethod
    def set_album_artists(file_path: Path, album_artists: List[str]):
        """Set multiple Vorbis album artists using external metaflac tool."""
        VorbisMetadataSetter.set_multiple_tags(file_path, "ALBUMARTIST", album_artists)
    
    @staticmethod
    def set_composers(file_path: Path, composers: List[str]):
        """Set multiple Vorbis composers using external metaflac tool."""
        VorbisMetadataSetter.set_multiple_tags(file_path, "COMPOSER", composers)
    
    @staticmethod
    def set_genres(file_path: Path, genres: List[str]):
        """Set multiple Vorbis genres using external metaflac tool."""
        VorbisMetadataSetter.set_multiple_tags(file_path, "GENRE", genres)
    
    @staticmethod
    def set_performers(file_path: Path, performers: List[str]):
        """Set multiple Vorbis performers using external metaflac tool."""
        VorbisMetadataSetter.set_multiple_tags(file_path, "PERFORMER", performers)
    
    @staticmethod
    def set_multiple_comments(file_path: Path, comments: List[str]):
        """Set multiple Vorbis comments using external metaflac tool."""
        VorbisMetadataSetter.set_multiple_tags(file_path, "COMMENT", comments)