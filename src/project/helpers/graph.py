import typing as t
from collections import deque

def trim_graph(edges: t.List[t.Tuple[int, int]]) -> (
        t.Dict[int, int], t.Dict[int, int], t.List[int]):
    vertices = set()
    #print('edges before trim', edges)
    for edge in edges:
        vertices.add(edge[0])
        vertices.add(edge[1])
    neighbors = construct_neighbors(vertices, edges)
    indegree = dict(map(lambda _: (_, 0), vertices))
    outdegree = dict(map(lambda _: (_, 0), vertices))
    for vertex in vertices:
        outdegree[vertex] = len(neighbors[vertex])
        for neighbor in neighbors[vertex]:
            indegree[neighbor] += 1
    previous_edges = []
    while len(previous_edges) != len(edges):
        previous_edges = [x for x in edges]
        trim_indegree(edges, neighbors, indegree, outdegree)
        if edges:
            trim_outdegree(edges, neighbors, indegree, outdegree)
    #print('edges after trim', edges)
    return indegree, outdegree, edges

def trim_indegree(edges: t.List[t.Tuple[int, int]], neighbors: t.Dict[int, t.List[int]],
                  indegree: t.Dict[int, int], outdegree: t.Dict[int, int]):
    vertices = set()
    for edge in edges:
        vertices.add(edge[0])
        vertices.add(edge[1])
    queue_with_zero_indegree = deque([vertex for vertex in vertices if indegree[vertex] == 0])
    while queue_with_zero_indegree:
        node = queue_with_zero_indegree.popleft()
        for neighbor in neighbors[node]:
            indegree[neighbor] -= 1
            outdegree[node] -= 1
            edges.remove((node, neighbor))
            if indegree[neighbor] == 0:
                queue_with_zero_indegree.append(neighbor)

def trim_outdegree(edges: t.List[t.Tuple[int, int]], neighbors: t.Dict[int, t.List[int]],
                   indegree: t.Dict[int, int], outdegree: t.Dict[int, int]):
    vertices = set()
    for edge in edges:
        vertices.add(edge[0])
        vertices.add(edge[1])
    queue_with_zero_outdegree = deque([i for i in vertices if outdegree[i] == 0])
    while queue_with_zero_outdegree:
        node = queue_with_zero_outdegree.popleft()
        #print('node', node, 'edges', edges)
        for edge, edge_neighbors in neighbors.items():
            for neighbor in edge_neighbors:
                if outdegree[edge] > 0:
                    if neighbor == node:
                        outdegree[edge] -= 1
                        indegree[neighbor] -= 1
                        edges.remove((edge, neighbor))
                    if outdegree[edge] == 0:
                        queue_with_zero_outdegree.append(edge)

def construct_neighbors(vertices: t.Set[int], edges:t.List[t.Tuple[int, int]]) -> t.Dict[int,t.List[int]]:
    neighbors = dict(map(lambda _:(_, []), vertices))
    for u, v in edges:
        neighbors[u].append(v)
    return neighbors

def topological_sort(edges: t.List[t.Tuple[int, int]]) -> (t.List[int], t.List[int]):
    vertices = set()
    for edge in edges:
        vertices.add(edge[0])
        vertices.add(edge[1])
    neighbors = construct_neighbors(vertices, edges)
    indegree = dict(map(lambda _:(_, 0), vertices))

    for vertex in vertices:
        for neighbor in neighbors[vertex]:
            indegree[neighbor] += 1

    queue_with_zero_indegree = deque([vertex for vertex in vertices if indegree[vertex] == 0])
    topological_sorted_order = []
    while queue_with_zero_indegree:
        node = queue_with_zero_indegree.popleft()
        topological_sorted_order.append(node)
        for neighbor in neighbors[node]:
            indegree[neighbor] -= 1
            edges.remove((node, neighbor))
            if indegree[neighbor] == 0:
                queue_with_zero_indegree.append(neighbor)
    # Check for cycle
    if len(topological_sorted_order) != len(vertices):
        return [], edges
    return topological_sorted_order, []


if __name__ == "__main__":
    vertices = [1, 2, 3]
    edges = [(1, 3), (2, 1), (3, 2)]

    topological_sorted_order, residual_edges = topological_sort(vertices, edges)