# VHS documentation: https://github.com/charmbracelet/vhs
#
# AudioMeta get_full_metadata() Demo for Twitter

# Output settings
Output audiometa_demo.mp4
Output audiometa_demo.gif

# Set up the terminal
Set FontSize 18
Set Width 1200
Set Height 600
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms
Set PlaybackSpeed 1.0

# Hide initial shell prompt
Hide

# Type the Python command
Type "python3" Enter
Sleep 1s

# Show the terminal
Show

# Type Python import
Type "from audiometa import get_full_metadata" Enter
Sleep 500ms

# Call the function
Type 'metadata = get_full_metadata("audiometa/test/assets/sample.mp3")' Enter
Sleep 800ms

# Show unified metadata
Type "metadata['unified_metadata']" Enter
Sleep 2s

# Show technical info
Type "metadata['technical_info']" Enter
Sleep 2s

# Show raw metadata keys
Type "list(metadata['raw_metadata'].keys())" Enter
Sleep 2s

# Show format priorities
Type "metadata['format_priorities']" Enter
Sleep 2s

# Add final comment
Type "# Complete metadata in one function!" Enter
Sleep 1s

# Exit Python
Type "exit()" Enter
Sleep 500ms
