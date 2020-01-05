from unittest import TestCase
from unittest.mock import MagicMock, call, patch
import numpy as np
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

    def test_rank_document_is_empty(self):
        """ValueError is raised.

        ValueError is raised if a document does not
        contain any acknowledged keywords.

        """
        query = q.Query([])
        document = d.Document([])

        with self.assertRaises(ValueError):
            self.target.rank(query, document)

    def test_rank_document_is_embedding(self):
        document = d.Document(['a', 'quick'])

        def getitem(k):
            if k == 'a':
                return np.array([0.2, 0.3]).reshape((2,))
            if k == 'quick':
                return np.array([0.3, 0.2]).reshape((2,))

        def contains(k):
            return True

        self.document_keyed_vectors.__contains__.side_effect = contains
        self.document_keyed_vectors.__getitem__.side_effect = getitem

        actual = self.target._to_embedding_document(document)

        expected = np.array([0.70710677, 0.70710677]).astype(np.float32)
        self.assertTrue(np.array_equal(actual, expected))
