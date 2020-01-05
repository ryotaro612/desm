"""Implement a class that represents document."""
from typing import List
from dataclasses import dataclass
from .first_class_collection import FirstClassSequence


@dataclass
class Document(FirstClassSequence):
    """Represent a tokenized document."""

    tokens: List[str]

    @property
    def sequence(self):
        """Return :py:class:`tokens`."""
        return self.tokens
