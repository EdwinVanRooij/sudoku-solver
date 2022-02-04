# -*- coding: utf-8 -*-

"""Main program entrypoint

The Jarvis Mediator acts as an intermediate between Jarvis 
components. For example, it may periodically retrieve state
updates from Home Assistant which will then be used by 
Jarvis Vision.
"""

from loguru import logger
from datetime import datetime

from main.constants.variables import DEFAULT_INPUT_FILENAME, DEFAULT_OUTPUT_FILENAME
from main.utilities.sudoku_solver import SudokuSolver
from main.utilities.sudoku_table_visualizer import SudokuTableVisualizer

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
    # sudoku_table_writer = SudokuTableWriter()

    absolute_filepath = os.path.abspath(args.input_file)
    input_exists = os.path.exists(absolute_filepath)
    if not input_exists:
        logger.error(f"Input file '{absolute_filepath}' does not exist. Please provide a valid filepath.")
        return

    logger.info(f"Reading sudoku table from input file '{absolute_filepath}'...")
    sudoku_table = sudoku_table_reader.read(absolute_filepath)
    sudoku_table_visualizer.show(sudoku_table)

    for index in range(9):
        # logger.info(f"Block {index}")
        # logger.info(sudoku_table.get_block(index))
        logger.info(f"Block set {index}: {sudoku_table.block_sets[index]}")

    for index in range(9):
        logger.info(f"Row set {index}: {sudoku_table.row_sets[index]}")

    for index in range(9):
        logger.info(f"Row column {index}: {sudoku_table.column_sets[index]}")

    # logger.info("Filling the table's cells with one possible outcome...")
    # sudoku_table = sudoku_solver.fill_certain_cells(sudoku_table)
    # sudoku_table_visualizer.show(sudoku_table)

    # if not sudoku_table.is_done(): 
    #     logger.info("Sudoku table is not yet done, bruteforcing all possibilities...")
    #     sudoku_table = sudoku_solver.bruteforce_remaining_tables(sudoku_table)

    # logger.info("Solved!")
    # sudoku_table_visualizer.show(sudoku_table)

    # logger.success("Solved!")
    # logger.info(f"Writing output to '{args.output_file}'...")
    # sudoku_table_writer.write(args.output_file)
