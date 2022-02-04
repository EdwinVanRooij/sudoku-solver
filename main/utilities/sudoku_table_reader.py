# -*- coding: utf-8 -*-

from loguru import logger

import json

class SudokuTableReader():
    def __init__(self):
        pass

    def read(self, filepath):
        """Reads a json filepath, parses the input, and converts it
        into a SudokuTable model instance."""
        with open(filepath) as json_file:
            data = json.load(json_file)

        if len(data) is not 9:
            SudokuTableReader.raise_invalid_json_exception()
        
        for raw_row in data:
            if len(raw_row) is not 9:
                SudokuTableReader.raise_invalid_json_exception()

            logger.info(raw_row)
            pass

    @staticmethod
    def raise_invalid_json_exception():
        error_message = "The json file must contain exactly 9 rows with 9 columns each."
        logger.error(error_message)
        raise Exception(error_message)
