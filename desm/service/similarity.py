"""
"""
from ..model import Desm
from ..keywords import KeywordContext
from ..gateway.similarity import SimilarityGateway


class SimilarityService:
    """
    """

    def __init__(self,
                 desm: Desm,
                 similarity_gateway: SimilarityGateway):
        """Take a Desm model and a gateway to save simliarities."""
        self.desm = desm
        self.similarity_gateway = similarity_gateway

    def find_similar_keywords(
            self, keyword_context: KeywordContext):
        """
        """
        raise NotImplementedError

