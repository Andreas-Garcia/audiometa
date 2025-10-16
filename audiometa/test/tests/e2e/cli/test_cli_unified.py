import json
import subprocess
import sys


class TestCLIUnified:
    
    def test_cli_unified_output(self, sample_mp3_file):
        result = subprocess.run([sys.executable, "-m", "audiometa", "unified", 
                               str(sample_mp3_file), "--format", "json"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
    
    def test_cli_with_spaces_in_filename_unified(self, sample_mp3_file, tmp_path):
        test_file = tmp_path / "Test Song - Artist (Remix).mp3"
        import shutil
        shutil.copy2(sample_mp3_file, test_file)
        
        result = subprocess.run([sys.executable, "-m", "audiometa", "unified", 
                               str(test_file), "--format", "json"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
