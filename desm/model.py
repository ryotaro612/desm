"""Implement DESM models."""
import os
import os.path
import tempfile
from typing import Optional
from logging import getLogger
import joblib
import numpy as np
import gensim.models.keyedvectors as kv
from .model_location import ModelLocation
from .keyword import Keyword
from .similar import Similarities, SimilarityScore
from .query import Query
from .document import Document


class Desm:
    """A base model that implements DESM."""

    _LOGGER = getLogger(__name__)

    def __init__(
            self,
            query_keyed_vectors: kv.Word2VecKeyedVectors,
            document_keyed_vectors: kv.Word2VecKeyedVectors):
        """Take KeyedVectors objects."""
        self.query_keyed_vectors = query_keyed_vectors
        self.document_keyed_vectors = document_keyed_vectors

    def save(self, model_location: ModelLocation):
        """Write this model to `model_location`."""
        with model_location.open_gz_writable_stream() as stream, \
                tempfile.TemporaryDirectory() as directory:
            query_kv_dest = os.path.join(directory, 'query_kv')
            self.query_keyed_vectors.save(query_kv_dest)
            self.query_keyed_vectors = None

            document_kv_dest = os.path.join(directory, 'document_kv')
            self.document_keyed_vectors.save(document_kv_dest)
            self.document_keyed_vectors = None

            stream.add(directory, arcname='keyed_vectors_directory')

            desm_path = os.path.join(directory, 'desm.pkl')
            joblib.dump(self, desm_path)
            stream.add(desm_path, arcname='desm.pkl')

    @classmethod
    def load(cls, model_location: ModelLocation):
        """Load an instance of :py:class:`Desm` to memory.

        Returns
        -------
        Desm

        """
        with model_location.open_gz_readable_stream() as stream, \
                tempfile.TemporaryDirectory() as directory:
            cls._LOGGER.debug(
                f'Unarchiving a desm model from {model_location}.')
            stream.extractall(directory)
            cls._LOGGER.debug(
                f'Deserializing a desm model.')
            desm_path = os.path.join(directory, 'desm.pkl')
            desm = joblib.load(desm_path)
            cls._LOGGER.debug(
                f'Deserializing a KeyedVectors for queries.')
            keyed_vectors_dir = 'keyed_vectors_directory'
            model_path = os.path.join(
                directory, keyed_vectors_dir, 'query_kv')
            desm.query_keyed_vectors = kv.Word2VecKeyedVectors.load(
                model_path)
            cls._LOGGER.debug(
                f'Deserializing a KeyedVectors for documents.')
            model_path = os.path.join(
                directory, keyed_vectors_dir, 'document_kv')
            desm.document_keyed_vectors = \
                kv.Word2VecKeyedVectors.load(model_path)
            return desm

    def find_similar_keywords(
            self, top_n: int, keyword: Keyword) -> Similarities:
        """
        """
        vector = keyword.handle(self.query_keyed_vectors.get_vector)
        similarities = self.document_keyed_vectors.similar_by_vector(
            vector, topn=top_n)
        return Similarities.create_from_tuples(similarities)

    def is_acknowledged(self, keyword: Keyword) -> bool:
        """
        """
        return keyword.handle(
            lambda raw: raw in self.query_keyed_vectors)

    def rank(self, query: Query, document: Document) \
            -> Optional[SimilarityScore]:
        """Apply ranking function."""
        try:
            document_vector = self._to_embedding_document(document)
            query_vector = self._to_query_vectors(query)
            return SimilarityScore(
                np.mean(document_vector @ query_vector.T).astype(np.float32))
        except ValueError:
            return None

    def _to_query_vectors(self, query: Query) -> np.ndarray:
        """Return np.array with (num_of_queries, dim) shape."""
        filtered_query = query.get_query_filtered_by_container(
            self.query_keyed_vectors)
        if filtered_query.is_empty():
            raise ValueError

        vectors = np.array(list(filtered_query.apply_function(
            lambda keyword: self.query_keyed_vectors[keyword.keyword])))
        l2_norm = np.linalg.norm(vectors, ord=2, axis=1).reshape((-1, 1))
        return np.divide(vectors, l2_norm)

    def _to_embedding_document(self, document: Document) -> np.ndarray:
        """Return np.array with (dim,) shape."""
        filtered_document = document.get_document_filtered_by_container(
            self.document_keyed_vectors)
        if filtered_document.is_empty():
            raise ValueError(
                f"{document} does not contain acknowledged keywords.")

        vectors = np.sum(list(filtered_document.apply_function(
            lambda keyword: self._l2_normalize(
                self.document_keyed_vectors[keyword]))), axis=0)

        return self._l2_normalize(
            vectors / len(filtered_document))

    def _l2_normalize(self, array: np.ndarray) -> np.ndarray:
        array_l2_norm = np.linalg.norm(array, ord=2)
        return array / array_l2_norm


class DesmInOut(Desm):
    """
    """
