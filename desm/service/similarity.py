"""
"""
from typing import Generator
from ..model import Desm
from ..keyword import KeywordContext
from ..gateway.similarity import SimilarityGateway
from ..similarity_request import SimilarityRequest
from ..similarity import Similarities


class SimilarityService:
    """Find similar keywords.

    Attributes
    ----------
    desm: Desm

    similarity_gateway: SimilarityGateway

    """

    def __init__(self,
                 desm: Desm,
                 similarity_gateway: SimilarityGateway):
        """Take a Desm model and a gateway to save simliarities."""
        self.desm = desm
        self.similarity_gateway = similarity_gateway

    def find_similar_keywords(
            self, request: SimilarityRequest) -> None:
        """Find similar keywords using a DESM model."""
        with request.keyword_stream() as keywords:
            similarities_generator = self._find_similarities(
                request.top_n, keywords)
            self.similarity_gateway.write_similarities(
                    similarities_generator)

    def _find_similarities(self, top_n, keywords) \
            -> Generator[Similarities, None, None]:
        for keyword in (keyword
                        for keyword
                        in keywords
                        if self.desm.is_acknowledged(keyword)):
            yield self.desm.find_similar_keywords(top_n, keyword)
