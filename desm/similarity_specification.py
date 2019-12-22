"""Provide :py:class:`SimilaritySpecification`."""
from dataclasses import dataclass
from .keywords import KeywordContext


@dataclass
class SimilaritySpecification:
    """
    TODO
    ----

    """

    top_n: int
    keyword_context: KeywordContext
