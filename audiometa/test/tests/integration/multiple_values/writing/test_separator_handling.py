from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestSeparatorHandling:
    def test_write_artists_with_semicolon_separators(self, temp_audio_file: Path):
        # Write artists that contain semicolon separators
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist; with; semicolons", "Another; Artist; with; semicolons"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist; with; semicolons" in artists
        assert "Another; Artist; with; semicolons" in artists

    def test_write_artists_with_comma_separators(self, temp_audio_file: Path):
        # Write artists that contain comma separators
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist, with, commas", "Another, Artist, with, commas"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist, with, commas" in artists
        assert "Another, Artist, with, commas" in artists

    def test_write_artists_with_pipe_separators(self, temp_audio_file: Path):
        # Write artists that contain pipe separators
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist | with | pipes", "Another | Artist | with | pipes"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist | with | pipes" in artists
        assert "Another | Artist | with | pipes" in artists

    def test_write_artists_with_slash_separators(self, temp_audio_file: Path):
        # Write artists that contain slash separators
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist / with / slashes", "Another / Artist / with / slashes"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist / with / slashes" in artists
        assert "Another / Artist / with / slashes" in artists

    def test_write_artists_with_backslash_separators(self, temp_audio_file: Path):
        # Write artists that contain backslash separators
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist \\ with \\ backslashes", "Another \\ Artist \\ with \\ backslashes"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist \\ with \\ backslashes" in artists
        assert "Another \\ Artist \\ with \\ backslashes" in artists

    def test_write_artists_with_mixed_separators(self, temp_audio_file: Path):
        # Write artists with mixed separator characters
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [
                "Artist; with, mixed | separators / and \\ slashes",
                "Another; Artist, with | mixed / separators \\ and \\ more"
            ]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist; with, mixed | separators / and \\ slashes" in artists
        assert "Another; Artist, with | mixed / separators \\ and \\ more" in artists

    def test_write_involved_people_with_separators(self, temp_audio_file: Path):
        # Write involved people with separator characters in their roles
        metadata = {
            UnifiedMetadataKey.INVOLVED_PEOPLE: [
                "Producer; Mixing: John Doe",
                "Engineer, Recording: Jane Smith",
                "Mastering | Engineer: Bob Johnson"
            ]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        involved_people = unified_metadata.get(UnifiedMetadataKey.INVOLVED_PEOPLE)
        
        assert isinstance(involved_people, list)
        assert len(involved_people) == 3
        assert "Producer; Mixing: John Doe" in involved_people
        assert "Engineer, Recording: Jane Smith" in involved_people
        assert "Mastering | Engineer: Bob Johnson" in involved_people

    def test_write_musicians_with_separators(self, temp_audio_file: Path):
        # Write musicians with separator characters in their descriptions
        metadata = {
            UnifiedMetadataKey.MUSICIANS: [
                "Guitar; Lead: Alice",
                "Bass, Electric: Bob",
                "Drums | Acoustic: Charlie",
                "Vocals / Backing: Diana"
            ]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        musicians = unified_metadata.get(UnifiedMetadataKey.MUSICIANS)
        
        assert isinstance(musicians, list)
        assert len(musicians) == 4
        assert "Guitar; Lead: Alice" in musicians
        assert "Bass, Electric: Bob" in musicians
        assert "Drums | Acoustic: Charlie" in musicians
        assert "Vocals / Backing: Diana" in musicians

    def test_write_keywords_with_separators(self, temp_audio_file: Path):
        # Write keywords with separator characters
        metadata = {
            UnifiedMetadataKey.KEYWORDS: [
                "rock; alternative",
                "indie, pop",
                "electronic | ambient",
                "jazz / fusion"
            ]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        keywords = unified_metadata.get(UnifiedMetadataKey.KEYWORDS)
        
        assert isinstance(keywords, list)
        assert len(keywords) == 4
        assert "rock; alternative" in keywords
        assert "indie, pop" in keywords
        assert "electronic | ambient" in keywords
        assert "jazz / fusion" in keywords

    def test_write_composers_with_separators(self, temp_audio_file: Path):
        # Write composers with separator characters
        metadata = {
            UnifiedMetadataKey.COMPOSER: [
                "Composer; Arranger: John Doe",
                "Composer, Lyricist: Jane Smith",
                "Composer | Producer: Bob Johnson"
            ]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
        
        assert isinstance(composers, list)
        assert len(composers) == 3
        assert "Composer; Arranger: John Doe" in composers
        assert "Composer, Lyricist: Jane Smith" in composers
        assert "Composer | Producer: Bob Johnson" in composers

    def test_write_album_artists_with_separators(self, temp_audio_file: Path):
        # Write album artists with separator characters
        metadata = {
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: [
                "Album Artist; Collective",
                "Various, Artists",
                "Compilation | Artists"
            ]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        album_artists = unified_metadata.get(UnifiedMetadataKey.ALBUM_ARTISTS_NAMES)
        
        assert isinstance(album_artists, list)
        assert len(album_artists) == 3
        assert "Album Artist; Collective" in album_artists
        assert "Various, Artists" in album_artists
        assert "Compilation | Artists" in album_artists

    def test_write_mixed_fields_with_separators(self, temp_audio_file: Path):
        # Write multiple fields with separator characters
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist; with; semicolons", "Another, Artist, with, commas"],
            UnifiedMetadataKey.COMPOSER: ["Composer | with | pipes", "Another / Composer / with / slashes"],
            UnifiedMetadataKey.INVOLVED_PEOPLE: ["Producer; Mixing: John", "Engineer, Recording: Jane"],
            UnifiedMetadataKey.KEYWORDS: ["rock; alternative", "indie, pop", "electronic | ambient"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        
        # Check each field
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist; with; semicolons" in artists
        assert "Another, Artist, with, commas" in artists
        
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
        assert isinstance(composers, list)
        assert len(composers) == 2
        assert "Composer | with | pipes" in composers
        assert "Another / Composer / with / slashes" in composers
        
        involved_people = unified_metadata.get(UnifiedMetadataKey.INVOLVED_PEOPLE)
        assert isinstance(involved_people, list)
        assert len(involved_people) == 2
        assert "Producer; Mixing: John" in involved_people
        assert "Engineer, Recording: Jane" in involved_people
        
        keywords = unified_metadata.get(UnifiedMetadataKey.KEYWORDS)
        assert isinstance(keywords, list)
        assert len(keywords) == 3
        assert "rock; alternative" in keywords
        assert "indie, pop" in keywords
        assert "electronic | ambient" in keywords
