# Sudoku Solver

This repository contains a Python implementation of a Sudoku solver.

## About

The primary purpose of this package package is to provide classes that model
Sudoku as an abstract, logic-based, combinatorial, symbol-placement puzzle,
and to provide classes and functions that can be used to solve puzzles that
can be modelled using those classes. This package contains a class that
specifically models classic Sudoku, but the contained solver can solve a
variety of problems that can be expressed the same abstraction. This includes,
but is not limited to, the following puzzles:

- Twin Sudoku, Samurai Sudoku, and other overlapping Sudoku puzzles
- Nonomino (Jigsaw Sudoku)
- Mini Sudoku
- Hyper Sudoku

This solver is not capable of solving Killer Sudoku, Kakuro, or other
number-placement puzzles where arithmetic is used as a restriction. This solver
is also not capable of solving puzzles where a grouping of single values can
contain duplicate entries, nor any puzzles where alpha-characters are used
and the resulting puzzle is expected to contain a hidden word or phrase.

Some of the sudoku-solving strategies used in this module were crafted based on
strategies that I have used to solve Sudokus. Other strategies and strategy
descriptions have been borrowed from
[SudokuWiki](https://www.sudokuwiki.org/Getting_Started), which has an
exhaustive list of strategies that can be used to solve Sudokus. This site is a
great resource is you are looking for strategies to improve your own personal
games and contains to a wealth of strategies that were not included in this
project.

## Example Execution

```
(venv) austin@ub:sudoku-solver$ python -m sudoku_solver

Beginner Starting Position:
? 4 2 3 ? 1 7 ? ? 
? ? 7 9 5 6 4 2 8 
5 6 ? 7 2 4 ? 1 ? 
8 9 ? ? 4 ? ? ? 7 
2 ? ? 6 9 7 ? 8 3 
1 7 6 2 ? 8 9 4 5 
? 8 9 5 1 2 6 3 4 
4 3 1 8 ? ? ? 7 2 
6 2 5 4 ? 3 8 ? 1 

Solved:
9 4 2 3 8 1 7 5 6 
3 1 7 9 5 6 4 2 8 
5 6 8 7 2 4 3 1 9 
8 9 3 1 4 5 2 6 7 
2 5 4 6 9 7 1 8 3 
1 7 6 2 3 8 9 4 5 
7 8 9 5 1 2 6 3 4 
4 3 1 8 6 9 5 7 2 
6 2 5 4 7 3 8 9 1 

Easy Starting Position:
4 5 9 1 7 3 2 8 6 
3 ? 1 6 8 ? ? ? ? 
? ? 6 5 ? 9 ? ? 1 
6 3 4 2 9 ? 5 7 ? 
5 ? ? 8 ? ? 3 ? ? 
8 1 7 ? ? 4 6 ? ? 
1 4 ? 7 3 6 ? ? 9 
? ? ? 9 ? 5 ? ? ? 
? 6 3 ? ? ? 1 ? 7 

Solved:
4 5 9 1 7 3 2 8 6 
3 7 1 6 8 2 9 4 5 
2 8 6 5 4 9 7 3 1 
6 3 4 2 9 1 5 7 8 
5 9 2 8 6 7 3 1 4 
8 1 7 3 5 4 6 9 2 
1 4 5 7 3 6 8 2 9 
7 2 8 9 1 5 4 6 3 
9 6 3 4 2 8 1 5 7 

Medium Starting Position:
5 6 1 3 ? ? ? ? 2 
? 3 ? 5 9 6 ? 1 ? 
? 7 ? ? ? 2 3 ? ? 
? 5 9 ? 6 ? ? ? ? 
6 8 ? ? ? 5 ? 3 1 
? ? 4 ? ? 9 ? ? ? 
? ? 3 6 1 ? ? ? 7 
? ? 6 ? 5 ? 2 ? 3 
7 ? ? ? ? ? 1 ? ? 

Solved:
5 6 1 3 7 8 4 9 2 
4 3 2 5 9 6 7 1 8 
9 7 8 1 4 2 3 5 6 
3 5 9 7 6 1 8 2 4 
6 8 7 4 2 5 9 3 1 
1 2 4 8 3 9 6 7 5 
2 9 3 6 1 4 5 8 7 
8 1 6 9 5 7 2 4 3 
7 4 5 2 8 3 1 6 9 

Hard Starting Position:
? 9 4 ? ? 8 ? ? 7 
? ? 6 5 1 ? ? ? ? 
? 1 ? ? ? 4 ? 2 5 
7 ? ? ? ? 3 ? ? 8 
? ? ? ? 9 1 ? 7 ? 
? 4 ? ? ? ? 9 ? 6 
? 8 3 4 ? ? ? ? ? 
4 ? ? ? ? ? ? ? 1 
? 6 ? ? ? ? 8 ? ? 

Solved:
5 9 4 3 2 8 1 6 7 
3 2 6 5 1 7 4 8 9 
8 1 7 9 6 4 3 2 5 
7 5 9 6 4 3 2 1 8 
6 3 8 2 9 1 5 7 4 
2 4 1 7 8 5 9 3 6 
1 8 3 4 5 6 7 9 2 
4 7 2 8 3 9 6 5 1 
9 6 5 1 7 2 8 4 3 

Extreme Starting Position:
? ? 9 ? ? 7 ? 4 ? 
? 7 1 ? 2 ? ? ? 5 
? 4 ? ? ? ? ? 3 9 
? ? ? ? ? 8 ? ? ? 
? ? ? 4 6 ? ? ? ? 
? ? 2 1 9 ? 8 ? ? 
? 6 ? ? ? ? 4 ? ? 
? 9 ? 2 8 6 5 ? ? 
5 ? ? ? ? ? ? ? ? 

Solved:
8 5 9 6 3 7 1 4 2 
3 7 1 9 2 4 6 8 5 
2 4 6 8 5 1 7 3 9 
6 1 5 3 7 8 2 9 4 
9 8 7 4 6 2 3 5 1 
4 3 2 1 9 5 8 6 7 
7 6 3 5 1 9 4 2 8 
1 9 4 2 8 6 5 7 3 
5 2 8 7 4 3 9 1 6 
```
