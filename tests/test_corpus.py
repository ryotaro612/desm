import os.path
from unittest import TestCase
from desm.corpus import Corpus
from desm.text import Text


class TestCorpus(TestCase):

    def setUp(self):
        self.corpus_text = os.path.join(os.path.dirname(__file__),
                                        'corpus.txt')

    def test_create_from_file(self):
        corpus = Corpus(self.corpus_text)
        with corpus() as f:
            self.assertEqual(
                list(f),
                [Text(text='もののは'), Text(text='あはれは秋こそ'), Text(text='まされ')])
