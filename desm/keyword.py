"""Provide classes relevant to keywords."""
from dataclasses import dataclass
from .first_class_collection import FirstClassFileContextManagerProvider


@dataclass
class Keyword:
    """Represent a keyword."""
    keyword: str


class KeywordContext(FirstClassFileContextManagerProvider):
    """Provide keywords."""

    def transform(self, item: str):
        """
        """
        return Keyword(item)
