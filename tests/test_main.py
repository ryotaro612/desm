"""
"""
import os
import tempfile
from unittest import TestCase
from click.testing import CliRunner
import gensim.models as mo
import desm
import desm.model as m
import desm.model_location as ml


class TestMain(TestCase):

    def setUp(self):
        self.word2vec_path = tempfile.mkstemp()[1]
        self.desm_path = tempfile.mkstemp()[1]

    def tearDown(self):
        for filename in [self.word2vec_path,
                         self.desm_path]:
            os.remove(filename)

    def test_smoke(self):
        runner = CliRunner()
        corpus_path = os.path.join(
            os.path.dirname(__file__),
            'test_main_corpus.txt')
        result = runner.invoke(
            desm.main,
            ['train',
             '--min-count',
             '1',
             corpus_path,
             self.word2vec_path])

        print(result.exit_code)
        result = runner.invoke(
            desm.main,
            ['build',
             'inout',
             self.word2vec_path,
             self.desm_path])
        print(result.exit_code)

        model_location = ml.ModelLocation.create(
            self.desm_path)
        model = m.Desm.load(model_location)
        self.assertIsInstance(model, m.DesmInOut)
        word2vec = model.word2vec
        self.assertIsInstance(word2vec, mo.Word2Vec)
