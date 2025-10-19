"""Shared utility for running external tools with consistent error handling."""

import subprocess
from typing import List

from ..id3v2.mid3v2_tool import ExternalMetadataToolError


def run_external_tool(command: List[str], tool_name: str = "external tool", check: bool = True) -> subprocess.CompletedProcess:
    """Run an external tool command with proper error handling.
    
    Args:
        command: List of command and arguments to execute
        tool_name: Name of the tool for error messages (e.g., "metaflac", "mid3v2")
        check: Whether to raise exception on non-zero exit code
        
    Returns:
        subprocess.CompletedProcess: The result of the command execution
        
    Raises:
        ExternalMetadataToolError: If the command fails or tool is not found
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=check
        )
        return result
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise ExternalMetadataToolError(f"{tool_name} failed: {e}") from e