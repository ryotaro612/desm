from unittest import TestCase
from unittest.mock import MagicMock, call, patch
import gensim.models.keyedvectors as kv
import desm.model as m
import desm.keyword as k
import desm.query as q
import desm.document as d


class TestDesm(TestCase):

    def setUp(self):
        self.query_keyed_vectors = MagicMock(
            spec=kv.Word2VecKeyedVectors)
        self.document_keyed_vectors = MagicMock(
            spec=kv.Word2VecKeyedVectors)

        self.target = m.Desm(self.query_keyed_vectors,
                             self.document_keyed_vectors)

    def test_is_acknowledged_keyword(self):
        """Accept Keyword value."""
        self.query_keyed_vectors.__contains__.return_value = True
        raw_keyword = 'キーワード'
        keyword = k.Keyword(raw_keyword)

        actual = self.target.is_acknowledged(keyword)

        self.assertTrue(actual)
        self.assertEqual(
            self.query_keyed_vectors.__contains__.call_args_list,
            [call(raw_keyword)])

    def test_rank_raise(self):
        """Raise KeyError if query is not acknowledged."""
        query = q.Query('doge')
        document = d.Document(['a', 'quick', 'brown', 'fox'])
        self.query_keyed_vectors.__getitem__.side_effect = KeyError
        with self.assertRaises(KeyError):
            self.target.rank(query, document)
