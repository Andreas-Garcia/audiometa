from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestSpecialCharactersEdgeCases:
    def test_write_unicode_characters(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["François", "José", "Müller", "北京"],
            UnifiedMetadataKey.TITLE: "Café Music 音乐"
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        
        assert isinstance(artists, list)
        assert len(artists) == 4
        assert "François" in artists
        assert "José" in artists
        assert "Müller" in artists
        assert "北京" in artists
        
        assert isinstance(title, str)
        assert title == "Café Music 音乐"

    def test_write_special_punctuation(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist & Co.", "Band (feat. Singer)", "Group - The Band"],
            UnifiedMetadataKey.TITLE: "Song (Remix) - Special Edition"
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist & Co." in artists
        assert "Band (feat. Singer)" in artists
        assert "Group - The Band" in artists
        
        assert isinstance(title, str)
        assert title == "Song (Remix) - Special Edition"

    def test_write_quotes_and_apostrophes(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist's Band", "The \"Quoted\" Band", "It's a Band"],
            UnifiedMetadataKey.TITLE: "Don't Stop \"Believing\""
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist's Band" in artists
        assert "The \"Quoted\" Band" in artists
        assert "It's a Band" in artists
        
        assert isinstance(title, str)
        assert title == "Don't Stop \"Believing\""

    def test_write_control_characters(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist\twith\ttabs", "Band\nwith\nnewlines", "Group\rwith\rcarriage"],
            UnifiedMetadataKey.TITLE: "Song\twith\ttabs"
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist\twith\ttabs" in artists
        assert "Band\nwith\nnewlines" in artists
        assert "Group\rwith\rcarriage" in artists
        
        assert isinstance(title, str)
        assert title == "Song\twith\ttabs"

    def test_write_very_long_strings(self, temp_audio_file: Path):
        long_string = "A" * 1000
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [long_string, "Short Artist"],
            UnifiedMetadataKey.TITLE: "B" * 500
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert long_string in artists
        assert "Short Artist" in artists
        
        assert isinstance(title, str)
        assert title == "B" * 500

    def test_write_mixed_encodings(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["ASCII Artist", "Français", "Русский", "العربية", "中文"],
            UnifiedMetadataKey.TITLE: "Mixed 编码 Title"
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        
        assert isinstance(artists, list)
        assert len(artists) == 5
        assert "ASCII Artist" in artists
        assert "Français" in artists
        assert "Русский" in artists
        assert "العربية" in artists
        assert "中文" in artists
        
        assert isinstance(title, str)
        assert title == "Mixed 编码 Title"

    def test_write_special_separator_characters(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist; with; semicolons", "Band, with, commas", "Group|with|pipes"],
            UnifiedMetadataKey.TITLE: "Song; with; separators"
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist; with; semicolons" in artists
        assert "Band, with, commas" in artists
        assert "Group|with|pipes" in artists
        
        assert isinstance(title, str)
        assert title == "Song; with; separators"

    def test_write_html_xml_characters(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist <tag>", "Band &amp; Co.", "Group &lt;test&gt;"],
            UnifiedMetadataKey.TITLE: "Song &amp; Title"
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist <tag>" in artists
        assert "Band &amp; Co." in artists
        assert "Group &lt;test&gt;" in artists
        
        assert isinstance(title, str)
        assert title == "Song &amp; Title"

    def test_write_emoji_characters(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 🎵", "Band 🎸", "Group 🎤"],
            UnifiedMetadataKey.TITLE: "Song 🎶 with 🎵 emojis"
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist 🎵" in artists
        assert "Band 🎸" in artists
        assert "Group 🎤" in artists
        
        assert isinstance(title, str)
        assert title == "Song 🎶 with 🎵 emojis"

    def test_write_null_bytes(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist\x00with\x00nulls", "Normal Artist"],
            UnifiedMetadataKey.TITLE: "Normal Title"
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Normal Artist" in artists
        # The null bytes might be stripped or handled differently by the format
        
        assert isinstance(title, str)
        assert title == "Normal Title"

    def test_write_mixed_special_characters(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [
                "François & Co. (feat. Müller) 🎵",
                "The \"Quoted\" Band - Special Characters",
                "Artist with\nnewlines\tand\ttabs"
            ],
            UnifiedMetadataKey.TITLE: "Mixed Special 🎵 Characters & \"Quotes\""
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "François & Co. (feat. Müller) 🎵" in artists
        assert "The \"Quoted\" Band - Special Characters" in artists
        assert "Artist with\nnewlines\tand\ttabs" in artists
        
        assert isinstance(title, str)
        assert title == "Mixed Special 🎵 Characters & \"Quotes\""
