# -*- coding: utf-8 -*-

from main.utilities.util import column_index_in_block_to_absolute, row_index_in_block_to_absolute


class SudokuTable:
  """Represents the complete 'physical' Sudoku table."""

  def __init__(self, rows: list):
    """Rows should contain a two-dimensional list (9x9)."""
    self.rows = rows

    self.row_sets = []
    self.column_sets = []
    self.block_sets = []

    self.initialize_block_sets()
    self.initialize_row_sets()
    self.initialize_column_sets()

  @property
  def completed(self):
    for row in self.rows:
      for number in row:
        if number is None:
          return False

    return True

  def fill(self, row_index, column_index, certain_number):
    # Update the number in the table
    self.rows[row_index][column_index] = certain_number

    # Update the sets to which the number belongs
    self.row_sets[row_index].add(certain_number)
    self.column_sets[column_index].add(certain_number)
    self.block_sets[SudokuTable.get_block_index(row_index, column_index)].add(certain_number)

  def get_column(self, index):
    column = []

    for row in self.rows:
      column.append(row[index])

    return column 

  def get_block(self, index):
    """Returns a square 3x3 block (zero-based), counting from 
    left to right where 0 is in the top-left corner and 8 is 
    in the right-bottom corner."""
    block = []

    rows = [
       self.rows[row_index_in_block_to_absolute(index, 0)], 
       self.rows[row_index_in_block_to_absolute(index, 1)], 
       self.rows[row_index_in_block_to_absolute(index, 2)], 
    ]

    for row in rows:
      cells = [
        row[column_index_in_block_to_absolute(index, 0)], 
        row[column_index_in_block_to_absolute(index, 1)], 
        row[column_index_in_block_to_absolute(index, 2)],
      ]
      block.append(cells)

    return block

  def initialize_block_sets(self): 
    """Initializes the 9 square blocks as Sets for O(1) searches 
    instead of O(N)."""
    for index in range(9):
      block = self.get_block(index)
      numbers_in_block = []

      for row in block:
        for number in row:
          if number:
            numbers_in_block.append(number)

      self.block_sets.append(set(numbers_in_block))

  def initialize_row_sets(self): 
    for index in range(9):
      row = self.rows[index]
      numbers_in_row = []

      for number in row:
        if number:
          numbers_in_row.append(number)

      self.row_sets.append(set(numbers_in_row))

  def initialize_column_sets(self): 
    for index in range(9):
      column = self.get_column(index)
      numbers_in_column = []

      for number in column:
        if number:
          numbers_in_column.append(number)

      self.column_sets.append(set(numbers_in_column))

  @staticmethod
  def get_block_index(row_index, column_index):
    if row_index < 3:
      # First three rows
      if column_index < 3:
        return 0
      elif column_index < 6:
        return 1
      else:
        return 2
    elif row_index < 6:
      # Middle 3 rows
      if column_index < 3:
        return 3
      elif column_index < 6:
        return 4
      else:
        return 5
    # Last 3 rows
    if column_index < 3:
      return 6
    elif column_index < 6:
      return 7
    else:
      return 8
