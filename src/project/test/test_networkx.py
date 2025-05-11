import networkx as nx


# Create Directed Graph
G=nx.DiGraph()

# Add a list of nodes:
G.add_nodes_from([3,4,6,7,8,9,10])

# Add a list of edges:
G.add_edges_from([(4, 7), (8, 3), (8, 4), (3,7), (3, 9), (4, 10), (10, 3), (7, 9), (9, 6), (6, 8), (7, 6), (10, 7), (8, 7)])

#Return a list of cycles described as a list o nodes
print(list(nx.simple_cycles(G)))
