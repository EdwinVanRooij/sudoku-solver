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

from .utilities.sudoku_table_reader import SudokuTableReader

import argparse

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
    # sudoku_table_writer = SudokuTableWriter()
    # sudoku_table_visualizer = SudokuTableVisualizer()
    # sudoku_solver = SudokuSolver()

    logger.info("Reading sudoku table from input file...")
    sudoku_table = sudoku_table_reader.read(args.input_file)
    # sudoku_table_visualizer.show(sudoku_table)

    # logger.info("Filling tables with one possible outcome...")
    # sudoku_table = sudoku_table.fill_certain_tables(sudoku_table)
    # sudoku_table_visualizer.show(sudoku_table)

    # if not sudoku_table.is_done(): 
    #     logger.info("Sudoku table is not yet done, bruteforcing all possibilities...")
    #     sudoku_table = sudoku_solver.bruteforce_remaining_tables(sudoku_table)

    # logger.info("Solved!")
    # sudoku_table_visualizer.show(sudoku_table)

    # logger.info("Solved!")
    # logger.info(f"Writing output to '{args.output_file}'...")
    # sudoku_table_writer.write(args.output_file)
