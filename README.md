`cidrtrie` is a simplistic implementation of a prefix tree and a library for classifying IP addresses based on prefix matching. Unlike other implementations (such as [py-radix](http://www.mindrot.org/projects/py-radix/)), this is pure-Python and aims to be as simple as possible.

## Why? ##
This implementation offers asymptotic performance improvement for problems that look like Internet routing.

`bench.py` contains a simple and used-elsewhere _O(n)_ implementation ("`NaiveCidrClassifier`) of this same functionalify. Some sample numbers for inserting 100,000 cidrs into the tree and then looking up 10,000 IPs on a 3GHz Intel i7-4578U:

    insert CidrClassifier 5.16s
    insert NaiveCidrClassifier 0.11s
    lookup CidrClassifier 0.25s
    lookup NaiveCidrClassifier 92.11s

An example use case would be to efficiently map IP addresses (from logs or some other source) to the originating network (and, eventually, to the owner) without using a commercial library like MaxMind or bringing in any native-code dependencies.
