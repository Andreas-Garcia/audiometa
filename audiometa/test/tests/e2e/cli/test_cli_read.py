import json
import subprocess
import sys
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestCLIRead:
    
    def test_cli_read_nonexistent_file(self, tmp_path):
        nonexistent_file = tmp_path / "nonexistent.mp3"
        result = subprocess.run([sys.executable, "-m", "audiometa", "read", str(nonexistent_file)], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        assert "error" in result.stderr.lower()
    
    def test_cli_read_with_continue_on_error(self, tmp_path):
        nonexistent_file = tmp_path / "nonexistent.mp3"
        result = subprocess.run([sys.executable, "-m", "audiometa", "read", 
                               str(nonexistent_file), "--continue-on-error"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
    
    def test_cli_read_output_formats(self, sample_mp3_file):
        result = subprocess.run([sys.executable, "-m", "audiometa", "read", 
                               str(sample_mp3_file), "--format", "json"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "unified_metadata" in data
        
        result = subprocess.run([sys.executable, "-m", "audiometa", "read", 
                               str(sample_mp3_file), "--format", "table"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "UNIFIED METADATA" in result.stdout or "TECHNICAL INFO" in result.stdout
    
    def test_cli_output_to_file(self, sample_mp3_file, tmp_path):
        output_file = tmp_path / "metadata.json"
        result = subprocess.run([sys.executable, "-m", "audiometa", "read", 
                               str(sample_mp3_file), "--output", str(output_file)], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert output_file.exists()
        
        with open(output_file) as f:
            data = json.load(f)
        assert isinstance(data, dict)
    
    def test_cli_with_spaces_in_filename(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            result = subprocess.run([sys.executable, "-m", "audiometa", "read", 
                                   str(test_file.path), "--format", "json"], 
                                  capture_output=True, text=True)
            assert result.returncode == 0
            data = json.loads(result.stdout)
            assert isinstance(data, dict)
            assert "unified_metadata" in data
