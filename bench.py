import contextlib
import random
import time
import socket
import struct
import operator

import ipcalc

from cidrtrie import CidrClassifier, CidrResult


class NaiveCidrClassifier(object):
    def __init__(self):
        self.cidrs = []

    def add_mapping(self, base, mask, value):
        base = struct.unpack('!L', socket.inet_aton(base))[0]
        omask = mask
        mask = (0xffffffff >> (32 - mask)) << (32 - mask)
        base = base & mask
        self.cidrs.append((base, mask, omask, value))

    def lookup(self, ip):
        ip = struct.unpack('!L', socket.inet_aton(ip))[0]
        matches = []
        for base, mask, omask, value in self.cidrs:
            if ip & mask == base:
                matches.append((base, mask, omask, value))
        matches.sort(key=operator.itemgetter(1), reverse=True)
        base, mask, omask, value = matches[0]
        return CidrResult(
            base=socket.inet_ntoa(struct.pack('!L', base)),
            mask=omask,
            data=value
        )


def generate_random_data(count):
    d = []
    seen = set()
    random.seed(4)
    while len(d) < count:
        base = socket.inet_ntoa(struct.pack('!L', random.randint(0, 1 << 32)))
        mask = random.randint(1, 32)
        canon = ipcalc.Network('%s/%d' % (base, mask)).network().hex()
        if (canon, mask) in seen:
            continue
        seen.add((canon, mask))
        d.append((base, mask, 0))
    return d


def generate_random_ips(count):
    d = []
    for _ in xrange(count):
        ip = socket.inet_ntoa(struct.pack('!L', random.randint(0, 1 << 32)))
        d.append(ip)
    return d


def bench_insert(impl, prefix_data):
    for base, mask, value in prefix_data:
        impl.add_mapping(base, mask, value)


def bench_lookup(impl, keys):
    res = []
    for key in keys:
        res.append(impl.lookup(key))
    return res


@contextlib.contextmanager
def time_simple(title, resd):
    start = time.time()
    yield
    end = time.time()
    resd[title] = end - start


def bench():
    # order of magnitude # of routes on the internet == normal use case
    data = generate_random_data(100000)
    keys = generate_random_ips(10000)
    results = {}

    c = CidrClassifier()
    n = NaiveCidrClassifier()

    c.add_mapping('0.0.0.0', 0, 'Base')
    n.add_mapping('0.0.0.0', 0, 'Base')

    with time_simple('insert CidrClassifier', results):
        bench_insert(c, data)

    with time_simple('insert NaiveCidrClassifier', results):
        bench_insert(n, data)

    with time_simple('lookup CidrClassifier', results):
        r1 = bench_lookup(c, keys)

    with time_simple('lookup NaiveCidrClassifier', results):
        r2 = bench_lookup(n, keys)

    assert r1 == r2

    for k, v in sorted(results.iteritems()):
        print '%s %.2fs' % (k, v)


bench()
