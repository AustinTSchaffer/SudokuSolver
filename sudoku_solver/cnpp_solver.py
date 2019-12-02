from . import cnpp

class NumberPlacementPuzzleSolver(object):
    def solve(self, puzzle: cnpp.NumberPlacementPuzzle):
        """
        Solves the input number-placement puzzle. Modifies and returns the
        original object.
        """
        while not puzzle.solved:
            for group in puzzle._groups:
                self.process_cell_group(group)

        return puzzle

    def process_cell_group(self, group: cnpp.CellGroup):
        if len(group.unsolved_cells) == 0:
            return

        self.remove_values_from_potential_values(group)

    def remove_values_from_potential_values(self, group: cnpp.CellGroup):
        """
        This function models the obvious strategy, where potential values
        (a.k.a. pencil markings) are erased from all of the cells in a group if
        the group already contains a solved cell that contains the value.

        Returns a set of the cells that were altered.
        """

        cells_changed = set()

        any_cells_changed = True
        while any_cells_changed:
            any_cells_changed = False

            distinct_values = {
                cell.value
                for cell in
                group.solved_cells
            }

            for cell in group.unsolved_cells:
                if not cell.value:
                    if cell.remove_values(distinct_values):
                        any_cells_changed = True
                        cells_changed.add(cell)

        return cells_changed
