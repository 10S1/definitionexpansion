import unittest

from cnltransforms.gfxml import X, build_tree


class TestGfXml(unittest.TestCase):
    def test_nested_wrap(self):
        xs = [
            X('0', [], {}),
            X('1', [], {}),
            X('2', [], {}),
        ]
        ast_str = 'f1 (wrap_a (tag 0) (wrap_b (tag 1) f2))'
        build_tree(xs, ast_str)
        # TODO: check if output is ast_str modulo whitespace and redundant parens