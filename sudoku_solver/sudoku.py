from typing import Optional, List, Collection
from collections import defaultdict
import os

from . import cnpp


class SudokuCell(cnpp.Cell):
    def __init__(self, location: tuple, value: int = None,
                 potential_values: Collection[int] = None):
        super().__init__(
            location=location,
            value=value,
            potential_values=(
                potential_values if potential_values else
                [] if value else
                [v+1 for v in range(9)]
            ),
        )


class SudokuPuzzle(cnpp.Puzzle):

    @classmethod
    def init_from_2d_list(cls, grid):
        r"""

        Initializes a model of a Sudoku puzzle from a 2D list. This initializer
        assumes that D1 corresponds to row index and D2 corresponds to column
        index.

        Empty cells can be specified with any false-y value in a specified
        index. Filled cells must be an integer 1 through 9. Cells can be
        specified with multiple values if they should be initialized with pencil
        markings.

        """

        cell_groups = defaultdict(set)

        assert len(grid) == 9
        for row_index, row in enumerate(grid):
            assert len(row) == 9
            for col_index, value in enumerate(row):
                loc = (row_index, col_index)
                cell = (
                    # Empty cell
                    SudokuCell(loc, value=0)
                    if not value or not int(value) else

                    # Cell with a specific value
                    SudokuCell(loc, value=int(value))
                    if len(str(value)) == 1 else

                    # Cell with pencil markings.
                    SudokuCell(loc, potential_values=[int(v) for v in str(value)])
                )

                box_index = (row_index // 3, col_index // 3)

                cell_groups[("row", row_index)].add(cell)
                cell_groups[("col", col_index)].add(cell)
                cell_groups[("box", box_index)].add(cell)

        return cls(
            [
                cnpp.Group(g)
                for g in cell_groups.values()
            ]
        )

    @classmethod
    def init_from_1d_list(cls, data: list):
        r"""
        Initializes a model of a Sudoku puzzle from a 1D list or string of
        integers. This initializer assumes that the puzzle is listed out as
        concatenated rows.

        Empty cells can be specified with any false-y value. Filled cells must
        be an integer 1 through 9.
        """

        return cls.init_from_2d_list(
            [
                [
                    int(char)
                    for char in
                    data[(index*9):(1+index)*9]
                ]
                for index in range(9)
            ]
        )

    def __str__(self) -> str:
        output = [
            ['?' for _ in range(9)]
            for _ in range(9)
        ]

        for cell in self.solved_cells():
            output[cell._location[0]][cell._location[1]] = cell.value()

        str_output = ""
        for row in output:
            for value in row:
                str_output += str(value)
                str_output += " "
            str_output += os.linesep

        return str_output
