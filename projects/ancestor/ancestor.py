import sys
import os
sys.path.append(f'{os.getcwd()}/graph')
print(sys.path)
from graph import Graph


def earliest_ancestor(ancestors, starting_node, path=[]):
    g = Graph()
    for v1, v2 in ancestors:
        if v1 not in g.vertices:
            g.add_vertex(v1)
        g.add_edge(v1, v2)
    children = set((x for x in g.find_parents(starting_node)))
    parents = set()
    for i in range(len(ancestors)):
        if ancestors[i][0] not in children:
            parents.add(ancestors[i][0])
    results = []
    for p in parents:
        res = g.dfs(p, starting_node)
        if res:
            results.append(res)
    if len(results[0]) == 1:
        return -1
    else:
        max_ancestor = results[0][0]
        max_length = len(results[0])
        for r in results:
            if len(r) > max_length:
                max_ancestor = r[0]
                max_length = len(r)
            elif len(r) == max_length and r[0] < max_ancestor:
                max_ancestor = r[0]
        return max_ancestor
