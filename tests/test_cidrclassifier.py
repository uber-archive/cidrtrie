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

from cidrtrie import CidrClassifier
import unittest


class CidrClassifierTestCase(unittest.TestCase):
    def test_basic(self):
        c = CidrClassifier()
        c.add_mapping('0.0.0.0', 0, 'NONE')
        c.add_mapping('192.168.0.0', 16, 'RFC1918')
        c.add_mapping('104.36.192.0', 21, 'Uber')
        c.add_mapping('104.36.192.0', 22, 'Uber1')
        self.assertEqual(c.lookup('104.36.192.1'), ('104.36.192.0', 22, 'Uber1'))
        self.assertEqual(c.lookup('104.36.196.1'), ('104.36.192.0', 21, 'Uber'))
        self.assertEqual(c.lookup('192.168.0.0'), ('192.168.0.0', 16, 'RFC1918'))
        self.assertEqual(c.lookup('192.1.0.0'), ('0.0.0.0', 0, 'NONE'))


# vim: set textwidth=120:
