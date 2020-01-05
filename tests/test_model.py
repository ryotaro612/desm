from unittest import TestCase
from unittest.mock import MagicMock, call, patch
import numpy as np
import gensim.models.keyedvectors as kv
import desm.model as m
import desm.keyword as k
import desm.query as q
import desm.document as d
import desm.similar as si


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

    @patch('desm.model.Desm._to_query_vectors', side_effect=ValueError)
    def test_rank_return_to_query_vectors_none(self, to_query_vectors):
        """Return None.

        _to_query_vectors raise Error.

        """
        query = q.Query([])
        document = d.Document([])
        self.assertFalse(self.target.rank(query, document))

    @patch('desm.model.Desm._to_embedding_document', side_effect=ValueError)
    def test_rank_return_to_embedding_document_none(
            self, to_embedding_document):
        """Return None.

        _to_embedding_document raise Error.

        """
        query = q.Query([])
        document = d.Document([])
        self.assertFalse(self.target.rank(query, document))

    @patch('desm.model.Desm._to_query_vectors',
           return_value=np.array([[1, 2, 3], [4, 5, 6]]))
    @patch('desm.model.Desm._to_embedding_document',
           return_value=np.array([1, 2, 1]))
    def test_rank(self, to_embedding_document, to_query_vectors):
        query = q.Query([k.Keyword('a')])
        document = d.Document(['a', 'quick'])
        self.assertEqual(
            self.target.rank(query, document),
            si.SimilarityScore(np.float32(14.0)))

    def test_to_embedding_document_raise(self):
        """Raise ValueError.

        Raise ValueError if document does not contain acknowledged kewyords.

        """
        document = d.Document([])
        with self.assertRaises(ValueError):
            self.target._to_embedding_document(document)

    def test_to_embedding_document(self):
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

        expected = np.array([0.70710677, 0.70710677])
        self.assertTrue((actual - expected < 0.001).all())

    def test_to_query_vectors_raise(self):
        """Raise ValueError

        Raise ValueError if query does not contain any acknowledged keywords.

        """
        query = q.Query([])
        with self.assertRaises(ValueError):
            self.target._to_query_vectors(query)

    def test_to_query_vectors_one(self):
        """_to_query_vectors can handle a query with one keyword."""
        query = q.Query([k.Keyword('a')])

        def contains(k):
            return True

        def getitem(k):
            if k == 'a':
                return np.array([0.1, 0.2, 0.3])

        self.query_keyed_vectors.__contains__.side_effect = contains
        self.query_keyed_vectors.__getitem__.side_effect = getitem

        actual = self.target._to_query_vectors(query)

        self.assertEqual(actual.shape, (1, 3))
        np.testing.assert_approx_equal(np.linalg.norm(actual, ord=2, axis=1),
                                       np.array([1.0]))

    def test_to_query_vectors_multi(self):
        query = q.Query([k.Keyword('a'), k.Keyword('quick')])

        def contains(k):
            return True

        def getitem(k):
            if k == 'a':
                return np.array([0.1, 0.2, 0.3])
            if k == 'quick':
                return np.array([0.3, 0.2, 0.1])

        self.query_keyed_vectors.__contains__.side_effect = contains
        self.query_keyed_vectors.__getitem__.side_effect = getitem

        actual = self.target._to_query_vectors(query)

        self.assertEqual(actual.shape, (2, 3))
        self.assertTrue(
            (np.linalg.norm(actual, ord=2, axis=1) - np.array([1.0, 1.0])
             < 0.001).all())
