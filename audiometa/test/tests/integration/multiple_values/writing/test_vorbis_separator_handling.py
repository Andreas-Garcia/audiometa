from pathlib import Path
import subprocess

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.test_helpers import TempFileWithMetadata


class TestVorbisMultipleEntriesWriting:
    def test_write_multiple_values_creates_separate_entries(self, sample_flac_file: Path):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Set up initial metadata with single entry containing separators
            subprocess.run([
                "metaflac",
                "--set-tag=ARTIST=Artist One;Artist Two;Artist Three",
                "--set-tag=COMPOSER=Composer A;Composer B",
                "--set-tag=GENRE=Rock;Alternative",
                str(test_file.path)
            ], check=True)
            
            # Verify initial state using metaflac - should show single entries with separators
            result = subprocess.run([
                "metaflac", "--list", "--block-type=VORBIS_COMMENT", str(test_file.path)
            ], capture_output=True, text=True, check=True)
            
            # Should see single entries with separators
            assert "ARTIST=Artist One;Artist Two;Artist Three" in result.stdout
            assert "COMPOSER=Composer A;Composer B" in result.stdout
            assert "GENRE=Rock;Alternative" in result.stdout
            
            # Write new multiple values - should create separate Vorbis entries
            new_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["New Artist 1", "New Artist 2", "New Artist 3"],
                UnifiedMetadataKey.COMPOSER: ["New Composer X", "New Composer Y"],
                UnifiedMetadataKey.GENRES_NAMES: ["Jazz", "Fusion", "Experimental"]
            }
            
            update_file_metadata(test_file.path, new_metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Verify final state using metaflac - should show separate entries
            result = subprocess.run([
                "metaflac", "--list", "--block-type=VORBIS_COMMENT", str(test_file.path)
            ], capture_output=True, text=True, check=True)
            
            # Should see separate ARTIST entries
            artist_lines = [line for line in result.stdout.split('\n') if 'artist=' in line]
            assert len(artist_lines) == 3
            assert "artist=New Artist 1" in result.stdout
            assert "artist=New Artist 2" in result.stdout
            assert "artist=New Artist 3" in result.stdout
            
            # Should see separate COMPOSER entries
            composer_lines = [line for line in result.stdout.split('\n') if 'composer=' in line]
            assert len(composer_lines) == 2
            assert "composer=New Composer X" in result.stdout
            assert "composer=New Composer Y" in result.stdout
            
            # Should see separate GENRE entries
            genre_lines = [line for line in result.stdout.split('\n') if 'genre=' in line]
            assert len(genre_lines) == 3
            assert "genre=Jazz" in result.stdout
            assert "genre=Fusion" in result.stdout
            assert "genre=Experimental" in result.stdout