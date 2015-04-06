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
