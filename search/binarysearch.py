#! /usr/bin/env python
# coding:utf-8

import bisect


def search(a, x):
    """Find the rightmost index of which value equals to x

    The argument a must be sorted. If the value x is not found in a,
    ValueError will be returned.
    """
    i = bisect.bisect(a, x)
    if i != len(a) and a[i-1] == x:
        return i - 1
    else:
        raise ValueError("{0} is not found".format(x))


def search_right(a, x):
    return search(a, x)


def search_left(a, x):
    """Find the leftmost index of which value equals to x

    The argument a must be sorted. If the value x is not found in a,
    ValueError will be returned.
    """
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        raise ValueError("{0} is not found".format(x))


def main():
    a = sorted([1, 3, 3, 5, 6, 7, 9])

    assert search(a, 3) == 2
    try:
        print search(a, 2)
    except ValueError:
        pass

    assert search_left(a, 3) == 1
    try:
        print search_right(a, 2)
    except ValueError:
        pass


if __name__ == '__main__':
    main()
