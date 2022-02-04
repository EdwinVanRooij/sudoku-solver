# -*- coding: utf-8 -*-

class SudokuTable:
  """Represents the complete 'physical' Sudoku table."""

  def __init__(self, rows: list):
    """Rows should contain a two-dimensional list (9x9)."""
    self.rows = rows

    self.block_sets = []
    self.row_sets = []
    self.column_sets = []
    self.initialize_blocks()
    # self.initialize_row_sets()
    # self.initialize_column_sets()

  def get_column(self, index):
    column = []

    for row in self.rows:
      column.append(row[index])

    return column 

  def get_block(self, index):
    """Returns a square 3x3 block, counting from left to right 
    where 1 is in the top-left corner and 9 is in the 
    right-bottom corner."""
    block = []

    if index == 0:
      rows = [self.rows[0], self.rows[1], self.rows[2]]
      for row in rows:
        current_cells = [row[0], row[1], row[2]]
        block.append(current_cells)

    return block

  def initialize_blocks(self): 
    """Initializes the 9 square blocks as Sets for O(1) searches 
    instead of O(N)."""
    for row in self.rows:
      numbers_in_row = []
      for number in row:
        if number:
          numbers_in_row.append(number)
        self.block_sets.append(set(numbers_in_row))
