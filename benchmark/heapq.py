#! /usr/bin/env python
# coding:utf-8

from __future__ import division
import heapq
import bintrees
import random


if __name__ == '__main__':
    from benchmarker import Benchmarker
    from itertools import repeat, izip
    from bintrees import FastRBTree

    # initialize heapq
    h = range(10000)
    heapq.heapify(h)
    # initialize AVLTree
    m = izip(xrange(10000), repeat(True))
    t = FastRBTree(m)

    for bm in Benchmarker(width=20, loop=100000, cycle=3, extra=1):
        for _ in bm.empty():
            pass
        for _ in bm('heapq'):
            heapq.heappop(h)
            heapq.heappush(h, random.randint(-100000, 100000))
        for _ in bm('FastRBTree'):
            t.pop_min()
            t[random.randint(-100000, 100000)] = True
