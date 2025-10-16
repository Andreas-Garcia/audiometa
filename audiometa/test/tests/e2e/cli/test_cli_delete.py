import subprocess
import sys


class TestCLIDelete:
    
    def test_cli_delete_metadata(self, sample_mp3_file, tmp_path):
        test_file = tmp_path / "test_delete.mp3"
        import shutil
        shutil.copy2(sample_mp3_file, test_file)
        
        result = subprocess.run([sys.executable, "-m", "audiometa", "delete", 
                               str(test_file)], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Deleted all metadata" in result.stdout or "No metadata found" in result.stdout
