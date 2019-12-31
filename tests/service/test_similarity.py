from unittest import TestCase
from unittest.mock import MagicMock, call
import desm.service.similarity as s
import desm.similar as si


class TestSimilarKeywordGenerator(TestCase):

    def test(self):
        """Yield SimilarKeywords object at a time."""
        desm = MagicMock()
        keyword1, keyword2 = MagicMock(), MagicMock()

        def is_acknowledged(keyword):
            return True if keyword == keyword1 else False

        desm.is_acknowledged.side_effect = is_acknowledged
        target = s.SimilarKeywordGenerator(desm)
        keywords = [keyword1, keyword2]
        top_n = MagicMock()

        actual = list(target(top_n, keywords))
        expected = [si.SimilarKeywords(
            keyword1,
            desm.find_similar_keywords.return_value)]
        self.assertEqual(actual, expected)
        self.assertEqual(desm.find_similar_keywords.call_args_list,
                         [call(top_n, keyword1)])
