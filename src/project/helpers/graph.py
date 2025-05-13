import typing as t

def get_vertices_from_edges(edges: t.List[t.Tuple[int, int]]) -> t.Set[int]:
    vertices = set()
    for edge in edges:
        vertices |= set(edge)
    return vertices

def construct_neighbors(vertices: t.Set[int], edges:t.List[t.Tuple[int, int]]) -> t.Dict[int,t.List[int]]:
    neighbors = dict(map(lambda _:(_, []), vertices))
    for i, j in edges:
        neighbors[i].append(j)
    return neighbors

def topological_sort(vertices:t.Set[int], edges: t.List[t.Tuple[int, int]]) -> t.List[int]:
    topological_order = []
    indegree = dict(map(lambda _: (_, 0), vertices))
    neighbors = construct_neighbors(vertices, edges)
    for vertex in vertices:
        for neighbor in neighbors[vertex]:
            indegree[neighbor] += 1
    nodes_with_zero_indegree = [vertex for vertex in vertices if indegree[vertex] == 0]
    while nodes_with_zero_indegree:
        node = nodes_with_zero_indegree.pop()
        topological_order.append(node)
        for neighbor in neighbors[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                nodes_with_zero_indegree.append(neighbor)
    return topological_order


def trim_graph(edges: t.List[t.Tuple[int, int]]) -> (t.List[t.Tuple[int, int]], t.Dict[int, int], t.Dict[int, int]):
    vertices = get_vertices_from_edges(edges)
    neighbors = construct_neighbors(vertices, edges)
    indegree = dict(map(lambda _: (_, 0), vertices))
    outdegree = dict(map(lambda _: (_, 0), vertices))
    for vertex in vertices:
        outdegree[vertex] = len(neighbors[vertex])
        for neighbor in neighbors[vertex]:
            indegree[neighbor] += 1
    nodes_with_zero_indegree = [vertex for vertex in vertices if indegree[vertex] == 0]
    nodes_with_zero_outdegree = [vertex for vertex in vertices if outdegree[vertex] == 0]
    previous_edges = []
    while len(previous_edges) != len(edges):
        previous_edges = [x for x in edges]
        while nodes_with_zero_indegree:
            node = nodes_with_zero_indegree.pop()
            for neighbor in neighbors[node]:
                indegree[neighbor] -= 1
                outdegree[node] -= 1
                if (node, neighbor) in edges:
                    edges.remove((node, neighbor))
                if indegree[neighbor] == 0:
                    nodes_with_zero_indegree.append(neighbor)
                if outdegree[node] == 0:
                    nodes_with_zero_outdegree.append(node)
        while nodes_with_zero_outdegree:
            node = nodes_with_zero_outdegree.pop()
            for vertex, edge_neighbors in neighbors.items():
                if outdegree[vertex] > 0 and node in edge_neighbors:
                    outdegree[vertex] -= 1
                    indegree[node] -= 1
                    if (vertex, node) in edges:
                        edges.remove((vertex, node))
                    if outdegree[vertex] == 0:
                        nodes_with_zero_outdegree.append(vertex)
                    if indegree[node] == 0:
                        nodes_with_zero_indegree.append(node)
    return edges, indegree, outdegree