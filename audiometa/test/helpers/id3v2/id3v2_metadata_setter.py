"""ID3v2 and ID3v1 metadata setting operations."""

from pathlib import Path
from typing import List, Dict, Any
from ..id3v1.id3v1_metadata_setter import ID3v1MetadataSetter
from ..common.external_tool_runner import run_external_tool


class ID3v2MetadataSetter:
    """Static utility class for ID3v2 metadata setting using external tools."""
    
    @staticmethod
    def set_metadata(file_path: Path, metadata: Dict[str, Any], version: str = None) -> None:
        """Set MP3 metadata with optional ID3v2 version specification.
        
        Args:
            file_path: Path to the MP3 file
            metadata: Dictionary of metadata to set
            version: Optional ID3v2 version ("2.3" or "2.4"). If None, uses mid3v2 default.
        """
        if version:
            # Use mutagen for version-specific creation
            from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, COMM, TRCK
            from mutagen.id3._util import ID3NoHeaderError
            
            # Map metadata keys to mutagen frame classes
            frame_mapping = {
                'title': TIT2,
                'artist': TPE1,
                'album': TALB,
                'year': TDRC,
                'genre': TCON,
                'track': TRCK
            }
            
            try:
                # Load existing ID3 tag or create new one
                id3 = ID3(file_path)
            except ID3NoHeaderError:
                id3 = ID3()
            
            # Set version
            version_tuple = (2, 3, 0) if version == "2.3" else (2, 4, 0)
            id3.version = version_tuple
            
            # Clear existing frames that we'll be setting
            for key in metadata.keys():
                if key.lower() in frame_mapping:
                    frame_class = frame_mapping[key.lower()]
                    frame_id = frame_class._framespec[0].name if hasattr(frame_class, '_framespec') else frame_class.__name__
                    if hasattr(id3, 'delall'):
                        id3.delall(frame_id)
            
            # Set encoding based on version
            encoding = 1 if version == "2.3" else 3  # UTF-16 for 2.3, UTF-8 for 2.4
            
            # Add metadata frames
            for key, value in metadata.items():
                if key.lower() in frame_mapping:
                    frame_class = frame_mapping[key.lower()]
                    if key.lower() == 'comment':
                        # Comments need special handling
                        id3.add(COMM(encoding=encoding, lang='eng', desc='', text=str(value)))
                    else:
                        id3.add(frame_class(encoding=encoding, text=str(value)))
            
            # Save with specified version
            version_major = 3 if version == "2.3" else 4
            id3.save(file_path, v2_version=version_major)
        else:
            # Use mid3v2 for default behavior
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
    def set_titles(file_path: Path, titles: List[str], in_separate_frames: bool = False, version: str = "2.4"):
        """Set ID3v2 multiple titles using external mid3v2 tool or manual frame creation.
        
        Args:
            file_path: Path to the audio file
            titles: List of title strings to set
            in_separate_frames: If True, creates multiple separate TIT2 frames (one per title) using manual binary construction.
                              If False (default), creates a single TIT2 frame with multiple values using mid3v2.
            version: ID3v2 version to use (e.g., "2.3", "2.4")
        """
        from .id3v2_metadata_deleter import ID3v2MetadataDeleter
        
        # Delete existing TIT2 tags
        ID3v2MetadataDeleter.delete_frame(file_path, "TIT2")
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate TIT2 frames
            ID3v2MetadataSetter._create_multiple_id3v2_frames(file_path, 'TIT2', titles, version)
        else:
            # For version-specific creation, use mutagen directly for proper version handling
            if version == "2.3":
                # Create a single frame with all titles as one value using mutagen
                combined_titles = ';'.join(titles) if len(titles) > 1 else titles[0] if titles else ""
                ID3v2MetadataSetter._set_single_frame_with_mutagen(file_path, 'TIT2', combined_titles, version)
            else:
                # Set all titles in a single command (creates one frame with multiple values)
                ID3v2MetadataSetter.set_multiple_values_single_frame(file_path, "TIT2", titles)
    
    @staticmethod
    def set_artist(file_path: Path, artist: str, version: str = "2.4") -> None:
        """Set ID3v2 artist using version-specific method."""
        if version == "2.3":
            ID3v2MetadataSetter._set_single_frame_with_mutagen(file_path, 'TPE1', artist, version)
        else:
            # For ID3v2.4, use mutagen to ensure proper version
            ID3v2MetadataSetter._set_single_frame_with_mutagen(file_path, 'TPE1', artist, "2.4")
    
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
    def set_multiple_values_single_frame(file_path: Path, frame_id: str, values: List[str]) -> None:
        """Set multiple values in a single ID3v2 frame using mid3v2."""
        command = ["mid3v2"]
        for value in values:
            command.extend([f"--{frame_id}", value])
        command.append(str(file_path))
        run_external_tool(command, "mid3v2")
    
    @staticmethod
    def set_artists(file_path: Path, artists: List[str], in_separate_frames: bool = False, version: str = "2.4"):
        """Set ID3v2 multiple artists using external mid3v2 tool or manual frame creation.
        
        Args:
            file_path: Path to the audio file
            artists: List of artist strings to set
            in_separate_frames: If True, creates multiple separate TPE1 frames (one per artist) using manual binary construction.
                              If False (default), creates a single TPE1 frame with multiple values using mid3v2.
            version: ID3v2 version to use (e.g., "2.3", "2.4")
        """
        from .id3v2_metadata_deleter import ID3v2MetadataDeleter
        
        # Delete existing TPE1 tags
        ID3v2MetadataDeleter.delete_frame(file_path, "TPE1")
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate TPE1 frames
            ID3v2MetadataSetter._create_multiple_id3v2_frames(file_path, 'TPE1', artists, version)
        else:
            # For version-specific creation, use mutagen directly for proper version handling
            if version == "2.3":
                # Create a single frame with all artists as one value using mutagen
                combined_artists = ';'.join(artists) if len(artists) > 1 else artists[0] if artists else ""
                ID3v2MetadataSetter._set_single_frame_with_mutagen(file_path, 'TPE1', combined_artists, version)
            else:
                # Set all artists in a single command (creates one frame with multiple values)
                ID3v2MetadataSetter.set_multiple_values_single_frame(file_path, "TPE1", artists)
    
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
        from .id3v2_metadata_deleter import ID3v2MetadataDeleter
        
        # Delete existing TCON tags
        ID3v2MetadataDeleter.delete_frame(file_path, "TCON")
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate TCON frames
            ID3v2MetadataSetter._create_multiple_id3v2_frames(file_path, 'TCON', genres, version)
        else:
            # For version-specific creation, use mutagen directly for proper version handling
            if version == "2.3":
                # Create a single frame with all genres as one value using mutagen
                combined_genres = ';'.join(genres) if len(genres) > 1 else genres[0] if genres else ""
                ID3v2MetadataSetter._set_single_frame_with_mutagen(file_path, 'TCON', combined_genres, version)
            else:
                # Set all genres in a single command (creates one frame with multiple values)
                ID3v2MetadataSetter.set_multiple_values_single_frame(file_path, "TCON", genres)
    
    @staticmethod
    def set_album_artists(file_path: Path, album_artists: List[str], in_separate_frames: bool = False):
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
            ID3v2MetadataSetter.set_multiple_values_single_frame(file_path, "TPE2", album_artists)
    
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
        from .id3v2_metadata_deleter import ID3v2MetadataDeleter
        
        # Delete existing TCOM tags
        ID3v2MetadataDeleter.delete_frame(file_path, "TCOM")
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate TCOM frames
            ID3v2MetadataSetter._create_multiple_id3v2_frames(file_path, 'TCOM', composers, version)
        else:
            # For version-specific creation, use mutagen directly for proper version handling
            if version == "2.3":
                # Create a single frame with all composers as one value using mutagen
                combined_composers = ';'.join(composers) if len(composers) > 1 else composers[0] if composers else ""
                ID3v2MetadataSetter._set_single_frame_with_mutagen(file_path, 'TCOM', combined_composers, version)
            else:
                # Set all composers in a single command (creates one frame with multiple values)
                ID3v2MetadataSetter.set_multiple_values_single_frame(file_path, "TCOM", composers)
    
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
    def _set_single_frame_with_mutagen(file_path: Path, frame_id: str, text: str, version: str) -> None:
        """Create a single ID3v2 frame with specified version using mutagen library.
        
        This provides proper version handling for ID3v2.3 vs ID3v2.4 without
        the complexity of manual binary construction when only one frame is needed.
        
        Args:
            file_path: Path to the audio file
            frame_id: The ID3v2 frame identifier (e.g., 'TPE1', 'TCON', 'TCOM', 'TIT2')
            text: Text value for the frame
            version: ID3v2 version to use (e.g., "2.3", "2.4")
        """
        from mutagen.id3 import ID3, TPE1, TPE2, TCON, TCOM, TIT2
        from mutagen.id3._util import ID3NoHeaderError
        
        # Map frame IDs to mutagen classes
        frame_classes = {
            'TPE1': TPE1,
            'TPE2': TPE2, 
            'TCON': TCON,
            'TCOM': TCOM,
            'TIT2': TIT2
        }
        
        if frame_id not in frame_classes:
            raise ValueError(f"Unsupported frame ID: {frame_id}")
        
        try:
            # Load existing ID3 tag or create new one
            id3 = ID3(file_path)
        except ID3NoHeaderError:
            id3 = ID3()
        
        # Set version
        version_tuple = (2, 3, 0) if version == "2.3" else (2, 4, 0)
        id3.version = version_tuple
        
        # Remove existing frames of this type
        id3.delall(frame_id)
        
        # Add new frame with proper encoding
        frame_class = frame_classes[frame_id]
        encoding = 1 if version == "2.3" else 3  # UTF-16 for 2.3, UTF-8 for 2.4
        id3.add(frame_class(encoding=encoding, text=text))
        
        # Save with specified version
        version_major = 3 if version == "2.3" else 4
        id3.save(file_path, v2_version=version_major)