#! /usr/bin/env python
# coding:utf-8

from __future__ import division
from collections import deque
import abc


class Container(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, container):
        self._container = container
        self.color = {}
        self.prev = {}
        self.cost = {}
        self.g = {}
        self.f = {}

    def __getattr__(self, name):
        getattr(self._container, name)

    @property
    def container(self):
        return self._container

    @abc.abstractmethod
    def push(self, item, cost):
        pass

    @abc.abstractmethod
    def pop(self):
        pass

    @abc.abstractmethod
    def is_empty(self):
        pass


class GraphSearch(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, graph):
        self._graph = graph

    @property
    def graph(self):
        return self._graph

    @abc.abstractmethod
    def _container(self):
        pass

    def _f_func(self, node, container):
        """If you want to implement A* algorithm, you must
        implement this methos in the inherited class"""
        return 0

    def _g_func(self, node, container):
        """If you want to implement A* algorithm, you must
        implement this methos in the inherited class"""
        return container.cost[container.prev[node]] + 1

    def search(self, name, start_node, verbose=False):
        con = self._container()
        # initialize
        for key in self._graph:
            con.color[key] = "w"
        # add the start node to deque
        con.color[start_node] = "g"
        con.prev[start_node] = 'root'
        con.cost[start_node] = 0
        con.g[start_node] = 0
        con.f[start_node] = self._f_func(start_node, con)
        con.push(start_node, con.cost[start_node])

        while(not con.is_empty()):

            node, ct = con.pop()
            if node == name:
                return {'result': True,
                        'route': self._route(con.prev, node),
                        'color': con.color,
                        'cost': con.cost,
                        'container': con}
            else:
                for v in [v for v in self._graph.neighbors(node)
                          if con.color[v] == "w"]:
                    con.color[v] = "g"
                    con.prev[v] = node
                    con.g[v] = self._g_func(v, con)
                    con.f[v] = self._f_func(v, con)
                    con.cost[v] = con.g[v] + con.f[v]
                    con.push(v, con.cost[v])
            con.color[node] = "b"
        return {'result': False,
                'route': None,
                'color': con.color,
                'cost': con.cost,
                'container': con}

    def _route(self, prev, node):
        n = node
        route = deque([])
        while (n != 'root'):
            route.append(n)
            n = prev[n]
        return route


class DFSContainer(Container):
    def __init__(self):
        Container.__init__(self, [])

    def push(self, item, cost):
        return self._container.append((item, cost))

    def pop(self):
        return self._container.pop()

    def is_empty(self):
        return False if self._container else True


class WFSContainer(Container):
    def __init__(self):
        Container.__init__(self, deque([]))

    def push(self, item, cost):
        return self._container.append((item, cost))

    def pop(self):
        return self._container.popleft()

    def is_empty(self):
        return False if self._container else True


class AStarContainer(Container):
    def __init__(self):
        Container.__init__(self, deque([]))

    def push(self, item, cost):
        return self._container.append((cost, item))

    def pop(self):
        ct, node = self._container.popleft()
        return node, ct

    def is_empty(self):
        return False if self._container else True


class DFS(GraphSearch):
    def _container(self):
        return DFSContainer()


class WFS(GraphSearch):
    def _container(self):
        return WFSContainer()


class AStar(GraphSearch):
    def _container(self):
        return AStarContainer()

    def _g_func(self, node, container):
        weight = self._graph[container.prev[node]][node]['weight']
        return container.cost[container.prev[node]] + weight


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
    pprint(DFS(g).search(goal, start))  # , verbose=True)
    pprint(WFS(g).search(goal, start))  # , verbose=True)
    pprint(AStar(g).search(goal, start))  # , verbose=True)
