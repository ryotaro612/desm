"""Implement a query class."""
from dataclasses import dataclass
from .primitive import Primitive


@dataclass
class Query(Primitive):
    """Represent a query."""

    query: str

    @property
    def primitive(self):
        """Return :py:attr:`query`."""
        return self.query
