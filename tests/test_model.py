from unittest import TestCase
from unittest.mock import MagicMock, call
import gensim.models.keyedvectors as kv
import desm.model as m
import desm.keyword as k


class TestDesm(TestCase):

    def test_is_acknowledged(self):
        query_keyed_vectors = MagicMock(
            spec=kv.Word2VecKeyedVectors)
        document_keyed_vectors = MagicMock(
            spec=kv.Word2VecKeyedVectors)

        target = m.Desm(query_keyed_vectors,
                        document_keyed_vectors)
        query_keyed_vectors.__contains__.return_value = True
        raw_keyword = 'キーワード'
        keyword = k.Keyword(raw_keyword)

        actual = target.is_acknowledged(keyword)

        self.assertTrue(actual)
        self.assertEqual(
                query_keyed_vectors.__contains__.call_args_list,
                [call(raw_keyword)])
