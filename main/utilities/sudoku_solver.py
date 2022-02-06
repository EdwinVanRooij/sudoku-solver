# -*- coding: utf-8 -*-

from loguru import logger

from main.models.sudoku_table import SudokuTable
from main.utilities.util import column_index_in_block_to_absolute, generate_one_to_nine_dictionary, generate_cell_id, row_index_in_block_to_absolute

class SudokuSolver():
    def __init__(self):
        pass

    def guess_cell(self, sudoku_table: SudokuTable, already_guessed_dict: dict):
        """Guesses a cell whithin the possibilities for the given Sudoku table,
        keeping in mind what's already guessed."""
        for row_index, row in enumerate(sudoku_table.rows):
            for column_index, number in enumerate(row):
                if number is None:
                    possible_numbers = self.determine_possible_numbers(sudoku_table, row_index, column_index)
                    current_cell_id = generate_cell_id(row_index, column_index)
                    already_guessed_numbers = already_guessed_dict.get(current_cell_id)
                    if already_guessed_numbers is None:
                        remaining_possible_numbers = possible_numbers
                    else:
                        remaining_possible_numbers = [number for number in possible_numbers if number not in already_guessed_numbers]

                    if len(remaining_possible_numbers) > 0:
                        # There is at least one possible guess left for this cell. Just pick the first one,
                        # there is no way of knowing which would be the better guess.
                        guessed_number = remaining_possible_numbers[0]
                        return current_cell_id, guessed_number

        logger.info(f'Could not find anything to guess anymore, returning None')
        return None, None

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

        number_of_cells_filled += self.fill_certain_cells_by_row(sudoku_table)
        number_of_cells_filled += self.fill_certain_cells_by_column(sudoku_table)
        number_of_cells_filled += self.fill_certain_cells_by_block(sudoku_table)

        return number_of_cells_filled

    def fill_certain_cells_by_block(self, sudoku_table: SudokuTable):
        number_of_cells_filled = 0

        for block_index in range(9):
            block = sudoku_table.get_block(block_index)
            number_occurrences_dictionary = generate_one_to_nine_dictionary()
            number_to_row_dictionary = generate_one_to_nine_dictionary()
            number_to_column_dictionary = generate_one_to_nine_dictionary()

            base_row_index = 0
            for row in block:
                for column_index, number in enumerate(row):
                    if number is None:
                        row_index = row_index_in_block_to_absolute(block_index, base_row_index)
                        column_index = column_index_in_block_to_absolute(block_index, column_index)

                        possible_numbers = self.determine_possible_numbers(sudoku_table, row_index, column_index)
                        for possible_number in possible_numbers:
                            number_occurrences_dictionary[possible_number] = number_occurrences_dictionary[possible_number] + 1
                            number_to_row_dictionary[possible_number] = row_index
                            number_to_column_dictionary[possible_number] = column_index
                base_row_index += 1
            
            for number, occurrences in number_occurrences_dictionary.items():
                if occurrences == 1:
                    # The number occurred once, so the only index set in the 
                    # number_to_column_dictionary is the column we need.
                    row_index = number_to_row_dictionary[number]
                    column_index = number_to_column_dictionary[number]
                    logger.success(f'Cell {column_index+1}:{row_index+1} is {number}! (block-method)')
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
                    # number_to_row_dictionary is the row we need.
                    row_index = number_to_row_dictionary[number]
                    logger.success(f'Cell {column_index+1}:{row_index+1} is {number}! (column-method)')
                    sudoku_table.fill(row_index, column_index, number)
                    number_of_cells_filled += 1

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
                    logger.success(f'Cell {column_index+1}:{row_index+1} is {number}! (row-method)')
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
                        logger.success(f'Cell {column_index+1}:{row_index+1} is {certain_number}! (cell-method)')
                        sudoku_table.fill(row_index, column_index, certain_number)
                        number_of_cells_filled += 1

        return number_of_cells_filled

    def determine_possible_numbers(self, sudoku_table, row_index, column_index):
        """Determines which numbers are possible for a single cell in a Sudoku table."""
        numbers_in_block = sudoku_table.block_sets[SudokuTable.get_block_index(row_index, column_index)]
        numbers_in_row = sudoku_table.row_sets[row_index]
        numbers_in_column = sudoku_table.column_sets[column_index]
        numbers_affecting_current_cell = numbers_in_block.union(numbers_in_row).union(numbers_in_column)

        all_numbers = range(1, 10)
        possible_numbers = [number for number in all_numbers if number not in numbers_affecting_current_cell]
        return possible_numbers
