import subprocess
import sys
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestCLIWrite:
    
    def test_cli_write_no_metadata(self, sample_mp3_file):
        result = subprocess.run([sys.executable, "-m", "audiometa", "write", str(sample_mp3_file)], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        assert "no metadata fields specified" in result.stderr.lower()
    
    def test_cli_write_basic_metadata(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            result = subprocess.run([sys.executable, "-m", "audiometa", "write", 
                                   str(test_file.path), "--title", "CLI Test Title"], 
                                  capture_output=True, text=True)
            assert result.returncode == 0
            assert "Updated metadata" in result.stdout
    
    def test_cli_with_spaces_in_filename_write(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            result = subprocess.run([sys.executable, "-m", "audiometa", "write", 
                                   str(test_file.path), "--title", "Test Title", "--artist", "Test Artist"], 
                                  capture_output=True, text=True)
            assert result.returncode == 0
            assert "Updated metadata" in result.stdout
