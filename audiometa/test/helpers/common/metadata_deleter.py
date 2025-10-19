"""Abstract base class for metadata deletion operations."""

from abc import ABC, abstractmethod
from pathlib import Path


class MetadataDeleter(ABC):
    """Abstract base class for format-specific metadata deletion operations.
    
    This class defines the standard interface for deleting metadata fields
    from audio files. Each metadata format (ID3v2, Vorbis, RIFF) should
    implement this interface with format-specific deletion logic.
    """
    
    def __init__(self, file_path: Path):
        """Initialize the deleter with a file path.
        
        Args:
            file_path: Path to the audio file
        """
        self.file_path = file_path
    
    @abstractmethod
    def delete_comment(self) -> None:
        """Delete comment metadata field."""
        pass
    
    @abstractmethod
    def delete_title(self) -> None:
        """Delete title metadata field."""
        pass
    
    @abstractmethod
    def delete_artist(self) -> None:
        """Delete artist metadata field."""
        pass
    
    @abstractmethod
    def delete_album(self) -> None:
        """Delete album metadata field."""
        pass
    
    @abstractmethod
    def delete_genre(self) -> None:
        """Delete genre metadata field."""
        pass
    
    def delete_lyrics(self) -> None:
        """Delete lyrics metadata field.
        
        Default implementation that can be overridden by subclasses
        that support lyrics.
        """
        raise NotImplementedError(f"Lyrics deletion not supported for {self.__class__.__name__}")
    
    def delete_language(self) -> None:
        """Delete language metadata field.
        
        Default implementation that can be overridden by subclasses
        that support language.
        """
        raise NotImplementedError(f"Language deletion not supported for {self.__class__.__name__}")
    
    def delete_bpm(self) -> None:
        """Delete BPM metadata field.
        
        Default implementation that can be overridden by subclasses
        that support BPM.
        """
        raise NotImplementedError(f"BPM deletion not supported for {self.__class__.__name__}")