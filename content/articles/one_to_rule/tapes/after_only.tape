# After only – for side-by-side combo with before_only.tape (audiometa unified)
# Half width (600) so hstack gives 1200 total. Run with cwd = article dir.
Output output/work/after_only.gif


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

Type "echo '=== After: audiometa (any format)'"
Enter
Sleep 2s

Type "(env -u NO_COLOR audiometa unified samples/sample.mp3 --format table --color | head -26; echo '...')"
Enter
Sleep 6s
