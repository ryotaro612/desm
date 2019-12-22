"""Implement classes that encapsulate access to a storage for similarity."""
from typing import Iterable
from ..similarity import Similarity


class SimilarityGateway:
    """
    TODO
    ----
    Abstract.

    """

    def __init__(self, filename: str):
        """
        """

    def write_similarities(self, simiarities: Iterable[Similarity]) -> None:
        """
        """
        raise NotImplementedError
