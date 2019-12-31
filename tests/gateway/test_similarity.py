from unittest import TestCase
import os.path
import numpy as np
import tempfile
import desm.similar as si
import desm.keyword as k
import desm.gateway.similarity as s


class TestSimilarityGateway(TestCase):

    def setUp(self):
        self.filename = tempfile.mkstemp()[1]
        self.target = s.SimilarityGateway(self.filename)

    def tearDown(self):
        os.remove(self.filename)

    def test_write_similar_keywords_empty(self):
        """Create an empty CSV file if iterator emits nothing."""
        self.target.write_similar_keywords([])
        with open(self.filename) as f:
            self.assertEqual(f.readlines(), [])

    def test_write_similar_kewyords(self):
        keyword = k.Keyword('test')
        similarity = si.Similarity(k.Keyword('flower'), np.float32(0.1))
        similarities = si.Similarities([similarity])
        similar_keywords = si.SimilarKeywords(keyword, similarities)
        similarities_iterator = iter([similar_keywords])
        self.target.write_similar_keywords(similarities_iterator)

        with open(self.filename) as f:
            actual = [line.strip() for line in f.readlines()]
        expected = ['keyword,neighbor 1,similarity 1', 'test,flower,0.1']
        self.assertEqual(actual, expected)
