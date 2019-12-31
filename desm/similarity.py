"""
"""
from dataclasses import dataclass
from collections.abc import Sequence
from typing import List, Tuple, Iterator
from numbers import Number
import numpy as np
from .keyword import Keyword


@dataclass
class Similarity:
    """
    """
    keyword: Keyword
    score: np.float32


class Similarities(Sequence):
    """
    """
    similarities: List[Similarity]

    @classmethod
    def create_from_tuples(
            cls, similarities: Iterator[Tuple[str, Number]]):
        """Create a Similarities."""
        return Similarities([Similarity(Keyword(similarity[0]),
                                        np.float32(similarity[1]))
                             for similarity in similarities])


class SimilarityWriter:
    """
    """

    def __init__(self, filename: str):
        """Take the path to a file to write."""
        self.filename = filename

    def write_similarities(self, similarities):
        """
        """
