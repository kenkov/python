#! /usr/bin/env python
# coding:utf-8

from __future__ import division
from collections import deque, defaultdict
import re
import abc
import itertools


class Adjenda(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, container):
        self._container = container
        self._adjenda_set = set()

    def __getattr__(self, name):
        getattr(self._container, name)

    @property
    def container(self):
        return self._container

    @abc.abstractmethod
    def _push(self, item):
        pass

    @abc.abstractmethod
    def _pop(self):
        pass

    def push(self, item):
        if item not in self._adjenda_set:
            self._push(item)
            self._adjenda_set.add(item)

    def pop(self):
        item = self._pop()
        self._adjenda_set.remove(item)
        return item

    @abc.abstractmethod
    def is_empty(self):
        pass


class ChartParser(object):
    def __init__(self, grammar):
        self._grammar = grammar

    @abc.abstractmethod
    def _deq(self):
        pass

    def terminals(self, grammar):
        """Collect word_names which has a "N -> 'word_name'" shape from
        grammar."""
        re_obj = re.compile(ur"^'\w+'$")
        ret = []
        for item in grammar:
            if re_obj.search(item[1]):
                ret.append(item)
        return ret

    def _dict_set_factory(self):
        '''define a local function for uniform probability initialization'''
        return itertools.repeat(defaultdict(set)).next

    def search(self, sent, verbose=False):
        adjenda = self._deq()
        # grammar dicts
        #gr_left = defaultdict(list)
        gr_right = defaultdict(list)
        for item in self._grammar:
            #gr_left[item[0]].append(item)
            gr_right[item[1]].append(item)

        # initial arcs
        init_arcs = defaultdict(dict)
        for k, v in self.terminals(self._grammar):
            init_arcs[v][k] = v

        # initialize
        for i, w in enumerate(sent):
            for lefths, word in init_arcs[w].items():
                adjenda.push((lefths, tuple([word]), tuple([]), (i, i+1)))

        # initialize chart
        chart = defaultdict(set)
        chart_init = defaultdict(self._dict_set_factory())
        chart_after = defaultdict(self._dict_set_factory())
        while not adjenda.is_empty():
            init, before, after, (start, end) = adjenda.pop()
            if start == end:
                arc = "self"
            elif after:
                arc = "incomp"
            else:
                arc = "comp"
            pretprit = self.pretty_print(init, before, after, sent,
                                         start, end, arc, size=10)
            # add to chart
            # Use set to remove deplicated items
            chart[(start, end)].add((init, before, after))
            chart_init[init][(start, end)].add((init, before, after))
            if after:
                #print "    after add {} -> {}・{}".format(init, before, after)
                #print after[0]
                chart_after[after[0]][(start, end)].add((init,
                                                        before,
                                                        after))
            # active edge
            if after:
                y = after[0]
                for (s, e), arcs in chart_init[y].items():
                    if s == end:
                        for _ in [arc for arc in arcs if not arc[2]]:
                            adjenda.push((init,
                                          tuple(before + tuple([y])),
                                          tuple(after[1:]),
                                          (start, e)))
                            if verbose:
                                verbs = self._verbose(
                                    s, e, arc[0], arc[1], arc[2],
                                    start, end, init, before, after)

            else:
                #print chart_after
                #print chart
                for (s, e), arcs in chart_after[init].items():
                    if e == start:
                        for arc in arcs:
                            adjenda.push((arc[0],
                                          tuple(arc[1] + tuple([arc[2][0]])),
                                          tuple(arc[2][1:]),
                                          (s, end)))
                            if verbose:
                                verbs = self._verbose(
                                    start, end, init, before, after,
                                    s, e, arc[0], arc[1], arc[2])

            # recommend new arc
            if not after:
                if init in gr_right:
                    for gr in gr_right[init]:
                        adjenda.push((gr[0],
                                      tuple([]),
                                      tuple(gr[1:]),
                                      (start, start)))
                        if verbose:
                            verbs = "add new arc"

            if verbose:
                print "{}  {}".format(pretprit, verbs)
            else:
                print pretprit
        return adjenda

    def _verbose(self, start, end, init, before, after,
                 _start, _end, _init, _before, _after):
        lh = "({}, {}) {} -> {}・{}".format(
            _start, _end,
            _init,
            " ".join(_before),
            " ".join(_after))

        rh = "({}, {}) {} -> {}・{}".format(
            start, end,
            init,
            " ".join(before),
            " ".join(after))
        return "    merge {} , {}".format(lh, rh)

    def _pretty_print(self, ln, start, end, arc, size=5):
        default = "." + " " * (size - 1)
        comp = "." + "=" * (size - 1)
        incomp = "." + "-" * (size - 2) + ">"
        incomp_not_finished = "." + "-" * (size - 1)
        self = "." + ">" + " " * (size - 2)
        if not arc in ["comp", "incomp", "self"]:
            raise Exception()
        if arc == "self":
            s = default * start + self + default * (ln - end - 1)
        elif arc == "comp":
            s = default * start + comp * (end - start) + default * (ln - end)
        elif arc == "incomp":
            s = default * start + incomp_not_finished \
                * (end - start - 1) + incomp + default * (ln - end)
        return s + "."

    def pretty_print(self, init, before, after,
                     sent, start, end, arc, size=10):
        if arc == "self":
            s = self._pretty_print(
                len(sent), start, end, "self", size)
        elif arc == "incomp":
            s = self._pretty_print(
                len(sent), start, end, "incomp", size)
        elif arc == "comp":
            s = self._pretty_print(
                len(sent), start, end, "comp", size=10)
        else:
            raise Exception('Specify "self", "comp", or "incomp"')
        detail = ("({}, {}) : " + "{} -> {}・{}").format(
            start,
            end,
            init,
            " ".join(before),
            " ".join(after))
        return "{}  {}".format(s, detail)


class QueueAdjenda(Adjenda):
    def __init__(self):
        Adjenda.__init__(self, deque([]))

    def _push(self, item):
        return self._container.append(item)

    def _pop(self):
        return self._container.popleft()

    def is_empty(self):
        return False if self._container else True


class StackAdjenda(Adjenda):
    def __init__(self):
        Adjenda.__init__(self, [])

    def _push(self, item):
        return self._container.append(item)

    def _pop(self):
        return self._container.pop()

    def is_empty(self):
        return False if self._container else True


class BUChartParser(ChartParser):
    def _deq(self):
        return QueueAdjenda()


class DepthBUChartParser(ChartParser):
    def _deq(self):
        return StackAdjenda()


def test_terminals():
    grammar = [["S", "NP", "VP"],
               ["S", "NP", "VP", "NP"],
               ["VP", "V", "NP"],
               ["NP", "N"],
               ["NP", "'Lee'"],
               ["NP", "'coffee'"],
               ["V", "'likes'"]]
    parser = BUChartParser(grammar)
    assert parser.terminals(grammar) == [['NP', "'Lee'"],
                                        ['NP', "'coffee'"],
                                        ['V', "'likes'"]]


def main():
    grammar = [["S", "NP", "VP"],
               ["VP", "V", "NP"],
               ["NP", "N"],
               ["NP", "'Lee'"],
               ["NP", "'coffee'"],
               ["V", "'likes'"]]
    sent = ["".join(["'", w, "'"]) for w in "Lee likes coffee".split()]
    parser = BUChartParser(grammar)
    res = parser.search(sent, verbose=True)
    print res
    dparser = DepthBUChartParser(grammar)
    res = dparser.search(sent, verbose=True)
    print res


if __name__ == '__main__':
    test_terminals()
    main()
