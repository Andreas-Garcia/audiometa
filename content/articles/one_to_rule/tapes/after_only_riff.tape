# After only (RIFF): read WAV metadata with audiometa; for video panel.
# Half width (600). Run with cwd = article dir.
Output output/after_only_riff.gif


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

Type "echo '=== After: audiometa unified (RIFF)'"
Enter
Sleep 2s

Type "(env -u NO_COLOR audiometa unified sample.wav --format table --color | head -26; echo '...')"
Enter
Sleep 5s
