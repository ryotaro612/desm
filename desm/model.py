"""
"""
import os
import os.path
import tempfile
import joblib
import gensim.models as m


class Desm:
    """
    TODO
    ----
    Use only Keyvector.

    """

    def __init__(self, word2vec: m.Word2Vec):
        """
        """
        self.word2vec = word2vec

    def save(self, stream):
        """
        """
        with tempfile.TemporaryDirectory() as directory:
            word2vec_path = os.path.join(directory, 'word2vec')
            self.word2vec.save(word2vec_path)
            stream.add(directory, arcname='word2vec_directory')
            self.word2vec = None
            desm_path = os.path.join(directory, 'desm.pkl')
            joblib.dump(self, desm_path)
            stream.add(desm_path, archname='desm.pkl')

    def load(self, stream):
        """

        Returns
        -------
        Desm

        """
        with tempfile.TemporaryDirectory() as directory:
            stream.extractall(directory)
            model_path = os.path.join(
                directory, 'word2vec_directory', 'word2vec')
            word2vec = m.Word2Vec.load(model_path)
            desm_path = os.path.join(directory, 'desm.pkl')
            desm = joblib.load(desm_path)
            desm.word2vec = word2vec
            return desm

class DesmInOut(Desm):
    """
    """
