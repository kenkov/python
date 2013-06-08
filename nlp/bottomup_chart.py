#! /usr/bin/env python
# coding:utf-8

from __future__ import division
from collections import deque, defaultdict
import re


def tdchart(grammar, sent, verbose=False):
    # grammar dicts
    gr_left = defaultdict(list)
    gr_right = defaultdict(list)
    for item in grammar:
        gr_left[item[0]].append(item)
        gr_right[item[1]].append(item)

    # adjenda
    adjenda = deque([])
    # init_ads = {"'likes'": ('V', "'likes'"),
    #             "'coffee'": ('NP', "'coffee'"),
    #             "'Lee'": ('NP', "'Lee'")}

    ## MUST MODIFY for duplicated v
    init_ads = defaultdict(list)
    for k, v in terminals(grammar):
        init_ads[v].append((k, v))

    # initialize
    for i, w in enumerate(sent):
        for start, word in init_ads[w]:
            adjenda.append([start, [word], [], (i, i+1)])
    #print adjenda
    chart = defaultdict(list)
    chart_init = defaultdict(dict)
    chart_after = defaultdict(dict)
    while adjenda:
        init, before, after, (start, end) = adjenda.popleft()
        if start == end:
            print prety_print(len(sent), start, end, "self", size=10),
        elif after:
            print prety_print(len(sent), start, end, "incomp", size=10),
        else:
            print prety_print(len(sent), start, end, "comp", size=10),

        print "  arc:", "{}->{}.{}, ({}, {})".format(init,
                                                     before,
                                                     after,
                                                     start,
                                                     end)
        # add to chart
        chart[(start, end)].append([init, before, after])
        if (start, end) in chart_init[init]:
            chart_init[init][(start, end)].append([init, before, after])
        else:
            chart_init[init][(start, end)] = [[init, before, after]]
        if after:
            if after[0] in chart_after[init]:
                chart_after[after[0]][(start, end)].append(
                    [init, before, after])
            else:
                chart_after[after[0]][(start, end)] = [[init, before, after]]

        # active edge
        if after:
            y = after[0]
            for (s, e), arcs in chart_init[y].items():
                if s == end:
                    for _ in arcs:
                        adjenda.append([init,
                                        before + [y],
                                        after[1:],
                                        (start, e)])
                        if verbose:
                            print "    add:", "{}->{}.{}, ({}, {})".format(
                                init,
                                before + [y],
                                after[1:],
                                start, e)
        else:
            for (s, e), arcs in chart_after[init].items():
                if e == start:
                    for arc in arcs:
                        adjenda.append([arc[0],
                                        arc[1] + [arc[2][0]],
                                        arc[2][1:],
                                        (s, end)])
                        if verbose:
                            print "    add", "{}->{}.{}, ({}, {})".format(
                                arc[0],
                                arc[1] + [arc[2][0]],
                                arc[2][1:],
                                s, end)
        # recommend new arc
        if not after:
            if init in gr_right:
                for gr in gr_right[init]:
                    adjenda.append([gr[0],
                                    [],
                                    gr[1:],
                                    (start, start)])
                    if verbose:
                        print "    add", "{}->{}.{}, ({}, {})".format(
                            gr[0],
                            [],
                            gr[1:],
                            start, start)


def terminals(grammar):
    re_obj = re.compile(ur"^'\w+'$")
    ret = []
    for item in grammar:
        if re_obj.search(item[1]):
            ret.append(item)
    return ret


def prety_print(ln, start, end, arc, size=5):
    default = "." + " " * (size - 1)
    comp = "." + "=" * (size - 1)
    incomp = "." + "-" * (size - 2) + ">"
    self = "." + ">" + " " * (size - 2)
    if not arc in ["comp", "incomp", "self"]:
        raise Exception()
    if arc == "self":
        s = default * start + self + default * (ln - end - 1)
    elif arc == "comp":
        s = default * start + comp * (end - start) + default * (ln - end)
    elif arc == "incomp":
        s = default * start + incomp * (end - start) + default * (ln - end)
    return s + "."


def main():
    grammar = [["S", "NP", "VP"],
               ["VP", "V", "NP"],
               ["NP", "N"],
               ["NP", "'Lee'"],
               ["NP", "'coffee'"],
               ["V", "'likes'"]]
    sent = ["".join(["'", w, "'"]) for w in "Lee likes coffee".split()]
    tdchart(grammar, sent)
    assert terminals(grammar) == [['NP', "'Lee'"],
                                  ['NP', "'coffee'"],
                                  ['V', "'likes'"]]
if __name__ == '__main__':
    main()
