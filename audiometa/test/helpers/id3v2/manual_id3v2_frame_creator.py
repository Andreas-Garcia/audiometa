#!/usr/bin/env python3
"""
Manual implementation to create multiple separate ID3v2 frames for testing.

This bypasses standard tools and libraries that automatically consolidate frames,
allowing creation of test files with truly separate TPE1, TPE2, TCON etc. frames.
"""

import struct
import tempfile
import subprocess
from pathlib import Path
from typing import List


class ManualID3v2FrameCreator:
    """Creates ID3v2 tags with multiple separate frames by manual binary construction."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        
    def create_multiple_tpe1_frames(self, artists: List[str]) -> None:
        """Create multiple separate TPE1 frames (one per artist)."""
        frames = []
        for artist in artists:
            frame_data = self._create_text_frame('TPE1', artist)
            frames.append(frame_data)
        
        self._write_id3v2_tag(frames)
    
    def create_multiple_tpe2_frames(self, album_artists: List[str]) -> None:
        """Create multiple separate TPE2 frames (one per album artist)."""
        frames = []
        for album_artist in album_artists:
            frame_data = self._create_text_frame('TPE2', album_artist)
            frames.append(frame_data)
        
        self._write_id3v2_tag(frames)
    
    def create_multiple_tcon_frames(self, genres: List[str]) -> None:
        """Create multiple separate TCON frames (one per genre)."""
        frames = []
        for genre in genres:
            frame_data = self._create_text_frame('TCON', genre)
            frames.append(frame_data)
        
        self._write_id3v2_tag(frames)
    
    def create_multiple_tcom_frames(self, composers: List[str]) -> None:
        """Create multiple separate TCOM frames (one per composer)."""
        frames = []
        for composer in composers:
            frame_data = self._create_text_frame('TCOM', composer)
            frames.append(frame_data)
        
        self._write_id3v2_tag(frames)
    
    def create_mixed_multiple_frames(self, artists: List[str], genres: List[str]) -> None:
        """Create multiple frames of different types."""
        frames = []
        
        # Add multiple TPE1 frames
        for artist in artists:
            frame_data = self._create_text_frame('TPE1', artist)
            frames.append(frame_data)
        
        # Add multiple TCON frames
        for genre in genres:
            frame_data = self._create_text_frame('TCON', genre)
            frames.append(frame_data)
        
        self._write_id3v2_tag(frames)
    
    def _create_text_frame(self, frame_id: str, text: str) -> bytes:
        """Create a single ID3v2.4 text frame with the given ID and text."""
        # Text encoding: 3 = UTF-8
        encoding = 3
        
        # Frame data: encoding byte + UTF-8 text + null terminator
        text_bytes = text.encode('utf-8')
        frame_data = struct.pack('B', encoding) + text_bytes + b'\x00'
        
        # Frame header: ID (4 bytes) + size (4 bytes) + flags (2 bytes)
        frame_id_bytes = frame_id.encode('ascii')
        frame_size = len(frame_data)
        frame_flags = 0x0000  # No flags
        
        frame_header = (
            frame_id_bytes +
            struct.pack('>I', frame_size) +  # Big-endian 32-bit size
            struct.pack('>H', frame_flags)   # Big-endian 16-bit flags
        )
        
        return frame_header + frame_data
    
    def _synchsafe_int(self, value: int) -> bytes:
        """Convert integer to ID3v2 synchsafe integer (7 bits per byte)."""
        # Split into 7-bit chunks, most significant first
        result = []
        for i in range(4):
            result.insert(0, value & 0x7f)
            value >>= 7
        return struct.pack('4B', *result)
    
    def _write_id3v2_tag(self, frames: List[bytes]) -> None:
        """Write ID3v2.4 tag with the given frames to the file."""
        # Calculate total size of all frames
        frames_data = b''.join(frames)
        tag_size = len(frames_data)
        
        # ID3v2.4 header: "ID3" + version + flags + size
        header = (
            b'ID3' +                           # ID3 identifier
            struct.pack('BB', 4, 0) +          # Version 2.4.0
            struct.pack('B', 0) +              # Flags (no unsynchronisation, etc.)
            self._synchsafe_int(tag_size)      # Size as synchsafe integer
        )
        
        # Read existing file content (audio data)
        with open(self.file_path, 'rb') as f:
            original_data = f.read()
        
        # Remove any existing ID3v2 tag
        audio_data = original_data
        if original_data.startswith(b'ID3'):
            # Skip existing ID3v2 tag
            if len(original_data) >= 10:
                # Extract size from existing tag
                size_bytes = original_data[6:10]
                existing_tag_size = 0
                for byte in size_bytes:
                    existing_tag_size = (existing_tag_size << 7) | (byte & 0x7f)
                
                # Audio data starts after header (10 bytes) + tag size
                audio_data = original_data[10 + existing_tag_size:]
        
        # Write new file with our custom ID3v2 tag
        with open(self.file_path, 'wb') as f:
            f.write(header)
            f.write(frames_data)
            f.write(audio_data)


def test_manual_multiple_frames():
    """Test the manual frame creation."""
    # Create a temporary MP3 file
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    try:
        # Create minimal MP3 file
        subprocess.run([
            'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=duration=1',
            '-acodec', 'mp3', '-y', str(tmp_path)
        ], check=True, capture_output=True)
        
        print(f"Testing manual multiple frame creation on {tmp_path}")
        
        # Create manual frame creator
        creator = ManualID3v2FrameCreator(tmp_path)
        
        # Test 1: Multiple TPE1 frames
        print("\n=== Test 1: Multiple TPE1 frames ===")
        artists = ["Artist One", "Artist Two", "Artist Three"]
        creator.create_multiple_tpe1_frames(artists)
        
        # Check result with mid3v2
        result = subprocess.run(['mid3v2', '-l', str(tmp_path)], capture_output=True, text=True)
        print("Result after manual multiple TPE1 frames:")
        print(result.stdout)
        
        # Count TPE1 occurrences
        tpe1_count = result.stdout.count("TPE1=")
        print(f"Number of TPE1 frames detected: {tpe1_count}")
        
        if tpe1_count > 1:
            print("✅ SUCCESS: Multiple separate TPE1 frames created!")
        else:
            print("❌ Only one TPE1 frame detected")
        
        # Test 2: Multiple TCON frames  
        print("\n=== Test 2: Multiple TCON frames ===")
        genres = ["Rock", "Pop", "Alternative"]
        creator.create_multiple_tcon_frames(genres)
        
        result = subprocess.run(['mid3v2', '-l', str(tmp_path)], capture_output=True, text=True)
        print("Result after manual multiple TCON frames:")
        print(result.stdout)
        
        tcon_count = result.stdout.count("TCON=")
        print(f"Number of TCON frames detected: {tcon_count}")
        
        # Test 3: Mixed multiple frames
        print("\n=== Test 3: Mixed multiple frames ===")
        creator.create_mixed_multiple_frames(
            artists=["Artist A", "Artist B"], 
            genres=["Genre X", "Genre Y"]
        )
        
        result = subprocess.run(['mid3v2', '-l', str(tmp_path)], capture_output=True, text=True)
        print("Result after mixed multiple frames:")
        print(result.stdout)
        
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


if __name__ == "__main__":
    test_manual_multiple_frames()