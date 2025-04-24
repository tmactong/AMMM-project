import typing
from src.project.heuristics.greedy import GreedyHeuristic
from src.project.helpers.cycles_generator import generate_all_permutations


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

    def get_formed_loops(self, cycles: typing.Iterable[typing.List[int]]) -> typing.Iterable[typing.List[int]]:
        for cycle in cycles:
            cycle_priority = 0
            for i in range(len(cycle) - 1):
                cycle_priority += self.MemberPriorities[cycle[i]][cycle[i + 1]]
            if cycle_priority + 1 == len(cycle):
                yield cycle

    def get_potential_flipped_candidates(
            self, increasing_bid: int, cycles: typing.List[typing.List[int]]
    ) -> (typing.List[typing.Tuple[int, int]], int):

        def most_candidate(
                _uncertain_candidates: typing.List[typing.List[typing.Tuple[int, int]]]
        ) -> typing.List[typing.Tuple[int, int]]:
            most_candidates = []
            while True:
                most_count = 0
                most_count_candidate = ()
                if most_candidates:
                    _uncertain_candidates = [x for x in _uncertain_candidates if most_candidates[-1] not in x]
                for candidates in _uncertain_candidates:
                    for candidate in candidates:
                        count = [ candidate in _candidates for _candidates in _uncertain_candidates ].count(True)
                        if count > most_count:
                            most_count = count
                            most_count_candidate = candidate
                if most_count:
                    most_candidates.append(most_count_candidate)
                else:
                    break
            return most_candidates

        candidate_groups = [[] for _ in range(len(cycles))]
        for i in range(len(cycles)):
            for j in range(len(cycles[i]) - 1):
                if self.Bids[cycles[i][j]][cycles[i][j + 1]] - self.Bids[cycles[i][j + 1]][cycles[i][j]] < increasing_bid and \
                        self.Bids[cycles[i][j]][cycles[i][j + 1]] >= self.Bids[cycles[i][j + 1]][cycles[i][j]]:
                    candidate_groups[i].append((cycles[i][j], cycles[i][j + 1]))
            if not candidate_groups[i]:
                print(f'no feasible flipped candidates for {cycles[i]}')
                return [], -1

        print('candidate_groups', candidate_groups)
        most_candidates = most_candidate(candidate_groups)
        decreasing_bid = 0
        for candidate in most_candidates:
            decreasing_bid += self.Bids[candidate[0]][candidate[1]] - self.Bids[candidate[1]][candidate[0]]
        if decreasing_bid >= increasing_bid:
            print(f'decreased bid is greater than increasing_bid: {decreasing_bid} > {increasing_bid}')
            return [], -1
        return most_candidates, decreasing_bid

    def can_be_flipped(self, pair: typing.Tuple[int, int]) -> bool:
        cycles = generate_all_permutations(self.MemberCount, pair)
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
            skip_this_pair = False
            potential_increasing_bid = self.Bids[pair[0]][pair[1]] - self.Bids[pair[1]][pair[0]]
            cycles = generate_all_permutations(self.MemberCount, pair)
            formed_loops = list(self.get_formed_loops(cycles))
            if not formed_loops:
                print('no loops formed')
                return True, potential_increasing_bid, pair, []
            print('formed loops: ', formed_loops)
            candidates, decreasing_bid = self.get_potential_flipped_candidates(potential_increasing_bid, formed_loops)
            if decreasing_bid == -1:
                continue
            print('candidates: ', candidates, 'decreasing bid: ', decreasing_bid)
            for candidate in candidates:
                print('validating candidate:', candidate)
                if not self.can_be_flipped(candidate):
                    print('Can be flipped: False')
                    skip_this_pair = True
                    break
                else:
                    print('Can be flipped: True')
            if skip_this_pair:
                continue
            else:
                return True, potential_increasing_bid - decreasing_bid, pair, candidates
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