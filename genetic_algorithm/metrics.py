from primitive import Primitive

# consts for hashing
P = 10003
MOD = int(1e9 + 7)


def list_nodes_with_hashes(primitive):
    ans = []
    hash_ = hash(primitive.str) % MOD

    for node in primitive.nodes:
        list_nodes = list_nodes_with_hashes(node)
        hash_ *= P
        hash_ += list_nodes[-1][1]
        hash_ %= MOD
        ans += list_nodes

    ans.append((primitive, hash_))
    
    return ans



def compare(p1, p2):
    if p1.str != p2.str:
        return False

    for l, r in zip(p1.nodes, p2.nodes):
        if not compare(l, r):
            return False

    return True



def get_first_structural_distance(p1, p2):

    nodes1 = list_nodes_with_hashes(p1)
    nodes2 = list_nodes_with_hashes(p2)
    
    max_same_part = 0
    
    for n1 in nodes1:
        for n2 in nodes2:
            if n1[1] == n2[1] and compare(n1[0], n2[0]):
                max_same_part = max(max_same_part, n1[0].get_tokens())

    return p1.get_tokens() + p2.get_tokens() - 2 * max_same_part


