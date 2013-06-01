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
        prev = {}
        cost = {}
        deq = deque([])
        # initialize
        for key in self._graph:
            color[key] = "w"
        # add the start node to deque
        deq.append(start_node)
        color[start_node] = "g"
        prev[start_node] = 'root'
        cost[start_node] = 0

        while(deq):
            if verbose:
                print deq, color
            node = self._pop(deq)
            if node == name:
                return {'result': True,
                        'route': self._route(prev, node),
                        'color': color,
                        'cost': cost,
                        'deq': deq}
            else:
                for v in [v for v in self._graph.neighbors(node)
                          if color[v] == "w"]:
                    color[v] = "g"
                    prev[v] = node
                    cost[v] = cost[node] + 1
                    deq.append(v)
            color[node] = "b"
        return {'result': False,
                'route': None,
                'color': color,
                'cost': cost,
                'deq': deq}

    def _route(self, prev, node):
        n = node
        route = deque([])
        while (n != 'root'):
            route.append(n)
            n = prev[n]
        return route


class DFS(GraphSearchWrapper):
    def _pop(self, deq):
        return deq.pop()


class WFS(GraphSearchWrapper):
    def _pop(self, deq):
        return deq.popleft()


if __name__ == '__main__':
    import networkx as nx
    from pprint import pprint
    g = nx.Graph()
    g.add_weighted_edges_from([
        ('a', 't', 118),
        ('t', 'l', 111),
        ('l', 'm', 70),
        ('m', 'd', 75),
        ('d', 'c', 120),
        ('c', 'r', 146),
        ('c', 'p', 138),
        ('r', 'p', 97),
        ('r', 's', 80),
        ('a', 's', 140),
        ('p', 'b', 101),
        ('b', 'g', 90),
        ('b', 'u', 85),
        ('b', 'f', 211),
        ('s', 'f', 99),
        ('a', 'z', 75),
        ('z', 'o', 71),
        ('o', 's', 151)])
    start = 'a'
    goal = 'b'
    pprint(DFS(g).search(start, goal))  # , verbose=True)
    pprint(WFS(g).search(start, goal))  # , verbose=True)
    pprint(DFS(g).search(start, goal))  # , verbose=True)
    pprint(WFS(g).search(start, goal))  # , verbose=True)
