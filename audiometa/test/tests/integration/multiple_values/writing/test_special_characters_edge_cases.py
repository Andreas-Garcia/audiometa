from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestSpecialCharactersEdgeCases:
    def test_write_unicode_characters(self, temp_audio_file: Path):
        # Write metadata with Unicode characters
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["François", "José", "Müller", "北京"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 4
        assert "François" in artists
        assert "José" in artists
        assert "Müller" in artists
        assert "北京" in artists

    def test_write_special_punctuation(self, temp_audio_file: Path):
        # Write metadata with special punctuation
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist & Co.", "Band (feat. Singer)", "Group - The Band"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist & Co." in artists
        assert "Band (feat. Singer)" in artists
        assert "Group - The Band" in artists

    def test_write_quotes_and_apostrophes(self, temp_audio_file: Path):
        # Write metadata with quotes and apostrophes
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist's Band", "The \"Quoted\" Band", "It's a Band"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist's Band" in artists
        assert "The \"Quoted\" Band" in artists
        assert "It's a Band" in artists

    def test_write_control_characters(self, temp_audio_file: Path):
        # Write metadata with control characters
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist\twith\ttabs", "Band\nwith\nnewlines", "Group\rwith\rcarriage"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist\twith\ttabs" in artists
        assert "Band\nwith\nnewlines" in artists
        assert "Group\rwith\rcarriage" in artists

    def test_write_very_long_strings(self, temp_audio_file: Path):
        # Write metadata with very long strings
        long_string = "A" * 1000
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [long_string, "Short Artist"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert long_string in artists
        assert "Short Artist" in artists

    def test_write_mixed_encodings(self, temp_audio_file: Path):
        # Write metadata with mixed character encodings
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["ASCII Artist", "Français", "Русский", "العربية", "中文"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 5
        assert "ASCII Artist" in artists
        assert "Français" in artists
        assert "Русский" in artists
        assert "العربية" in artists
        assert "中文" in artists

    def test_write_special_separator_characters(self, temp_audio_file: Path):
        # Write metadata with characters that might be used as separators
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist; with; semicolons", "Band, with, commas", "Group|with|pipes"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist; with; semicolons" in artists
        assert "Band, with, commas" in artists
        assert "Group|with|pipes" in artists

    def test_write_html_xml_characters(self, temp_audio_file: Path):
        # Write metadata with HTML/XML-like characters
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist <tag>", "Band &amp; Co.", "Group &lt;test&gt;"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist <tag>" in artists
        assert "Band &amp; Co." in artists
        assert "Group &lt;test&gt;" in artists

    def test_write_emoji_characters(self, temp_audio_file: Path):
        # Write metadata with emoji characters
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 🎵", "Band 🎸", "Group 🎤"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist 🎵" in artists
        assert "Band 🎸" in artists
        assert "Group 🎤" in artists

    def test_write_null_bytes(self, temp_audio_file: Path):
        # Write metadata with null bytes (should be handled gracefully)
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist\x00with\x00nulls", "Normal Artist"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Normal Artist" in artists
        # The null bytes might be stripped or handled differently by the format

    def test_write_mixed_special_characters(self, temp_audio_file: Path):
        # Write metadata with a mix of special characters
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [
                "François & Co. (feat. Müller) 🎵",
                "The \"Quoted\" Band - Special Characters",
                "Artist with\nnewlines\tand\ttabs"
            ]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "François & Co. (feat. Müller) 🎵" in artists
        assert "The \"Quoted\" Band - Special Characters" in artists
        assert "Artist with\nnewlines\tand\ttabs" in artists
