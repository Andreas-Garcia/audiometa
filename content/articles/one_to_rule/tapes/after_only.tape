# After only – for side-by-side combo with before_only.tape (audiometa read)
# Half width (600) so hstack gives 1200 total. Run from repo root with venv.
Output content/articles/one_to_rule/output/after_only.gif

Require audiometa

Set Shell "bash"
Set FontSize 16
Set Width 600
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms

Type "echo '=== After: audiometa (any format)'"
Enter
Sleep 2s

Type "(env -u NO_COLOR audiometa read content/articles/one_to_rule/sample.mp3 --format table --color | head -26; echo '...')"
Enter
Sleep 6s
