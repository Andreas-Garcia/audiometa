import pytest
from pathlib import Path
import subprocess
import shutil
import time

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestPerformanceLargeData:
    def test_performance_with_many_entries(self, sample_flac_file: Path, temp_flac_file: Path):
        # Copy sample file to temporary location
        shutil.copy2(sample_flac_file, temp_flac_file)
        
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(temp_flac_file)], 
                          check=True, capture_output=True)
            
            artist_commands = []
            for i in range(20):
                artist_commands.extend(["--set-tag", f"ARTIST=Artist {i+1}"])
            
            subprocess.run(["metaflac"] + artist_commands + [str(temp_flac_file)], 
                          check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set many artists")
        
        for _ in range(5):
            unified_metadata = get_merged_unified_metadata(temp_flac_file)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 20

    def test_performance_with_large_separated_values(self, sample_flac_file: Path, temp_flac_file: Path):
        # Copy sample file to temporary location
        shutil.copy2(sample_flac_file, temp_flac_file)
        
        # Create a single tag with many values separated by semicolons
        many_artists = ";".join([f"Artist {i+1}" for i in range(50)])
        
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(temp_flac_file)], 
                          check=True, capture_output=True)
            
            subprocess.run([
                "metaflac",
                f"--set-tag=ARTIST={many_artists}",
                str(temp_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set many separated artists")
        
        start_time = time.time()
        unified_metadata = get_merged_unified_metadata(temp_flac_file)
        end_time = time.time()
        
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 50
        
        # Performance should be reasonable (less than 1 second for 50 artists)
        assert (end_time - start_time) < 1.0

    def test_performance_with_mixed_separators_large(self, sample_flac_file: Path, temp_flac_file: Path):
        # Copy sample file to temporary location
        shutil.copy2(sample_flac_file, temp_flac_file)
        
        # Test performance with complex separator scenarios
        complex_artists = "//".join([f"Artist {i+1};Artist {i+2},Artist {i+3}" for i in range(0, 30, 3)])
        
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(temp_flac_file)], 
                          check=True, capture_output=True)
            
            subprocess.run([
                "metaflac",
                f"--set-tag=ARTIST={complex_artists}",
                str(temp_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set complex separated artists")
        
        start_time = time.time()
        unified_metadata = get_merged_unified_metadata(temp_flac_file)
        end_time = time.time()
        
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        # Should have many artists after complex separation
        assert len(artists) >= 30
        
        # Performance should be reasonable
        assert (end_time - start_time) < 2.0

    def test_memory_usage_with_large_values(self, sample_flac_file: Path, temp_flac_file: Path):
        # Copy sample file to temporary location
        shutil.copy2(sample_flac_file, temp_flac_file)
        
        # Test with very long individual values
        long_artist = "A" * 50000  # 50,000 character artist name
        
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(temp_flac_file)], 
                          check=True, capture_output=True)
            
            subprocess.run([
                "metaflac",
                f"--set-tag=ARTIST={long_artist}",
                str(temp_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set very long artist")
        
        unified_metadata = get_merged_unified_metadata(temp_flac_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 1
        assert artists[0] == long_artist

    def test_performance_repeated_reads(self, sample_flac_file: Path, temp_flac_file: Path):
        # Copy sample file to temporary location
        shutil.copy2(sample_flac_file, temp_flac_file)
        
        # Set up test data
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(temp_flac_file)], 
                          check=True, capture_output=True)
            
            artist_commands = []
            for i in range(10):
                artist_commands.extend(["--set-tag", f"ARTIST=Artist {i+1}"])
            
            subprocess.run(["metaflac"] + artist_commands + [str(temp_flac_file)], 
                          check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set test artists")
        
        # Test repeated reads
        start_time = time.time()
        for _ in range(100):
            unified_metadata = get_merged_unified_metadata(temp_flac_file)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(artists, list)
            assert len(artists) == 10
        end_time = time.time()
        
        # 100 reads should complete in reasonable time
        assert (end_time - start_time) < 5.0

    def test_performance_with_all_multi_value_fields(self, sample_flac_file: Path, temp_flac_file: Path):
        # Copy sample file to temporary location
        shutil.copy2(sample_flac_file, temp_flac_file)
        
        # Test performance when multiple multi-value fields are populated
        try:
            subprocess.run(["metaflac", "--remove-all-tags", str(temp_flac_file)], 
                          check=True, capture_output=True)
            
            # Set multiple artists
            artist_commands = []
            for i in range(10):
                artist_commands.extend(["--set-tag", f"ARTIST=Artist {i+1}"])
            
            # Set multiple genres
            genre_commands = []
            for i in range(5):
                genre_commands.extend(["--set-tag", f"GENRE=Genre {i+1}"])
            
            # Set multiple composers
            composer_commands = []
            for i in range(8):
                composer_commands.extend(["--set-tag", f"COMPOSER=Composer {i+1}"])
            
            all_commands = artist_commands + genre_commands + composer_commands + [str(temp_flac_file)]
            subprocess.run(["metaflac"] + all_commands, check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set multiple multi-value fields")
        
        start_time = time.time()
        unified_metadata = get_merged_unified_metadata(temp_flac_file)
        end_time = time.time()
        
        # Check all multi-value fields
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 10
        
        genres = unified_metadata.get(UnifiedMetadataKey.GENRE_NAME)
        assert isinstance(genres, list)
        assert len(genres) == 5
        
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
        assert isinstance(composers, list)
        assert len(composers) == 8
        
        # Performance should be reasonable
        assert (end_time - start_time) < 2.0

    def test_performance_with_whitespace_heavy_data(self, sample_flac_file: Path, temp_flac_file: Path):
        # Copy sample file to temporary location
        shutil.copy2(sample_flac_file, temp_flac_file)
        
        # Test performance with data that has lots of whitespace processing
        whitespace_heavy_artists = "   Artist One   ;   Artist Two   ,   Artist Three   "
        
        try:
            subprocess.run(["metaflac", "--remove-tag=ARTIST", str(temp_flac_file)], 
                          check=True, capture_output=True)
            
            subprocess.run([
                "metaflac",
                f"--set-tag=ARTIST={whitespace_heavy_artists}",
                str(temp_flac_file)
            ], check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("metaflac not available or failed to set whitespace-heavy artists")
        
        start_time = time.time()
        unified_metadata = get_merged_unified_metadata(temp_flac_file)
        end_time = time.time()
        
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist One" in artists
        assert "Artist Two" in artists
        assert "Artist Three" in artists
        
        # Check that whitespace was properly stripped
        for artist in artists:
            assert artist == artist.strip()
        
        # Performance should be reasonable
        assert (end_time - start_time) < 1.0