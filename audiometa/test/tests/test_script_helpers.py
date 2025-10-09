"""Helper functions for using external scripts in tests.

This module provides Python functions that call the external scripts
in audiometa/test/data/scripts/ to set up test files with metadata
without using the app's own update functions. This prevents circular
dependencies in tests where writing logic could mask reading bugs.
"""

import subprocess
from pathlib import Path
from typing import Optional


class ScriptHelper:
    
    def __init__(self, scripts_dir: Optional[Path] = None):
        if scripts_dir is None:
            # Default to the scripts directory relative to this file
            self.scripts_dir = Path(__file__).parent.parent / "data" / "scripts"
        else:
            self.scripts_dir = scripts_dir
    
    def _run_script(self, script_name: str, file_path: Path, check: bool = True) -> subprocess.CompletedProcess:
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")
        
        if not script_path.is_file():
            raise FileNotFoundError(f"Script is not a file: {script_path}")
        
        # Make script executable
        script_path.chmod(0o755)
        
        try:
            result = subprocess.run(
                [str(script_path), str(file_path)],
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Script {script_name} failed: {e.stderr}") from e
    
    def set_id3v2_max_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("set-id3v2-max-metadata.sh", file_path)
    
    def set_vorbis_max_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("set-vorbis-max-metadata.sh", file_path)
    
    def set_riff_max_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("set-riff-max-metadata.sh", file_path)
    
    def set_id3v1_max_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("set-id3v1-max-metadata.sh", file_path)
    
    def set_artists_one_two_three_vorbis(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("set-artists-One-Two-Three-vorbis.sh", file_path)
    
    def remove_id3_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("remove_id3.py", file_path)
    
    def remove_riff_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("remove_riff.py", file_path)
