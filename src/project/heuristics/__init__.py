import os
import typing as t
import itertools
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    PLOTLIB_IMPORTED = True
except ImportError:
    print("Packages networkx, matplotlib not installed...")
    PLOTLIB_IMPORTED = False


class HeuristicMethod:

    MemberCount: int
    Bids: t.Dict[int, t.Dict[int, int]]
    Candidates: t.List[t.Tuple[int, int]]
    Solution: t.List[t.Tuple[int, int]]
    MemberPriorities: t.Dict[t.Any, t.Dict[t.Any, int]]
    Objective: int
    CoveredMembers: t.Set[int]
    InfeasiblePairs: t.List[t.Tuple[int, int]]
    DrawGraph: bool
    DrawCounter: int

    def __init__(self, member_count: int, bids: t.Dict[int, t.Dict[int, int]], project_name: str, draw_graph: bool = False) -> None:
        self.MemberCount = member_count
        self.Bids = bids
        self.ProjectName = project_name
        self.DrawGraph = draw_graph
        self.DrawCounter = 0
        self.InfeasiblePairs = []
        self.SortedCandidates = []
        self.initialize_variables()

    def initialize_variables(self) -> None:
        self.Solution = list()
        self.MemberPriorities = dict(
            map(lambda _: (
                _, dict(map(lambda _: (_, 0), range(1, self.MemberCount + 1)))
            ), range(1, self.MemberCount + 1)))
        self.Objective = 0
        self.Candidates = [(i,j) for i,j in itertools.permutations(range(1, self.MemberCount + 1), 2)
                           if self.Bids[i][j] != 0 or self.Bids[j][i] != 0]
        self.CoveredMembers = set()

    def update_objective(self, pair: t.Tuple[int, int]) -> None:
        self.Objective += self.Bids[pair[0]][pair[1]]

    def get_local_search_edge_colors(
            self, edges: t.List[t.Tuple[int, int]], cycles: t.Optional[t.List[t.List[int]]] = None):
        if cycles:
            red_edges = set()
            for cycle in cycles:
                cycle.append(cycle[0])
                for i in range(len(cycle)-1):
                    red_edges.add((cycle[i], cycle[i+1]))
            edge_colors = ['red' if edge in red_edges else 'blue' for edge in edges]
        else:
            edge_colors = ['blue' for _ in edges]
        return edge_colors

    def get_local_search_drawing_table(
            self, current_flipped_pair: t.Tuple[int,int],
            selected_edges: t.Optional[t.List[t.Tuple[int, int]]] = None,
            candidate_degrees: t.Optional[t.Dict[t.Tuple[int, int], int]] = None,
            red_edges: t.Optional[t.Set[t.Tuple[int, int]]] = None
    ):
        if candidate_degrees is None:
            candidate_degrees = {}
        if red_edges is None:
            red_edges = set()
        if selected_edges is None:
            selected_edges = set()
        # cell text
        cell_text = [['']*5 for _ in self.Solution]
        cell_colors = [['white'] * 5 for _ in self.Solution]
        columns = ('Solution', 'Excluded', 'Degree', 'Impact', 'Objective')
        # first & second & fifth column
        objective = 0
        for idx, (i,j) in enumerate(self.Solution):
            objective += self.Bids[i][j]
            cell_text[idx][0] = f'{i}->{j}: {self.Bids[i][j]}'
            cell_text[idx][1] = f'{j}->{i}: {self.Bids[j][i]}'
            if (i,j) in candidate_degrees:
                cell_text[idx][2] = f'{candidate_degrees[(i,j)]}'
            if (i,j) in selected_edges:
                cell_text[idx][3] = f'{self.Bids[j][i] - self.Bids[i][j]}'
            cell_text[idx][4] = str(objective)
        # cell color
        for idx, (i, j) in enumerate(self.Solution):
            # first column
            if (i,j) in red_edges:
                cell_colors[idx][0] = 'yellow'
            if (i,j) in selected_edges:
                cell_colors[idx][0] = 'green'
                cell_colors[idx][3] = 'green'
            # second column
            if self.Bids[j][i] - self.Bids[i][j] > 0:
                cell_colors[idx][1] = 'red'
            if (j,i) == current_flipped_pair:
                cell_colors[idx][1] = 'yellow'
        return cell_text, columns, cell_colors, [0.25, 0.25, 0.1666, 0.1666,0.1666]

    def get_grasp_edge_colors(
            self, edges: t.List[t.Tuple[int, int]],
            red_edges: t.Optional[t.Set[t.Tuple[int, int]]] = None
    ):
        if red_edges:
            edge_colors = ['red' if edge in red_edges else 'blue' for edge in edges]
        else:
            edge_colors = ['blue' for _ in edges]
        return edge_colors

    def get_greedy_edge_colors(
            self, edges: t.List[t.Tuple[int, int]], infeasible_edge: t.Optional[t.Tuple[int,int]] = None,
            red_edges: t.Optional[t.Set[t.Tuple[int, int]]] = None):
        edge_colors = []
        if infeasible_edge:
            for edge in edges:
                if edge == infeasible_edge:
                    edge_colors.append('red')
                else:
                    edge_colors.append('blue')
        elif red_edges:
            edge_colors = ['red' if edge in red_edges else 'blue' for edge in edges]
        else:
            edge_colors = ['blue' for _ in edges]
        return edge_colors

    def get_grasp_drawing_table(
            self, rows: t.List[str],
            rcl: t.Optional[t.List[t.Tuple[int, int]]] = None,
            alpha: t.Optional[float] = None,
            selected_candidate: t.Optional[t.Tuple[int, int]] = None,
            current_infeasible_pair: t.Optional[t.Tuple[int, int]] = None,
    ):
        if rcl is None:
            rcl = []
        cell_text = [[''] * 4 for _ in rows]
        cell_colors = [['white'] * 4 for _ in rows]
        columns = ('Solution', 'Excluded', 'RCL', 'Objective')
        objective = 0
        # cell text
        for idx, (i,j) in enumerate(self.Solution):
            objective += self.Bids[i][j]
            cell_text[idx][0] = f'{i}->{j}: {self.Bids[i][j]}'
            cell_text[idx][1] = f'{j}->{i}: {self.Bids[j][i]}'
            cell_text[idx][3] = str(objective)
        if current_infeasible_pair:
            i,j = current_infeasible_pair
            cell_text[len(self.Solution)][0] = f'{i}->{j}: {self.Bids[i][j]}'
            cell_text[len(self.Solution)][1] = f'{j}->{i}: {self.Bids[j][i]}'
        for idx in range(len(rows)):
            if idx < len(rcl):
                m, n = rcl[idx]
                cell_text[idx][2] = f'{m}->{n}: {self.Bids[m][n]}'
        # cell color
        for idx, (i, j) in enumerate(self.Solution):
            if (j,i) in self.InfeasiblePairs:
            #if self.Bids[j][i] - self.Bids[i][j] > 0:
                cell_colors[idx][1] = 'red'
        if current_infeasible_pair:
            cell_colors[len(self.Solution)][0] = 'red'
        for idx in range(len(rcl)):
            if idx < len(rcl):
                x, y = rcl[0]
                l, h = rcl[-1]
                m, n = rcl[idx]
                if self.Bids[m][n] >= self.Bids[x][y] - alpha* (self.Bids[x][y] - self.Bids[l][h]):
                    cell_colors[idx][2] = 'green'
                if selected_candidate == (m, n):
                    cell_colors[idx][2] = 'yellow'
        return cell_text, columns, cell_colors, [0.25, 0.25, 0.25, 0.25]

    def get_greedy_drawing_table(
            self, rows: t.List[str], edges: t.List[t.Tuple[int, int]],
            current_infeasible_pair: t.Optional[t.Tuple[int, int]] = None,
            draw_cycle: t.Optional[bool] = None, skip_objective: t.Optional[bool] = None,
            candidates: t.Optional[t.List[t.Tuple[int, int]]] = None,
            selected_candidate: t.Optional[t.Tuple[int, int]] = None
    ) -> (t.List[t.List[str]], t.Tuple[str, str, str], t.List[t.List[str]]):
        if candidates is None:
            candidates = []
        cell_text = []
        cell_colors = []
        columns = ('Solution', 'Excluded', 'Candidates', 'Objective')
        objective = 0
        for i,j in edges:
            cell_color = []
            for infeasible_edge in self.InfeasiblePairs:
                if (i,j) == infeasible_edge:
                    cell_color = ['red', 'white', 'white','white']
                    break
                elif (j,i) == infeasible_edge:
                    cell_color = ['white', 'red', 'white','white']
                    break
            if not cell_color:
                cell_color = ['white', 'white', 'white','white']
            objective += self.Bids[i][j]
            cell_text.append([f'{i}->{j}: {self.Bids[i][j]}', f'{j}->{i}: {self.Bids[j][i]}','',str(objective)])
            cell_colors.append(cell_color)
        if current_infeasible_pair or skip_objective or draw_cycle:
            cell_text[-1][-1] = ''
        if current_infeasible_pair:
            cell_colors[-1][0] = 'red'
        for i in range(len(edges), len(rows)):
            cell_text.append(['', '', '', ''])
            cell_colors.append(['white', 'white', 'white', 'white'])
        for i in range(len(rows)):
            if i < len(candidates):
                m, n = candidates[i]
                cell_text[i][2] = f'{m}->{n}: {self.Bids[m][n]}'
                if (m,n) == selected_candidate:
                    cell_colors[i][2] = 'yellow'
        return cell_text, columns, cell_colors, [0.25, 0.25, 0.25, 0.25]

    def plot_graph(self, algorithm:str, edges: t.List[t.Tuple[int, int]],
                   infeasible_edge: t.Optional[t.Tuple[int,int]] = None, draw_cycle: t.Optional[bool] = None,
                   skip_objective: t.Optional[bool] = None,
                   selected_edges: t.Optional[t.List[t.Tuple[int, int]]] = None,
                   candidate_degrees: t.Optional[t.Dict[t.Tuple[int, int], int]] = None,
                   rcl: t.Optional[t.List[t.Tuple[int, int]]] = None,
                   alpha: t.Optional[float] = None,
                   selected_candidate: t.Optional[t.Tuple[int, int]] = None,
    ) -> None:
        if not PLOTLIB_IMPORTED:
            return
        self.DrawCounter += 1
        graph = nx.DiGraph()
        graph.add_nodes_from(range(1, self.MemberCount + 1))
        graph.add_edges_from(edges)
        pos = nx.circular_layout(graph)
        #fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5),gridspec_kw={'width_ratios': [2, 1]})
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [10, 6]})
        nx.draw_networkx_nodes(graph, pos, node_size=1500, node_color='skyblue', ax=ax1)
        nx.draw_networkx_labels(graph, pos, ax=ax1)
        edge_labels = {(i,j): self.Bids[i][j] for i,j in graph.edges()}
        cycles = []
        red_edges = set()
        if draw_cycle:
            cycles = list(nx.simple_cycles(graph))
            for cycle in cycles:
                cycle.append(cycle[0])
                for i in range(len(cycle) - 1):
                    red_edges.add((cycle[i], cycle[i + 1]))
        if algorithm == 'greedy':
            edge_colors = self.get_greedy_edge_colors(graph.edges(), infeasible_edge, red_edges)
        elif algorithm == 'local_search':
            edge_colors = self.get_local_search_edge_colors(graph.edges(), cycles)
        elif algorithm == 'grasp':
            edge_colors = self.get_grasp_edge_colors(graph.edges(), red_edges=red_edges)
        nx.draw_networkx_edges(
            graph, pos, arrows=True, node_size=1500, arrowsize=20, arrowstyle='->', edge_color=edge_colors, ax=ax1)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax1)
        candidates = [(i, j) for i, j in itertools.permutations(range(1, self.MemberCount + 1), 2)
                      if self.Bids[i][j] != 0 or self.Bids[j][i] != 0]
        rows = [str(i + 1) for i in range(int(len(candidates) / 2))]
        if algorithm == 'greedy':
            cell_text, columns, cell_colors, column_width = self.get_greedy_drawing_table(
                rows, edges, current_infeasible_pair=infeasible_edge, skip_objective=skip_objective,
                draw_cycle=draw_cycle, candidates=rcl, selected_candidate=selected_candidate)
        elif algorithm == 'local_search':
            cell_text, columns, cell_colors, column_width = self.get_local_search_drawing_table(
                red_edges=red_edges,selected_edges=selected_edges,
                candidate_degrees=candidate_degrees, current_flipped_pair=infeasible_edge
            )
        elif algorithm == 'grasp':
            cell_text, columns, cell_colors, column_width = self.get_grasp_drawing_table(
                rows, rcl=rcl, alpha=alpha, selected_candidate=selected_candidate, current_infeasible_pair=infeasible_edge
            )
        table = ax2.table(
            cellText=cell_text, colLabels=columns, cellColours=cell_colors, colWidths=column_width,bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1)
        image_folder = f'../assets/image/solution/project.{self.ProjectName}/{algorithm}'
        ax1.axis('off')
        ax2.axis('off')
        plt.tight_layout()
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        plt.savefig(f'{image_folder}/plot-{str(self.DrawCounter).zfill(3)}.png')
        plt.close()

    def solve(self) -> None:
        raise NotImplementedError("Method solve not implemented")