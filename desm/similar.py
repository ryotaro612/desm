"""
"""
from dataclasses import dataclass
from collections.abc import Sequence
from typing import List, Tuple, Iterator
from numbers import Number
import numpy as np
from .keyword import Keyword
from .first_class_collection import FirstClassSequence


@dataclass
class Similarity:
    """
    """
    keyword: Keyword
    score: np.float32


@dataclass
class Similarities(FirstClassSequence):
    """A sequence of :py:class:`Similarity` objects."""

    similarities: List[Similarity]

    @property
    def sequence(self):
        """
        """
        return self.similarities

    @classmethod
    def create_from_tuples(
            cls, similarities: Iterator[Tuple[str, Number]]):
        """Create a Similarities."""
        return Similarities([Similarity(Keyword(similarity[0]),
                                        np.float32(similarity[1]))
                             for similarity in similarities])


@dataclass
class SimilarKeywords:
    """
    """

    keyword: Keyword
    similarities:  Similarities

    def get_number_of_similar_keywords(self) -> int:
        """
        """
        return len(self.similarities)

    def raw_keyword(self) -> str:
        """
        """
        return self.keyword.keyword

    def get_similarity_tuples(self) -> List[Tuple[str, np.float32]]:
        """
        """
        return [(similarity.keyword.keyword, similarity.score)
                for similarity in self.similarities]
