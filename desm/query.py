"""Implement a query class."""
from dataclasses import dataclass
from typing import List
from .keyword import Keyword
from .first_class_collection import FirstClassSequence


@dataclass
class Query(FirstClassSequence):
    """Represent a query."""

    keywords: List[Keyword]

    @property
    def sequence(self):
        """Return :py:attr:`keywords`."""
        return self.keywords
