import typing
import copy
from src.project.heuristics.greedy import GreedyHeuristic
from src.project.helpers.graph import topological_sort, trim_graph


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

    def get_potential_flipped_candidates(
            self, increasing_bid: int, edges: typing.List[typing.Tuple[int, int]]
    ) -> (typing.List[typing.Tuple[int, int]], int):
        chosen_candidates = []
        candidates_bid_decrease = {}
        for i,j in edges:
            candidates_bid_decrease[(i,j)] = self.Bids[j][i] - self.Bids[i][j]
        #print(candidates_bid_decrease)
        bid_decrease = 0
        #print('edges:', edges)
        while edges:
            indegree, outdegree, edges = trim_graph(edges)
            #print('edges:', edges)
            if not edges:
                break
            candidates = [(i, j) for i, j in edges if 0 <= self.Bids[i][j] - self.Bids[j][i] < increasing_bid and
                          (i,j) not in chosen_candidates and (j,i) not in chosen_candidates]
            #print('candidates:', candidates)
            if not candidates:
                print(f'no feasible flipped candidates')
                return [], -1
            member_degree = {}
            candidates_degree = {}
            for member in self.CoveredMembers:
                member_degree[member] = max(indegree[member] if member in indegree else 0,
                                            outdegree[member] if member in outdegree else 0)
            for i,j in candidates:
                candidates_degree[(i,j)] = member_degree[i] + member_degree[j]
            candidates.sort(key=lambda pair: (candidates_degree[pair], candidates_bid_decrease[pair]), reverse=True)
            chosen_candidate = candidates.pop(0)
            #print(f'chosen candidate: {chosen_candidate}, decrease: {self.Bids[chosen_candidate[0]][chosen_candidate[1]]-self.Bids[chosen_candidate[1]][chosen_candidate[0]]}')
            bid_decrease += self.Bids[chosen_candidate[0]][chosen_candidate[1]] - \
                            self.Bids[chosen_candidate[1]][chosen_candidate[0]]
            if bid_decrease >= increasing_bid:
                print(f'decreased bid is greater than increasing_bid: {bid_decrease} > {increasing_bid}')
                return [], -1
            chosen_candidates.append(chosen_candidate)
            edges[edges.index(chosen_candidate)] = chosen_candidate[::-1]
        return chosen_candidates, bid_decrease

    def can_be_flipped(self, pair: typing.Tuple[int, int],knockon_pairs: typing.List[typing.Tuple[int, int]]) -> bool:
        solution = copy.deepcopy(self.Solution)
        solution[solution.index(pair[::-1])] = pair
        for knockon_pair in knockon_pairs:
            solution[solution.index(knockon_pair)] = knockon_pair[::-1]
        _, residual_edges = topological_sort(solution)
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
            _, residual_edges = topological_sort(solution)
            if not residual_edges:
                print('no loops formed')
                return True, potential_increasing_bid, pair, []

            candidates, decreasing_bid = self.get_potential_flipped_candidates(potential_increasing_bid, residual_edges)
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