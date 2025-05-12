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
        for pair in self.Solution:
            if self.Bids[pair[1]][pair[0]] > self.Bids[pair[0]][pair[1]]:
                yield pair[::-1]

    def get_knockon_pairs(
            self, increasing_bid: int, edges: typing.List[typing.Tuple[int, int]]
    ) -> (typing.List[typing.Tuple[int, int]], int):
        chosen_knockon_pairs = []
        candidates_bid_decrease = dict(map(lambda _: (_, self.Bids[_[1]][_[0]] - self.Bids[_[0]][_[1]]), edges))
        total_bid_decrease = 0
        edges, indegree, outdegree = trim_graph(edges)
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
                    vertex_degrees[pair[0]] + vertex_degrees[pair[1]],candidates_bid_decrease[pair]
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

    def flip_pairs_with_improvement(self, excluded_pairs: typing.List[typing.Tuple[int, int]]) -> (
            bool, int, typing.Tuple[int, int], typing.List[typing.Tuple[int, int]]) :
        print(f'{"#"*20} EXAMINING PAIRS {excluded_pairs} {"#" *20}')
        for pair in excluded_pairs:
            print(f'{"="*20} EXAMINING PAIR {pair} {"=" *20}')
            print(f'{pair} -> {pair[::-1]}: {self.Bids[pair[0]][pair[1]]} -> {self.Bids[pair[1]][pair[0]]}')
            potential_increasing_bid = self.Bids[pair[0]][pair[1]] - self.Bids[pair[1]][pair[0]]
            solution = copy.deepcopy(self.Solution)
            solution[solution.index(pair[::-1])] = pair
            residual_edges, _, _ = trim_graph(solution)
            if not residual_edges:
                print('no loops formed')
                return True, potential_increasing_bid, pair, []
            candidates, decreasing_bid = self.get_knockon_pairs(potential_increasing_bid, residual_edges)
            if decreasing_bid == -1:
                continue
            print('candidates: ', candidates, 'decreasing bid: ', decreasing_bid)
            if self.can_be_flipped(pair, candidates):
                return True, potential_increasing_bid - decreasing_bid, pair, candidates
        return False, 0, [], []

    def solve(self) -> None:
        super().solve()
        pairs_with_higher_bid = list(self.obtain_pairs_with_higher_bid())
        flipped, increased_bid, pair, knocked_on_pairs = self.flip_pairs_with_improvement(pairs_with_higher_bid)
        while flipped:
            print('Updating Solution...')
            print(f"Objective: {self.Objective} -> {self.Objective + increased_bid}")
            print(f"solution: flipped {pair[::-1]} -> {pair}")
            self.Solution[self.Solution.index(pair[::-1])] = pair
            self.Objective += increased_bid
            self.MemberPriorities[pair[0]][pair[1]] = 1
            self.MemberPriorities[pair[1]][pair[0]] = 0
            for candidate in knocked_on_pairs:
                print(f'solution: flipped {candidate} -> {candidate[::-1]}')
                self.Solution[self.Solution.index(candidate)] = candidate[::-1]
                self.MemberPriorities[candidate[0]][candidate[1]] = 0
                self.MemberPriorities[candidate[1]][candidate[0]] = 1
            pairs_with_higher_bid = list(self.obtain_pairs_with_higher_bid())
            flipped, increased_bid, pair, knocked_on_pairs = self.flip_pairs_with_improvement(pairs_with_higher_bid)