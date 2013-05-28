#! /usr/bin/env python
# coding:utf-8

import heapq


def heapsort(iterable):
    h = []
    for value in iterable:
        heapq.heappush(h, value)
    return (heapq.heappop(h) for _ in range(len(h)))


if __name__ == "__main__":
    ans = heapsort([1, 4, 2, 5, 6, 4, 2, 1, 6, 4, 10])
    print list(ans)
