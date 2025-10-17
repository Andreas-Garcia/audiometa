"""Base helper class with common functionality for all metadata format helpers."""

import subprocess
from pathlib import Path
from typing import Dict, Any


class BaseHelper:
    """Base class providing common functionality for all metadata format helpers."""
    
    @staticmethod
    def _get_scripts_dir() -> Path:
        """Get the scripts directory path."""
        return Path(__file__).parent.parent.parent / "data" / "scripts"
    
    @staticmethod
    def _run_script(script_name: str, file_path: Path, check: bool = True) -> subprocess.CompletedProcess:
        """Run an external script with proper error handling."""
        scripts_dir = BaseHelper._get_scripts_dir()
        script_path = scripts_dir / script_name
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
    
    @staticmethod
    def _run_external_tool(command: list[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run an external tool with proper error handling."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(f"External tool failed: {e}") from e
    
    @staticmethod
    def check_metadata_with_external_tools(file_path: Path) -> Dict[str, Any]:
        """Check metadata using external tools for comprehensive verification."""
        results = {}
        
        # Check with mid3v2
        try:
            result = subprocess.run(
                ['mid3v2', '-l', str(file_path)],
                capture_output=True, text=True, check=True
            )
            results['mid3v2'] = {
                'success': True,
                'output': result.stdout,
                'has_id3v2': 'ID3v2 tag' in result.stdout and 'No ID3v2 tag found' not in result.stdout,
                'has_id3v1': 'ID3v1 tag' in result.stdout and 'No ID3v1 tag found' not in result.stdout
            }
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            results['mid3v2'] = {'success': False, 'error': str(e)}
        
        # Check with mutagen-inspect
        try:
            result = subprocess.run(
                ['mutagen-inspect', str(file_path)],
                capture_output=True, text=True, check=True
            )
            results['mutagen_inspect'] = {
                'success': True,
                'output': result.stdout,
                'has_metadata': 'No tags' not in result.stdout
            }
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            results['mutagen_inspect'] = {'success': False, 'error': str(e)}
        
        # Check with metaflac (for FLAC files)
        if file_path.suffix.lower() == '.flac':
            try:
                result = subprocess.run(
                    ['metaflac', '--list', str(file_path)],
                    capture_output=True, text=True, check=True
                )
                results['metaflac'] = {
                    'success': True,
                    'output': result.stdout,
                    'has_vorbis': 'VORBIS_COMMENT' in result.stdout
                }
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                results['metaflac'] = {'success': False, 'error': str(e)}
        
        return results
