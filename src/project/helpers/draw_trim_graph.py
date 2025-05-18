import networkx as nx
import matplotlib.pyplot as plt
import typing as t
from graph import get_vertices_from_edges, construct_neighbors
import os

Bids={
    1:{1:0,2:3,3:6,4:4,5:8,6:1,7:0,8:7,9:0,10:9},
    2:{1:2,2:0,3:6,4:0,5:0,6:4,7:0,8:0,9:0,10:0},
    3:{1:8,2:4,3:0,4:6,5:6,6:5,7:0,8:0,9:4,10:2},
    4:{1:5,2:0,3:1,4:0,5:8,6:5,7:6,8:5,9:3,10:8},
    5:{1:7,2:0,3:5,4:8,5:0,6:6,7:0,8:1,9:0,10:0},
    6:{1:3,2:4,3:5,4:2,5:5,6:0,7:0,8:0,9:9,10:3},
    7:{1:0,2:0,3:0,4:3,5:0,6:0,7:0,8:2,9:0,10:0},
    8:{1:9,2:0,3:0,4:7,5:4,6:0,7:3,8:0,9:0,10:7},
    9:{1:0,2:0,3:5,4:4,5:0,6:8,7:0,8:0,9:0,10:9},
    10:{1:5,2:0,3:7,4:9,5:0,6:4,7:0,8:2,9:9,10:0}
}

counter = 0

def trim_graph(edges: t.List[t.Tuple[int, int]]) -> (
        t.List[t.Tuple[int, int]], t.Dict[int, int], t.Dict[int, int]):
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
                    plot_graph(edges)
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
                        plot_graph(edges)
                    if outdegree[vertex] == 0:
                        nodes_with_zero_outdegree.append(vertex)
                    if indegree[node] == 0:
                        nodes_with_zero_indegree.append(node)
    return edges, indegree, outdegree

def get_edge_colors(
        edges: t.List[t.Tuple[int, int]],
        red_edges: t.Set[t.Tuple[int, int]],
        selected_edge: t.Optional[t.Tuple[int, int]] = None):
    if selected_edge is None:
        selected_edge = ()
    edge_colors = ['red' if edge in red_edges else 'blue' for edge in edges]
    for idx, edge in enumerate(edges):
        if edge == selected_edge[::-1]:
            edge_colors[idx] = 'yellow'
    return edge_colors

def get_drawing_table(
            rows: int, chosen_edges: t.List[t.Tuple[int, int]],
            candidate_edges: t.List[t.Tuple[int, int]],
            selected_edge: t.Optional[t.Tuple[int, int]] = None,
            candidate_degrees: t.Optional[t.Dict[t.Tuple[int, int], int]] = None
    ):
        columns = ('Chosen', 'Cand.', 'Degree', 'Impact')
        # cell text
        cell_text = [[''] * 4 for _ in range(rows)]
        cell_colors = [['white'] * 4 for _ in range(rows)]
        for idx, (i,j) in enumerate(chosen_edges):
            cell_text[idx][0] = f'{i}->{j}: {Bids[j][i] - Bids[i][j]}'
        for idx, (i,j) in enumerate(candidate_edges):
            cell_text[idx][1] = f'{i}->{j}'
            cell_text[idx][2] = f'{candidate_degrees[(i,j)]}'
            cell_text[idx][3] = f'{Bids[j][i] - Bids[i][j]}'
        # cell color
        for idx, (i, j) in enumerate(candidate_edges):
            if (i,j) == selected_edge:
                cell_colors[idx][1] = 'yellow'
        return cell_text, columns, cell_colors, [0.25, 0.25, 0.25, 0.25]

