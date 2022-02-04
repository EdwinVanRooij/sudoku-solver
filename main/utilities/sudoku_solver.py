# -*- coding: utf-8 -*-

from loguru import logger

from main.models.sudoku_table import SudokuTable
from main.utilities.util import generate_one_to_nine_dictionary

class SudokuSolver():
    def __init__(self):
        pass

    def fill_certain_cells(self, sudoku_table: SudokuTable):
        number_of_cells_filled = 0

        number_of_cells_filled += self.fill_certain_cells_by_cell(sudoku_table)
        number_of_cells_filled += self.fill_certain_cells_by_number(sudoku_table)

        return number_of_cells_filled

    def fill_certain_cells_by_number(self, sudoku_table: SudokuTable):
        """Fills all cells which can be known for sure by checking the number
        of possibilities for each number. If a number is only possible in one 
        spot for a row, column, or block, that one is filled in."""
        number_of_cells_filled = 0

        # Check for all rows
        number_of_cells_filled = self.fill_certain_cells_by_row(sudoku_table)

        # Check for all columns
        # number_of_cells_filled = self.fill_certain_cells_by_column(sudoku_table)

        # Check for all blocks
        #todo

        return number_of_cells_filled

    def fill_certain_cells_by_row(self, sudoku_table: SudokuTable):
        number_of_cells_filled = 0

        for row_index, row in enumerate(sudoku_table.rows):
            number_occurrences_dictionary = generate_one_to_nine_dictionary()
            number_to_column_dictionary = generate_one_to_nine_dictionary()

            for column_index, number in enumerate(row):
                if number is None:
                    possible_numbers = self.determine_possible_numbers(sudoku_table, row_index, column_index)
                    for possible_number in possible_numbers:
                        number_occurrences_dictionary[possible_number] = number_occurrences_dictionary[possible_number] + 1
                        number_to_column_dictionary[possible_number] = column_index
            
            for number, occurrences in number_occurrences_dictionary.items():
                if occurrences == 1:
                    # The number occurred once, so the only index set in the 
                    # number_to_column_dictionary is the column we need.
                    column_index = number_to_column_dictionary[number]
                    logger.success(f'Cell x{column_index+1} y{row_index+1} must be {number}! (solved using row-method)')
                    sudoku_table.fill(row_index, column_index, number)
                    number_of_cells_filled += 1

        return number_of_cells_filled

    def fill_certain_cells_by_column(self, sudoku_table: SudokuTable):
        number_of_cells_filled = 0

        for column_index in range(9):
            column = sudoku_table.get_column(column_index)
            number_occurrences_dictionary = generate_one_to_nine_dictionary()
            number_to_row_dictionary = generate_one_to_nine_dictionary()

            for row_index, number in enumerate(column):
                if number is None:
                    possible_numbers = self.determine_possible_numbers(sudoku_table, row_index, column_index)
                    for possible_number in possible_numbers:
                        number_occurrences_dictionary[possible_number] = number_occurrences_dictionary[possible_number] + 1
                        number_to_row_dictionary[possible_number] = row_index
            
            for number, occurrences in number_occurrences_dictionary.items():
                if occurrences == 1:
                    # The number occurred once, so the only index set in the 
                    # number_to_column_dictionary is the column we need.
                    column_index = number_to_row_dictionary[number]
                    logger.success(f'Cell {column_index+1}:{row_index+1} must be {number}! (solved using column-method)')
                    sudoku_table.fill(row_index, column_index, number)
                    number_of_cells_filled += 1

        return number_of_cells_filled

    def fill_certain_cells_by_cell(self, sudoku_table: SudokuTable):
        """Fills all cells which can be known for sure by checking the number of
        possibilities for each individual cell. If there is only one possibility,
        that one is filled in."""
        number_of_cells_filled = 0

        for row_index, row in enumerate(sudoku_table.rows):
            for column_index, cell in enumerate(row):
                if cell is None:
                    possible_numbers = self.determine_possible_numbers(sudoku_table, row_index, column_index)

                    if len(possible_numbers) == 1:
                        certain_number = possible_numbers[0]
                        logger.success(f'Cell {column_index+1}:{row_index+1} must be {certain_number}! (solved using cell-method)')
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
