import time
import typing
import json
from src.project.heuristics.greedy import GreedyHeuristic


class LocalSearch(GreedyHeuristic):

    def __init__(self, member_count: int, bids: typing.Dict[int, typing.Dict[int, int]], solution_file: typing.Optional[str] = None ) -> None:
        super().__init__(member_count, bids)
        self.solution_file = solution_file
        if self.solution_file:
            print('import Greedy solution from file:', self.solution_file)
            self.load_greedy_solution()

    def load_greedy_solution(self):
        with open(self.solution_file, 'r') as f:
            greedy_result = json.load(f)
            Solution = greedy_result['Solution']
            self.Solution = [tuple(x) for x in Solution]
            MemberPriorities = greedy_result['MemberPriorities']
            for i in MemberPriorities:
                for j in MemberPriorities[i]:
                    self.MemberPriorities[int(i)][int(j)] = MemberPriorities[i][j]
            self.Objective = greedy_result['Objective']
            for i in range(1, self.MemberCount+1):
                for j in range(1, self.MemberCount+1):
                    if i != j:
                        self.CoveredPairs.append((i, j))

    def excluded_pairs_with_higher_bid(self) -> typing.Iterable[typing.Tuple[int, int]]:
        """
        get pairs that have higher bid
        for example:
            if Bids[i][j] > Bids[j][i] and Priority[i][j] = 0:
                yield (i,j), Bids[i][j] - Bids[j][i]
        """
        for pair in self.Solution:
            if self.Bids[pair[1]][pair[0]] > self.Bids[pair[0]][pair[1]]:
                yield pair[::-1]

    def cycles_with_specified_pair(self, pair: typing.Tuple[int, int]) -> typing.List[typing.List[int]]:
        """
        pair (i, j)
        Priority[i][j] = 0 & Bids[i][j] > Bids[j][i]
        """
        cycles = self._uniq_newly_constructed_cycles(pair)
        return [cycle for cycle in cycles if cycle != list(pair[::-1])]

    """
        def get_infeasible_cycles(self, cycles: typing.List[typing.List[int]]) -> typing.Iterable[typing.List[int]]:
        # find infeasible cycles that really caused by pair (i,j) where Bids[i][j] > Bids[j][i] and Priority[i][j] = 0
        # that means max(Bids[k][l], Bids[l][k]) >= Bids[i][j] for every (k,l) in cycle if (k,l) != (i,j)  
        for cycle in cycles:
            cycle_priority = 0
            for i in range(len(cycle) - 1):
                cycle_priority += self.MemberPriorities[cycle[i]][cycle[i + 1]]
            if cycle_priority + 1 == len(cycle):
                bids_greater_than_this_pair = True
                for j in range(len(cycle) - 1):
                    if max(self.Bids[cycle[j]][cycle[j + 1]],
                           self.Bids[cycle[j + 1]][cycle[j]]) < self.Bids[cycle[-1]][cycle[0]]:
                        bids_greater_than_this_pair = False
                        break
                if bids_greater_than_this_pair:
                    print('infeasible cycle', cycle)
                    yield cycle
    """

    def get_infeasible_cycles(self, cycles: typing.List[typing.List[int]]) -> typing.Iterable[typing.List[int]]:
        for cycle in cycles:
            cycle_priority = 0
            for i in range(len(cycle) - 1):
                cycle_priority += self.MemberPriorities[cycle[i]][cycle[i + 1]]
            if cycle_priority + 1 == len(cycle):
                yield cycle

    def get_potential_flipped_candidates(
            self, increasing_bid: int, cycles: typing.List[typing.List[int]]
    ) -> (typing.List[typing.Tuple[int, int]], int, typing.List[typing.Tuple[typing.List[int], int]]):
        def inner_loop(
                pairs: typing.List[typing.Tuple[int, int]], decreasing_bid: int,
                candidates: typing.List[typing.List[typing.Tuple[int, int]]]
        ) -> typing.Iterable[typing.Tuple[typing.List[typing.Tuple[int, int]], int]]:
            #print('candidates', candidates)
            for candidate in candidates[len(pairs)]:
                added = False
                decreasing_bid_from_k = 0
                if candidate in pairs:
                    added = True
                elif self.Bids[candidate[0]][candidate[1]] - self.Bids[candidate[1]][candidate[0]] + decreasing_bid < \
                        increasing_bid:
                    added = True
                    decreasing_bid_from_k = self.Bids[candidate[0]][candidate[1]] - self.Bids[candidate[1]][candidate[0]]
                if added:
                    if len(pairs) + 1 == len(candidates):
                        yield pairs + [candidate], decreasing_bid + decreasing_bid_from_k
                    else:
                        yield from inner_loop(pairs + [candidate], decreasing_bid + decreasing_bid_from_k, candidates)

        candidate_groups = [[] for _ in range(len(cycles))]
        for i in range(len(cycles)):
            for j in range(len(cycles[i]) - 1):
                if self.Bids[cycles[i][j]][cycles[i][j + 1]] - self.Bids[cycles[i][j + 1]][cycles[i][j]] < increasing_bid and \
                        self.Bids[cycles[i][j]][cycles[i][j + 1]] >= self.Bids[cycles[i][j + 1]][cycles[i][j]]:
                    candidate_groups[i].append((cycles[i][j], cycles[i][j + 1]))
            if not candidate_groups[i]:
                print(f'no feasible flipped candidates for {cycles[i]}')
                return [], -1, []
        certain_candidates = list()
        certain_candidates_decreasing_bid = 0
        uncertain_candidates = list()
        print('candidate_groups', candidate_groups)
        for candidate_group in candidate_groups:
            if len(candidate_group) == 1:
                if candidate_group[0] not in certain_candidates:
                    certain_candidates.append(candidate_group[0])
                    certain_candidates_decreasing_bid += self.Bids[candidate_group[0][0]][candidate_group[0][1]] - \
                                                           self.Bids[candidate_group[0][1]][candidate_group[0][0]]
        if certain_candidates_decreasing_bid >= increasing_bid:
            print(f'decreased bid is already greater than increasing_bid: {certain_candidates_decreasing_bid} > {increasing_bid}')
            return [], -1, []
        for candidate_group in candidate_groups:
            if not set(candidate_group) & set(certain_candidates):
                uncertain_candidates.append(candidate_group)
        if not uncertain_candidates:
            print('no uncertain candidates')
            return certain_candidates, certain_candidates_decreasing_bid, []
        potential_flipped_candidates = inner_loop([], certain_candidates_decreasing_bid, uncertain_candidates)
        to_check_candidates = list()
        for candidates, decreasing_bid in potential_flipped_candidates:
            drop = False
            for i in range(len(candidates)):
                for j in range(len(uncertain_candidates)):
                    if i != j:
                        if candidates[i] in uncertain_candidates[j] and candidates[j] != candidates[i]:
                            """drop these candidates"""
                            drop = True
                            break
                if drop:
                    break
                else:
                    to_check_candidates.append((candidates, decreasing_bid))
        return certain_candidates, certain_candidates_decreasing_bid, to_check_candidates

    def can_be_flipped(self, pair: typing.Tuple[int, int]) -> bool:
        # TODO: flip more pairs if needed
        cycles = self._uniq_newly_constructed_cycles(pair)
        for cycle in cycles:
            priorities = 0
            for i in range(len(cycle) - 1):
                priorities += self.MemberPriorities[cycle[i]][cycle[i + 1]]
            if priorities == len(cycle) - 1:
                return False
        return True

    def flip_pairs_with_improvement(self, excluded_pairs: typing.List[typing.Tuple[int, int]]) -> bool:
        for pair in excluded_pairs:
            already_examined_pairs = dict()
            pair_can_be_flipped = True
            certain_candidates = []
            flipped_uncertain_candidates = []
            flipped_decreasing_bid = 0
            print('#'*20, 'CHECKING PAIR', '#'*20)
            print(pair, '->', pair[::-1], ':', self.Bids[pair[0]][pair[1]], '->', self.Bids[pair[1]][pair[0]])
            potential_increasing_bid = self.Bids[pair[0]][pair[1]] - self.Bids[pair[1]][pair[0]]
            cycles = self.cycles_with_specified_pair(pair)
            infeasible_cycles = list(self.get_infeasible_cycles(cycles))
            if not infeasible_cycles:
                print('no feasible cycles')
            else:
                print('infeasible cycles: ', infeasible_cycles)
                certain_candidates, certain_candidates_decreasing_bid, potential_flipped_candidates = self.get_potential_flipped_candidates(
                    potential_increasing_bid, infeasible_cycles)
                if certain_candidates_decreasing_bid == -1:
                    continue
                print('certain_candidates: ', certain_candidates, 'decreasing bid: ', certain_candidates_decreasing_bid)
                print('potential flipped candidates: ', potential_flipped_candidates)
                skip_this_pair = False
                for candidate in certain_candidates:
                    print('Validating candidate:', candidate)
                    if not self.can_be_flipped(candidate):
                        print('Can be flipped: False')
                        skip_this_pair = True
                        break
                    else:
                        print('Can be flipped: True')
                if skip_this_pair:
                    continue
                for uncertain_candidates, decreasing_bid in sorted(potential_flipped_candidates, key=lambda x:x[1]):
                    print('uncertain_candidates:', uncertain_candidates)
                    for potential_flipped_candidate in uncertain_candidates:
                        print('Validating candidate:', potential_flipped_candidate)
                        if potential_flipped_candidate in already_examined_pairs:
                            flipped = already_examined_pairs[potential_flipped_candidate]
                        else:
                            flipped = self.can_be_flipped(potential_flipped_candidate)
                            already_examined_pairs[potential_flipped_candidate] = flipped
                        print('Can be flipped:', flipped)
                        if not flipped:
                            pair_can_be_flipped = False
                            break
                    if pair_can_be_flipped:
                        flipped_uncertain_candidates = uncertain_candidates
                        flipped_decreasing_bid = decreasing_bid
                        break
            if pair_can_be_flipped:
                print(f"Objective increases: {potential_increasing_bid - flipped_decreasing_bid}")
                print(f"solution: flipped {pair[::-1]} -> {pair}")
                self.Solution[self.Solution.index(pair[::-1])] = pair
                self.Objective += potential_increasing_bid - flipped_decreasing_bid
                self.MemberPriorities[pair[0]][pair[1]] = 1
                self.MemberPriorities[pair[1]][pair[0]] = 0
                for candidate in certain_candidates + flipped_uncertain_candidates:
                    print(f'solution: flipped {candidate} -> {candidate[::-1]}')
                    self.Solution[self.Solution.index(candidate)] = candidate[::-1]
                    self.MemberPriorities[candidate[0]][candidate[1]] = 0
                    self.MemberPriorities[candidate[1]][candidate[0]] = 1

    def solve(self) -> None:
        """
        TODO: potential_flipped_pair blacklist
        """
        if self.solution_file is None:
            super().solve()
        excluded_pairs = list(self.excluded_pairs_with_higher_bid())
        print('excluded_pairs:', excluded_pairs)
        for pair in excluded_pairs:
            checked_pairs = dict()
            pair_can_be_flipped = True
            certain_candidates = []
            flipped_uncertain_candidates = []
            flipped_decreasing_bid = 0
            print('#'*20, 'CHECKING PAIR', '#'*20)
            print(pair, '->', pair[::-1], ':', self.Bids[pair[0]][pair[1]], '->', self.Bids[pair[1]][pair[0]])
            potential_increasing_bid = self.Bids[pair[0]][pair[1]] - self.Bids[pair[1]][pair[0]]
            cycles = self.cycles_with_specified_pair(pair)
            infeasible_cycles = list(self.get_infeasible_cycles(cycles))
            if not infeasible_cycles:
                print('no feasible cycles')
            else:
                print('infeasible cycles: ', infeasible_cycles)
                certain_candidates, certain_candidates_decreasing_bid, potential_flipped_candidates = self.get_potential_flipped_candidates(
                    potential_increasing_bid, infeasible_cycles)
                if certain_candidates_decreasing_bid == -1:
                    continue
                print('certain_candidates: ', certain_candidates, 'decreasing bid: ', certain_candidates_decreasing_bid)
                print('potential flipped candidates: ', potential_flipped_candidates)
                skip_this_pair = False
                for candidate in certain_candidates:
                    print('Validating candidate:', candidate)
                    if not self.can_be_flipped(candidate):
                        print('Can be flipped: False')
                        skip_this_pair = True
                        break
                    else:
                        print('Can be flipped: True')
                if skip_this_pair:
                    continue
                for uncertain_candidates, decreasing_bid in sorted(potential_flipped_candidates, key=lambda x:x[1]):
                    print('uncertain_candidates:', uncertain_candidates)
                    for potential_flipped_candidate in uncertain_candidates:
                        print('Validating candidate:', potential_flipped_candidate)
                        if potential_flipped_candidate in checked_pairs:
                            flipped = checked_pairs[potential_flipped_candidate]
                        else:
                            flipped = self.can_be_flipped(potential_flipped_candidate)
                            checked_pairs[potential_flipped_candidate] = flipped
                        print('Can be flipped:', flipped)
                        if not flipped:
                            pair_can_be_flipped = False
                            break
                    if pair_can_be_flipped:
                        flipped_uncertain_candidates = uncertain_candidates
                        flipped_decreasing_bid = decreasing_bid
                        break
            if pair_can_be_flipped:
                print(f"Objective increases: {potential_increasing_bid - flipped_decreasing_bid}")
                print(f"solution: flipped {pair[::-1]} -> {pair}")
                self.Solution[self.Solution.index(pair[::-1])] = pair
                self.Objective += potential_increasing_bid - flipped_decreasing_bid
                self.MemberPriorities[pair[0]][pair[1]] = 1
                self.MemberPriorities[pair[1]][pair[0]] = 0
                for candidate in certain_candidates + flipped_uncertain_candidates:
                    print(f'solution: flipped {candidate} -> {candidate[::-1]}')
                    self.Solution[self.Solution.index(candidate)] = candidate[::-1]
                    self.MemberPriorities[candidate[0]][candidate[1]] = 0
                    self.MemberPriorities[candidate[1]][candidate[0]] = 1

