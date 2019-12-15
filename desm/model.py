"""
"""
import gensim.models as m
from .corpus import Corpus


class Model:
    """
    """

    def __init__(self, word2vec: m.Word2Vec, tokenizer):
        """
        """
        self.word2vec = word2vec
        self.tokenizer = tokenizer

    def transform(self):
        """
        """


    def train(self, corpus: Corpus):
        """
        """

    def save(self):
        """
        """

    def load(self):
        """
        """
