r"""

Contains models that can be abstracted to model various combinatorial,
number-placement puzzles. The most famous puzzle in this category is Sudoku, but
there are other variants of the game that follow the same rules.

"""

from collections import defaultdict
import enum
from typing import Optional, Collection, Hashable, Set, Iterable, DefaultDict


class Cell(object):
    """
    Models a cell in a number-placement puzzle, which is described by a single
    cell that must contain a single value, but can be described by a list of
    potential values if the exact value of the cell is uncertain.
    """

    def __init__(self, value: Hashable = None, potential_values: Collection[Hashable] = None):
        r"""
        Initializes a cell, accepting either a single value or a collection of
        potential values.

        All potential values should be hashable and truth-y. The collection of
        symbols used by a puzzle will most likely be integers. If the puzzle
        uses 0 as a valid value, the potential values should be specified as
        strings instead of integers.
        """
        assert bool(value) ^ bool(potential_values), (
            "A Cell must have either a single value or a collection of \
                potential values. At least one must be truthy, but not both."
        )

        self._value = value
        self._potential_values = set(potential_values or ())  # type: Set[Hashable]

    def value(self) -> Optional[Hashable]:
        """
        Retrieves the value of the cell, if the value has been set or if the set
        of potential values only contains one item. If this result is truthy, it
        indicates that the cell is solved.
        """

        if self._value:
            return self._value

        if len(self._potential_values) == 1:
            self.set_value(next(iter(self._potential_values)))
            return self._value

        return None

    def set_value(self, value: Hashable):
        """
        Sets the value of this cell to a single value and erases any pencil
        markings.
        """
        self._value = value
        self._potential_values.clear()

    def potential_values(self) -> Set[Hashable]:
        """
        Returns the set of potential values for the cell.
        """
        return self._potential_values

    def iter_potential_values(self) -> Iterable[Hashable]:
        return iter(self._potential_values)

    def remove_value(self, value: Hashable) -> bool:
        """
        Removes a value the set of potential values for this cell.
        Returns true if any values were removed.
        """
        return self.remove_values([value])

    def remove_values(self, values: Collection[Hashable]) -> bool:
        """
        Removes a set of values from the set of potential values for this cell.
        Returns true if any values were removed.
        """
        any_values_removed = False

        for value in values:
            if value in self._potential_values:
                self._potential_values.remove(value)
                any_values_removed = True

        return any_values_removed

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Cell) and
            self.value() is not None and
            self.value() == other.value()
        )

    def __hash__(self):
        return id(self)


class Group(set):
    """
    Models a set of cells in a number-placement puzzle.
    """

    def __init__(self, cells: Collection[Cell]):
        super().__init__(cells)

    def __hash__(self):
        return id(self)

    def solved_cells(self) -> Set[Cell]:
        """
        Returns a set of the solved cells within the puzzle.
        """
        return {
            cell
            for cell in self
            if cell.value()
        }

    def unsolved_cells(self) -> Set[Cell]:
        """
        Returns a set of the unsolved cells within the group.
        """
        return {
            cell
            for cell in self
            if not cell.value()
        }

    def __iter__(self) -> Cell:
        return super().__iter__()

    def potential_value_map(self) -> DefaultDict[Hashable, Set[Cell]]:
        """
        Returns a default dict that maps each of the distinct hashable values
        from the group's collection of cells to sets containing the unsolved
        cells that have the value in their set of potential values.
        """

        value_to_cell_map = defaultdict(set)

        for cell in self:
            if not cell.value():
                for value in cell.potential_values():
                    value_to_cell_map[value].add(cell)

        return value_to_cell_map


class PuzzleState(enum.Enum):
    """
    Enumerates the state of a 
    """

    Solved = enum.auto(),
    Unsolved = enum.auto(),
    Conflict = enum.auto(),


class Puzzle(object):
    """
    Models a number-placement puzzle as a collection of groups of cells.
    """

    def __init__(self, groups: Collection[Group]):
        self._groups = set()  # type: Set[Group]
        self._cells = set()  # type: Set[Cell]
        self._cells_to_group_map = defaultdict(set)

        for group in groups:
            assert group not in self._groups
            self._groups.add(group)
            for cell in group:
                self._cells.add(cell)
                self._cells_to_group_map[cell].add(group)

    def state(self) -> PuzzleState:
        """
        - Returns `PuzzleState.Solved` if all of the cells in this puzzle have
        a value and there are no value conflicts.
        - Returns `PuzzleState.Conflict` if there are any groups that contain
        a duplicate value or if there are any cells that have 
        - Returns `PuzzleState.Unsolved` otherwise.
        """
        for cell in self._cells:
            if not (cell.value() or any(cell.potential_values())):
                return PuzzleState.Conflict

        for group in self._groups:
            if len(group.unsolved_cells()) > 0:
                return PuzzleState.Unsolved

            distinct_values = set()
            for cell in group:
                value = cell.value()
                if value in distinct_values:
                    return PuzzleState.Conflict
                distinct_values.add(value)

        return PuzzleState.Solved

    def solved_cells(self) -> Set[Cell]:
        """
        Returns a set of the solved cells within the puzzle.
        """
        return {
            cell
            for cell in self._cells
            if cell.value()
        }

    def unsolved_cells(self) -> Set[Cell]:
        """
        Returns a set of the unsolved cells within the puzzle.
        """
        return {
            cell
            for cell in self._cells
            if not cell.value()
        }

    def get_groups(self, cell: Cell) -> Set[Group]:
        """
        Returns all of the groups that contain the cell.
        """
        assert cell in self._cells
        return self._cells_to_group_map[cell]

    def iter_groups(self):
        return iter(self._groups)

    def iter_cells(self):
        return iter(self._cells)
