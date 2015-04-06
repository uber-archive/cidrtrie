import collections
import struct
import socket


class DuplicateKeyError(Exception):
    pass


class _TrieNode(object):
    def __init__(self, value, terminal=False, data=None, children=None):
        self.value = value
        self.terminal = terminal
        self.data = data
        if children:
            self.children = children
        else:
            self.children = {}

    def __contains__(self, item):
        return item in self.children

    def __getitem__(self, value):
        return self.children[value]

    def add_child(self, value):
        assert value not in self
        new_node = _TrieNode(value)
        self.children[value] = new_node
        return new_node

    def __repr__(self):
        return 'TrieNode(%r, terminal=%r) @ %s' % (self.value, self.terminal, id(self))


class Trie(object):
    """A trie (a.k.a. prefix tree) stores a sequence such that lookups take O(m) time (where m is the number of items
    in the sequence), as opposed to the usual O(log n) time (where n is the number of items in the tree). It's commonly
    used for doing efficient prefix lookups over large corpuses of data, such as IP routes.

    This implementation doesn't include Patricia merging.
    """

    MODE_SHORTEST_PREFIX = 0
    MODE_LONGEST_PREFIX = 1
    MODE_EXACT_ONLY = 2

    def __init__(self):
        self.root = _TrieNode(None)

    def insert(self, string, data=None):
        """Insert a string into the trie, optionally with some attached data"""
        current = self.root
        for character in string:
            if character in current:
                current = current[character]
            else:
                current = current.add_child(character)
        if current.terminal:
            raise DuplicateKeyError(string)
        current.terminal = True
        current.data = data

    def find(self, string, mode=MODE_LONGEST_PREFIX):
        """Find a string in the Trie.

        :param mode: one of SHORTEST_PREFIX, LONGEST_PREFIX, EXACT_ONLY
          SHORTEST_PREFIX finds the *first* matching terminal noode
          LONGEST_PREFIX behaves like IP routing and uses the most specific
            prefix
          EXACT_MATCH is for when you want to use this to back a dictionary
        """
        current = self.root
        path = []
        if current.terminal and mode == self.MODE_SHORTEST_PREFIX:
            return '', current.data
        for character in string:
            if character in current:
                current = current[character]
                path.append(current)
                if current.terminal and mode == self.MODE_SHORTEST_PREFIX:
                    return ''.join(p.value for p in path), current.data
            else:
                break
        else:
            # got to the end without breaking == we found it exactly
            if current.terminal:
                return ''.join(p.value for p in path), current.data
        # crap, we reached a node that doesn't match somewhere. backtrack to
        # find the last terminal node in the path
        if mode == self.MODE_LONGEST_PREFIX:
            for i in reversed(range(len(path))):
                if path[i].terminal:
                    return ''.join(p.value for p in path[:i+1]), path[i].data
            if self.root.terminal:
                return '', self.root.data
        raise KeyError(string)


def _ip_to_binary_string(ip):
    integer = struct.unpack('!L', socket.inet_aton(ip))[0]
    binary = bin(integer)[2:].zfill(32)
    return binary


CidrResult = collections.namedtuple('CidrResult', ['base', 'mask', 'data'])


class CidrClassifier(object):
    """Look up IPs in a corpus of cidr prefixes"""
    def __init__(self):
        self.trie = Trie()

    def add_mapping(self, base, mask, value):
        """Add a mapping that base/mask -> value"""
        string = _ip_to_binary_string(base)[:mask]
        self.trie.insert(string, (mask, value))

    def lookup(self, ip, return_unroutable=False):
        """Look up an IP's value"""
        string = _ip_to_binary_string(ip)
        try:
            prefix, (mask, data) = self.trie.find(string)
            prefix = prefix + '0'*(32 - len(prefix))
            prefix = int(prefix, 2)
            prefix = socket.inet_ntoa(struct.pack('!L', prefix))
            return CidrResult(prefix, mask, data)
        except KeyError:
            if return_unroutable:
                base = '0.0.0.0'
                mask = 0
                data = 0
                return CidrResult(base, mask, data)
            else:
                raise
