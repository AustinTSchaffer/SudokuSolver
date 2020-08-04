r"""

Contains a collection of functions that can be used to solve combinatorial,
number placement puzzles that can be modeled using the classes from the cnpp
module.

"""

from collections import defaultdict
import copy
import itertools

import heapdict

from . import cnpp


def solve(puzzle: cnpp.Puzzle) -> (cnpp.Puzzle, cnpp.PuzzleState):
	"""
	Solves the input number-placement puzzle. Returns a tuple containing a copy
	of the puzzle and its resulting state. Does not modify the input puzzle.
	"""

	def _solve(_puzzle: cnpp.Puzzle) -> (cnpp.Puzzle, cnpp.PuzzleState):
		"""
		Solves the input number-placement puzzle. Modifies the input puzzle.
		Returns a tuple containing the puzzle's resulting state as well as the
		a reference to the input puzzle.
		"""

		# Uses a priority queue to help select the next cell group to process.
		group_priority_queue = heapdict.heapdict()
		for group in _puzzle.iter_groups():
			group_priority_queue[group] = 0

		current_puzzle_state = _puzzle.state()

		def _should_loop() -> bool:
			"""
			Satisfies the condition of the while loop below.
			"""
			return (
				current_puzzle_state == cnpp.PuzzleState.Unsolved
				and len(group_priority_queue) > 0
			)

		while _should_loop():
			# Pull the next group from the priority
			(group, _) = group_priority_queue.popitem()

			# Process the current group
			changed_cells = process_cell_group(_puzzle, group)

			# Calculate the number of times each group was changed
			groups_changed = defaultdict(int)
			for cell in changed_cells:
				for changed_group in _puzzle.get_groups(cell):
					groups_changed[changed_group] += 1

			# Update priorities for groups using the calculations above
			for changed_group, times_changed in groups_changed.items():
				if changed_group not in group_priority_queue:
					group_priority_queue[changed_group] = 0
				group_priority_queue[changed_group] -= times_changed

			# Recalculate the puzzle's current state
			current_puzzle_state = _puzzle.state()

		return _puzzle, current_puzzle_state

	_puzzle = copy.deepcopy(puzzle)
	_puzzle, _puzzle_state = _solve(_puzzle)

	if _puzzle_state != cnpp.PuzzleState.Unsolved:
		return _puzzle, _puzzle_state

	# If the deterministic puzzle-solving functions were not able to fully
	# solve the puzzle or determine if it has a conflict, then the solver
	# needs to make a guess. Make a copy of the puzzle in case the guess turns
	# out to cause a conflict.

	_modified_puzzle = copy.deepcopy(_puzzle)

	# Choose a cell that has the fewest number of potential values and make a
	# guess by choosing the first available potential value within that cell.
	cell_with_a_guess = None
	for cell in _modified_puzzle.iter_unsolved_cells():
		should_swap_cell = (
			not cell_with_a_guess or
			len(cell.potential_values()) < len(cell_with_a_guess.potential_values())
		)

		if should_swap_cell:
			cell_with_a_guess = cell

	guess = next(cell_with_a_guess.iter_potential_values())
	cell_with_a_guess.set_value(guess)

	# Attempt to solve using the recursive variant of solve.
	_modified_puzzle, _puzzle_state = solve(_modified_puzzle)

	if _puzzle_state == cnpp.PuzzleState.Conflict:
		# The modified puzzle could not be solved, which means the guess cannot
		# be a possible value for the cell. Remove guess from the cell's
		# potential values in the original copy.

		del _modified_puzzle

		original_cell = _puzzle.get_cell(cell_with_a_guess.location())
		original_cell.remove_value(guess)

		return solve(_puzzle)

	return _modified_puzzle, _puzzle_state

def process_cell_group(puzzle: cnpp.Puzzle, group: cnpp.Group) -> set:
	if not any(group.unsolved_cells()):
		return set()

	strategies = [
		('Erase Pencil Markings', lambda: erase_pencil_markings(puzzle)),
		('Last Remaining Cell', lambda: last_remaining_cell(group)),
		('Conjugates', lambda: check_conjugates(group)),
		('Hidden conjugates', lambda: check_hidden_conjugates(group)),
		('Intersections', lambda: check_intersections(puzzle, group)),
	]

	for name, _callable in strategies:
		cells_changed = _callable()
		if any(cells_changed):
			return cells_changed

	return set()

