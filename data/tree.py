#! /usr/bin/env python
# coding:utf-8

import abc
import bintrees


class MetaTree(object):
    """Template class for each Tree classes provided by bintrees.

    Subclasses inheriting this class must implement _set_tree method.

    Design pattern:
        Template and Wrapper
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._tree = self._set_tree()

    def __getattr__(self, name):
        return getattr(self._tree, name)

    @abc.abstractmethod
    def _set_tree(self):
        pass


class BinaryTree(bintrees.BinaryTree):
    def _set_tree(self, items=None):
        bintrees.BinaryTree.__init__(self, items)

    def pprint(self):
        root = self.root
        return self._iter_print(root, root.left, root.right, 1)

    def _iter_print(self, node, left, right, ind):
        if node:
            return ("{node} (\n{ind}{left},\n{ind}{right})").format(
                ind="  "*ind,
                node=node.key,
                left=self._iter_print(
                    left,
                    left.left,
                    left.right,
                    ind+1) if left else "None",
                right=self._iter_print(
                    right,
                    right.left,
                    right.right,
                    ind+1) if right else "None")
        else:
            return "None"


if __name__ == '__main__':
    m = zip(range(10), "abcdefghijklmn")
    print BinaryTree(m).pprint()
    m = zip([5, 2, 6, 3, 7], "abcdefghijklmn")
    print BinaryTree(m).pprint()
