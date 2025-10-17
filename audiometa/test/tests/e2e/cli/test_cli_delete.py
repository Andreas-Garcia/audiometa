import subprocess
import sys
from audiometa.test.tests.test_helpers import TempFileWithMetadata


class TestCLIDelete:
    
    def test_cli_delete_metadata(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            result = subprocess.run([sys.executable, "-m", "audiometa", "delete", 
                                   str(test_file.path)], 
                                  capture_output=True, text=True)
            assert result.returncode == 0
            assert "Deleted all metadata" in result.stdout or "No metadata found" in result.stdout
