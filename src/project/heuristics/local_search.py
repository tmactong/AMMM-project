import typing
from src.project.heuristics.greedy import GreedyHeuristic


class LocalSearch(GreedyHeuristic):

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

    def get_formed_loops(self, cycles: typing.List[typing.List[int]]) -> typing.Iterable[typing.List[int]]:
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
        if not potential_flipped_candidates:
            print(f'no feasible uncertain flipped candidates')
            return [], -1, []
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

    def flip_pairs_with_improvement(self, excluded_pairs: typing.List[typing.Tuple[int, int]]) -> (
            bool, int, typing.Tuple[int, int], typing.List[typing.Tuple[int, int]]) :
        print(f'{"#"*20} EXAMINING PAIRS {excluded_pairs} {"#" *20}')
        for pair in excluded_pairs:
            print(f'{"="*20} EXAMINING PAIR {pair} {"=" *20}')
            print(f'{pair} -> {pair[::-1]}: {self.Bids[pair[0]][pair[1]]} -> {self.Bids[pair[1]][pair[0]]}')
            already_examined_pairs = dict()
            pair_can_be_flipped = True
            skip_this_pair = False
            potential_increasing_bid = self.Bids[pair[0]][pair[1]] - self.Bids[pair[1]][pair[0]]
            cycles = self.cycles_with_specified_pair(pair)
            formed_loops = list(self.get_formed_loops(cycles))
            if not formed_loops:
                print('no loops formed')
                return True, potential_increasing_bid, pair, []
            print('formed loops: ', formed_loops)
            certain_candidates, certain_candidates_decreasing_bid, potential_flipped_candidates = \
                self.get_potential_flipped_candidates(potential_increasing_bid, formed_loops)
            if certain_candidates_decreasing_bid == -1:
                continue
            print('certain_candidates: ', certain_candidates, 'decreasing bid: ', certain_candidates_decreasing_bid)
            print('potential flipped candidates: ', potential_flipped_candidates)
            for candidate in certain_candidates:
                print('validating candidate:', candidate)
                if not self.can_be_flipped(candidate):
                    print('Can be flipped: False')
                    skip_this_pair = True
                    break
                else:
                    print('Can be flipped: True')
            if skip_this_pair:
                continue
            if not potential_flipped_candidates:
                return True, potential_increasing_bid - certain_candidates_decreasing_bid, pair, certain_candidates
            for uncertain_candidates, decreasing_bid in sorted(potential_flipped_candidates, key=lambda x:x[1]):
                print('uncertain_candidates:', uncertain_candidates)
                for potential_flipped_candidate in uncertain_candidates:
                    print('validating candidate:', potential_flipped_candidate)
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
                    # Bugfix: uncertain_candidates: [(10, 9), (10, 9)]
                    return True, potential_increasing_bid - decreasing_bid, pair, certain_candidates + list(set(uncertain_candidates))
        return False, 0, [], []

    def solve(self) -> None:
        if self.solution_file is None:
            super().solve()
        excluded_pairs = list(self.excluded_pairs_with_higher_bid())
        flipped, increased_bid, pair, knocked_on_pairs = self.flip_pairs_with_improvement(excluded_pairs)
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
            excluded_pairs = list(self.excluded_pairs_with_higher_bid())
            flipped, increased_bid, pair, knocked_on_pairs = self.flip_pairs_with_improvement(excluded_pairs)