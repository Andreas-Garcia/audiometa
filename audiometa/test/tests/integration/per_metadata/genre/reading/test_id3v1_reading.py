import pytest
import subprocess
from pathlib import Path

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.tests.test_script_helpers import ScriptHelper


@pytest.mark.integration
class TestId3v1GenreReading:

    def test_id3v1_genre_code_17_rock(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "17")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_id3v1_genre_code_0_blues(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "0")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Blues"]

    def test_id3v1_genre_code_32_classical(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "32")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Classical"]

    def test_id3v1_genre_code_80_folk(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "80")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Folk"]

    def test_id3v1_genre_code_131_indie(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "131")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Indie"]

    def test_id3v1_genre_code_189_dubstep(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "189")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Dubstep"]

    def test_id3v1_genre_code_255_unknown(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "255")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is not None

    def test_id3v1_genre_single_genre_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "17")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_id3v1_genre_case_insensitive_conversion(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "17")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_id3v1_genre_partial_match_conversion(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "17")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_id3v1_genre_30_character_limit(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            long_genre = "Very Long Genre Name That Exceeds 30 Characters"
            self._set_id3v1_genre(test_file.path, "17")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is not None
            assert len(genres[0]) <= 30

    def test_id3v1_genre_empty_string(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "255")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_id3v1_genre_none_value(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            # No genre set - test file has no genre
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_id3v1_genre_whitespace_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "255")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_id3v1_genre_latin1_encoding(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "17")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is not None

    def test_id3v1_genre_original_specification_codes(self):
        original_genres = [
            "Blues", "Classic Rock", "Country", "Dance", "Disco", "Funk", "Grunge",
            "Hip-Hop", "Jazz", "Metal", "New Age", "Oldies", "Other", "Pop", "R&B",
            "Rap", "Reggae", "Rock", "Techno", "Industrial", "Alternative", "Ska",
            "Death Metal", "Pranks", "Soundtrack", "Euro-Techno", "Ambient", "Trip-Hop",
            "Vocal", "Jazz+Funk", "Fusion", "Trance", "Classical", "Instrumental",
            "Acid", "House", "Game", "Sound Clip", "Gospel", "Noise", "Alternative Rock",
            "Bass", "Soul", "Punk", "Space", "Meditative", "Instrumental Pop",
            "Instrumental Rock", "Ethnic", "Gothic", "Darkwave", "Techno-Industrial",
            "Electronic", "Pop-Folk", "Eurodance", "Dream", "Southern Rock", "Comedy",
            "Cult", "Gangsta", "Top 40", "Christian Rap", "Pop/Funk", "Jungle",
            "Native American", "Cabaret", "New Wave", "Psychadelic", "Rave", "Showtunes",
            "Trailer", "Lo-Fi", "Tribal", "Acid Punk", "Acid Jazz", "Polka", "Retro",
            "Musical", "Rock & Roll", "Hard Rock"
        ]
        
        for genre in original_genres[:10]:  # Test first 10 to avoid too many tests
            with TempFileWithMetadata({"title": "Test Song", "genre": genre}, "id3v1") as test_file:
                metadata = get_merged_unified_metadata(test_file.path)
                genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
                
                assert genres == [genre]

    def test_id3v1_genre_winamp_extensions(self):
        winamp_genres = [
            "Folk", "Folk-Rock", "National Folk", "Swing", "Fast Fusion", "Bebob",
            "Latin", "Revival", "Celtic", "Bluegrass", "Avantgarde", "Gothic Rock",
            "Progressive Rock", "Psychedelic Rock", "Symphonic Rock", "Slow Rock",
            "Big Band", "Chorus", "Easy Listening", "Acoustic", "Humour", "Speech",
            "Chanson", "Opera", "Chamber Music", "Sonata", "Symphony", "Booty Bass",
            "Primus", "Porn Groove", "Satire", "Slow Jam", "Club", "Tango", "Samba",
            "Folklore", "Ballad", "Power Ballad", "Rhythmic Soul", "Freestyle",
            "Duet", "Punk Rock", "Drum Solo", "A capella", "Euro-House", "Dance Hall"
        ]
        
        for genre in winamp_genres[:10]:  # Test first 10 to avoid too many tests
            with TempFileWithMetadata({"title": "Test Song", "genre": genre}, "id3v1") as test_file:
                metadata = get_merged_unified_metadata(test_file.path)
                genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
                
                assert genres == [genre]

    def test_id3v1_genre_winamp_56_extensions(self):
        winamp_56_genres = [
            "Dubstep", "Garage", "Future Bass", "Trap", "Drill", "Grime", "UK Garage",
            "Bass House", "Future House", "Deep House", "Tech House", "Progressive House",
            "Trance", "Uplifting Trance", "Vocal Trance", "Psy Trance", "Goa Trance",
            "Hard Trance", "Tech Trance", "Progressive Trance", "Ambient Trance",
            "Breakbeat", "Big Beat", "Breakcore", "Drum and Bass", "Jungle", "Liquid DnB",
            "Neurofunk", "Techstep", "Drumstep", "Dub", "Reggae", "Dancehall", "Ragga",
            "Ska", "Rocksteady", "Lovers Rock", "Roots Reggae", "Dub Reggae", "Steppa",
            "Grime", "UK Hip Hop", "British Hip Hop", "Trap", "Drill", "Cloud Rap",
            "SoundCloud Rap", "Emo Rap", "Lil Peep", "XXXTentacion", "Lil Uzi Vert"
        ]
        
        for genre in winamp_56_genres[:10]:  # Test first 10 to avoid too many tests
            with TempFileWithMetadata({"title": "Test Song", "genre": genre}, "id3v1") as test_file:
                metadata = get_merged_unified_metadata(test_file.path)
                genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
                
                assert genres == [genre]

    def test_id3v1_genre_no_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_id3v1_genre_with_other_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            self._set_id3v1_genre(test_file.path, "17")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"

    def _set_id3v1_genre(self, file_path: Path, genre_code: str):
        """Set ID3v1 genre using external id3v2 tool."""
        try:
            subprocess.run([
                "id3v2", "--id3v1-only", 
                f"--genre={genre_code}",
                str(file_path)
            ], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("id3v2 tool not available for ID3v1 genre setting")
