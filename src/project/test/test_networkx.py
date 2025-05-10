import networkx as nx


# Create Directed Graph
G=nx.DiGraph()

# Add a list of nodes:
G.add_nodes_from([0,1,2,3,4,5])

# Add a list of edges:
G.add_edges_from([(0, 4), (4, 5), (5, 1), (1, 0), (2, 5), (1, 2),(2,3)])

#Return a list of cycles described as a list o nodes
print(list(nx.simple_cycles(G)))
