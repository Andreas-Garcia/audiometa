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
    
    @staticmethod
    def set_multiple_artists(file_path: Path, artists: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple artists using external mid3v2 tool or manual frame creation.
        
        Args:
            file_path: Path to the audio file
            artists: List of artist strings to set
            in_separate_frames: If True, creates multiple separate TPE1 frames (one per artist) using manual binary construction.
                              If False (default), creates a single TPE1 frame with multiple values using mid3v2.
        """
        from .id3v2_metadata_deleter import ID3v2MetadataDeleter
        
        # Delete existing TPE1 tags
        ID3v2MetadataDeleter.delete_frame(file_path, "TPE1")
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate TPE1 frames
            ID3v2MetadataSetter._create_multiple_id3v2_frames(file_path, 'TPE1', artists)
        else:
            # Set all artists in a single command (creates one frame with multiple values)
            ID3v2MetadataDeleter.set_multiple_values_single_frame(file_path, "TPE1", artists)
    
    @staticmethod
    def set_multiple_genres(file_path: Path, genres: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple genres using external mid3v2 tool or manual frame creation.
        
        Args:
            file_path: Path to the audio file
            genres: List of genre strings to set
            in_separate_frames: If True, creates multiple separate TCON frames (one per genre) using manual binary construction.
                              If False (default), creates a single TCON frame with multiple values using mid3v2.
        """
        from .id3v2_metadata_deleter import ID3v2MetadataDeleter
        
        # Delete existing TCON tags
        ID3v2MetadataDeleter.delete_frame(file_path, "TCON")
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate TCON frames
            ID3v2MetadataSetter._create_multiple_id3v2_frames(file_path, 'TCON', genres)
        else:
            # Set all genres in a single command (creates one frame with multiple values)
            ID3v2MetadataDeleter.set_multiple_values_single_frame(file_path, "TCON", genres)
    
    @staticmethod
    def set_multiple_album_artists(file_path: Path, album_artists: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple album artists using external mid3v2 tool or manual frame creation.
        
        Args:
            file_path: Path to the audio file
            album_artists: List of album artist strings to set
            in_separate_frames: If True, creates multiple separate TPE2 frames (one per album artist) using manual binary construction.
                              If False (default), creates a single TPE2 frame with multiple values using mid3v2.
        """
        from .id3v2_metadata_deleter import ID3v2MetadataDeleter
        
        # Delete existing TPE2 tags
        ID3v2MetadataDeleter.delete_frame(file_path, "TPE2")
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate TPE2 frames
            ID3v2MetadataSetter._create_multiple_id3v2_frames(file_path, 'TPE2', album_artists)
        else:
            # Set all album artists in a single command (creates one frame with multiple values)
            ID3v2MetadataDeleter.set_multiple_values_single_frame(file_path, "TPE2", album_artists)
    
    @staticmethod
    def set_multiple_composers(file_path: Path, composers: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple composers using external mid3v2 tool or manual frame creation.
        
        Args:
            file_path: Path to the audio file
            composers: List of composer strings to set
            in_separate_frames: If True, creates multiple separate TCOM frames (one per composer) using manual binary construction.
                              If False (default), creates a single TCOM frame with multiple values using mid3v2.
        """
        from .id3v2_metadata_deleter import ID3v2MetadataDeleter
        
        # Delete existing TCOM tags
        ID3v2MetadataDeleter.delete_frame(file_path, "TCOM")
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate TCOM frames
            ID3v2MetadataSetter._create_multiple_id3v2_frames(file_path, 'TCOM', composers)
        else:
            # Set all composers in a single command (creates one frame with multiple values)
            ID3v2MetadataDeleter.set_multiple_values_single_frame(file_path, "TCOM", composers)
    
    @staticmethod
    def set_multiple_comments(file_path: Path, comments: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple comments using external mid3v2 tool.
        
        Args:
            file_path: Path to the audio file
            comments: List of comment strings to set
            in_separate_frames: If True, creates multiple separate COMM frames (one per comment).
                              If False (default), creates a single COMM frame with the first comment value.
        """
        from .id3v2_metadata_deleter import ID3v2MetadataDeleter
        
        # Delete existing COMM tags
        ID3v2MetadataDeleter.delete_frame(file_path, "COMM")
        
        if in_separate_frames:
            # Set each comment in a separate mid3v2 call to force multiple frames
            for comment in comments:
                command = ["mid3v2", "--comment", comment, str(file_path)]
                run_external_tool(command, "mid3v2")
        else:
            # Set only the first comment (ID3v2 comment fields are typically single-valued)
            if comments:
                command = ["mid3v2", "--comment", comments[0], str(file_path)]
                run_external_tool(command, "mid3v2")
    
    @staticmethod
    def _create_multiple_id3v2_frames(file_path: Path, frame_id: str, texts: List[str]) -> None:
        """Create multiple separate ID3v2 frames using manual binary construction.
        
        This uses the ManualID3v2FrameCreator to bypass standard tools that 
        consolidate multiple frames of the same type, allowing creation of 
        truly separate frames for testing purposes.
        
        Args:
            file_path: Path to the audio file
            frame_id: The ID3v2 frame identifier (e.g., 'TPE1', 'TPE2', 'TCON', 'TCOM')
            texts: List of text values, one per frame
        """
        from .id3v2_frame_manual_creator import ManualID3v2FrameCreator
        
        creator = ManualID3v2FrameCreator(file_path)
        
        # Create frames based on the frame type
        if frame_id == 'TPE1':
            creator.create_multiple_tpe1_frames(texts)
        elif frame_id == 'TPE2':
            creator.create_multiple_tpe2_frames(texts)
        elif frame_id == 'TCON':
            creator.create_multiple_tcon_frames(texts)
        elif frame_id == 'TCOM':
            creator.create_multiple_tcom_frames(texts)
        else:
            # Generic frame creation for other frame types
            frames = []
            for text in texts:
                frame_data = creator._create_text_frame(frame_id, text)
                frames.append(frame_data)
            creator._write_id3v2_tag(frames)