def plot_graph(
        edges: t.List[t.Tuple[int, int]],
        selected_edge: t.Optional[t.Tuple[int, int]] = None,
        draw_table: bool = False,
        rows: int = 8,
        candidate_degrees: t.Optional[t.Dict[t.Tuple[int, int], int]] = None,
        candidates: t.Optional[t.List[t.Tuple[int, int]]] = None,
        chosen_edges: t.Optional[t.List[t.Tuple[int, int]]] = None,
) -> None:
    global counter
    counter += 1
    graph = nx.DiGraph()
    graph.add_nodes_from(range(1, 11))
    graph.add_edges_from(edges)
    pos = nx.circular_layout(graph)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [10, 6]})
    nx.draw_networkx_nodes(graph, pos, node_size=1500, node_color='skyblue', ax=ax1)
    nx.draw_networkx_labels(graph, pos, ax=ax1)
    edge_labels = {(i, j): Bids[i][j] for i, j in graph.edges()}
    red_edges = set()
    cycles = list(nx.simple_cycles(graph))
    for cycle in cycles:
        cycle.append(cycle[0])
        for i in range(len(cycle) - 1):
            red_edges.add((cycle[i], cycle[i + 1]))
    edge_colors = get_edge_colors(graph.edges(), red_edges, selected_edge)
    nx.draw_networkx_edges(
        graph, pos, arrows=True, node_size=1500, arrowsize=20, arrowstyle='->', edge_color=edge_colors, ax=ax1)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax1)
    if draw_table:
        cell_text, columns, cell_colors, column_width = get_drawing_table(
            rows, chosen_edges, candidate_edges=candidates, selected_edge=selected_edge, candidate_degrees=candidate_degrees)
        table = ax2.table(
            cellText=cell_text, colLabels=columns, cellColours=cell_colors, colWidths=column_width, bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 1)
    image_folder = f'../assets/image/solution/ts'
    ax1.axis('off')
    ax2.axis('off')
    plt.tight_layout()
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    plt.savefig(f'{image_folder}/plot-{str(counter).zfill(3)}.png')
    plt.close()


'''
finished:
(10, 3) -> (3, 10): 7 -> 2
before trim graph [(9, 10), (6, 9), (10, 4), (8, 1), (1, 10), (4, 5), (1, 5), (3, 1), (8, 4), (8, 10), (10, 3), (3, 5), (6, 5), (2, 3), (4, 7), (3, 4), (3, 6), (1, 4), (3, 9), (6, 4), (2, 6), (9, 4), (6, 10), (8, 5), (2, 1), (8, 7), (6, 1)]
after trim graph [(9, 10), (6, 9), (1, 10), (3, 1), (10, 3), (3, 6), (3, 9), (6, 10), (6, 1)]
candidate_pairs [(6, 10), (3, 6), (3, 9), (9, 10), (6, 9), (3, 1), (6, 1), (1, 10)]
edge degrees: {(6, 10): 8, (3, 6): 8, (3, 9): 7, (9, 10): 7, (6, 9): 7, (3, 1): 7, (6, 1): 7, (1, 10): 7}
chosen candidate: (6, 10)
before trim graph [(9, 10), (6, 9), (1, 10), (3, 1), (10, 3), (3, 6), (3, 9), (10, 6), (6, 1)]
after trim graph [(9, 10), (6, 9), (1, 10), (3, 1), (10, 3), (3, 6), (3, 9), (10, 6), (6, 1)]
chosen candidate: (3, 6)
before trim graph [(9, 10), (6, 9), (1, 10), (3, 1), (10, 3), (6, 3), (3, 9), (6, 10), (6, 1)]
after trim graph [(9, 10), (1, 10), (3, 1), (10, 3), (3, 9)]
chosen knockon_pairs [(3, 6)]
candidate_pairs [(3, 9), (9, 10), (3, 1), (1, 10)]
edge degrees: {(3, 9): 5, (9, 10): 5, (3, 1): 5, (1, 10): 5}
chosen candidate: (3, 9)
before trim graph [(9, 10), (1, 10), (3, 1), (10, 3), (9, 3)]
after trim graph [(1, 10), (3, 1), (10, 3)]
chosen knockon_pairs [(3, 6), (3, 9)]
candidate_pairs [(3, 1), (1, 10), (10, 3)]
edge degrees: {(3, 1): 4, (1, 10): 4, (10, 3): 4}
chosen candidate: (3, 1)
before trim graph [(1, 10), (1, 3), (10, 3)]
after trim graph []
chosen knockon_pairs [(3, 6), (3, 9), (3, 1)]

knockon pairs:  [(3, 6), (3, 9), (3, 1)] decreasing bid:  1
before trim graph [(9, 10), (6, 9), (10, 4), (8, 1), (1, 10), (4, 5), (1, 5), (1, 3), (8, 4), (8, 10), (10, 3), (3, 5), (6, 5), (2, 3), (4, 7), (3, 4), (6, 3), (1, 4), (9, 3), (6, 4), (2, 6), (9, 4), (6, 10), (8, 5), (2, 1), (8, 7), (6, 1)]
after trim graph []
Updating Solution...
Objective: 152 -> 156
solution: flipped (3, 10) -> (10, 3)
solution: flipped (3, 6) -> (6, 3)
solution: flipped (3, 9) -> (9, 3)
solution: flipped (3, 1) -> (1, 3)
'''

