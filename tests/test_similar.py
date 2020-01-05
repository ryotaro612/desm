from unittest import TestCase
from unittest.mock import MagicMock
import numpy as np
import desm.similar as s
import desm.keyword as k


class TestSimilarities(TestCase):

    def test_sequence(self):
        similarities = [MagicMock()]
        target = s.Similarities(similarities)
        self.assertEqual(target.sequence, similarities)

    def test_create_from_tuples(self):
        score = np.float32(0.2)
        similarities = iter([('a', score)])
        actual = s.Similarities.create_from_tuples(similarities)

        self.assertEqual(actual, s.Similarities(
            [s.Similarity(k.Keyword('a'),
                          s.SimilarityScore(score))]))


class TestSimilarKeywords(TestCase):

    def test_get_similarity_tuples(self):
        keyword = k.Keyword('dog')
        raw_score = np.float32(0.1234)
        similarity = s.Similarity(
            k.Keyword('cat'), s.SimilarityScore(raw_score))
        similarities = s.Similarities([similarity])

        actual = s.SimilarKeywords(
            keyword, similarities).get_similarity_tuples()

        self.assertEqual(actual, [('cat', raw_score)])
