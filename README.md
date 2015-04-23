`cidrtrie` is a dumb implementation of a prefix tree and a library for classifying IP addresses based on prefix matching. I know that there other implementations (like [py-radix](http://www.mindrot.org/projects/py-radix/)) that are faster or whatever, but this one is simple and pure-Python.

## Why? ##
`bench.py` contains a simple _O(n)_ implementation (`NaiveCidrClassifier`)of this which I've seen in a few dozen projects (compared with the O(32) prefix tree). Some sample numbers for inserting 100,000 cidrs into the tree and then looking up 10,000 IPs:

    insert CidrClassifier 5.16s
    insert NaiveCidrClassifier 0.11s
    lookup CidrClassifier 0.25s
    lookup NaiveCidrClassifier 92.11s

So, yeah, that's why.

I use it to load in a mapping from CIDRs to ASNs from our edge routers and then efficiently map hundreds of thousands of IPs from log data to the corresponding ASN (which I can then translate into an actual owner through WHOIS).
