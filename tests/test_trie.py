# Copyright (c) 2015 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
