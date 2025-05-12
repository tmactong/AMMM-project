import time
from collections import deque
from src.project.helpers.graph import trim_vertices_with_zero_outdegree, trim_vertices_with_zero_indegree, trim_graph


# We mainly take input graph as a set of edges. This function is
# mainly a utility function to convert the edges to an adjacency
# list
def constructadj(V, edges):
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
    return adj

def ts_outdegree(V, edges):
    adj = constructadj(V, edges)
    outdegree = [0] * V
    for u in range(V):
        outdegree[u] = len(adj[u])
    #print('outdegree', outdegree)
    q = deque([i for i in range(V) if outdegree[i] == 0])
    while q:
        node = q.popleft()
        print('node', node)

        for idx, neighbors in enumerate(adj):
            #print('idx:',idx, neighbors)
            for neighbor in neighbors:
                #print('neighbor', neighbor, outdegree[neighbor])
                if outdegree[idx] > 0:
                    if neighbor == node:
                        outdegree[idx] -= 1
                    if outdegree[idx] == 0:
                        q.append(idx)
                else:
                    edges.remove([idx, neighbor])
    print('outdegree', outdegree)
    print('edges', edges)
    print([idx for idx in range(len(outdegree)) if outdegree[idx] != 0])


# Function to return list containing vertices in Topological order
def topologicalSort(V, edges):
    adj = constructadj(V, edges)
    indegree = [0] * V

    # Calculate indegree and outdegree of each vertex
    for u in range(V):
        #outdegree[u] = len(adj[u])
        for v in adj[u]:
            indegree[v] += 1
    print('indegree',indegree)
    #print('outdegree',outdegree)

    # Queue to store vertices with indegree 0
    q = deque([i for i in range(V) if indegree[i] == 0])

    result = []
    while q:
        node = q.popleft()
        result.append(node)
        #outdegree[node] = 0

        for neighbor in adj[node]:
            indegree[neighbor] -= 1
            edges.remove([node, neighbor])
            if indegree[neighbor] == 0:
                q.append(neighbor)

    # Check for cycle
    if len(result) != V:
        print("Graph contains cycle!")
        print('indegree', indegree)
        ts_outdegree(V, edges)
        return []

    return result


def test_trim(edges):
    print('edges', edges)
    edges = trim_graph(edges)
    print('edges', edges)



if __name__ == "__main__":
    # edges = [[0, 1], [1, 2], [2, 3], [4, 5], [5, 1], [5, 2]]
    # edges = [[0, 1], [1, 2], [2, 3], [4, 5], [5, 1], [2, 5]]
    edges = [(0, 4), (4, 5), (5, 1), (1, 0), (2, 5), (1, 2),(2,3)]
    #edges = [(0, 2), (1, 0), (2, 1)]
    #edges = [(4, 2), (4, 7), (8, 3), (8, 4), (9, 2), (3, 7), (3, 9), (4, 10), (10, 3), (7, 9), (9, 6), (6, 8), (7, 6), (3, 2), (10, 7), (9, 5), (8, 1), (8, 7), (6, 1)]
    #edges =  [(4, 7), (8, 3), (8, 4), (7, 3), (3, 9), (4, 10), (10, 3), (7, 9), (9, 6), (6, 8), (7, 6), (10, 7), (8, 7)]
    #result = topologicalSort(V, edges)
    #if result:
    #    print("Topological Order:", result)
    # test_trim([1,2,3,4,5,6,7,8,9,10], edges)
    test_trim(edges)