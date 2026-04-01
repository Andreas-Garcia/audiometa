# Read same FLAC with audiometa (unified).
Output output/read_vorbis_audiometa.gif


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

Type "clear"
Enter
Sleep 400ms

Type "echo '=== Vorbis (FLAC): audiometa unified'"
Enter
Sleep 1s

Type "(env -u NO_COLOR audiometa unified demo_read_vorbis.flac --format table --color | head -22; echo '...')"
Enter
Sleep 6s
