from cidrtrie import Trie, DuplicateKeyError
import unittest

from mock import sentinel as s


class TrieTestCase(unittest.TestCase):
    def setUp(self):
        self.t = Trie()
        self.t.insert('abc', s.obj1)
        self.t.insert('abcde', s.obj2)
        self.t.insert('abcdef', s.obj3)

    def test_basic(self):
        t = Trie()
        t.insert('abcdef', s.foo)
        self.assertEqual(t.find('abcdef'), ('abcdef', s.foo))

    def test_find_shortest_prefix(self):
        result = self.t.find('abcdef', Trie.MODE_SHORTEST_PREFIX)
        self.assertEqual(result, ('abc', s.obj1))

    def test_find_longest_prefix(self):
        result = self.t.find('abcdeg', Trie.MODE_LONGEST_PREFIX)
        self.assertEqual(result, ('abcde', s.obj2))

    def test_find_exact_match(self):
        self.assertRaises(KeyError, self.t.find, 'abcdeg', Trie.MODE_EXACT_ONLY)
        self.assertEqual(self.t.find('abcdef'), ('abcdef', s.obj3))

    def test_no_dups(self):
        t = Trie()
        t.insert('abcdef', s.foo)
        self.assertRaises(DuplicateKeyError, t.insert, 'abcdef')


# vim: set textwidth=120:
