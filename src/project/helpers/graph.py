import typing as t

def get_vertices_from_edges(edges: t.List[t.Tuple[int, int]]) -> t.Set[int]:
    vertices = set()
    for edge in edges:
        vertices |= set(edge)
    return vertices

def trim_graph(edges: t.List[t.Tuple[int, int]]) -> t.List[t.Tuple[int, int]]:
    vertices = get_vertices_from_edges(edges)
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
        trim_vertices_with_zero_indegree(edges, neighbors, indegree, outdegree)
        if edges:
            trim_vertices_with_zero_outdegree(edges, neighbors, indegree, outdegree)
    return edges

def trim_vertices_with_zero_indegree(
        edges: t.List[t.Tuple[int, int]], neighbors: t.Dict[int, t.List[int]],
        indegree: t.Dict[int, int], outdegree: t.Dict[int, int]):
    vertices = get_vertices_from_edges(edges)
    nodes_with_zero_indegree = [vertex for vertex in vertices if indegree[vertex] == 0]
    while nodes_with_zero_indegree:
        node = nodes_with_zero_indegree.pop()
        for neighbor in neighbors[node]:
            indegree[neighbor] -= 1
            outdegree[node] -= 1
            edges.remove((node, neighbor))
            if indegree[neighbor] == 0:
                nodes_with_zero_indegree.append(neighbor)

def trim_vertices_with_zero_outdegree(
        edges: t.List[t.Tuple[int, int]], neighbors: t.Dict[int, t.List[int]],
        indegree: t.Dict[int, int], outdegree: t.Dict[int, int]):
    vertices = get_vertices_from_edges(edges)
    nodes_with_zero_outdegree = [i for i in vertices if outdegree[i] == 0]
    while nodes_with_zero_outdegree:
        node = nodes_with_zero_outdegree.pop()
        for edge, edge_neighbors in neighbors.items():
            if outdegree[edge] > 0 and node in edge_neighbors:
                outdegree[edge] -= 1
                indegree[node] -= 1
                edges.remove((edge, node))
                if outdegree[edge] == 0:
                    nodes_with_zero_outdegree.append(edge)

def construct_neighbors(vertices: t.Set[int], edges:t.List[t.Tuple[int, int]]) -> t.Dict[int,t.List[int]]:
    neighbors = dict(map(lambda _:(_, []), vertices))
    for i, j in edges:
        neighbors[i].append(j)
    return neighbors