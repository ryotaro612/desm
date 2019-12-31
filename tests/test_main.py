"""
"""
import os.path
import tempfile
import csv
from unittest import TestCase
from click.testing import CliRunner
import desm


class TestMain(TestCase):

    def setUp(self):
        self.word2vec_path = tempfile.mkstemp()[1]
        self.desm_path = tempfile.mkstemp()[1]
        self.similarity_file = tempfile.mkstemp()[1]

    def tearDown(self):
        for filename in [self.word2vec_path,
                         self.desm_path,
                         self.similarity_file]:
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

        keyword_file = os.path.join(os.path.dirname(
            __file__), 'main_smoke_keywords.txt')
        runner.invoke(
            desm.main,
            ['similarity',
             '--top-n', '1',
             self.desm_path, keyword_file, self.similarity_file])

        with open(self.similarity_file) as f:
            lines = list(csv.DictReader(f))
            self.assertEqual(len(lines), 3)
            self.assertEqual(
                list(lines[0].keys()),
                ['keyword', 'neighbor 1', 'similarity 1'])

