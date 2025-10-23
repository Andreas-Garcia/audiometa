"""ID3v2 and ID3v1 metadata setting operations."""

from pathlib import Path
from typing import List, Dict, Any

from ..common.external_tool_runner import run_external_tool


class ID3v2MetadataSetter:
    """Static utility class for ID3v2 metadata setting using external tools."""
    
    @staticmethod
    def set_metadata(file_path: Path, metadata: Dict[str, Any], version: str = None) -> None:
        """Set MP3 metadata using appropriate ID3v2 tool based on version.
        
        Args:
            file_path: Path to the MP3 file
            metadata: Dictionary of metadata to set
            version: Optional ID3v2 version ("2.3" or "2.4"). Defaults to "2.4" if not specified.
        """
        if version == "2.3":
            tool = "id3v2"
            cmd = ["id3v2", "--id3v2-only"]
        else:
            # Default to 2.4 with mid3v2
            tool = "mid3v2"
            cmd = ["mid3v2"]
        
        # Map common metadata keys to tool arguments
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
        run_external_tool(cmd, tool)
    
    @staticmethod
    def set_title(file_path: Path, title: str, version: str = "2.4") -> None:
        if version == "2.3":
            command = ["id3v2", "--id3v2-only", "--song", title, str(file_path)]
            run_external_tool(command, "id3v2")
        else:
            command = ["mid3v2", "--song", title, str(file_path)]
            run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_titles(file_path: Path, titles: List[str], in_separate_frames: bool = False, version: str = "2.4"):
        """Set ID3v2 multiple titles using external mid3v2 tool or manual frame creation.
        
        Args:
            file_path: Path to the audio file
            titles: List of title strings to set
            in_separate_frames: If True, creates multiple separate TIT2 frames (one per title) using manual binary construction.
                              If False (default), creates a single TIT2 frame with multiple values using mid3v2.
            version: ID3v2 version to use (e.g., "2.3", "2.4")
        """
        ID3v2MetadataSetter._set_multiple_metadata_values(file_path, "TIT2", titles, in_separate_frames, version)
    
    @staticmethod
    def set_artist(file_path: Path, artist: str, version: str = "2.4") -> None:
        if version == "2.3":
            command = ["id3v2", "--id3v2-only", "--artist", artist, str(file_path)]
            run_external_tool(command, "id3v2")
        else:
            command = ["mid3v2", "--artist", artist, str(file_path)]
            run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_album(file_path: Path, album: str, version: str = "2.4") -> None:
        if version == "2.3":
            command = ["id3v2", "--id3v2-only", "--album", album, str(file_path)]
            run_external_tool(command, "id3v2")
        else:
            command = ["mid3v2", "--album", album, str(file_path)]
            run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_genre(file_path: Path, genre: str, version: str = "2.4") -> None:
        if version == "2.3":
            command = ["id3v2", "--id3v2-only", "--genre", genre, str(file_path)]
            run_external_tool(command, "id3v2")
        else:
            command = ["mid3v2", "--genre", genre, str(file_path)]
            run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_lyrics(file_path: Path, lyrics: str, version: str = "2.4") -> None:
        if version == "2.3":
            command = ["id3v2", "--id3v2-only", "--USLT", f"eng:{lyrics}", str(file_path)]
            run_external_tool(command, "id3v2")
        else:
            command = ["mid3v2", "--USLT", f"eng:{lyrics}", str(file_path)]
            run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_language(file_path: Path, language: str, version: str = "2.4") -> None:
        if version == "2.3":
            command = ["id3v2", "--id3v2-only", "--TLAN", language, str(file_path)]
            run_external_tool(command, "id3v2")
        else:
            command = ["mid3v2", "--TLAN", language, str(file_path)]
            run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_bpm(file_path: Path, bpm: int, version: str = "2.4") -> None:
        if version == "2.3":
            command = ["id3v2", "--id3v2-only", "--TBPM", str(bpm), str(file_path)]
            run_external_tool(command, "id3v2")
        else:
            command = ["mid3v2", "--TBPM", str(bpm), str(file_path)]
            run_external_tool(command, "mid3v2")

    @staticmethod
    def set_max_metadata(file_path: Path) -> None:
        from ..common.external_tool_runner import run_script
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        run_script("set-id3v2-max-metadata.sh", file_path, scripts_dir)

    @staticmethod
    def _set_multiple_values_single_frame(file_path: Path, frame_id: str, values: List[str], version: str = "2.4", separator: str = None) -> None:
        """Set multiple values in a single ID3v2 frame with version-specific handling.
        
        Args:
            file_path: Path to the audio file
            frame_id: The ID3v2 frame identifier (e.g., 'TPE1', 'TCON', 'TCOM', 'TIT2')
            values: List of values to set in the frame
            version: ID3v2 version to use (e.g., "2.3", "2.4")
            separator: Separator to use between values. If None, uses default behavior
                      (semicolon for ID3v2.3, null byte for ID3v2.4)
        """
        # Determine separator if not provided
        if separator is None:
            separator = ";" if version == "2.3" else "\x00"
        
        # Use appropriate method for all cases
        ID3v2MetadataSetter._set_single_frame_with_mid3v2(file_path, frame_id, values, version, separator)
    
    @staticmethod
    def _set_multiple_metadata_values(file_path: Path, frame_id: str, values: List[str], in_separate_frames: bool = False, version: str = "2.4", separator: str = None) -> None:
        """Set multiple metadata values, either in separate frames or a single frame.
        
        Args:
            file_path: Path to the audio file
            frame_id: The ID3v2 frame identifier (e.g., 'TPE1', 'TCON', 'TCOM', 'TIT2')
            values: List of values to set
            in_separate_frames: If True, creates multiple separate frames. If False, creates a single frame with multiple values.
            version: ID3v2 version to use (e.g., "2.3", "2.4")
            separator: Separator to use between values when in_separate_frames=False. If None, uses default behavior.
        """
        from .id3v2_metadata_deleter import ID3v2MetadataDeleter
        
        # Delete existing frames
        ID3v2MetadataDeleter.delete_frame(file_path, frame_id)
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate frames
            ID3v2MetadataSetter._create_multiple_id3v2_frames(file_path, frame_id, values, version)
        else:
            # Create a single frame with multiple values (version-specific handling)
            ID3v2MetadataSetter._set_multiple_values_single_frame(file_path, frame_id, values, version, separator)
    
    @staticmethod
    def set_artists(file_path: Path, artists: List[str], in_separate_frames: bool = False, version: str = "2.4", separator: str = None):
        """Set ID3v2 multiple artists using external mid3v2 tool or manual frame creation.
        
        Args:
            file_path: Path to the audio file
            artists: List of artist strings to set
            in_separate_frames: If True, creates multiple separate TPE1 frames (one per artist) using manual binary construction.
                              If False (default), creates a single TPE1 frame with multiple values using mid3v2.
            version: ID3v2 version to use (e.g., "2.3", "2.4")
            separator: Separator to use between values when in_separate_frames=False. If None, uses default behavior
                      (semicolon for ID3v2.3, null byte for ID3v2.4). Use ";" for semicolon, " / " for slash, "\x00" for null byte.
        """
        ID3v2MetadataSetter._set_multiple_metadata_values(file_path, "TPE1", artists, in_separate_frames, version, separator)
    
    @staticmethod
    def set_genres(file_path: Path, genres: List[str], in_separate_frames: bool = False, version: str = "2.4"):
        """Set ID3v2 multiple genres using external mid3v2 tool or manual frame creation.
        
        Args:
            file_path: Path to the audio file
            genres: List of genre strings to set
            in_separate_frames: If True, creates multiple separate TCON frames (one per genre) using manual binary construction.
                              If False (default), creates a single TCON frame with multiple values using mid3v2.
            version: ID3v2 version to use (e.g., "2.3", "2.4")
        """
        ID3v2MetadataSetter._set_multiple_metadata_values(file_path, "TCON", genres, in_separate_frames, version)
    
    @staticmethod
    def set_album_artists(file_path: Path, album_artists: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple album artists using external mid3v2 tool or manual frame creation.
        
        Args:
            file_path: Path to the audio file
            album_artists: List of album artist strings to set
            in_separate_frames: If True, creates multiple separate TPE2 frames (one per album artist) using manual binary construction.
                              If False (default), creates a single TPE2 frame with multiple values using mid3v2.
        """
        ID3v2MetadataSetter._set_multiple_metadata_values(file_path, "TPE2", album_artists, in_separate_frames)
    
    @staticmethod
    def set_composers(file_path: Path, composers: List[str], in_separate_frames: bool = False, version: str = "2.4"):
        """Set ID3v2 multiple composers using external mid3v2 tool or manual frame creation.
        
        Args:
            file_path: Path to the audio file
            composers: List of composer strings to set
            in_separate_frames: If True, creates multiple separate TCOM frames (one per composer) using manual binary construction.
                              If False (default), creates a single TCOM frame with multiple values using mid3v2.
            version: ID3v2 version to use (e.g., "2.3", "2.4")
        """
        ID3v2MetadataSetter._set_multiple_metadata_values(file_path, "TCOM", composers, in_separate_frames, version)
    
    @staticmethod
    def set_comments(file_path: Path, comments: List[str], in_separate_frames: bool = False):
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
    def _create_multiple_id3v2_frames(file_path: Path, frame_id: str, texts: List[str], version: str = "2.4") -> None:
        """Create multiple separate ID3v2 frames using manual binary construction.
        
        This uses the ManualID3v2FrameCreator to bypass standard tools that 
        consolidate multiple frames of the same type, allowing creation of 
        truly separate frames for testing purposes.
        
        Args:
            file_path: Path to the audio file
            frame_id: The ID3v2 frame identifier (e.g., 'TPE1', 'TPE2', 'TCON', 'TCOM')
            texts: List of text values, one per frame
            version: ID3v2 version to use (e.g., "2.3", "2.4")
        """
        from .id3v2_frame_manual_creator import ManualID3v2FrameCreator
        
        # Create frames based on the frame type
        if frame_id == 'TPE1':
            ManualID3v2FrameCreator.create_multiple_tpe1_frames(file_path, texts, version)
        elif frame_id == 'TPE2':
            ManualID3v2FrameCreator.create_multiple_tpe2_frames(file_path, texts, version)
        elif frame_id == 'TCON':
            ManualID3v2FrameCreator.create_multiple_tcon_frames(file_path, texts, version)
        elif frame_id == 'TCOM':
            ManualID3v2FrameCreator.create_multiple_tcom_frames(file_path, texts, version)
        else:
            # Generic frame creation for other frame types (including TIT2)
            creator = ManualID3v2FrameCreator()
            frames = []
            for text in texts:
                frame_data = creator._create_text_frame(frame_id, text, version)
                frames.append(frame_data)
            creator._write_id3v2_tag(file_path, frames, version)
    
    @staticmethod
    def _set_single_frame_with_mid3v2(file_path: Path, frame_id: str, alist: List[str], version: str, separator: str = None) -> None:
        """Internal helper: Create a single ID3v2 frame using appropriate method based on version.
        
        For ID3v2.4, uses manual binary construction to handle null bytes in data.
        For ID3v2.3, uses external id3v2 tool.
        
        Args:
            file_path: Path to the audio file
            frame_id: The ID3v2 frame identifier (e.g., 'TPE1', 'TCON', 'TCOM', 'TIT2')
            alist: List of text values for the frame
            version: ID3v2 version to use (e.g., "2.3", "2.4")
            separator: Separator to use between values. If None, uses default.
        """
        # Determine separator if not provided
        if separator is None:
            separator = ";" if version == "2.3" else "\x00"
        
        # Combine values with the appropriate separator
        combined_text = separator.join(alist) if len(alist) > 1 else alist[0] if alist else ""
        
        if version == "2.4":
            # Use manual binary construction to handle null bytes in data
            from .id3v2_frame_manual_creator import ManualID3v2FrameCreator
            creator = ManualID3v2FrameCreator()
            frame_data = creator._create_text_frame(frame_id, combined_text, version)
            creator._write_id3v2_tag(file_path, [frame_data], version)
        else:
            # Use external tool for 2.3
            # Map frame IDs to tool flags
            flag_mapping = {
                'TCON': '--genre',
                'TIT2': '--song',
                'TPE1': '--artist',
                'TALB': '--album',
                'TDRC': '--year',
                'TRCK': '--track',
                'COMM': '--comment'
            }
            
            flag = flag_mapping.get(frame_id, f'--{frame_id.lower()}')
            
            command = ["id3v2", "--id3v2-only", flag, combined_text, str(file_path)]
            tool = "id3v2"
            
            run_external_tool(command, tool)