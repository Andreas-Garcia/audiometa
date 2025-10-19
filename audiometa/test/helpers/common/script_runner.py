"""Script runner utilities for executing external shell scripts."""

import subprocess
from pathlib import Path

from ..id3v2.mid3v2_tool import ExternalMetadataToolError


class ScriptRunner:
    """Utilities for running external shell scripts."""
    
    def __init__(self, scripts_dir: Path):
        self.scripts_dir = scripts_dir
    
    def run_script(self, script_name: str, target_file: Path) -> subprocess.CompletedProcess:
        """Run an external script with proper error handling."""
        script_path = self.scripts_dir / script_name
        
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")
        
        if not script_path.is_file():
            raise FileNotFoundError(f"Script is not a file: {script_path}")
        
        # Make script executable
        script_path.chmod(0o755)
        
        try:
            result = subprocess.run(
                [str(script_path), str(target_file)],
                capture_output=True,
                text=True,
                check=True
            )
            return result
        except subprocess.CalledProcessError as e:
            raise ExternalMetadataToolError(f"Script {script_name} failed: {e.stderr}") from e