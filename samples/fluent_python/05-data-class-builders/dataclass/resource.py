import datetime

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class ResourceType(Enum):
    BOOK = auto()
    EBOOK = auto()
    VIDEO = auto()


@dataclass
class Resource:
    """Media resource description."""
    identifier: str
    title: str = '<untitle>'
    creators: list[str] = field(default_factory=list)
    date: Optional[datetime.date] = None
    resource_type: ResourceType = ResourceType.BOOK
    description: str = ''
    language: str = ''
    subjects: list[str] = field(default_factory=list)
    