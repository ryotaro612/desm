"""Implement a query class."""
from dataclasses import dataclass
from typing import List
from .primitive import Primitive
from .keyword import Keyword


@dataclass
class Query(Primitive):
    """Represent a query."""

    keywords: List[Keyword]

    @property
    def primitive(self):
        """Return :py:attr:`keywords`."""
        return self.keywords
