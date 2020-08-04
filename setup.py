from setuptools import setup

setup(
	name="sudoku-solver",
	version="1.0.0",
	description="Provides classes that model Sudoku as an abstract, logic-based, combinatorial, symbol-placement puzzle and functions that can be used to solve puzzles that can be modelled using those classes.",
	url="https://github.com/AustinTSchaffer/SudokuSolver",
	author="Austin T Schaffer",
	author_email="schaffer.austin.t@gmail.com",
	classifiers=[
		"Intended Audience :: Developers",
		"Programming Language :: Python"
	],
	keywords="sudoku solver",
	packages=["sudoku_solver"],
	install_requires=["HeapDict>=1,<2"],
	python_requires=">=3",
	license="MIT"
)
