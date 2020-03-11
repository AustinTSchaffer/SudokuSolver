import csv
import os

import multiprocessing

from sudoku_solver import sudoku, cnpp_solver, cnpp

# Downloaded 1-million sudokus as a CSV, where column 1 was titled "quizzes" and
# was filled with 1D-formatted sudokus.
DATA_FILE_NAME = os.path.expanduser('~/Downloads/sudoku_data.csv')

def iterate_through_puzzles():
    with open(DATA_FILE_NAME, 'r') as data:
        reader = csv.DictReader(data)
        for index, row in enumerate(reader, 1):
            puzzle, _ = row['quizzes'], row['solutions']
            yield index, puzzle

def solve_sudoku(input_data):
    index, puzzle = input_data
    sudoku_puzzle = sudoku.SudokuPuzzle.init_from_1d_list(puzzle)
    completed_puzzle, state = cnpp_solver.solve(sudoku_puzzle)
    return (index, puzzle, state, completed_puzzle)

def main():
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_cores - 2)

    for index, puzzle, result, completed_puzzle in pool.imap_unordered(solve_sudoku, iterate_through_puzzles()):
        print(f'Result {result} Puzzle Index: {index} Initial configuration: {puzzle}')

    print('Done')

if __name__ == '__main__':
    main()
