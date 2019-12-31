"""Implement classes that encapsulate access to a storage for similarity."""
import csv
from typing import Iterator, List
from ..similar import SimilarKeywords


class SimilarityGateway:
    """
    """

    def __init__(self, filename: str):
        """

        Parameters
        ----------
        filename : str

        """
        self.filename = filename

    def write_similar_keywords(
            self, simiarities_iterator: Iterator[SimilarKeywords]) -> None:
        """Write similarities to the :py:attr:`filename`."""
        with open(self.filename, 'w') as stream:
            writer = None
            for similarities in simiarities_iterator:
                writer if writer else csv.DictWriter(
                    stream, self._build_header(similarities))
                writer.writerow(self._to_row(similarities))

    def _build_header(self, similarities: SimilarKeywords) -> List[str]:
        num_similar_keywords = similarities.get_number_of_similar_keywords()
        tail_headers = [
            column
            for indice in range(num_similar_keywords)
            for column in (f'keyword {indice}', f'score {indice}')]
        return ['keyword'] + tail_headers

    def _to_row(self, similarities: SimilarKeywords) -> dict:
        row_tail = [item
                    for keyword_score in similarities.get_similarity_tuples()
                    for item in keyword_score]
        headers = self._build_header(similarities)
        return dict((key, val)
                    for key, val
                    in zip(headers, [similarities.raw_keyword()] + row_tail))
