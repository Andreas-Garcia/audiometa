# VHS documentation: https://github.com/charmbracelet/vhs
#
# AudioMeta get_full_metadata() Demo - Script Version

# Output settings
Output audiometa_demo.mp4
Output audiometa_demo.gif

# Set up the terminal
Set FontSize 18
Set Width 1200
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 40ms
Set PlaybackSpeed 1.0

# Show demo script being run
Type "cat demo_repl_fixed.py" Enter
Sleep 3s

# Clear and run the demo
Type "clear" Enter
Sleep 500ms
Type "python demo_repl_fixed.py" Enter

# Wait for demo to complete (script runs ~8 seconds + we want to show final output)
Sleep 12s
