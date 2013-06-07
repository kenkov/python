#! /usr/bin/env python
# coding:utf-8

from __future__ import division
from collections import deque


class Viterbi(object):
    def __init__(self, graph):
        self._graph = graph
        self._best_score = {}
        self._best_edge = {}

    @property
    def graph(self):
        return self._graph

    def search(self, start_node):
        self._best_score = {}
        self._best_edge = {}
        self._color = {}

        deq = deque([])
        # initialize
        for key in self._graph:
            self._color[key] = "w"
        self._best_score[start_node] = 0
        self._color[start_node] = "g"
        deq.append(start_node)
        while(deq):
            node = deq.popleft()
            for nnode in [nnode for nnode in self._graph.neighbors(node)
                          if self._color[nnode] in ["w", "g"]]:
                wei = self._graph[node][nnode]['weight'] + \
                    self._best_score[node]
                print wei, (node, nnode)
                if not nnode in self._best_score or \
                        wei < self._best_score[nnode]:
                    self._best_score[nnode] = wei
                    self._best_edge[nnode] = (node, nnode)
                if self._color[nnode] == "w":
                    deq.append(nnode)
                    self._color[nnode] = "g"
            self._color[node] = "b"


if __name__ == '__main__':
    import networkx as nx

    g = nx.Graph()
    g.add_weighted_edges_from([
        (0, 1, 2.5),
        (0, 2, 1.4),
        (1, 2, 4.0),
        (1, 3, 2.1),
        (2, 3, 2.3)])
    v = Viterbi(g)
    v.search(0)
    print v._best_edge, v._best_score
