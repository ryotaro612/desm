"""Provide a service to find similar keywords."""
from typing import Generator, Iterator
from ..model import Desm
from ..gateway.similarity import SimilarityGateway
from ..similarity_request import SimilarityRequest
from ..similar import SimilarKeywords
from ..keyword import Keyword


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
        generator = SimilarKeywordGenerator(self.desm)
        with request.keyword_stream() as keywords:
            generated = generator(request.top_n, keywords)
            self.similarity_gateway.write_similar_keywords(
                generated)


class SimilarKeywordGenerator:
    """
    """

    def __init__(self, desm: Desm):
        """
        """
        self.desm = desm

    def __call__(self, top_n: int, keywords: Iterator[Keyword]) \
            -> Generator[SimilarKeywords, None, None]:
        """
        """
        for keyword in (keyword
                        for keyword
                        in keywords
                        if self.desm.is_acknowledged(keyword)):

            similarities = self.desm.find_similar_keywords(top_n, keyword)
            yield SimilarKeywords(keyword, similarities)
