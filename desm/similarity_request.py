"""Provide a class that represent a request to find similar keywords."""
from dataclasses import dataclass
from .keyword import KeywordContext


@dataclass
class SimilarityRequest:
    """Represent a request to find similar keywords.

    Attributes
    ----------
    top_n: int

    keyword_context: KeywordContext

    """

    top_n: int
    keyword_context: KeywordContext

    def keyword_stream(self):
        """
        """
        return self.keyword_context()
