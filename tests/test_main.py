"""
"""
import os
import tempfile
from unittest import TestCase
from click.testing import CliRunner
import gensim.models.keyedvectors as kv
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
        runner.invoke(
            desm.main,
            ['train',
             '--min-count',
             '1',
             corpus_path,
             self.word2vec_path])

        runner.invoke(
            desm.main,
            ['build',
             'inout',
             self.word2vec_path,
             self.desm_path])

        model_location = ml.ModelLocation.create(
            self.desm_path)
        model = m.Desm.load(model_location)
        self.assertIsInstance(model, m.DesmInOut)
        for keyed_vectors in [model.query_keyed_vectors,
                              model.document_keyed_vectors]:
            self.assertIsInstance(keyed_vectors,
                                  kv.Word2VecKeyedVectors)