def erase_pencil_markings(puzzle: cnpp.Puzzle) -> set:
	"""
	This function models the obvious strategy, where pencil markings
	are erased from all of the cells in a puzzle depending on whether
	any cells .
	"""

	cells_changed = set()
	solved_cells = puzzle.iter_solved_cells()

	any_solved_cells = True
	while any_solved_cells:
		any_solved_cells = False
		newly_solved_cells = []

		for solved_cell in solved_cells:
			for group in puzzle.get_groups(solved_cell):
				for unsolved_cell in group.iter_unsolved_cells():
					if unsolved_cell.remove_value(solved_cell.value()):
						cells_changed.add(unsolved_cell)
						if unsolved_cell.value():
							any_solved_cells = True
							newly_solved_cells.append(unsolved_cell)

		solved_cells = newly_solved_cells

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
		group.iter_solved_cells()
	}

	pencil_marking_map = defaultdict(set)
	for cell in group.iter_unsolved_cells():
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
	and "one more than half the number of cells in the group, rounded down".
	"""

	changed_cells = set()

	for number in range(2, int(len(group) / 2) + 1):
		for cell_changed in check_conjugate(number, group):
			changed_cells.add(cell_changed)

	return changed_cells


def check_conjugate(number: int, group: cnpp.Group) -> set:
	"""
	Checks for conjugate (a.k.a. naked) pairs, triples, quads, etc in the
	specified group. The `number` argument specifies how many distinct
	cells and distinct symbols it should consider when checking for
	conjugates.
	"""

	# A cell is only offered for consideration into this algorithm if its
	# number of potential values is equal to or less than the `number`
	# argument. As an example, a cell with 4 potential values cannot be
	# part of a naked triple.

	applicable_cells = set()
	for cell in group.iter_unsolved_cells():
		if len(cell.potential_values()) <= number:
			applicable_cells.add(cell)

	# This algorithm operates on sub-sets of a given size from the set of
	# unsolved cells within the current group.

	changed_cells = set()
	for combination in itertools.combinations(applicable_cells, number):

		# Create a set of the distinct pencil markings that exist within
		# the specified combination of cells.

		pencil_markings = {
			pencil_marking
			for cell in combination
			for pencil_marking in cell.iter_potential_values()
		}

		if len(pencil_markings) == number:

			# If this point is reached, the number of distinct pencil markings
			# equals the number of cells in the combination, meaning those
			# symbols cannot exist in any of the other cells in this group.

			for cell in group.iter_unsolved_cells():
				if cell not in combination:
					if cell.remove_values(pencil_markings):
						changed_cells.add(cell)

			# Returning early, because the state of "applicable_cells" may no
			# longer accurately reflect the state of the group.
			if any(changed_cells):
				return changed_cells

	return changed_cells


def check_hidden_conjugates(group: cnpp.Group) -> set:
	"""
	Checks for hidden conjugate pairs, triples, quads, etc in the specified
	group. Checks for all sizes of conjugate groups between "2" and "one more
	than half the number of cells in the group, rounded down".
	"""
	changed_cells = set()

	for number in range(2, int(len(group) / 2) + 1):
		for cell_changed in check_hidden_conjugate(number, group):
			changed_cells.add(cell_changed)

	return changed_cells


def check_hidden_conjugate(number: int, group: cnpp.Group) -> set:
	"""
	Checks for hidden conjugate pairs, triples, quads, etc in the
	specified group. The `number` argument specifies how many distinct
	cells and distinct symbols it should consider when checking for
	conjugates.
	"""

	value_to_cell_map = group.potential_value_map()

	# Slims the list of values to consider down based on the `number`
	# argument. As an example, a number that could exist in 6 cells
	# cannot be part of a hidden conjugate that consists of 4 values
	# across 4 cells. Only values that appear up to `number` times in
	# the group can be considered by this section of the algorithm.

	applicable_values = set()
	for value, cells in value_to_cell_map.items():
		if len(cells) <= number:
			applicable_values.add(value)

	changed_cells = set()
	for value_combination in itertools.combinations(applicable_values, number):
		value_combination = set(value_combination)

		cells_containing_value = {
			cell
			for value in value_combination
			for cell in value_to_cell_map[value]
		}

		# If there exists a combination of values where "the number of cells
		# that reference the values" matches "the number of values being
		# considered", then all of the values that are not in that combination
		# can be removed from those cells.

		if len(cells_containing_value) == number:
			for cell in cells_containing_value:

				# Remove all potential values from the cell if the value does
				# not exist in `value_combination`

				values_to_remove = cell.potential_values() - value_combination
				if cell.remove_values(values_to_remove):
					changed_cells.add(cell)

			# Returning early, because the state of "applicable_values" may no
			# longer accurately reflect the state of the group.
			if any(changed_cells):
				return changed_cells

	return changed_cells


def check_intersections(puzzle: cnpp.Puzzle, group: cnpp.Group) -> set:
	"""
	If any one number can only be placed in the intersection of 2 groups, then
	we can remove that number from all of the cells that aren't included in that
	intersection.

	This situation is illustrated in a classic Sudoku when a 3x3 box has a
	collection cells that share a common pencil marking, when all of those cells
	are in the same row or column. If any of the other cells in that row or
	column are given that shared value, then the 3x3 box no longer has any
	cells remaining that can hold the value. This means that the value must
	exist in that intersection of the box and the row/column, removing the value
	from the rest of the row or column.

	If all of the cells in a group that contain a specific value all exist in a
	single other group that isn't the original group, then those values can be
	removed from all cells in the other group that aren't also in the original
	group.
	"""

	changed_cells = set()

	value_to_cell_map = group.potential_value_map()

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
