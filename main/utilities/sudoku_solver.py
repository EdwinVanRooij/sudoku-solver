# -*- coding: utf-8 -*-

from loguru import logger

from main.models.sudoku_table import SudokuTable

class SudokuSolver():
    def __init__(self):
        pass

    def fill_certain_cells(self, sudoku_table: SudokuTable):
        for row_index, row in enumerate(sudoku_table.rows):
            for column_index, cell in enumerate(row):
                if cell is None:
                    numbers_in_block = sudoku_table.block_sets[SudokuTable.get_block_index(row_index, column_index)]
                    numbers_in_row = sudoku_table.row_sets[row_index]
                    numbers_in_column = sudoku_table.column_sets[column_index]
                    numbers_affecting_current_cell = numbers_in_block.union(numbers_in_row).union(numbers_in_column)
                    # logger.info(f'Numbers affecting cell x{column_index} y{row_index}: {numbers_affecting_current_cell}')

                    all_numbers = range(1, 9)
                    possible_numbers = [number for number in all_numbers if number not in numbers_affecting_current_cell]
                    logger.info(f'Which leaves \'{possible_numbers}\' as possibilities')

        return sudoku_table
