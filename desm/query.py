"""Implement a query class."""
from dataclasses import dataclass
from typing import List, Container
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

    def get_query_filtered_by_container(self, container: Container[str]):
        """Filter by a container.

        Returns
        -------
        Query

        """
        return Query([keyword for keyword in self.keywords
                      if keyword.keyword in container])
