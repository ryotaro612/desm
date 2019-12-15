"""
"""
from unittest import TestCase
import desm.factory as f


class TestDouble:

    def double_kwargs(self, a, *args, **kwargs):
        pass

    def double(self, a):
        pass


class TestArgumentInspector(TestCase):

    def test_drop_invalid_arguments_unsupported(self):
        target = f.ArgumentInspector(TestDouble.double_kwargs, True)
        params = {'a': 2, 'b': 3}
        with self.assertRaises(NotImplementedError):
            target.drop_invalid_arguments(params)

    def test_filtered(self):
        target = f.ArgumentInspector(TestDouble.double, True)

        params = {'a': 2, 'b': 3}

        actual = target.drop_invalid_arguments(params)

        self.assertEqual(
            actual, {'a': 2},
            'Return only the entries that the keys '
            'are members of the parameters.')
