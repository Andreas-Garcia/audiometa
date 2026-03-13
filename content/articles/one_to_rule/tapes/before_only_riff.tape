# Before only (RIFF): read WAV metadata with ffprobe; for video panel.
# Half width (600). Run from repo root. Requires ffprobe on PATH. sample.wav must exist (script creates it).
Output content/articles/one_to_rule/output/before_only_riff.gif

Require audiometa

Set Shell "bash"
Set FontSize 16
Set Width 600
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms

Type "echo '=== Before: RIFF (ffprobe)'"
Enter
Sleep 2s

Type "(ffprobe -show_entries format_tags -v quiet -of default=noprint_wrappers=1 content/articles/one_to_rule/sample.wav 2>/dev/null | head -20; echo '...')"
Enter
Sleep 5s
