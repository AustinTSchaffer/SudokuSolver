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
descriptions have been borrowed from [SudokuWiki](https://www.sudokuwiki.org/),
which has an exhaustive list of strategies that can be used to solve Sudokus.
This site is a great resource is you are looking for strategies to improve your
own personal games and contains to a wealth of strategies that were not included
in this project.
