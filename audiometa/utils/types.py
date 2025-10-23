
from enum import Enum

from .UnifiedMetadataKey import UnifiedMetadataKey


class RawMetadataKey(str, Enum):
    pass

    def __str__(self) -> str:
        return str(self.value)


"""
Raw metadata value can be none (when not set), string (title), integer (rating), float(BPM) or list[str] (artists 
names).
"""
AppMetadataValue = int | float | str | list[str] | None
RawMetadataValue = list[int] | list[float] | list[str] | None
RawMetadataDict = dict[RawMetadataKey, RawMetadataValue]
UnifiedMetadata = dict[UnifiedMetadataKey, AppMetadataValue]
