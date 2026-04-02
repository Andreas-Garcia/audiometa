"""Parse combined disc index/total strings (ID3v2 TPOS-style) for unified metadata read."""

import re

_DISC_NUMBER_RE = re.compile(r"^(\d+)(?:[-/](\d+))?$")
_DISC_TOTAL_FROM_COMBINED_RE = re.compile(r"^(\d+)[-/](\d+)$")


def parse_disc_number_from_combined_str(value: str) -> int | None:
    m = _DISC_NUMBER_RE.match(value)
    if m:
        return int(m.group(1))
    return None


def parse_disc_total_from_combined_str(value: str) -> int | None:
    m = _DISC_TOTAL_FROM_COMBINED_RE.match(value)
    if m:
        return int(m.group(2))
    return None


def parse_explicit_non_negative_disctotal(value: str) -> int | None:
    try:
        n = int(value)
    except (ValueError, TypeError):
        return None
    if n < 0:
        return None
    return n
