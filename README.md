# Sudoku Solver

A little hobby project to solve the Sudoku I got stuck on during vacation. 
I know there are existing solutions out there, I just wanted to do it myself.

![](https://raw.githubusercontent.com/EdwinVanRooij/sudoku-solver/main/readme_screenshot_1.png)

![](https://raw.githubusercontent.com/EdwinVanRooij/sudoku-solver/main/readme_screenshot_2.png)

## Installation

Execute in a terminal

```bash
pip3 install -r requirements.txt
```

## Usage

Execute in a terminal

```bash
python3 -m main --input_file=assets/input/hard_input.json
```

---

## Implementation

The algorithm to solve the Sudoku is quite smart, in the sense that it doesn't just bruteforce 
all possibilities at random. It follows the rules of the game and never performs an action 
which would be illegal. First, it checks if it can figure out all cells for certain by using 
various strategies (see `sudoku_solver.fill_certain_cells(...)`). This will solve most Sudokus.
If it's not yet solved, it will start guessing all possibilities for each cell, quitting if
it's stuck. In the end, this should solve all Sudokus, even the hardest ones.
