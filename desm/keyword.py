"""Provide classes relevant to keywords."""
from dataclasses import dataclass
from .first_class_collection import FirstClassFileContextManagerProvider
from .primitive import Primitive


@dataclass
class Keyword(Primitive):
    """Represent a keyword."""

    keyword: str

    @property
    def primitive(self):
        """
        """
        return self.keyword


class KeywordContext(FirstClassFileContextManagerProvider):
    """Provide keywords."""

    def transform(self, item: str):
        """
        """
        return Keyword(item)
