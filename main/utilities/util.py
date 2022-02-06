# -*- coding: utf-8 -*-

def generate_one_to_nine_dictionary():
    return {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
    }

def column_index_in_block_to_absolute(block_index, relative_column_index):
    """Converts a column index inside a block to the absolute index 
    within the Sudoku table."""
    block_width = 3
    number_of_blocks_per_row = 3
    return block_index % number_of_blocks_per_row * block_width + relative_column_index

def row_index_in_block_to_absolute(block_index, relative_row_index):
    """Converts a row index inside a block to the absolute index 
    within the Sudoku table."""
    if block_index < 3:
        start_row_index = 0
    elif block_index < 6:
        start_row_index = 3
    else:
        start_row_index = 6

    result = start_row_index + relative_row_index

    return result

def generate_cell_id(row_index, column_index):
    return f'{column_index}:{row_index}'

def split_cell_id(cell_id):
    """Returns row_index, column_index"""
    return int(cell_id[2]), int(cell_id[0])