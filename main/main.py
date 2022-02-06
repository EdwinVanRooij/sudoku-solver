# -*- coding: utf-8 -*-

"""Main program entrypoint

The Jarvis Mediator acts as an intermediate between Jarvis 
components. For example, it may periodically retrieve state
updates from Home Assistant which will then be used by 
Jarvis Vision.
"""

from loguru import logger
from datetime import datetime
from copy import deepcopy

from main.constants.variables import DEFAULT_INPUT_FILENAME, DEFAULT_OUTPUT_FILENAME
from main.utilities.sudoku_solver import SudokuSolver
from main.utilities.sudoku_table_visualizer import SudokuTableVisualizer
from main.utilities.sudoku_table_writer import SudokuTableWriter
from main.utilities.util import split_cell_id

from .utilities.sudoku_table_reader import SudokuTableReader

import argparse
import os

def main():
    date = datetime.today().strftime('%Y-%m-%d')
    logger.add(f"logs/{date}.log", rotation="1 day")
    logger.info("Starting Sudoku Solver...")

    parser = argparse.ArgumentParser()

    parser.add_argument('--input_file', help='Input file of the Sudoku to solve, in json format.', type=str, default=DEFAULT_INPUT_FILENAME)
    parser.add_argument('--output_file', help='Output file with the solved Sudoku, in json format.', type=str, default=DEFAULT_OUTPUT_FILENAME)
    parser.add_argument('--tag', help='For DevOps purposes', type=str)

    args = parser.parse_args()

    sudoku_table_reader = SudokuTableReader()
    sudoku_table_visualizer = SudokuTableVisualizer()
    sudoku_solver = SudokuSolver()
    sudoku_table_writer = SudokuTableWriter()

    absolute_filepath = os.path.abspath(args.input_file)
    input_exists = os.path.exists(absolute_filepath)
    if not input_exists:
        logger.error(f"Input file '{absolute_filepath}' does not exist. Please provide a valid filepath.")
        return

    logger.info(f"Reading sudoku table from input file '{absolute_filepath}'...")
    sudoku_table = sudoku_table_reader.read(absolute_filepath)
    sudoku_table_visualizer.show(sudoku_table)

    logger.info("Filling the table's cells with one possible outcome...")
    number_of_cells_filled = sudoku_solver.fill_certain_cells(sudoku_table)
    while number_of_cells_filled > 0:
        number_of_cells_filled = sudoku_solver.fill_certain_cells(sudoku_table)

    if sudoku_table.completed: 
        logger.success("Successfully completed the Sudoku!")
        sudoku_table_visualizer.show(sudoku_table)
        sudoku_table_writer.write(args.output_file, sudoku_table)
        return
    else:
        logger.warning("Could not complete the Sudoku by filling out all certainties. Moving on to guessing...")
    
    # Track the guesses in a dictionary of (cell_id, number) records
    guesses_dictionary = {}
    while True:
        temp_sudoku_table = deepcopy(sudoku_table)
        cell_id, number = sudoku_solver.guess_cell(temp_sudoku_table, guesses_dictionary)

        if cell_id is None and number is None:
            logger.warning(f'No possible guesses left, tried {guesses_dictionary}')
            break

        logger.info(f'Guessing {cell_id} = {number}')

        row_index, column_index = split_cell_id(cell_id)
        temp_sudoku_table.fill(row_index, column_index, number)

        # Save the guess, preventing a duplicate guess in the future
        if guesses_dictionary.get(cell_id) is None:
            guesses_dictionary[cell_id] = [number]
        else:
            guesses_dictionary[cell_id].append(number)

        logger.info("Filling the table's cells with one possible outcome...")
        number_of_cells_filled = sudoku_solver.fill_certain_cells(temp_sudoku_table)
        while number_of_cells_filled > 0:
            number_of_cells_filled = sudoku_solver.fill_certain_cells(temp_sudoku_table)

        if temp_sudoku_table.completed:
            logger.success("Successfully completed the Sudoku!")
            sudoku_table_visualizer.show(temp_sudoku_table)
            sudoku_table_writer.write(args.output_file, temp_sudoku_table)
            break
        else:
            logger.error(f'Guess {cell_id} = {number} did not work out, got stuck here:')
            sudoku_table_visualizer.show(temp_sudoku_table)

    if not temp_sudoku_table.completed:
        logger.warning("Could not complete the Sudoku by filling out all certainties after " + \
            "guessing every cell's possibilities one by one. A next step to this program could be to " + \
            "support multiple guesses within the same temp_sudoku_table.")

