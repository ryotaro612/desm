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

    def get_document_filtered_by_container(self, container):
        """Return a :py:class:`Document`.

        The document contains tokens shared with container.

        Returns
        -------
        Document

        """
        return Document(list(self.filter_by_container(container)))
