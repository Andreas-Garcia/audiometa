import json
import subprocess
import sys
from audiometa.test.tests.test_helpers import TempFileWithMetadata


class TestCLIUnified:
    
    def test_cli_unified_output(self, sample_mp3_file):
        result = subprocess.run([sys.executable, "-m", "audiometa", "unified", 
                               str(sample_mp3_file), "--format", "json"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
    
    def test_cli_with_spaces_in_filename_unified(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            result = subprocess.run([sys.executable, "-m", "audiometa", "unified", 
                                   str(test_file.path), "--format", "json"], 
                                  capture_output=True, text=True)
            assert result.returncode == 0
            data = json.loads(result.stdout)
            assert isinstance(data, dict)
