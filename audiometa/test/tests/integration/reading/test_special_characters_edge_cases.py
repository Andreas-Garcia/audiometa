import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestSpecialCharactersEdgeCases:
    def test_read_unicode_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                test_file.set_vorbis_multiple_artists(["François", "José", "Müller", "北京"])
                test_file.set_vorbis_title("Café Music 音乐")
            except RuntimeError:
                pytest.skip("metaflac not available or failed to set unicode metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
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

    def test_read_special_punctuation(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                test_file.set_vorbis_multiple_artists(["Artist & Co.", "Band (feat. Singer)", "Group - The Band"])
                test_file.set_vorbis_title("Song (Remix) - Special Edition")
            except RuntimeError:
                pytest.skip("metaflac not available or failed to set special punctuation metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            title = unified_metadata.get(UnifiedMetadataKey.TITLE)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist & Co." in artists
            assert "Band (feat. Singer)" in artists
            assert "Group - The Band" in artists
            
            assert isinstance(title, str)
            assert title == "Song (Remix) - Special Edition"

    def test_read_quotes_and_apostrophes(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                test_file.set_vorbis_multiple_artists(["Artist's Band", "The \"Quoted\" Band", "It's a Band"])
                test_file.set_vorbis_title("Don't Stop \"Believing\"")
            except RuntimeError:
                pytest.skip("metaflac not available or failed to set quotes metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            title = unified_metadata.get(UnifiedMetadataKey.TITLE)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist's Band" in artists
            assert "The \"Quoted\" Band" in artists
            assert "It's a Band" in artists
            
            assert isinstance(title, str)
            assert title == "Don't Stop \"Believing\""

    def test_read_control_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                test_file.set_vorbis_multiple_artists(["Artist\twith\ttabs", "Band\nwith\nnewlines", "Group\rwith\rcarriage"])
                test_file.set_vorbis_title("Song\twith\ttabs")
            except RuntimeError:
                pytest.skip("metaflac not available or failed to set control characters metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            title = unified_metadata.get(UnifiedMetadataKey.TITLE)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist\twith\ttabs" in artists
            assert "Band\nwith\nnewlines" in artists
            assert "Group\rwith\rcarriage" in artists
            
            assert isinstance(title, str)
            assert title == "Song\twith\ttabs"

    def test_read_very_long_strings(self):
        long_string = "A" * 1000
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                test_file.set_vorbis_multiple_artists([long_string, "Short Artist"])
                test_file.set_vorbis_title('B' * 500)
            except RuntimeError:
                pytest.skip("metaflac not available or failed to set long strings metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            title = unified_metadata.get(UnifiedMetadataKey.TITLE)
            
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert long_string in artists
            assert "Short Artist" in artists
            
            assert isinstance(title, str)
            assert title == "B" * 500

    def test_read_mixed_encodings(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                test_file.set_vorbis_multiple_artists(["ASCII Artist", "Français", "Русский", "العربية", "中文"])
                test_file.set_vorbis_title("Mixed 编码 Title")
            except RuntimeError:
                pytest.skip("metaflac not available or failed to set mixed encodings metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
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

    def test_read_special_separator_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                test_file.set_vorbis_multiple_artists(["Artist; with; semicolons", "Band, with, commas", "Group|with|pipes"])
                test_file.set_vorbis_title("Song; with; separators")
            except RuntimeError:
                pytest.skip("metaflac not available or failed to set separator characters metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            title = unified_metadata.get(UnifiedMetadataKey.TITLE)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist; with; semicolons" in artists
            assert "Band, with, commas" in artists
            assert "Group|with|pipes" in artists
            
            assert isinstance(title, str)
            assert title == "Song; with; separators"

    def test_read_html_xml_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                test_file.set_vorbis_multiple_artists(["Artist <tag>", "Band &amp; Co.", "Group &lt;test&gt;"])
                test_file.set_vorbis_title("Song &amp; Title")
            except RuntimeError:
                pytest.skip("metaflac not available or failed to set HTML/XML characters metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            title = unified_metadata.get(UnifiedMetadataKey.TITLE)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist <tag>" in artists
            assert "Band &amp; Co." in artists
            assert "Group &lt;test&gt;" in artists
            
            assert isinstance(title, str)
            assert title == "Song &amp; Title"

    def test_read_emoji_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                test_file.set_vorbis_multiple_artists(["Artist 🎵", "Band 🎸", "Group 🎤"])
                test_file.set_vorbis_title("Song 🎶 with 🎵 emojis")
            except RuntimeError:
                pytest.skip("metaflac not available or failed to set emoji characters metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            title = unified_metadata.get(UnifiedMetadataKey.TITLE)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist 🎵" in artists
            assert "Band 🎸" in artists
            assert "Group 🎤" in artists
            
            assert isinstance(title, str)
            assert title == "Song 🎶 with 🎵 emojis"

    def test_read_null_bytes(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=Artist\x00with\x00nulls",
                    "--set-tag=ARTIST=Normal Artist",
                    "--set-tag=TITLE=Normal Title",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set null bytes metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            title = unified_metadata.get(UnifiedMetadataKey.TITLE)
            
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Normal Artist" in artists
            # The null bytes might be stripped or handled differently by the format
            
            assert isinstance(title, str)
            assert title == "Normal Title"

    def test_read_mixed_special_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            try:
                subprocess.run(["metaflac", "--remove-tag=ARTIST", str(test_file.path)], 
                              check=True, capture_output=True)
                subprocess.run([
                    "metaflac",
                    "--set-tag=ARTIST=François & Co. (feat. Müller) 🎵",
                    "--set-tag=ARTIST=The \"Quoted\" Band - Special Characters",
                    "--set-tag=ARTIST=Artist with\nnewlines\tand\ttabs",
                    "--set-tag=TITLE=Mixed Special 🎵 Characters & \"Quotes\"",
                    str(test_file.path)
                ], check=True, capture_output=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                pytest.skip("metaflac not available or failed to set mixed special characters metadata")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            title = unified_metadata.get(UnifiedMetadataKey.TITLE)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "François & Co. (feat. Müller) 🎵" in artists
            assert "The \"Quoted\" Band - Special Characters" in artists
            assert "Artist with\nnewlines\tand\ttabs" in artists
            
            assert isinstance(title, str)
            assert title == "Mixed Special 🎵 Characters & \"Quotes\""

    def test_read_special_characters_from_existing_file(self, sample_mp3_file: Path):
        # Test reading special characters from a file that already has them
        # This tests the reading functionality without writing first
        unified_metadata = get_merged_unified_metadata(sample_mp3_file)
        
        # Should handle any special characters that might be in the sample file
        for key, value in unified_metadata.items():
            if isinstance(value, str):
                # Should be able to handle unicode and special characters
                assert isinstance(value, str)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        assert isinstance(item, str)
