import unittest

from cnltransforms.treeutils import get_pgf


class TestPgf(unittest.TestCase):
    def test_type(self):
        pgf = get_pgf()
        self.assertEqual(pgf.functionType('property_with_arg').cat, 'Property')
