"""ID3v2 multiple metadata manager for creating test files with specific configurations."""

from pathlib import Path
from typing import List

from .mid3v2_tool import Mid3v2Tool


class ID3v2MultipleMetadataManager:
    """Manager for setting multiple values in ID3v2 metadata."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
    
    def set_multiple_artists(self, artists: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple artists using external mid3v2 tool or manual frame creation.
        
        Args:
            artists: List of artist strings to set
            in_separate_frames: If True, creates multiple separate TPE1 frames (one per artist) using manual binary construction.
                              If False (default), creates a single TPE1 frame with multiple values using mid3v2.
        """
        # Delete existing TPE1 tags
        Mid3v2Tool.delete_frame(self.file_path, "TPE1")
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate TPE1 frames
            self._create_multiple_id3v2_frames('TPE1', artists)
        else:
            # Set all artists in a single command (creates one frame with multiple values)
            Mid3v2Tool.set_multiple_values_single_frame(self.file_path, "TPE1", artists)
    
    def set_multiple_genres(self, genres: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple genres using external mid3v2 tool or manual frame creation.
        
        Args:
            genres: List of genre strings to set
            in_separate_frames: If True, creates multiple separate TCON frames (one per genre) using manual binary construction.
                              If False (default), creates a single TCON frame with multiple values using mid3v2.
        """
        # Delete existing TCON tags
        Mid3v2Tool.delete_frame(self.file_path, "TCON")
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate TCON frames
            self._create_multiple_id3v2_frames('TCON', genres)
        else:
            # Set all genres in a single command (creates one frame with multiple values)
            Mid3v2Tool.set_multiple_values_single_frame(self.file_path, "TCON", genres)
    
    def set_multiple_album_artists(self, album_artists: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple album artists using external mid3v2 tool or manual frame creation.
        
        Args:
            album_artists: List of album artist strings to set
            in_separate_frames: If True, creates multiple separate TPE2 frames (one per album artist) using manual binary construction.
                              If False (default), creates a single TPE2 frame with multiple values using mid3v2.
        """
        # Delete existing TPE2 tags
        Mid3v2Tool.delete_frame(self.file_path, "TPE2")
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate TPE2 frames
            self._create_multiple_id3v2_frames('TPE2', album_artists)
        else:
            # Set all album artists in a single command (creates one frame with multiple values)
            Mid3v2Tool.set_multiple_values_single_frame(self.file_path, "TPE2", album_artists)
    
    def set_multiple_composers(self, composers: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple composers using external mid3v2 tool or manual frame creation.
        
        Args:
            composers: List of composer strings to set
            in_separate_frames: If True, creates multiple separate TCOM frames (one per composer) using manual binary construction.
                              If False (default), creates a single TCOM frame with multiple values using mid3v2.
        """
        # Delete existing TCOM tags
        Mid3v2Tool.delete_frame(self.file_path, "TCOM")
        
        if in_separate_frames:
            # Use manual binary construction to create truly separate TCOM frames
            self._create_multiple_id3v2_frames('TCOM', composers)
        else:
            # Set all composers in a single command (creates one frame with multiple values)
            Mid3v2Tool.set_multiple_values_single_frame(self.file_path, "TCOM", composers)
    
    def set_multiple_comments(self, comments: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple comments using external mid3v2 tool.
        
        Args:
            comments: List of comment strings to set
            in_separate_frames: If True, creates multiple separate COMM frames (one per comment).
                              If False (default), creates a single COMM frame with the first comment value.
        """
        # Delete existing COMM tags
        Mid3v2Tool.delete_frame(self.file_path, "COMM")
        
        if in_separate_frames:
            # Set each comment in a separate mid3v2 call to force multiple frames
            for comment in comments:
                command = ["mid3v2", "--comment", comment, str(self.file_path)]
                Mid3v2Tool.run_command(command)
        else:
            # Set only the first comment (ID3v2 comment fields are typically single-valued)
            if comments:
                command = ["mid3v2", "--comment", comments[0], str(self.file_path)]
                Mid3v2Tool.run_command(command)
    
    def _create_multiple_id3v2_frames(self, frame_id: str, texts: List[str]) -> None:
        """Create multiple separate ID3v2 frames using manual binary construction.
        
        This uses the ManualID3v2FrameCreator to bypass standard tools that 
        consolidate multiple frames of the same type, allowing creation of 
        truly separate frames for testing purposes.
        
        Args:
            frame_id: The ID3v2 frame identifier (e.g., 'TPE1', 'TPE2', 'TCON', 'TCOM')
            texts: List of text values, one per frame
        """
        from .manual_id3v2_frame_creator import ManualID3v2FrameCreator
        
        creator = ManualID3v2FrameCreator(self.file_path)
        
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