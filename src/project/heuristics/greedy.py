import typing

from . import HeuristicMethod

class GreedyHeuristic(HeuristicMethod):

    CoveredPairs: typing.List[typing.Tuple[int, int]]

    def __init__(self, member_count: int, bids: typing.Dict[int, typing.Dict[int]]):
        super().__init__(member_count, bids)
        self.CoveredPairs = []

    def update_covered_pairs(self, member_pair: typing.Tuple[int, int]) -> None:
        self.CoveredPairs.append(member_pair)
        self.CoveredPairs.append(member_pair[::-1])

    def update_candidates(self, member_pair: typing.Tuple[int, int]) -> None:
        """
        Example:
            self.Candidates = [ (1, 3), (2, 3), (3, 1), (3, 2)]
            self.Solution = [(1,2), (2,3)]
            self.update_candidates((2,3))
            => self.Candidates = [ (1, 3), (3, 1)]
        """
        """
        candidates = list()
        for candidate in self.Candidates:
            if candidate != new_member_pair and candidate != new_member_pair[::-1]:
                for member_pair in self.Solution:
                    if set(member_pair) & set(candidate):
                        candidates.append(candidate)
        self.Candidates = candidates
        """
        self.Candidates = [candidate for candidate in self.Candidates
                           if candidate != member_pair and candidate != member_pair[::-1]]


    def sort_candidates_by_quality(self) -> typing.List[typing.Tuple[int, int]]:
        return sorted(self.Candidates, key=lambda x: self.bids[x[0]][x[1]], reverse=True)

    def _newly_constructed_cycles(self, member_pair: typing.Tuple[int, int]) -> typing.List[typing.Tuple[int, ...]]:
        start_point = member_pair[0]
        for covered_pair in self.CoveredPairs:
            if start_point == covered_pair[0]:

    def validate_candidate(self, candidate: typing.Tuple[int, int]) -> bool:
        pass