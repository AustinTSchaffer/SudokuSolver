r"""

Contains the `NumberPlacementPuzzleSolver` class, which is an abstractable
collection of functions that can be used to solve combinatorial, number
placement puzzles that can be modeled using the classes from the cnpp module.

"""

from collections import defaultdict
import itertools

import heapdict

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
            clear_solved_cells(group) or
            last_remaining_cell(group) or
            check_conjugates(group) or
            check_hidden_conjugates(group) or
            check_intersections(puzzle, group) or
            set()
        )


def clear_solved_cells(group: cnpp.Group) -> set:
    """
    This function models the obvious strategy, where pencil markings
    are erased from all of the cells in a group if the group already
    contains a solved cell that contains the value.
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


def last_remaining_cell(group: cnpp.Group) -> set:
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


def check_conjugates(group: cnpp.Group) -> set:
    """
    Checks for conjugate (a.k.a. naked) pairs, triples, quads, etc in the
    specified group. Checks for all sizes of conjugate groups between "2"
    and "half the number of cells in the group, rounded down".
    """

    changed_cells = set()

    for number in range(2, int(len(group) / 2) + 1):
        for cell_changed in check_conjugate(number, group):
            changed_cells.add(cell_changed)

    return changed_cells


def check_conjugate(number: int, group: cnpp.Group) -> set:
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

    for combination in itertools.combinations(applicable_cells, number):
        # combination = set(combination)
        pencil_markings = set()
        for cell in combination: # type: cnpp.Cell
            pencil_markings = pencil_markings.union(cell.potential_values())
        if len(pencil_markings) == number:
            for cell in group.unsolved_cells():
                if cell not in combination:
                    if cell.remove_values(pencil_markings):
                        changed_cells.add(cell)

    return changed_cells


def check_hidden_conjugates(group: cnpp.Group) -> set:
    changed_cells = set()

    for number in range(2, int(len(group) / 2) + 1):
        for cell_changed in check_hidden_conjugate(number, group):
            changed_cells.add(cell_changed)

    return changed_cells


def check_hidden_conjugate(number: int, group: cnpp.Group) -> set:
    changed_cells = set()

    return changed_cells


def check_intersections(puzzle: cnpp.Puzzle, group: cnpp.Group) -> set:
    """
    If any one number can only be placed in the intersection of 2 groups, then
    we can remove that number from all of the cells that aren't included in that
    intersection.

    This situation is illustrated in a classic Sudoku when a 3x3 box has a
    collection cells that share a common pencil marking, when all of those cells
    are in the same row or column. If any of the other cells in that row or
    collumn are given that shared value, then the 3x3 box no longer has any
    cells remaining that can hold the value. This means that the value must
    exist in that intersection of the box and the row/column, removing the value
    from the rest of the row or column.

    If all of the cells in a group that contain a specific value all exist in a
    single other group that isn't the original group, then those values can be
    removed from all cells in the other group that aren't also in the original
    group.
    """

    changed_cells = set()

    if not any(group.unsolved_cells()):
        return changed_cells

    value_to_cell_map = defaultdict(set)
    for cell in group:
        if not cell.value():
            for value in cell.potential_values():
                value_to_cell_map[value].add(cell)

    # Caches the groups that intersect with the current group
    intersecting_groups = {
        intersecting_group
        for cell in group
        for intersecting_group in puzzle.get_groups(cell)
        if intersecting_group != group
    }

    for value, cells_containing_value in value_to_cell_map.items():
        cells_to_prune = (
            cell

            for intersecting_group in intersecting_groups
            if intersecting_group.issuperset(cells_containing_value)

            for cell in intersecting_group.unsolved_cells()
            if cell not in cells_containing_value
        )

        for cell in cells_to_prune:
            if cell.remove_value(value):
                changed_cells.add(cell)

    return changed_cells
