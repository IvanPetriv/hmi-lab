from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Blog:
    """
    Represents a Blog object.
    """
    title: str
    author: str
    description: str | None
    datetime: datetime
    author_image_url: str
