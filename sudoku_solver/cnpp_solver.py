r"""

Contains the `NumberPlacementPuzzleSolver` class, which is an abstractable
collection of functions that can be used to solve combinatorial, number
placement puzzles that can be modeled using the classes from the cnpp module.

"""

import heapdict
from collections import defaultdict

from . import cnpp


class NumberPlacementPuzzleSolver(object):
    def solve(self, puzzle: cnpp.Puzzle):
        """
        Solves the input number-placement puzzle. Modifies and returns the
        original object.
        """

        group_priority_queue = heapdict.heapdict()
        for group in puzzle.iter_groups():
            group_priority_queue[group] = 0

        while len(group_priority_queue) > 0:
            (group, _) = group_priority_queue.popitem()

            changed_cells = self.process_cell_group(puzzle, group)
            groups_changed = defaultdict(int)

            for cell in changed_cells:
                for changed_group in puzzle.get_groups(cell):
                    groups_changed[changed_group] += 1
            for changed_group, times_changed in groups_changed.items():
                if changed_group in group_priority_queue:
                    group_priority_queue[changed_group] -= times_changed
                else:
                    group_priority_queue[changed_group] = - times_changed

        return puzzle

    def process_cell_group(self, puzzle: cnpp.Puzzle, group: cnpp.Group) -> set:
        if len(group.unsolved_cells()) == 0:
            return set()

        return (
            self.clear_solved_cells(group) or
            self.last_remaining_cell(group) or
            # TODO: 2,3,4 are magic numbers which might not apply to non-9x9 sudokus.
            # IDEA: loop from "2" to "half the number of distinct symbols, rounded down"
            self.check_conjugates(2, group) or
            self.check_conjugates(3, group) or
            self.check_conjugates(4, group) or
            set()
        )

    def clear_solved_cells(self, group: cnpp.Group) -> set:
        """
        This function models the obvious strategy, where pencil markings
        are erased from all of the cells in a group if the group already
        contains a solved cell that contains the value.

        Returns a set of the cells that were altered.
        """

        cells_changed = set()

        solved_values = {
            cell.value()
            for cell in
            group.solved_cells()
        }

        for cell in group.unsolved_cells():
            if cell.remove_values(solved_values):
                cells_changed.add(cell)

        return cells_changed

    def last_remaining_cell(self, group: cnpp.Group) -> set:
        """
        Looks through all of the pencil markings in the group to check for
        symbols that only occur once in the pencil markings for that group.
        Checks to make sure that the pencil markings are up to date.
        """

        cells_changed = set()

        solved_values = {
            cell.value()
            for cell in
            group.solved_cells()
        }

        pencil_marking_map = defaultdict(set)
        for cell in group.unsolved_cells():
            for value in cell.iter_potential_values():
                pencil_marking_map[value].add(cell)

        for value, cells in pencil_marking_map.items():
            if value in solved_values:
                for cell in cells:  # type: cnpp.Cell
                    cell.remove_value(value)
                    cells_changed.add(cell)
            elif len(cells) == 1:
                cell = next(iter(cells))
                cell.set_value(value)
                cells_changed.add(cell)

        return cells_changed

    def check_conjugates(self, number: int, group: cnpp.Group):
        """
        Checks for conjugate (a.k.a. naked) pairs, triples, quads, etc in the
        specified group. The `number` property specifies how many distinct
        cells and distinct symbols it should consider when checking for
        conjugates.
        """

        applicable_cells = set()
        for cell in group.unsolved_cells():
            if len(cell.potential_values()) <= number:
                applicable_cells.add(cell)

        if len(applicable_cells) < number:
            return set()

        changed_cells = set()

        # for cell in nCr of applicable cells:
        #   check if union of the cells' potential values == number
        #     for cell in cells that aren't in that nCr
        #       if (remove those values):
        #         add cells to changed cells

        return changed_cells
