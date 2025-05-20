import typing
import copy
from src.project.heuristics.greedy import GreedyHeuristic
from src.project.helpers.graph import trim_graph, get_vertices_from_edges


class LocalSearch(GreedyHeuristic):

    def obtain_pairs_with_higher_bid(self) -> typing.Iterable[typing.Tuple[int, int]]:
        """
        get pairs that have higher bid
        for example:
            if Bids[i][j] > Bids[j][i] and Priority[i][j] = 0:
                yield (i,j), Bids[i][j] - Bids[j][i]
        """
        for i,j in self.Solution:
            if self.Bids[j][i] > self.Bids[i][j]:
                yield j,i

    def get_knockon_pairs(
            self, increasing_bid: int, edges: typing.List[typing.Tuple[int, int]],
            indegree: typing.Dict[int, int], outdegree: typing.Dict[int, int]
    ) -> (typing.List[typing.Tuple[int, int]], int):
        chosen_knockon_pairs = []
        candidates_bid_decrease = dict(map(lambda _: (_, self.Bids[_[1]][_[0]] - self.Bids[_[0]][_[1]]), edges))
        total_bid_decrease = 0
        while edges:
            # edges: [(4, 7), (8, 3), (8, 4), (7, 3), (3, 9), (4, 10), (10, 3), (7, 9), (9, 6), (6, 8), (7, 6), (10, 7), (8, 7)]
            # edges: [(4, 7), (8, 3), (8, 4), (3, 7), (3, 9), (4, 10), (10, 3), (7, 9), (9, 6), (6, 8), (7, 6), (10, 7), (8, 7)]
            # flip (7,3) to (3,7) , no cycles were eliminated!!!.
            candidate_pairs = [(i, j) for i, j in edges if self.Bids[i][j] - self.Bids[j][i] + total_bid_decrease < increasing_bid ]
            if not candidate_pairs:
                print(f'no feasible flipped candidates')
                return [], -1
            vertices = get_vertices_from_edges(edges)
            vertex_degrees = dict(map(lambda v: (v, indegree[v] + outdegree[v]), vertices))
            candidate_pairs.sort(
                key=lambda pair: (
                    vertex_degrees[pair[0]] + vertex_degrees[pair[1]], candidates_bid_decrease[pair]
                ),
                reverse=True
            )
            # find candidate
            found = False
            for i,j in candidate_pairs:
                new_edges = [x for x in edges]
                new_edges[new_edges.index((i,j))] = (j,i)
                new_edges, indegree, outdegree = trim_graph(new_edges)
                if len(new_edges) < len(edges):
                    total_bid_decrease += self.Bids[i][j] - self.Bids[j][i]
                    edges = new_edges
                    chosen_knockon_pairs.append((i,j))
                    print(f'chosen candidate: {(i,j)}')
                    found = True
                    break
            if not found:
                print(f'no feasible flipped useful candidates')
                return [], -1
        return chosen_knockon_pairs, total_bid_decrease

    def can_be_flipped(self, pair: typing.Tuple[int, int],knockon_pairs: typing.List[typing.Tuple[int, int]]) -> bool:
        solution = copy.deepcopy(self.Solution)
        solution[solution.index(pair[::-1])] = pair
        for knockon_pair in knockon_pairs:
            solution[solution.index(knockon_pair)] = knockon_pair[::-1]
        residual_edges, _, _ = trim_graph(solution)
        if residual_edges:
            return False
        return True

    def flip_pair_with_improvement(self, excluded_pair: typing.Tuple[int, int]) -> (
            bool, int, typing.List[typing.Tuple[int, int]]):
        i,j = excluded_pair
        potential_increasing_bid = self.Bids[i][j] - self.Bids[j][i]
        solution = copy.deepcopy(self.Solution)
        solution[solution.index((j,i))] = i,j
        residual_edges, indegree, outdegree = trim_graph(solution)
        if not residual_edges:
            print('no loops formed')
            return True, potential_increasing_bid, []
        knockon_pairs, decreasing_bid = self.get_knockon_pairs(
            potential_increasing_bid, residual_edges, indegree, outdegree)
        if decreasing_bid == -1:
            return False, 0, []
        print('knockon pairs: ', knockon_pairs, 'decreasing bid: ', decreasing_bid)
        if self.can_be_flipped((i,j), knockon_pairs):
            return True, potential_increasing_bid - decreasing_bid, knockon_pairs
        return False, 0, []

    def solve(self) -> None:
        # Greedy Construction Phase
        super().solve()
        improved = True
        previous_unflipped = []
        while improved:
            improved = False
            pairs_with_higher_bid = list(self.obtain_pairs_with_higher_bid())
            for idx, (i,j) in enumerate(pairs_with_higher_bid):
                if (i,j) in self.Solution:
                    # already flipped during the previous process
                    continue
                if not improved and (i,j) in previous_unflipped:
                    # no need to check
                    continue
                print(f'{"="*20} EXAMINING PAIR {(i,j)} {"=" *20}')
                print(f'{(i,j)} -> {(j,i)}: {self.Bids[i][j]} -> {self.Bids[j][i]}')
                flipped, increasing_bid, knockon_pairs = self.flip_pair_with_improvement((i, j))
                if flipped:
                    improved = True
                    previous_unflipped = pairs_with_higher_bid[idx+1:]
                    print('Updating Solution...')
                    print(f"Objective: {self.Objective} -> {self.Objective + increasing_bid}")
                    print(f"solution: flipped {(j, i)} -> {(i, j)}")
                    self.Solution[self.Solution.index((j, i))] = (i, j)
                    self.Objective += increasing_bid
                    self.MemberPriorities[i][j] = 1
                    self.MemberPriorities[j][i] = 0
                    for m, n in knockon_pairs:
                        print(f'knockon flipped {(m, n)} -> {(n, m)}')
                        self.Solution[self.Solution.index((m, n))] = (n, m)
                        self.MemberPriorities[m][n] = 0
                        self.MemberPriorities[n][m] = 1
