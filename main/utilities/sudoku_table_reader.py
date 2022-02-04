# -*- coding: utf-8 -*-

from loguru import logger

import json

class SudokuTableReader():
    def __init__(self):
        pass

    def read(self, filepath):
        """Reads a json filepath, parses the input, and converts it
        into a SudokuTable model instance."""
        json_object = json.loads(filepath)

        logger.info(f"Received json object:")
        print(json_object)