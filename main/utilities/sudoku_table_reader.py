# -*- coding: utf-8 -*-

from loguru import logger

import json

from main.models.sudoku_row import SudokuRow

class SudokuTableReader():
    def __init__(self):
        pass

    def read(self, filepath):
        """Reads a json filepath, parses the input, and converts it
        into a SudokuTable model instance."""
        with open(filepath) as json_file:
            data = json.load(json_file)

        if len(data) != 9:
            SudokuTableReader.raise_invalid_json_exception()
        
        for raw_row in data:
            if len(raw_row) != 9:
                SudokuTableReader.raise_invalid_json_exception()

            sudoku_row = SudokuTableReader.read_row(raw_row)
            logger.info(sudoku_row)

    @staticmethod
    def read_row(row):
        numbers = []

        for column in row:
            if column == ' ':
                numbers.append(None)
            else:
                numbers.append(int(column))

        if len(numbers) != 9:
            error_message = "Could not create a SudokuRow from a row. " + \
                "This should never happen, check the SudokuTableReader implementation."
            logger.error(error_message)
            raise Exception(error_message)

        return SudokuRow(numbers)


    @staticmethod
    def raise_invalid_json_exception():
        error_message = "The json file must contain exactly 9 rows with 9 columns each."
        logger.error(error_message)
        raise Exception(error_message)
