from typing import Optional, List
from collections import defaultdict
import os

from . import cnpp


class SudokuCell(cnpp.Cell):
    def __init__(self, value: Optional[int], location: tuple,):
        super().__init__(
            value=value,
            potential_values=(
                [] if value else
                [v+1 for v in range(9)]
            ),
        )

        self._location = location


class SudokuPuzzle(cnpp.NumberPlacementPuzzle):
    def __init__(self, grid: List[List[int]]):
        r"""

        Initializes a model of a Sudoku puzzle from a 2D list of integers. This
        initializer assumes that D1 corresponds to row index and D2 corresponds
        to column index.

        Empty cells can be specified with any false-y value. Filled cells must
        be an integer 1 through 9.

        """

        cell_groups = defaultdict(set)

        assert len(grid) == 9
        for row_index, row in enumerate(grid):
            assert len(row) == 9
            for col_index, value in enumerate(row):
                cell = SudokuCell(
                    value=value,
                    location=(row_index, col_index),
                )

                box_index = (row_index // 3, col_index // 3)

                cell_groups[("row", row_index)].add(cell)
                cell_groups[("col", col_index)].add(cell)
                cell_groups[("box", box_index)].add(cell)

        super().__init__([
            cnpp.CellGroup(g)
            for g in cell_groups.values()
        ])

    def __str__(self) -> str:
        output = [
            ['?' for _ in range(9)]
            for _ in range(9)
        ]

        for cell in self._cells:  # type: SudokuCell
            if cell.value:
                output[cell._location[0]][cell._location[1]] = cell.value

        str_output = ""
        for row in output:
            for value in row:
                str_output += str(value)
                str_output += " "
            str_output += os.linesep

        return str_output
