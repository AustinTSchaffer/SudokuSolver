r"""

Contains models that can be abstracted to model various combinatorial,
number-placement puzzles. The most famous puzzle in this category is Sudoku, but
there are other variants of the game that follow the same rules.

"""

from typing import Optional, Collection, Union

__all__ = [
    "Cell",
    "CellGroup",
    "NumberPlacementPuzzle",
]


class Cell(object):
    """
    Models a cell in a number-placement puzzle, which is described by a single
    cell that must contain a single value, but can be described by a list of
    potential values if the exact value of the cell is uncertain.
    """

    def __init__(self, value: int = None, potential_values: Collection[int] = None):
        r"""
        Initializes a cell, accepting either a value or 
        """
        assert bool(value) ^ bool(potential_values), (
            "A Cell must have either a single value or a collection of \
                potential values. At least one must be truthy, but not both."
        )

        self._value = value
        self._potential_values = set(potential_values or ())

    @property
    def value(self) -> Optional[int]:
        """
        Retrieves the value of the cell, if the value has been set or if the
        set of potential values only contains one item, indicating that the
        cell 
        """

        if self._value:
            return self._value

        if len(self._potential_values) == 1:
            self._value = next(iter(self._potential_values))
            return self._value

        return None

    @property
    def potential_values(self) -> Collection[int]:
        """
        Returns a copy of the set of potential values
        """
        return set(self._potential_values)

    def remove_values(self, values: Union[int, Collection[int]]):
        """
        Removes a value or a set of values from the set of potential values for
        this cell.
        """
        def _safe_remove(value):
            if value in self._potential_values:
                self._potential_values.remove(value)

        if type(values) is int:
            _safe_remove(values)
            return

        for value in values:
            _safe_remove(value)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Cell) and
            self.value is not None and
            self.value == other.value
        )

    def __hash__(self):
        return id(self)


class CellGroup(object):
    """
    Models a set of cells in a number-placement puzzle.
    """

    def __init__(self, cells: Collection[Cell]):
        self._cells = set()
        for cell in cells:
            assert cell not in self._cells
            self._cells.add(cell)

    def __contains__(self, cell: Cell) -> bool:
        return cell in self._cells

    def __hash__(self):
        return id(self)

    def __iter__(self):
        return iter(self._cells)


class NumberPlacementPuzzle(object):
    """
    Models a number-placement puzzle as a collection of groups of Cells.
    """

    def __init__(self, groups: Collection[CellGroup]):
        self._groups = set()
        self._cells = set()
        for group in groups:
            assert group not in self._groups
            self._groups.add(group)
            for cell in group:
                self._cells.add(cell)
