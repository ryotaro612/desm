import os.path
from unittest import TestCase
import desm.first_class_collection as fcc


class Double(fcc.FirstClassFileContextManagerProvider):

    def transform(self, item):
        return len(item)


class TestFirstClassFileContextManagerProvider(TestCase):

    def test_call(self):
        module_dir = os.path.dirname(__file__)
        testdata = os.path.join(module_dir,
                                'first_class_collection_call_test.txt')
        target = Double(testdata)

        with target() as stream:
            self.assertEqual([3, 5], list(stream))

