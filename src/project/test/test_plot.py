import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
graph = nx.DiGraph()

# Add nodes
graph.add_nodes_from([x for x in range(1, 11)])

# Add directed edges
#graph.add_edges_from([(9, 10), (6, 9), (10, 4), (8, 1), (1, 10), (4, 5), (1, 5), (3, 1), (8, 4), (8, 10), (10, 3), (3, 5), (6, 5), (2, 3), (4, 7), (3, 4), (3, 6), (1, 4), (3, 9), (6, 4), (2, 6), (9, 4), (6, 10), (8, 5), (2, 1), (8, 7), (6, 1)])
graph.add_edges_from([(9, 10), (6, 9), (1, 10), (3, 1), (10, 3), (3, 6), (3, 9), (6, 10), (6, 1)])

cycles = list(nx.simple_cycles(graph))
print(cycles)
# Draw the graph
pos = nx.circular_layout(graph)
nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=1500, arrowstyle='->', arrowsize=20, )

# Show the plot
plt.show()