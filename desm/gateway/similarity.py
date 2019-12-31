"""Implement classes that encapsulate access to a storage for similarity."""
import csv
from typing import Iterator, List, Union, Iterable
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
            self,
            similar_keywords_iter: Iterator[SimilarKeywords]) -> None:
        """Write similarities to the :py:attr:`filename`."""
        try:
            similar_keywords_iter = iter(similar_keywords_iter)
            similar_keywords = next(similar_keywords_iter)
        except StopIteration:
            return

        with open(self.filename, 'w') as stream:
            header = self._build_header(similar_keywords)
            writer = csv.DictWriter(stream, header)
            writer.writeheader()
            writer.writerow(self._to_row(similar_keywords))
            self._write_rows(writer, similar_keywords_iter)

    def _write_rows(self, writer, similar_keywords_iter):
        for similar_keywords in similar_keywords_iter:
            writer.writerow(self._to_row(similar_keywords))

    def _build_header(self, similarities: SimilarKeywords) -> List[str]:
        num_similar_keywords = similarities.get_number_of_similar_keywords()
        tail_headers = [
            column
            for indice in range(num_similar_keywords)
            for column in (f'neighbor {indice+1}', f'similarity {indice+1}')]
        return ['keyword'] + tail_headers

    def _to_row(self, similarities: SimilarKeywords) -> dict:
        row_tail = [item
                    for keyword_score in similarities.get_similarity_tuples(3)
                    for item in keyword_score]
        headers = self._build_header(similarities)
        return dict((key, val)
                    for key, val
                    in zip(headers, [similarities.raw_keyword()] + row_tail))
