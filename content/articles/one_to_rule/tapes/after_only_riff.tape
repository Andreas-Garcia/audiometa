# After only (RIFF): read WAV metadata with audiometa; for video panel.
# Half width (600). Run from repo root with venv.
Output content/articles/one_to_rule/output/after_only_riff.gif

Require audiometa

Set Shell "bash"
Set FontSize 16
Set Width 600
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms

Type "echo '=== After: audiometa read (RIFF)'"
Enter
Sleep 2s

Type "(env -u NO_COLOR audiometa read content/articles/one_to_rule/sample.wav --format table --color | head -26; echo '...')"
Enter
Sleep 5s
