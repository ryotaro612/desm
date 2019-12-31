from unittest import TestCase
from unittest.mock import MagicMock
import desm.similar as s


class TestSimilarities(TestCase):

    def test_sequence(self):
        similarities = [MagicMock()]
        target = s.Similarities(similarities)
        self.assertEqual(target.sequence, similarities)
