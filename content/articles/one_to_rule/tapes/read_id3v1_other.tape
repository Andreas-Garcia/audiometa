# Read ID3v1: print raw TAG fields (other tool). Requires demo from scripts/ensure_demo_read_id3v1.py (run by video script).
Output output/work/read_id3v1_other.gif


Set Shell "bash"
Set FontSize 16
Set Width 600
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms
Env HOME "@@ONE_TO_RULE_ABS@@"


Sleep 300ms

Type "echo '=== ID3v1: parse 128-byte TAG'"
Enter
Sleep 1s

Type "python3 scripts/print_id3v1_tags.py"
Enter
Sleep 5s
