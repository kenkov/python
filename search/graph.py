#! /usr/bin/env python
# coding:utf-8

from __future__ import division
from collections import deque
import abc


class GraphSearchWrapper(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, graph):
        self._graph = graph

    @property
    def graph(self):
        return self._graph

    @abc.abstractmethod
    def _pop(self, deq):
        pass

    def search(self, name, start_node, verbose=False):
        color = {}
        deq = deque([])
        # initialize
        for key in self._graph:
            color[key] = "w"
        # add the start node to deque
        deq.append(start_node)
        color[start_node] = "g"

        while(deq):
            if verbose:
                print deq, color
            node = self._pop(deq)
            if node == name:
                return True
            else:
                for v in [v for v in self._graph.neighbors(node)
                          if color[v] == "w"]:
                    color[v] = "g"
                    deq.append(v)
            color[node] = "b"
        return False


class DFS(GraphSearchWrapper):
    def _pop(self, deq):
        return deq.pop()


class WFS(GraphSearchWrapper):
    def _pop(self, deq):
        return deq.popleft()


if __name__ == '__main__':
    import networkx as nx
    g = nx.Graph([(1, 2), (1, 3), (2, 3),
                  (3, 4), (4, 5)])
    print DFS(g).search(5, 1, verbose=True)
    print WFS(g).search(5, 1, verbose=True)
    print DFS(g).search(2, 1, verbose=True)
    print WFS(g).search(2, 1, verbose=True)
