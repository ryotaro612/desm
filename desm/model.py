"""
"""
import os
import os.path
import tempfile
import joblib
import gensim.models as m
from .model_location import ModelLocation
from .keyword import Keyword


class Desm:
    """A base model that implement DESM."""

    def __init__(self, word2vec: m.Word2Vec):
        """Take a trained word2vec model."""
        self.word2vec = word2vec

    def save(self, model_location: ModelLocation):
        """Write this model to `model_location`."""
        with model_location.open_gz_writable_stream() as stream, \
                tempfile.TemporaryDirectory() as directory:
            word2vec_path = os.path.join(directory, 'word2vec')
            self.word2vec.save(word2vec_path)
            stream.add(directory, arcname='word2vec_directory')
            self.word2vec = None
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
            stream.extractall(directory)
            model_path = os.path.join(
                directory, 'word2vec_directory', 'word2vec')
            word2vec = m.Word2Vec.load(model_path)
            desm_path = os.path.join(directory, 'desm.pkl')
            desm = joblib.load(desm_path)
            desm.word2vec = word2vec
            return desm

    def find_similar_keywords(self, top_n: int, keyword: Keyword):
        """
        """
        raise NotADirectoryError

    def is_acknowledged(self, keyword: Keyword) -> bool:
        """
        """
        raise NotImplementedError


class DesmInOut(Desm):
    """
    """
