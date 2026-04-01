# Before only – for side-by-side combo with after_only.tape (mid3v2 output)
# Half width (600) so hstack gives 1200 total. Run with cwd = article dir (see article README).
Output output/before_only.gif


Require audiometa

Set Shell "bash"
Set FontSize 16
Set Width 600
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms
Env HOME "@@ONE_TO_RULE_ABS@@"


Sleep 300ms

Type "echo '=== Before: mid3v2 (MP3 only)'"
Enter
Sleep 2s

Type "(mid3v2 -l sample.mp3 2>/dev/null | head -26; echo '...')"
Enter
Sleep 6s
