#! /usr/bin/env python
# coding:utf-8

import bintrees


class MetaTree(object):
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


class BinaryTree(bintrees.BinaryTree, MetaTree):
    pass


class AVLTree(bintrees.AVLTree, MetaTree):
    pass


class RBTree(bintrees.RBTree, MetaTree):
    pass


class FastBinaryTree(bintrees.FastBinaryTree, MetaTree):
    pass


class FastAVLTree(bintrees.FastAVLTree, MetaTree):
    pass


class FastRBTree(bintrees.FastRBTree, MetaTree):
    pass


if __name__ == '__main__':
    m = zip(range(10), "abcdefghijklmn")
    print BinaryTree(m).pprint()
    print AVLTree(m).pprint()
    print RBTree(m).pprint()
