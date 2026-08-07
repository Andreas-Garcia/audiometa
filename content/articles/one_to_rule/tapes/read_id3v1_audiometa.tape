# Read ID3v1: same file as read_id3v1_other; audiometa unified (table).
Output output/work/read_id3v1_audiometa.gif


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

Type "echo '=== ID3v1: audiometa unified'"
Enter
Sleep 1s

Type "(env -u NO_COLOR audiometa unified output/work/demo_read_id3v1.mp3 --format table --color | head -22; echo '...')"
Enter
Sleep 6s
