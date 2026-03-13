# Before only – for side-by-side combo with after_only.tape (mid3v2 output)
# Half width (600) so hstack gives 1200 total. Run from repo root with venv.
Output content/articles/one_to_rule/output/before_only.gif

Require audiometa

Set Shell "bash"
Set FontSize 16
Set Width 600
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms

Type "echo '=== Before: mid3v2 (MP3 only)'"
Enter
Sleep 2s

Type "(mid3v2 -l content/articles/one_to_rule/sample.mp3 2>/dev/null | head -26; echo '...')"
Enter
Sleep 6s
