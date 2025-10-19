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
    
    def __init__(self, file_path: Path, version: str = "2.4"):
        self.file_path = file_path
        if version not in ["2.3", "2.4"]:
            raise ValueError("Version must be '2.3' or '2.4'")
        self.version = version
        
    def create_multiple_tpe1_frames(self, artists: List[str]) -> None:
        frames = []
        for artist in artists:
            frame_data = self._create_text_frame('TPE1', artist)
            frames.append(frame_data)
        
        self._write_id3v2_tag(frames)
    
    def create_multiple_tpe2_frames(self, album_artists: List[str]) -> None:
        frames = []
        for album_artist in album_artists:
            frame_data = self._create_text_frame('TPE2', album_artist)
            frames.append(frame_data)
        
        self._write_id3v2_tag(frames)
    
    def create_multiple_tcon_frames(self, genres: List[str]) -> None:
        frames = []
        for genre in genres:
            frame_data = self._create_text_frame('TCON', genre)
            frames.append(frame_data)
        
        self._write_id3v2_tag(frames)
    
    def create_multiple_tcom_frames(self, composers: List[str]) -> None:
        frames = []
        for composer in composers:
            frame_data = self._create_text_frame('TCOM', composer)
            frames.append(frame_data)
        
        self._write_id3v2_tag(frames)
    
    def create_mixed_multiple_frames(self, artists: List[str], genres: List[str]) -> None:
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
        """Create a single ID3v2 text frame with the given ID and text."""
        # Choose encoding based on version
        if self.version == "2.3":
            # ID3v2.3: Use ISO-8859-1 or UTF-16 (we'll use UTF-16 for broader compatibility)
            encoding = 1  # UTF-16 with BOM
            text_bytes = text.encode('utf-16')
        else:  # ID3v2.4
            # ID3v2.4: Use UTF-8
            encoding = 3
            text_bytes = text.encode('utf-8')
        
        # Frame data: encoding byte + text + null terminator
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
        """Write ID3v2 tag with the given frames to the file."""
        # Calculate total size of all frames
        frames_data = b''.join(frames)
        tag_size = len(frames_data)
        
        # Create header based on version
        if self.version == "2.3":
            # ID3v2.3 header: "ID3" + version + flags + size (regular integer)
            header = (
                b'ID3' +                           # ID3 identifier
                struct.pack('BB', 3, 0) +          # Version 2.3.0
                struct.pack('B', 0) +              # Flags (no unsynchronisation, etc.)
                struct.pack('>I', tag_size)        # Size as regular 32-bit integer
            )
        else:  # ID3v2.4
            # ID3v2.4 header: "ID3" + version + flags + size (synchsafe integer)
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
                # Extract version and size from existing tag
                existing_version = original_data[3]
                size_bytes = original_data[6:10]
                
                if existing_version == 4:
                    # ID3v2.4 uses synchsafe integers
                    existing_tag_size = 0
                    for byte in size_bytes:
                        existing_tag_size = (existing_tag_size << 7) | (byte & 0x7f)
                else:
                    # ID3v2.3 and earlier use regular integers
                    existing_tag_size = struct.unpack('>I', size_bytes)[0]
                
                # Audio data starts after header (10 bytes) + tag size
                audio_data = original_data[10 + existing_tag_size:]
        
        # Write new file with our custom ID3v2 tag
        with open(self.file_path, 'wb') as f:
            f.write(header)
            f.write(frames_data)
            f.write(audio_data)


def test_manual_multiple_frames():
    """Test the manual frame creation for both ID3v2.3 and ID3v2.4."""
    def test_version(version: str):
        """Test a specific ID3v2 version."""
        print(f"\n{'='*50}")
        print(f"TESTING ID3v{version}")
        print(f"{'='*50}")
        
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
            
            # Create manual frame creator with specified version
            creator = ManualID3v2FrameCreator(tmp_path, version)
            
            # Test 1: Multiple TPE1 frames
            print(f"\n=== Test 1: Multiple TPE1 frames (ID3v{version}) ===")
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
                print(f"✅ SUCCESS: Multiple separate TPE1 frames created in ID3v{version}!")
            else:
                print(f"❌ Only one TPE1 frame detected in ID3v{version}")
            
            # Test 2: Multiple TCON frames  
            print(f"\n=== Test 2: Multiple TCON frames (ID3v{version}) ===")
            genres = ["Rock", "Pop", "Alternative"]
            creator.create_multiple_tcon_frames(genres)
            
            result = subprocess.run(['mid3v2', '-l', str(tmp_path)], capture_output=True, text=True)
            print("Result after manual multiple TCON frames:")
            print(result.stdout)
            
            tcon_count = result.stdout.count("TCON=")
            print(f"Number of TCON frames detected: {tcon_count}")
            
            # Test 3: Mixed multiple frames
            print(f"\n=== Test 3: Mixed multiple frames (ID3v{version}) ===")
            creator.create_mixed_multiple_frames(
                artists=["Artist A", "Artist B"], 
                genres=["Genre X", "Genre Y"]
            )
            
            result = subprocess.run(['mid3v2', '-l', str(tmp_path)], capture_output=True, text=True)
            print("Result after mixed multiple frames:")
            print(result.stdout)
            
            # Check version in the file and verify multiple frames exist in binary
            result = subprocess.run(['mid3v2', '-l', str(tmp_path)], capture_output=True, text=True)
            if result.stdout:
                print(f"✅ ID3v{version} tag successfully created and readable")
                
                # Verify multiple frames exist by checking raw binary
                with open(tmp_path, 'rb') as f:
                    data = f.read(1000)  # Read first 1KB to check for multiple frame IDs
                    tpe1_count = data.count(b'TPE1')
                    tcon_count = data.count(b'TCON')
                    print(f"Raw binary analysis: {tpe1_count} TPE1 frame headers, {tcon_count} TCON frame headers")
                    
                    if tpe1_count > 1 or tcon_count > 1:
                        print("✅ SUCCESS: Multiple separate frames confirmed in binary data!")
                    else:
                        print("ℹ️  Note: mid3v2 may be consolidating frames for display")
            
        finally:
            if tmp_path.exists():
                tmp_path.unlink()
    
    # Test both versions
    test_version("2.3")
    test_version("2.4")


def create_test_file_with_version(output_path: Path, version: str = "2.4", 
                                 artists: List[str] = None, genres: List[str] = None) -> None:
    """Create a test MP3 file with multiple frames in the specified ID3v2 version."""
    if artists is None:
        artists = ["Artist One", "Artist Two", "Artist Three"]
    if genres is None:
        genres = ["Rock", "Pop", "Alternative"]
    
    # Create minimal MP3 file
    subprocess.run([
        'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=duration=1',
        '-acodec', 'mp3', '-y', str(output_path)
    ], check=True, capture_output=True)
    
    # Add multiple frames
    creator = ManualID3v2FrameCreator(output_path, version)
    creator.create_mixed_multiple_frames(artists, genres)
    
    print(f"Created test file {output_path} with ID3v{version} containing:")
    print(f"  - Artists: {artists}")
    print(f"  - Genres: {genres}")


if __name__ == "__main__":
    test_manual_multiple_frames()