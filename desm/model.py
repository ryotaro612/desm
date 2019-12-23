"""Implement DESM models."""
import os
import os.path
import tempfile
from logging import getLogger
import joblib
import gensim.models.keyedvectors as kv
from .model_location import ModelLocation
from .keyword import Keyword


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
            desm.query_keyed_vectors = kv.Word2VecKeyedVectors.load(model_path)
            cls._LOGGER.debug(
                    f'Deserializing a KeyedVectors for documents.')
            model_path = os.path.join(
                directory, keyed_vectors_dir, 'document_kv')
            desm.document_keyed_vectors = kv.Word2VecKeyedVectors.load(
                    model_path)
            return desm

    def find_similar_keywords(self, top_n: int, keyword: Keyword):
        """
        """
        raise NotADirectoryError

    def is_acknowledged(self, keyword: Keyword) -> bool:
        """
        """
        print(self.query_keyed_vectors)
        return keyword.handle(
                lambda raw: raw in self.query_keyed_vectors)


class DesmInOut(Desm):
    """
    """
