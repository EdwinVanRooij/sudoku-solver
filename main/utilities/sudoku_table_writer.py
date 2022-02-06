# -*- coding: utf-8 -*-

from loguru import logger

import json

from main.models.sudoku_table import SudokuTable

class SudokuTableWriter():
    def __init__(self):
        pass

    def write(self, filepath, sudoku_table: SudokuTable):
        """Writes a SudokuTable to a json file."""
        logger.info(f"Writing output to '{filepath}'...")
        data = []

        for row in sudoku_table.rows:
            data_row = row
            data.append(data_row)

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        logger.info("Done")
