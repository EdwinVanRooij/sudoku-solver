# -*- coding: utf-8 -*-

from loguru import logger

from main.models.sudoku_table import SudokuTable

class SudokuSolver():
    def __init__(self):
        pass

    def fill_certain_cells(self, sudoku_table: SudokuTable):
        number_of_cells_filled = 0

        for row_index, row in enumerate(sudoku_table.rows):
            for column_index, cell in enumerate(row):
                if cell is None:
                    possible_numbers = self.determine_possible_numbers(sudoku_table, row_index, column_index)

                    if len(possible_numbers) == 1:
                        certain_number = possible_numbers[0]
                        logger.success(f'Cell x{column_index+1} y{row_index+1} must be {certain_number}!')
                        sudoku_table.fill(row_index, column_index, certain_number)
                        number_of_cells_filled += 1
                    else:
                        pass
                        # logger.info(f'Cell x{column_index+1} y{row_index+1} still has {len(possible_numbers)} possibilities')

        return number_of_cells_filled

    def determine_possible_numbers(self, sudoku_table, row_index, column_index):
        """Determines which numbers are possible for a single cell in a Sudoku table."""
        numbers_in_block = sudoku_table.block_sets[SudokuTable.get_block_index(row_index, column_index)]
        numbers_in_row = sudoku_table.row_sets[row_index]
        numbers_in_column = sudoku_table.column_sets[column_index]
        numbers_affecting_current_cell = numbers_in_block.union(numbers_in_row).union(numbers_in_column)
        # logger.info(f'Numbers affecting cell x{column_index} y{row_index}: {numbers_affecting_current_cell}')

        all_numbers = range(1, 10)
        possible_numbers = [number for number in all_numbers if number not in numbers_affecting_current_cell]
        return possible_numbers
