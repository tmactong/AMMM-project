import typing

from src.project.heuristics.greedy import GreedyHeuristic


class LocalSearch(GreedyHeuristic):

    def __init__(self, member_count: int, bids: typing.Dict[int, typing.Dict[int, int]], import_solution: bool = False):
        super().__init__(member_count, bids)

    def excluded_pairs_with_higher_bid(self) -> typing.Iterable[typing.Tuple[int, int]]:
        """
        get pairs that have higher bid
        for example:
            if Bids[i][j] > Bids[j][i] and Priority[i][j] = 0:
                yield (i,j)
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

    def get_infeasible_cycles(self, cycles: typing.List[typing.List[int]]) -> typing.Iterable[typing.List[int]]:
        """
        find infeasible cycles that really caused by pair (i,j) where Bids[i][j] > Bids[j][i] and Priority[i][j] = 0
        that means max(Bids[k][l], Bids[l][k]) >= Bids[i][j] for every (k,l) in cycle if (k,l) != (i,j)
        """
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

    def get_potential_flipped_chains(
            self, increasing_bid: int, cycles: typing.List[typing.List[int]]
    ) -> typing.Iterable[typing.Tuple[typing.List[typing.Tuple[int, int]], int]]:
        def inner_loop(
                pairs: typing.List[typing.Tuple[int, int]], decreasing_bid: int,
                candidates: typing.List[typing.List[typing.Tuple[int, int]]]
        ) -> typing.Iterable[typing.Tuple[typing.List[typing.Tuple[int, int]], int]]:
            print('candidates', candidates)
            for candidate in candidates[len(pairs)]:
                added = False
                decreasing_bid_from_k = 0
                if candidate in pairs:
                    added = True
                elif self.Bids[candidate[0]][candidate[1]] >= self.Bids[candidate[1]][candidate[0]] and \
                        self.Bids[candidate[0]][candidate[1]] - self.Bids[candidate[1]][candidate[0]] + decreasing_bid < \
                        increasing_bid:
                    """only consider (i,j) that if Bids[i][j] >= Bids[j][i] and Priority[i][j] = 1"""
                    added = True
                    decreasing_bid_from_k = self.Bids[candidate[0]][candidate[1]] - self.Bids[candidate[1]][
                        candidate[0]]
                if added:
                    if len(pairs) + 1 == len(cycles):
                        yield pairs + [candidate], decreasing_bid + decreasing_bid_from_k
                    else:
                        yield from inner_loop(pairs + [candidate], decreasing_bid + decreasing_bid_from_k, candidates)

        candidates = [[] for _ in range(len(cycles))]
        for i in range(len(cycles)):
            for j in range(len(cycles[i]) - 1):
                if self.Bids[cycles[i][j]][cycles[i][j + 1]] - self.Bids[cycles[i][j + 1]][
                    cycles[i][j]] < increasing_bid:
                    candidates[i].append((cycles[i][j], cycles[i][j + 1]))
            if not candidates[i]:
                return None
        yield from inner_loop([], 0, candidates)

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

    def solve(self) -> None:
        """
        TODO: potential_flipped_pair blacklist
        (5, 6) -> (6, 5) : 6 -> 5
        infeasible cycle [6, 9, 10, 4, 5]
        infeasible cycle [6, 9, 10, 3, 4, 5]
        infeasible cycle [6, 9, 10, 3, 5]
        candidates [[(9, 10), (4, 5)], [(9, 10), (4, 5)], [(9, 10)]]
        candidates [[(9, 10), (4, 5)], [(9, 10), (4, 5)], [(9, 10)]]
        candidates [[(9, 10), (4, 5)], [(9, 10), (4, 5)], [(9, 10)]]
        candidates [[(9, 10), (4, 5)], [(9, 10), (4, 5)], [(9, 10)]]
        candidates [[(9, 10), (4, 5)], [(9, 10), (4, 5)], [(9, 10)]]
        candidates [[(9, 10), (4, 5)], [(9, 10), (4, 5)], [(9, 10)]]
        candidates [[(9, 10), (4, 5)], [(9, 10), (4, 5)], [(9, 10)]]
        (9, 10) can be flipped: False ,decreasing bid: 0 ,potential increasing bid: 1
        (9, 10) can be flipped: False ,decreasing bid: 0 ,potential increasing bid: 1
        """
        super().solve()
        for pair in self.excluded_pairs_with_higher_bid():
            print(pair, '->', pair[::-1], ':', self.Bids[pair[0]][pair[1]], '->', self.Bids[pair[1]][pair[0]])
            potential_increasing_bid = self.Bids[pair[0]][pair[1]] - self.Bids[pair[1]][pair[0]]
            cycles = self.cycles_with_specified_pair(pair)
            infeasible_cycles = self.get_infeasible_cycles(cycles)
            potential_flipped_chains = self.get_potential_flipped_chains(
                potential_increasing_bid, list(infeasible_cycles))
            sorted_flipped_chains = sorted(potential_flipped_chains, key=lambda _: _[1])
            found_flipped_pair = False
            for chain, decreasing_bid in sorted_flipped_chains:
                for potential_flipped_pair in chain:
                    flipped = self.can_be_flipped(potential_flipped_pair)
                    print(potential_flipped_pair, 'can be flipped:', flipped, ',decreasing bid:',
                          decreasing_bid, ',potential increasing bid:', potential_increasing_bid)
                    if flipped:
                        self.Solution.remove(potential_flipped_pair)
                        self.Solution.append(potential_flipped_pair[::-1])
                        self.Solution.remove(pair[::-1])
                        self.Solution.append(pair)
                        self.MemberPriorities[potential_flipped_pair[0]][potential_flipped_pair[1]] = 0
                        self.MemberPriorities[potential_flipped_pair[1]][potential_flipped_pair[0]] = 1
                        self.MemberPriorities[pair[0]][pair[1]] = 1
                        self.MemberPriorities[pair[1]][pair[0]] = 0
                        self.Objective += potential_increasing_bid - decreasing_bid
                        found_flipped_pair = True
                        break
                if found_flipped_pair:
                    break
