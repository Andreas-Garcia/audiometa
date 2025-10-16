from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestMultipleEntriesRiff:
    def test_write_multiple_artists(self, temp_audio_file: Path):
        # Write multiple artists using update_file_metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Artist Three"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.RIFF)
        
        # Read back using unified function
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist One" in artists
        assert "Artist Two" in artists
        assert "Artist Three" in artists

    def test_write_multiple_artists_riff_specific(self, temp_audio_file: Path):
        # Write multiple artists to RIFF format specifically
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Primary Artist", "Secondary Artist", "Featured Artist"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.RIFF)
        
        # Read back using RIFF specific function
        riff_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.RIFF)
        artists = riff_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Primary Artist" in artists
        assert "Secondary Artist" in artists
        assert "Featured Artist" in artists

    def test_write_multiple_album_artists(self, temp_audio_file: Path):
        # Write multiple album artists
        metadata = {
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: ["Album Artist One", "Album Artist Two"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.RIFF)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        album_artists = unified_metadata.get(UnifiedMetadataKey.ALBUM_ARTISTS_NAMES)
        
        assert isinstance(album_artists, list)
        assert len(album_artists) == 2
        assert "Album Artist One" in album_artists
        assert "Album Artist Two" in album_artists

    def test_write_multiple_composers(self, temp_audio_file: Path):
        # Write multiple composers
        metadata = {
            UnifiedMetadataKey.COMPOSER: ["Composer A", "Composer B", "Composer C"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.RIFF)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
        
        assert isinstance(composers, list)
        assert len(composers) == 3
        assert "Composer A" in composers
        assert "Composer B" in composers
        assert "Composer C" in composers

    def test_write_multiple_involved_people(self, temp_audio_file: Path):
        # Write multiple involved people
        metadata = {
            UnifiedMetadataKey.INVOLVED_PEOPLE: ["Producer: John Doe", "Engineer: Jane Smith", "Mixer: Bob Johnson"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.RIFF)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        involved_people = unified_metadata.get(UnifiedMetadataKey.INVOLVED_PEOPLE)
        
        assert isinstance(involved_people, list)
        assert len(involved_people) == 3
        assert "Producer: John Doe" in involved_people
        assert "Engineer: Jane Smith" in involved_people
        assert "Mixer: Bob Johnson" in involved_people

    def test_write_multiple_musicians(self, temp_audio_file: Path):
        # Write multiple musicians
        metadata = {
            UnifiedMetadataKey.MUSICIANS: ["Guitar: Alice", "Bass: Bob", "Drums: Charlie", "Vocals: Diana"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.RIFF)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        musicians = unified_metadata.get(UnifiedMetadataKey.MUSICIANS)
        
        assert isinstance(musicians, list)
        assert len(musicians) == 4
        assert "Guitar: Alice" in musicians
        assert "Bass: Bob" in musicians
        assert "Drums: Charlie" in musicians
        assert "Vocals: Diana" in musicians

    def test_write_multiple_keywords(self, temp_audio_file: Path):
        # Write multiple keywords
        metadata = {
            UnifiedMetadataKey.KEYWORDS: ["rock", "alternative", "indie", "2023"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.RIFF)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        keywords = unified_metadata.get(UnifiedMetadataKey.KEYWORDS)
        
        assert isinstance(keywords, list)
        assert len(keywords) == 4
        assert "rock" in keywords
        assert "alternative" in keywords
        assert "indie" in keywords
        assert "2023" in keywords

    def test_write_mixed_single_and_multiple_values(self, temp_audio_file: Path):
        # Write a mix of single and multiple values
        metadata = {
            UnifiedMetadataKey.TITLE: "Single Title",  # Single value
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1", "Artist 2"],  # Multiple values
            UnifiedMetadataKey.ALBUM_NAME: "Single Album",  # Single value
            UnifiedMetadataKey.COMPOSER: ["Composer 1", "Composer 2", "Composer 3"]  # Multiple values
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.RIFF)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        
        # Check single values
        assert unified_metadata.get(UnifiedMetadataKey.TITLE) == "Single Title"
        assert unified_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Single Album"
        
        # Check multiple values
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist 1" in artists
        assert "Artist 2" in artists
        
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
        assert isinstance(composers, list)
        assert len(composers) == 3
        assert "Composer 1" in composers
        assert "Composer 2" in composers
        assert "Composer 3" in composers

    def test_write_empty_list_removes_field(self, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
        }
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.RIFF)
        
        # Verify it was written
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is not None
        
        # Now write empty list (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: []
        }
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.RIFF)
        
        # Verify field was removed
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_write_none_removes_field(self, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
        }
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.RIFF)
        
        # Verify it was written
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is not None
        
        # Now write None (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: None
        }
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.RIFF)
        
        # Verify field was removed
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None
