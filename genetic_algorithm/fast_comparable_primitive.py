from enum import Enum
import numpy as np
from primitive import Primitive

# consts for hashing
P = 10003
MOD = int(1e9 + 7)

class FastComparablePrimitive(Primitive):
    """
        use autorecalcable hashes for fast compare
    """
    def __init__(self, *args, **kwargs):
        super(FastComparablePrimitive, self).__init__(*args, **kwargs)
        self.hash = None
        self.recalc_hash()


    def get_hash(self):
        if self.hash is None:
            raise Exception("getting None hash")

        return self.hash


    def set_node(self, id_, new_val):
        i = 0
        while self.nodes[i].get_tokens() <= n:
            n -= self.nodes[i].get_tokens()
            i += 1
        if n == 0:
            self.nodes[i] = new_val
            self.recalc_hash()
        else:
            self.nodes[i].set_node(n - 1, new_val)
            self.recalc_hash()


    def recalc_hash(self):
        if self.func is None:
            raise Exception("getting hash from undefined primitive")

        # if primitive is new constructed, it's sons may be strange
        recalc_sons = False
        if self.hash is None:
            recalc_sons = True

        self.hash = hash(self.str) % MOD

        # TODO: kostil...
        if len(self.nodes) > 0 and (self.str == 'add' or self.str == 'multiply'):
            if recalc_sons:
                for node in self.nodes:
                    node.recalc_hash()
            if self.nodes[0].get_hash() > self.nodes[1].get_hash():
                self.nodes = self.nodes[::-1]

        for node in self.nodes:
            if recalc_sons:
                node.recalc_hash()
            self.hash *= P
            self.hash += node.get_hash()
            self.hash %= MOD


    def add_nodes(self, *args, **kwargs):
        super(FastComparablePrimitive, self).add_nodes(*args, **kwargs)
        self.recalc_hash()
        return self
    

    def equals(self, primitive):
        if self.get_hash() != primitive.get_hash():
            return False

        if self.func != primitive.func:
            return False

        for l, r in zip(self.nodes, primitive.nodes):
            if not l.equals(r):
                return False

        return True

    def list_nodes(self):
        ans = [self]
        for node in self.nodes:
            ans += node.list_nodes()
        return ans

    def get_first_structural_distance(self, primitive):
        nodes1 = self.list_nodes()
        nodes2 = primitive.list_nodes()
        max_same_part = 0
        for n1 in nodes1:
            for n2 in nodes2:
                if n1.equals(n2):
                    max_same_part = max(max_same_part, n1.get_tokens())

        return self.get_tokens() + primitive.get_tokens() - 2 * max_same_part
