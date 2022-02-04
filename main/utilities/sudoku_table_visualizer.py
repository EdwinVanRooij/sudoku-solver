# -*- coding: utf-8 -*-

from loguru import logger

import json

from main.models.sudoku_row import SudokuRow
from main.models.sudoku_table import SudokuTable

class SudokuTableVisualizer():
    def __init__(self):
        pass

    def show(self, sudoku_table: SudokuTable):
        for idx, sudoku_row in enumerate(sudoku_table.rows):
            row_as_string = "|"

            for number in sudoku_row.numbers:
                if number:
                    row_as_string += f"{number}|"
                else:
                    row_as_string += f" |"

            if idx % 3 == 0:
                print("--------------------")
                pass

            print(row_as_string)
        print("--------------------")
