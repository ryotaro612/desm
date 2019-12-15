"""Implement the factory to create word2vec models."""
from logging import getLogger
import gensim.models as m
from .factory import ArgumentInspector


class Word2VecFactory:
    """Provide a method to create word2vec models."""

    _LOGGER = getLogger(__name__)

    @classmethod
    def create(cls, **kwargs) -> m.Word2Vec:
        """Create a word2vec model."""
        inspector = ArgumentInspector(m.Word2Vec.__init__, True)
        valid_arguments = inspector.drop_invalid_arguments(kwargs)
        cls._LOGGER.info('Create a word2vec model with parameters as %s',
                         valid_arguments)
        return m.Word2Vec(**valid_arguments)
