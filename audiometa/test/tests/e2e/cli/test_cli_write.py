import subprocess
import sys
from pathlib import Path


class TestCLIWrite:
    
    def test_cli_write_no_metadata(self, sample_mp3_file):
        result = subprocess.run([sys.executable, "-m", "audiometa", "write", str(sample_mp3_file)], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        assert "no metadata fields specified" in result.stderr.lower()
    
    def test_cli_write_basic_metadata(self, sample_mp3_file, tmp_path):
        test_file = tmp_path / "test_write.mp3"
        import shutil
        shutil.copy2(sample_mp3_file, test_file)
        
        result = subprocess.run([sys.executable, "-m", "audiometa", "write", 
                               str(test_file), "--title", "CLI Test Title"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Updated metadata" in result.stdout
    
    def test_cli_with_spaces_in_filename_write(self, sample_mp3_file, tmp_path):
        test_file = tmp_path / "Test Song - Artist (Remix).mp3"
        import shutil
        shutil.copy2(sample_mp3_file, test_file)
        
        result = subprocess.run([sys.executable, "-m", "audiometa", "write", 
                               str(test_file), "--title", "Test Title", "--artist", "Test Artist"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Updated metadata" in result.stdout
