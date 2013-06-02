#! /usr/bin/env python
# coding:utf-8

from __future__ import division

if __name__ == '__main__':
    from collections import deque
    from benchmarker import Benchmarker

    # initialize
    deq = deque(range(100000))
    h = range(100000)

    for bm in Benchmarker(width=20, loop=1000000, cycle=3, extra=1):
        for _ in bm.empty():
            pass
        for _ in bm('deque'):
            deq.append(100001)
            deq.pop()
        for _ in bm('list'):
            h.append(100001)
            h.pop(100000)