edges = [
        (9, 10), (6, 9), (10, 4), (8, 1), (1, 10), (4, 5), (1, 5),
        (3, 1), (8, 4), (8, 10), (10, 3), (3, 5), (6, 5), (2, 3),
        (4, 7), (3, 4), (3, 6), (1, 4), (3, 9), (6, 4), (2, 6),
        (9, 4), (6, 10), (8, 5), (2, 1), (8, 7), (6, 1)
]

def main():
    plot_graph(edges)
    trim_graph(edges)
    # (6, 10)
    plot_graph(
        [(9, 10), (6, 9), (1, 10), (3, 1), (10, 3), (3, 6), (3, 9), (10, 6), (6, 1)],
        selected_edge=(6, 10),draw_table=True,rows=10,
        candidate_degrees={(6, 10): 8, (3, 6): 8, (3, 9): 7, (9, 10): 7, (6, 9): 7, (3, 1): 7, (6, 1): 7, (1, 10): 7},
        candidates=[(6, 10), (3, 6), (3, 9), (9, 10), (6, 9), (3, 1), (6, 1), (1, 10)], chosen_edges=[]
    )
    # (3, 6)
    plot_graph(
        [(9, 10), (6, 9), (1, 10), (3, 1), (10, 3), (6, 3), (3, 9), (6, 10), (6, 1)],
        selected_edge=(3, 6), draw_table=True, rows=10,
        candidate_degrees={(6, 10): 8, (3, 6): 8, (3, 9): 7, (9, 10): 7, (6, 9): 7, (3, 1): 7, (6, 1): 7, (1, 10): 7},
        candidates=[(6, 10), (3, 6), (3, 9), (9, 10), (6, 9), (3, 1), (6, 1), (1, 10)], chosen_edges=[]
    )
    plot_graph(
        [(9, 10), (1, 10), (3, 1), (10, 3), (3, 9)],
        selected_edge=(3, 6),draw_table=True, rows=10,
        candidate_degrees={(6, 10): 8, (3, 6): 8, (3, 9): 7, (9, 10): 7, (6, 9): 7, (3, 1): 7, (6, 1): 7, (1, 10): 7},
        candidates=[(6, 10), (3, 6), (3, 9), (9, 10), (6, 9), (3, 1), (6, 1), (1, 10)], chosen_edges=[(3,6)]
    )
    # (3,9)
    plot_graph(
        [(9, 10), (1, 10), (3, 1), (10, 3), (9, 3)],
        selected_edge=(3, 9), draw_table=True, rows=10,
        candidate_degrees={(3, 9): 5, (9, 10): 5, (3, 1): 5, (1, 10): 5},
        candidates=[(3, 9), (9, 10), (3, 1), (1, 10)], chosen_edges=[(3,6)]
    )
    plot_graph(
        [(1, 10), (3, 1), (10, 3)],
        selected_edge=(3,9), draw_table=True, rows=10,
        candidate_degrees={(3, 9): 5, (9, 10): 5, (3, 1): 5, (1, 10): 5},
        candidates=[(3, 9), (9, 10), (3, 1), (1, 10)], chosen_edges=[(3,6),(3,9)]
    )
    # (3, 1)
    plot_graph(
        [(1, 10), (1, 3), (10, 3)],
        selected_edge=(3,1), draw_table=True, rows=10,
        candidate_degrees={(3, 1): 4, (1, 10): 4, (10, 3): 4},
        candidates=[(3, 1), (1, 10), (10, 3)], chosen_edges=[(3,6),(3,9)]
    )
    plot_graph(
        [], draw_table=True, rows=10,
        candidate_degrees={},
        candidates=[], chosen_edges=[(3, 6), (3, 9), (3,1)]
    )


if __name__ == '__main__':
    main()



