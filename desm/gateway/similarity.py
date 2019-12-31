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
        self.filename = filename

    def write_similarities(self, simiarities) -> None:
        """
        """
        raise NotImplementedError
